# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       VandenBusscheSiebe                                           #
#   Created:      4/23/2026, 12:37:54 PM                                       #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
from vex import *
# ---------------------------------------------------------------------------- #
#   Devices                                                                    #
# ---------------------------------------------------------------------------- #
brain = Brain()
controller = Controller()
left  = MotorGroup(Motor(Ports.PORT9), Motor(Ports.PORT10))
right = MotorGroup(Motor(Ports.PORT19), Motor(Ports.PORT20))
# ---------------------------------------------------------------------------- #
#   Drive functions                                                            #
# ---------------------------------------------------------------------------- #
k = 1
def driveGraph(x):
    """
    A simple mathemathic function to translate controller input into velocity output.
    """
    return (x * k) / 10 ** ((k - 1) * 2)
def changeDriveGraph(controller: Controller):
    """
    changes the constant in the DriveGraph on button press
    """
    global k
    if controller.buttonUp.pressed:
        k+=1
    elif controller.buttonDown.pressed:
        k-=1
    controller.screen.clear_screen()
    controller.screen.print(k)
def arcadeDriveGraph(left: MotorGroup, right: MotorGroup, controller: Controller):
    """
    Arcade drive using the left joystick for forward/backward movement and the right joystick for turning.
    a graph translates forward controller input to forward speed.
    """
    left.set_velocity((driveGraph(controller.axis3.position()) + controller.axis1.position()), PERCENT)
    right.set_velocity(-(driveGraph(controller.axis3.position()) - controller.axis1.position()), PERCENT)
    left.spin(FORWARD)
    right.spin(FORWARD)
# ---------------------------------------------------------------------------- #
#   Competition                                                                #
# ---------------------------------------------------------------------------- #
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Autonomous")
    # place autonomous code here
def user_control():
    brain.screen.clear_screen()
    brain.screen.print("Driver Control")
    while True:
        arcadeDriveGraph(left, right, controller)
        wait(20, MSEC)
# ---------------------------------------------------------------------------- #
#   Other thing                                                                #
# ---------------------------------------------------------------------------- #
comp = Competition(user_control, autonomous)
brain.screen.clear_screen()