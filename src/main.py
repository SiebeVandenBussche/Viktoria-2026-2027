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
intake = Motor(Ports.PORT3, True) # The intake motors.

# Lift
lift = MotorGroup( # Both lift motors are in a motor group, so the left and right are controlled together.
    Motor(Ports.PORT2, GearSetting.RATIO_36_1, False), # Red Cartridge (36:1) for more torque, not reversed
    Motor(Ports.PORT12, GearSetting.RATIO_36_1, True) # Red Cartridge (36:1) for more torque, reversed, because the motor is mounted in the opposite direction
)
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
#   Intake Functions                                                           #
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
#   Lift Functions                                                           #
# ---------------------------------------------------------------------------- #
LIFT_MIN = 0 # The lowest position of the lift, in degrees.
LIFT_MAX = 1400 # To find put on 300 then go run code and go lift higher, if not at limit raise LIFT_MAX by 200-300, repeat, if lift at height limit do that degree maybe minus 20 or 30???

LIFT_KP = 0.25 # How strong the lift reacts to the error. Higher is faster.
LIFT_TOLERENCE = 10 # How many degrees the lift may be off target and still be considered as at the target position.
LIFT_MANUAL_STEP = 8 # How many degrees the target moves each loop while we hold the buttons.

lift.set_stopping(HOLD) # When the lift is not moving, it will hold its position.
lift.set_position(0, DEGREES) # Sets the current position as 0, so the lift must be fully down when the program starts.

lift_target = 0 # The position in degrees where we want the lift to go.

def lift_update():
    """
    Moves the lift to the target position using a simple proportional controller. The further away, the faster it moves.
    """
    global lift_target # We change it in this function, so it needs to be global.

    # Keeps the lift target within the limits of the lift, so it doesn't try to go higher or lower than it can.
    if lift_target > LIFT_MAX:
        lift_target = LIFT_MAX
    if lift_target < LIFT_MIN:
        lift_target = LIFT_MIN

    position = lift.position(DEGREES) # Where the lift is now.
    error = lift_target - position # How far away the lift is from the target position. Positive = up, Negative = down

    # If the lift is close enough to the target position, we stop moving it, and hold it in place.
    if error < LIFT_TOLERENCE and error > -LIFT_TOLERENCE:
        lift.stop()
        return

    speed = error * LIFT_KP # A big error gives a high speed, so the lift slows down as it gets closer.

    # Limits the speed to a maximum of 100% up and down.
    if speed > 100:
        speed = 100
    if speed < -100:
        speed = -100

    lift.spin(FORWARD, speed, PERCENT) # If speed is negative, it goes down.

def lift_control():
    """
    Lets the driver move the lift. R1 and R2 only change the target position, the lift_update function moves the lift to that position.
    """
    global lift_target # We change it in this function, so it needs to be global.

    if controller.buttonR1.pressing(): # When we hold the R1-button the target goes up.
        lift_target = lift_target + LIFT_MANUAL_STEP
    if controller.buttonR2.pressing(): # When we hold the R2-button the target goes down.
        lift_target = lift_target - LIFT_MANUAL_STEP

    # Maybe possible like set heights? For later
    lift_update() # Runs every loop, so the lift will always move to the target position, even if we don't press any buttons.


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
        lift_control()
        brain.screen.set_cursor(2, 1)
        brain.screen.print("LIFT:", lift.position(DEGREES))
        wait(20, MSEC)
# ---------------------------------------------------------------------------- #
#   Other thing                                                                #
# ---------------------------------------------------------------------------- #
comp = Competition(user_control, autonomous)
brain.screen.clear_screen()