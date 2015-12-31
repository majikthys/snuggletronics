# snuggletronics
Wirelessly controlled Sunbeam® heated mattress pads with a Raspberry Pi.

## Software Requirements
 * bower to install angular and bootstrap (defined by .bowerrc and bower.json)
 * python 3.3+ (to run flask)
 * python modules: flask-restful, RPi.GPIO


## Hardware Requirements
 * Raspberry Pi 
 * 418MHZ ASK/OOK transmitter module

This circuit an program have been built and test on Rasberry Pi 2, with 418MHZ ASK/OOK transmitter module STPA-418H–B. 

The STPA-418H–B is available from Circuit Specialist (no affiliation) http://www.circuitspecialists.com/stpa-418h-b.html. The 

Raspberry Pi is commonly available but I encourage you to keep our maker/hacker ecosystem fertile and support vendors that create original open source hardware http://adafruit.com or http://sparkfun.com

## Installation

GPIO requires escalated privileges, so the easiest manner to install and run this software is to us pip3 to manually install all modules used:

    pip3 install flask-restful RPi.GPIO

## Running

Because GPIO requires escalated privileges, simply start using sudo

    sudo python3 runserver.py

You may, of course, also wrap with an service execution script and run as daemon, if you do so please send a merge request :)






