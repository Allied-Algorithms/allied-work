"""Test run: drives a 24 in square. Put the robot at the start, then:  python run.py test"""
from alliedwork import *

set_pose(x=20, y=10, heading=0)     # where the robot sits at the start (room to drive up + right)

for _ in range(4):
    drive(24, 8)                    # 24 inches forward
    turn(90)                        # quarter turn right
beep()
log("square done")
