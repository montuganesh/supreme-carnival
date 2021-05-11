import numpy as np
import pigpio

class Motor():
    
    PUL = 0
    DIR = 0
    MCSTP = 0
    MXSPD = 0 # Seems to be capped at 1 kHz for now, theoretical limit is 100 kHz.
    MXACC = 0
    PWMCLOCKS = None
    pi = pigpio.pi()
    max_PWM_frequency = 0
    allowed_PWM_frequencies = np.array([])
    max_speed = 0 # Degrees per second
    
    
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
        
    
    def actuate(self, degrees):
        # Degress: + for CCW, - for CW
        # Main actuation function
        return
        
    
    def create_waveform(self, steps):
        # Decides on the best waveform for the job, sends it to the generate function
        steps_left = steps
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
    
    
    def generate_waveform(self, waveform_instructions):
        """Generates a composite waveform.
        waveform_instructions:  List of [Frequency, Steps]
        """
        self.pi.wave_clear()     # clear existing waves
        length = len(waveform_instructions)  # number of ramp levels
        wid = [-1] * length
    
        # Generate a wave per ramp level
        for i in range(length):
            frequency = waveform_instructions[i][0]
            micros = int(500000 / frequency)
            wf = []
            wf.append(pigpio.pulse(1 << self.PUL, 0, micros))  # pulse on
            wf.append(pigpio.pulse(0, 1 << self.PUL, micros))  # pulse off
            self.pi.wave_add_generic(wf)
            wid[i] = self.pi.wave_create()
    
        # Generate a chain of waves
        # Handle this in a separate function to transimit the wave to hardware
        chain = []
        for i in range(length):
            steps = waveform_instructions[i][1]
            x = steps & 255
            y = steps >> 8
            chain += [255, 0, wid[i], 255, 1, x, y]
    
        self.pi.wave_chain(chain)  # Transmit chain.
        
        