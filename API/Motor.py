import numpy as np
from time import sleep
import pigpio


class Motor():
    
    # Maybe the pi should be a static variable of the Telescope?
    pi = pigpio.pi()
    
    # Positive degree rotations correspond to counter-clockwise motor rotation
    CCW = 1
    CW = -1
    
    def __init__(self, cfg):
        self.PUL = cfg['PUL']
        self.DIR = cfg['DIR']
        self.PWMCLOCKS = np.array(cfg['PWMCLOCKS'])
        self.MCSTP = cfg['MCSTP']
        self.MXSPD = cfg['MXSPD']
        self.MXACC = cfg['MXACC']
        self.max_PWM_frequency = self.MXSPD / 360 * self.MCSTP
        self.allowed_PWM_frequencies = self.PWMCLOCKS[self.PWMCLOCKS <= self.max_PWM_frequency]
        
        if self.max_PWM_frequency not in self.PWMCLOCKS:
            # Finds the next smallest PWM speed in PWMCLOCKS
            self.max_PWM_frequency = self.allowed_PWM_frequencies[(self.allowed_PWM_frequencies-self.max_PWM_frequency).argmin()]      
        
        self.max_speed = self.max_PWM_frequency / self.MCSTP * 360
        Motor.pi.set_mode(self.PUL, pigpio.OUTPUT)
        Motor.pi.set_mode(self.DIR, pigpio.OUTPUT)
        
    
    def actuate(self, degrees):
        # Sets the dirction
        if degrees* Motor.CCW >= 0:
            Motor.pi.write(self.DIR, 1)
        else: 
            Motor.pi.write(self.DIR, 0)
        
        # Ensures the direction change takes effect before sending pulses to the motor
        sleep(0.001)    
        
        steps = abs(degrees) / 360 * self.MCSTP
        
        waveform = self.create_waveform(steps)
        frequencies = [item[0] for item in waveform]
        all_steps = [item[1] for item in waveform]
        
        wid = self.generate_waveIDs(frequencies)
        
        # ****
        self.transmit_waveIDs(wid, all_steps)
        # ****
        
        # Probably returns wid and steps to Telescope for dual actuation
        return
        
    
    def create_waveform(self, steps):
        # Decides on the best waveform for the job, sends it to the generate function
        steps_left = int(steps)
        ramp_up = []        
        ramp_down = []
        
        last_freq = self.allowed_PWM_frequencies[0]
        for freq in self.allowed_PWM_frequencies[1:]:
            if steps_left != 0:
                # Calculates minimum number of steps needed at the last fequency value to ensure we remain under the maximum acceleration
                dv = (freq-last_freq) / self.MCSTP * 360
                t = dv / self.MXACC
                steps_to_take = int(t * last_freq)
                step_up, step_down = 0, 0
                
                # This part handles the case when the necessary steps to take is not enough to accelerate to max speed
                if 2*steps_to_take >= steps_left:
                    steps_to_take = int(steps_left/2)
                    
                    # Handles step loss when the remaining steps needed is odd
                    if 2*steps_to_take != steps_left:
                        step_up += 1
                
                    steps_left = 0
                else:
                    steps_left -= 2*steps_to_take   
                
                step_up += steps_to_take
                step_down += steps_to_take
                    
                ramp_up.append([last_freq, step_up])
                ramp_down.insert(0, [last_freq, step_down])
                
                last_freq = freq
        
        hold = []
        if steps_left != 0:
            print("Max Speed Acheived")
            hold.append([self.allowed_PWM_frequencies[-1], steps_left])
            steps_left = 0
        
        waveform = []
        waveform.extend(ramp_up)
        waveform.extend(hold)
        waveform.extend(ramp_down)
        
        return waveform
    
    
    def generate_waveIDs(self, frequencies):
        """Generates a composite waveform.
        waveform_instructions:  List of [Frequency, Steps]
        """
        Motor.pi.wave_clear()     # clear existing waves -- bump to Telescope
        length = len(frequencies)  # number of ramp levels
        wid = [-1] * length
        
        # Generate a wave per ramp level
        for i in range(length):
            frequency = frequencies[i]
            micros = int(500000 / frequency)
            wf = []
            wf.append(pigpio.pulse(1 << self.PUL, 0, micros))  # pulse on
            wf.append(pigpio.pulse(0, 1 << self.PUL, micros))  # pulse off
            Motor.pi.wave_add_generic(wf)
            wid[i] = Motor.pi.wave_create()
        
        return wid
    
    
    def transmit_waveIDs(self, wid, all_steps):
        # Generate a chain of waves
        
        length = len(all_steps)
        length_is_odd = length % 2 == 1
        
        '''
        Multichaining seems like a very bad idea but in testing it works quite well
        Single chains can only run up to 20 individual loops but in many cases length>20
        At a max speed of 1800 deg/sec we need at least 2 chains to rotate 729 times
        so only two chains are implemented here
        Other solutions involve limiting further the number of discrete frequency levels for ramping
        but these may present mechanical acceleration issues
        '''
        
        chain_up, chain_down, chain_max = [], [], []
        
        for i in range(length):
            steps = all_steps[i]
            x = steps & 255
            y = steps >> 8
            
            if length_is_odd and i == int(length/2):
                mod = y >> 8
                rem = y & 255
                
                # This part handles very long chains >= 2^16 steps.
                # Should be able to handle up to 2^32 steps in one go (way more than necessary)
                chain_max += [255, 0, 255, 0, wid[i], 255, 1, 255, 255, 255, 1, mod, 0]
                chain_max += [255, 0, wid[i], 255, 1, x + mod, rem]
                
            elif i < length/2:
                chain_up += [255, 0, wid[i], 255, 1, x, y]
            else:
                chain_down += [255, 0, wid[i], 255, 1, x, y]
                
                
        Motor.pi.wave_chain(chain_up)
        self.sleep_until_transmitted()
        
        Motor.pi.wave_chain(chain_max)
        self.sleep_until_transmitted()
            
        Motor.pi.wave_chain(chain_down)
        
        
    def sleep_until_transmitted(self):
        
        while Motor.pi.wave_tx_busy():
            sleep(0.001)
        