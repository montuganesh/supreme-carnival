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
In order to facilitate the remote work environment of this project, it was necessary to make the software as user-friendly and modular as possible such that the integration of various parts went smoothly. Since this was almost a necessity anyway, one of our goals was to provide a highly modular and extensible yet user-friendly software to control the telescope. We will go into detail about the main elements pieces of our software below, each being largely independent of the others to allow for this modularity, yet all working together to provide telescope functionality.

### Pointing Angle Calculation

#### Star Database

### Motor Control
We wanted the motor control to be entirely self-contained, which makes it easier to debug code if the motors fail to run and allows for more freedom when it comes to pointing the telescope. The code uses the pigpio library, which is a 3rd party python library for Raspberry Pi which gives us control of key features of the Pi's hardware, such as its internal, hardware PWM clock. It is important that we use this hardware clock as opposed to the more common software PWM, since python is notoriously bad at handling precision time measurements, which would result in erratic and unreliable PWM signals. The hardware clock, on the other hand, is extremely precise to within about a 1 microsecond. This means that we could very precisiely control the amount of PWM signals outputted and, as each pulse is an instruction to step the motor once, this is crucial for precision control. The hardware clock does, however, come with the limitation that it can only operate at a few discrete frequencies, so we cannot continuously accelerate the motors as we sould if using a software clock. The motor control therefore includes the aility to automatically generate the necessary acceleration curve, given the maximum acceleration, maximum speed, and list of available clock frequencies provided by the user. One example of the generated acceleration curve is shown below, the acceleration is linear, then peaks and holds that maximum speed, then it decreases linearly (or as linearly as possible given the available speeds).

<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Accel_Curve_10_Revs.png" width=500><img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Accel_Curve_100_Revs.png" width=500>

The maximum speed, maximum acceleration, and the available frequencies for each motor are all mutable by the user, providing them control of the telescope not achievable by many commercial equivalents. One major limitation of the motor software design is that multiple motors cannot be actuated simultaneously. This is a limitation of the the pigpio library which could easily be fixed by purchasing an external clock or (painstakingly) fixed in software. Due to time contraints, none of these fixes were implemented here.

### Telescope Control

#### Tracking

#### Calibration

## Project Workflow (Who did what and when? - intended to chronicle the journey, idk if you guys want this or not)

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
