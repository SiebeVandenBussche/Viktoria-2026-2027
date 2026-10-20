# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       VandenBusscheSiebe                                           #
#   Created:      4/23/2026, 12:37:54 PM                                       #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
from vex import * # This gives us access to all VEX robot tools.
# ---------------------------------------------------------------------------- #
#   Devices                                                                    #
# ---------------------------------------------------------------------------- #
brain = Brain() # The robot's brain. It defines how we can call te robot and its devices.
controller = Controller() # The controller. It defines how we can call the controller and its buttons/joysticks.
left  = MotorGroup(Motor(Ports.PORT9), Motor(Ports.PORT10)) # The left motor group. It defines how we control them together. We also define which ports the motors are plugged into.
right = MotorGroup(Motor(Ports.PORT19), Motor(Ports.PORT20)) # The right motor group. It defines how we control them together. We also define which ports the motors are plugged into.
intake = Motor(Ports.PORT2, True) # The intake motors.
# ---------------------------------------------------------------------------- #
#   Drive functions                                                            #
# ---------------------------------------------------------------------------- #
k = 1 # A constant that defines the shape of the drive graph. The higher k is, the more exponential the graph becomes. The lower k is, the more linear the graph becomes. It can be changed on the fly using the controller buttons.
def driveGraph(x): # 
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
#   Intake Functions                                                                #
# ---------------------------------------------------------------------------- #
INTAKE_SPEED = 100 # Define with what speed we want the intake to run

def intakeControl(intake: Motor, controller: Controller):
    if controller.buttonL1.pressing(): # When we hold the L1-button the intake spins forward, so it can take in pins & cups.
        intake.spin(FORWARD, INTAKE_SPEED, PERCENT)
    elif controller.buttonL2.pressing(): # When we hold the L2-button the intake spins backwards, so it can take out the pins & cups.
        intake.spin(REVERSE, INTAKE_SPEED, PERCENT)
    else: # When no button is pressed, the intake doesn't move
        intake.stop()

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
        intakeControl(intake, controller)
        wait(20, MSEC)
# ---------------------------------------------------------------------------- #
#   Other thing                                                                #
# ---------------------------------------------------------------------------- #
comp = Competition(user_control, autonomous)
brain.screen.clear_screen()