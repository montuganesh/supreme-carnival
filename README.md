# Automatic Telesocpe Control
Welcome to the project page of the automatic pointing telescope. The goal of this project was to design, build, and program a mounting system for a telescope that is free to rotate in all directions without the need for the user to physically interact with the telescope. Such a system is more accurate, less finicky, and able to view the night sky remotely, without constant user monitoring. This project required us to design the hardware necessary for a maneuverable yet precise mounting system, the electronics necesary to rotate a 5 kg telescope and mounting system with about 30 arseconds of precision, as well as the software which controls the motors, calculation of required pointing angle, and the telescope as a whole.
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Telescope_Setup.jpg">

## Table of Contents
- [Components and Budget](#components-and-budget)
- [Design](#design)
  * [Mounting System](#mounting-system)
  * [Electronics](#electronics)
    + [Circuit Diagram](#circuit-diagram)
- [Code](#code)
  * [Pointing Angle Calculation](#pointing-angle-calculation)
    + [Star Database](#star-database)
  * [Motor Control](#motor-control)
  * [Telescope Control](#telescope-control)
    + [Tracking](#tracking)
    + [Calibration](#calibration)
- [Project Flow (Who did what and when? - intended to chronicle the journey, idk if you guys want this or not)](#project-flow--who-did-what-and-when----intended-to-chronicle-the-journey--idk-if-you-guys-want-this-or-not-)
- [Results](#results)
  * [Raw Images](#raw-images)
  * [Z-Scaled Images](#z-scaled-images)
- [Conclusion](#conclusion)
- [Contributors and Acknowldegements](#contributors-and-acknowldegements)


## Components and Budget
These are the electrical and mechanical parts that we used for this design. Many of the electrical parts could be substituted for parts with comparable specifications, but these are the ones we used for this design. All parts were purchased from Amazon.
\# | Part | Subtotal ($)
---------|------|------
1 | ALITOVE 110VAC to 24VDC 10A Power Supply | 20.99
2 | DM542 Stepper Motor Controller | 45.98
2 | NEMA 23 Stepper Motor | 58.00
1 | Raspberry Pi 2B | —
1 | MH Level Converter | ~0.60
1 | Nexstar 127 SLT Telescope* | —
4 | Worm Gear Set 27:1 | 86.96

Collin, do the mechanical parts and cost we ended up using. 

\* Optical part of the telescope only

— Part was on hand, no purchase necessary

The total cost of the electrical components we used (including shipping) came out to about $230. Including a basic Raspberry Pi and the necessary mechanical parts, this total cost of this porject comes out to just under $300. For comparison, many similar commercial telescopes with these capabilities sell closer to the $500-$1500 range, though they also usually also include the optical part of the telescope itself.

### Extra Parts
In the interest of full disclosure, we list here the parts that we bought but did not end up using, and the parts that we bought to facilitate remote work on this project (such as multiple Raspberry Pis so that each of us could test code on them individually)
\# | Part | Subtotal ($)
---------|------|------
2 | AS5048A 14-bit Rotary Encoder | 39.98
2 | Raspberry Pi 0W + Essential Peripherals | ~50.00
2 | AS5600 12-bit Rotary Encoder | ~20.00
2 | Diametric Magnets | 0.68

We did not have time to fully implement encoders, although much of the functionality for controlling the telescope using encoders exists within the code.

## Design

### Mounting System

### Electronics
To control the telescope, we needed extremely precisce yet powerful rotary motors—not necessarily fast motors. We settled on the use of stepper motors, which are ideal for these circumstances: they are not as fast as other types of motors, but the notion of discrete 'steps' means that the motor torque and precision were exactly what we need. To power the NEMA 23 motors we selected, however, required the purchase of two dedicated controllers, which could convert the logic signals from the RPi to 24V and up to 4A signals to the motors themselves. We settled on the DM542 controllers since we did not care about high microstepping fidelity (as microstepping decreases torque) and it met the requirements of our motors. The ALITOVE power supplywas simply chosen because it was the cheapest available which could provide 24VDC power at up to 5A for each motor simultaneously. The choice of RPi was unimportant, in fact, we used many different RPis throughout the project. However, since the RPi only supplies 3.3V on its digital GPIO pins, and the controllers needed at least 3.5V to interpret the signals, we had to purchase a level converter, which would amplify the digital signals coming from the RPi so that they could be read by the controllers. We had attempted a solution involving a non-inverting amplifier using an op-amp, but this had issues at high frequencies, so we purchased dedicated logic converters which doubled the maximum rotation speed of the motors.

#### Circuit Diagram
The blue lines indicate wires that carry the PWM signal from the RPi to the controllers. Each pulse in the PWM signal is an instruction to step the motor once, so it was important that the PWM signal work at high frequencies so the motor would rotate fast, considering we were already stepping down the motor speed by a factor of 729. The green lines indicate wires which carry the binary direction signal to the controllers so that we could rotate the motors in either direction. 

<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Electronics_Schematic.png">

## Code

### Pointing Angle Calculation

#### Star Database

### Motor Control

### Telescope Control

#### Tracking

#### Calibration

## Project Flow (Who did what and when? - intended to chronicle the journey, idk if you guys want this or not)

## Results
(What we accomplished, as well as what we didn't manage to accomplish)

### Raw Images
More images are available <a href="https://github.com/cbrahana/supreme-carnival/blob/main/images">here</a>, but here are some of the best ones.
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Raw1.JPG">
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Raw2.JPG">

### Z-Scaled Images
(Include a brief explanation of what z-scaling is and why we did it before linking the images)

## Conclusion 

## Contributors and Acknowldegements
This project was made for the spring 2021 UCSB physics 15C/13CH lab class by (in alphabetical order by last name) Collin Brahana, Sam Crossley, Montu Ganesh, and Jack Grossman, under the observation of Dr. Andrew Jayich, and TAs Sean Buechele and Mingyu Fan.