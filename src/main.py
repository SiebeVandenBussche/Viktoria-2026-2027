#region VEXcode Generated Robot Configuration
from vex import *

brain = Brain()

# Drivetrain motors (6 total, 3 per side)
Left_motor_1 = Motor(Ports.PORT11, True)
Left_motor_2 = Motor(Ports.PORT12,  True)
Left_motor_3 = Motor(Ports.PORT13,  True)
Left = MotorGroup(Left_motor_1, Left_motor_2, Left_motor_3)

Right_motor_1 = Motor(Ports.PORT3, False)
Right_motor_2 = Motor(Ports.PORT2, False)
Right_motor_3 = Motor(Ports.PORT1, False)
Right = MotorGroup(Right_motor_1, Right_motor_2, Right_motor_3)

controller_1 = Controller(PRIMARY)

#####################
#   Drive function  #
#####################

def Drive():
    Left.set_velocity((controller_1.axis3.position() + controller_1.axis1.position()), PERCENT)
    Right.set_velocity((controller_1.axis3.position() - controller_1.axis1.position()), PERCENT)
    Left.spin(FORWARD)
    Right.spin(FORWARD)

def vexcode_driver_function():
    while competition.is_driver_control() and competition.is_enabled():
        Drive()
        wait(5, MSEC)

competition = Competition(vexcode_driver_function, None)