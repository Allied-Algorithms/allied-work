"""Copy this file to run1.py, run2.py ... then:  python run.py run1"""
from alliedwork import *

set_pose(x=0, y=0, heading=0)       # the launch area's start pose

# M01_example: drive to the approach pose, then push the model
mission("M01")
drive_to(43, 16, 8)
turn_to(0)
drive(4, 4)                         # slow near models
drive(-4, 4)
