# UHAP (Unified Home Automation Platform)

## Brief
UHAP is a python writen home automation control platform, it allows user to integrate different brands of IoT device to the platform and allow them to work together as a system.

## Function discription
The software allow user to run the program at the platform and using script to do a single or multiple action as a scene package. The event triger can be customized to fit in different situations.
Using different [API](#API-supported) from the manufacture, the platform is allow control from the user interface into command send to the device and preform actions. By doing so, some of the device which has [API](#API-supported) on local area network can be respond in millesecond and make the workflow more smooth.

## Support system
* Linux
_// Under development_

## Installation
_// Under development_

## Clone the repo
1. Make sure you have Python [3.11](https://www.python.org/downloads/release/python-3110/) or higher version installed.
2. Clone the repository to local machine ``git clone https://github.com/qqpp4130/UHAP.git``
3. Enter the cloned repo ``cd .\UHAP``
4. Enter the virtual enviroment and install dependency ``python -m venv env`` <br>
	4.1. If the pip is not installed, use this command ``python -m pip install --upgrade pip``
	4.2. Install dependency ``python -m pip install -r requirements.txt``
5. Build _// Under development_ <br>
	5.1. Please follow the [guide](#content-guide) to put the content to right directory<br>
	5.2. When commit your contribution, please briefly discribe the content you commiting<br>

## Check out the example
1. [Clone](#clone-the-repo) the repo and enter the virtual enviroment
2. Run ``python ./Example/ui_showcase.py``
3. Use web browser access url [localhost:8080](http://localhost:8080/page/index) to see the example UI

## Content guide
* ``Scripts`` for python enviroment setup and pre-requirement for launch development enviroment<br>
* ``src`` for core function implimentation for better coding:<br>
    ![Linus](https://pic1.zhimg.com/v2-08509d0e37e2787cb0a5e1df5c15f331_720w.jpg?source=172ae18b)<br>
* ``var`` for build-in content for development<br>
    * ``blueprint`` for automation blueprint<br>
    * ``img`` for front end developer to store UI/UX elements<br>
    * ``scheme`` for API scheme collected for future implimentation<br>
    

## API supported
_// Under development_

## Support us
_// Link under development_

## Special Thanks
[Smart Home Connect](https://smarthomeconnect.readthedocs.io/en/latest/)
