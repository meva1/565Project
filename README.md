# 565Project User Guide

## Running the Application
The application is written in Python 3 and uses the tkinter and matplotlib modules. If these are missing they can be installed with "pip install tkinter" or "pip install matplotlib". Running the application is as simple as "python ising_gui.py"

## Features and Usage

### Ising Animation Page
The Ising animation page is the starting screen. Different values for the temperature, coupling constant and magnetic field can be selected with the sliders. To run the animation, click the "Ising animation" button. To pause the animation, click the button again. The values on the sliders can be adjusted while the animation is running and it will respond apropriately. 

There are many different configurations that can be obtained for different values on the sliders. Magnetic domains will form when run with the default values. If you then set the magnetic field to positive or negative values, the domains parallel to the field will grow while those anti parallel will shrink.
![](https://github.com/meva1/565Project/blob/master/domains.jpg)

Setting the coupling constant to -1.0 will cause spins to align anti parallel.

![](https://github.com/meva1/565Project/blob/master/negativecoupling.jpg)

Increasing the temperature above the critical temperature will cause a more disorganized pattern overall with similar localized patterns appearing unpredictably.

![](https://github.com/meva1/565Project/blob/master/negativecouplinghightemp.jpg)

### Hysteresis Page

You can navigate to the Hysteresis Page by clicking the "Hysteresis Page" button on the top row. The temperature and coupling constant can be selected from the sliders and click the "Create Magnetic Hysteresis Graph" but to generate the plot. Lowering the temperature will widen the plot while reducing the coupling constant towards 0 will narrow it. Hysteresis cannot occur for temperatures above the critical temperature or negative coupling constant.

![](https://github.com/meva1/565Project/blob/master/hysteresis.jpg)

### Critical Temperature Page

You can navigate to the Critical Temperature Page by clicking the "Critical Temperature Page" button on the top row. The coupling constant can be selected from the sliders and click the "Create Critical Temperature Graph" but to generate the plot. Lowering the coupling constant towards 0 will cause the critical temperature to drop. Below 0 coupling constant there will not be a phase change and so critical temperature.

![](https://github.com/meva1/565Project/blob/master/crittemp.jpg)

