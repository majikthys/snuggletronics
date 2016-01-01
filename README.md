# snuggletronics
Wirelessly controlled Sunbeam® heated mattress pads with a Raspberry Pi.

## Software Requirements
 * bower to install angular and bootstrap (defined by .bowerrc and bower.json)
 * python 3.3+ (to run flask)
 * python modules: flask-restful, wiringPi2


## Hardware Requirements
 * Raspberry Pi 
 * 418MHZ ASK/OOK transmitter module

This circuit an program have been built and test on Rasberry Pi 2, with 418MHZ ASK/OOK transmitter module STPA-418H–B. 

The STPA-418H–B is available from Circuit Specialist (no affiliation) [http://www.circuitspecialists.com/stpa-418h-b.html](http://www.circuitspecialists.com/stpa-418h-b.html). The 

Raspberry Pi is commonly available but I encourage you to keep our maker/hacker ecosystem fertile and support vendors that create original open source hardware [adafruit](http://adafruit.com) or [sparkfun](http://sparkfun.com)

## Installation

Install npm and bower if you have not yet had a chance to do so.

### install npm:

    sudo apt-get install nodejs npm
    
    # note: the following command fixes a common ubuntu npm issue, this may not be necessary in the near future
    sudo ln -s /usr/bin/nodejs /usr/bin/node 

### install bower:

    sudo npm install -g bower

### install angular, jquery, and bootstrap

bower is used to install javascript and css components of angular, bootstrap, and jquery, these dependencies are configured via bower.json and the target directory is set via .bowerrc

     # make sure you are in the directry where this README.md is located
     cd snuggletronics
     
     # install dependencies 
     bower install 

### install flask-restful

GPIO requires escalated privileges, so the easiest manner to install and run this software is to us pip3 to manually install all modules used:

    pip3 install flask-restful

### install WiringPi2

WiringPi2 needs to be built manuallly. Find canonical directions at [https://github.com/Gadgetoid/WiringPi2-Python](https://github.com/Gadgetoid/WiringPi2-Python) 


## Running the Application

Because GPIO requires escalated privileges, simply start using sudo

    sudo python3 runserver.py

Normal start up example:

    pi@raspberrypi:~/snuggletronics $ sudo python3 runserver.py 
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger pin code: 280-224-703

You may, of course, also wrap with an service execution script and run as daemon, if you do so please send a merge request :)

Viewed through browser

![Mobile Interface](docs/phone.jpg "Mobile app")




