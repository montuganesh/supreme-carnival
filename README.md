# Automatic Telesocpe Control
Welcome to the project page of the automatic pointing telescope. The goal of this project was to design, build, and program a mounting system for a telescope that is free to rotate in all directions without the need for the user to physically interact with the telescope. Such a system is more accurate, less finicky, and able to view the night sky remotely, without constant user monitoring. This project required us to design the hardware necessary for a maneuverable yet precise mounting system, the electronics necesary to rotate a 5 kg telescope and mounting system with about 30 arseconds of precision, as well as the software which controls the motors, calculation of required pointing angle, and the telescope as a whole.

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
1 | Raspberry Pi 2B | ---
1 | MH Level Converter | ~0.60
1 | Nexstar 127 SLT Telescope* | ---
4 | Worm Gear Set 27:1 | 86.96

Collin, do the mechanical parts and cost we ended up using. 

\* Optical part of the telescope only

--- Part was on hand, no purchase necessary

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

#### Circuit Diagram
![Circuit Diagram](https://supreme-carnival.github.com/images/Elecronics_Shematic.png)

## Code

### Pointing Angle Calculation

#### Star Database

### Motor Control

### Telescope Control

#### Tracking

#### Calibration

## Project Flow (Who did what and when? - intended to chronicle the journey, idk if you guys want this or not)

## Results

### Raw Images

### Z-Scaled Images
(Include a brief explanation of what z-scaling is, before the images)

## Conclusion 

## Contributors and Acknowldegements
This porject was made for the spring 2021 UCSB physics 15C/13CH lab class by (in alphabetical order by last name) Collin Brahana, Sam Crossley, Montu Ganesh, and Jack Grossman, under the observation of Dr. Andrew Jayich, and TAs Sean Buechele and Mingyu Fan.