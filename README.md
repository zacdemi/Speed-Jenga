# ScaleJenga

A fast-paced Jenga experience. 

## Hardware
For a basic weight sensing hardware setup to begin playing ScaleJenga and playing around with your own modifications to the ScaleJenga code, only a few components are needed:
1. Load cell
2. Platform for Jenga tower
3. Load cell Amplifier
4. Serial communications and microprocessor (for weighing and reporting)

You can piece together your own hardware for the above, however, we’ve selected two components, which, for under $40 can get you up and running with minimal effort. 

### OpenScale
This Sparkfun board is an easy solution to provide both the load cell amplifier and serial communications. It contains the HX711 amplifier chip, an Atmel microprocessor, and USB interface. Everything you need to interface a PC or Mac to digitally read the weight measured by a load cell. 
https://www.sparkfun.com/products/13261 (~$30)

### Cheap Kitchen Scale
Any load cell should do, however, it’s likely easiest and cheapest to buy a prebuilt kitchen scale and use the internals of this. Most cheap kitchen scales should work just fine, all you’re looking for is a mechanical base, load cell, and platform to set the Jenga tower on. This provides a prebuilt platform already mounted to the load cell. All that needs to be done is to open up the scale to access the four wires exiting the load cell and attach them color for color to the OpenScale’s terminal block. 
Cheap Scale on Amazon (~$9):https://www.amazon.com/Threatened-competitor-Scale-Capacity-Stainless/dp/B004G7IRN0 

The load cell in these types of scales are typically rectangular aluminum blocks designed to flex slightly when any weight is cantilevered on the end. This scale attaches the platform to one end to provide the flexing. A strain gauge epoxied onto the block senses the slight mechanical changes in the system and, if supplied with a source voltage, supplies a corresponding differential voltage change. There will be four wires exiting something that looks like Figure 1, and going to a PCB in the scale itself. Simply cut the wires away from the PCB, strip away the insulation, and attach to the OpenScale, matching the colors.
Figure 1: https://www.sparkfun.com/products/13329

Connect the OpenScale via USB to the platform running your Python code and you’re now set up and ready to play ScaleJenga!
