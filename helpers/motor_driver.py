"""Helpers for controlling the right and Back Motors"""
import configuration
import RPi.GPIO as GPIO
import time

LEFT_MOTOR_DATA_ONE = configuration.LEFT_MOTOR_DATA_ONE
LEFT_MOTOR_DATA_TWO = configuration.LEFT_MOTOR_DATA_TWO
LEFT_MOTOR_ENABLE_PIN = configuration.LEFT_MOTOR_ENABLE_PIN
RIGHT_MOTOR_DATA_ONE = configuration.RIGHT_MOTOR_DATA_ONE
RIGHT_MOTOR_DATA_TWO = configuration.RIGHT_MOTOR_DATA_TWO
RIGHT_MOTOR_ENABLE_PIN = configuration.RIGHT_MOTOR_ENABLE_PIN
PWM_FREQUENCY = configuration.PWM_FREQUENCY
INITIAL_PWM_DUTY_CYCLE = configuration.INITIAL_PWM_DUTY_CYCLE
INITIAL_TIME_SLEEP = configuration.INITIAL_TIME_SLEEP

def set_left_mode():
    """Set mode to Right"""
    GPIO.output(LEFT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DATA_TWO, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_DATA_ONE, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_DATA_TWO, GPIO.LOW)
    time.sleep(INITIAL_TIME_SLEEP)
    print("left turn")
    #GPIO.cleanup()

def set_right_mode():
    """Set mode to Left"""
    GPIO.output(LEFT_MOTOR_DATA_ONE, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_DATA_TWO, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_DATA_TWO, GPIO.HIGH)
    time.sleep(INITIAL_TIME_SLEEP)
    #GPIO.cleanup()

def set_reverse_mode():
    """Set mode to Reverse"""
    GPIO.output(LEFT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DATA_TWO, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_DATA_TWO, GPIO.HIGH)
    time.sleep(INITIAL_TIME_SLEEP)
    #GPIO.cleanup()

def set_forward_mode():
    """Set mode to Forward"""
    GPIO.output(LEFT_MOTOR_DATA_ONE, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_DATA_TWO, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_DATA_ONE, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_DATA_TWO, GPIO.LOW)
    time.sleep(INITIAL_TIME_SLEEP)
    #GPIO.cleanup()

def set_idle_mode():
    """Set mode to Idle"""
    set_left_motor_to_idle()
    set_right_motor_to_idle()

def set_left_motor_to_idle():
    """Sets the Back motor to Idle state"""
    GPIO.output(LEFT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DATA_TWO, GPIO.LOW)

def set_right_motor_to_idle():
    """Sets the right motor to Idle state"""
    GPIO.output(RIGHT_MOTOR_DATA_ONE, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_DATA_TWO, GPIO.LOW)

def set_gpio_pins():
    """Sets the GPIO pins for the two motors"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LEFT_MOTOR_DATA_ONE, GPIO.OUT)
    GPIO.setup(LEFT_MOTOR_DATA_TWO, GPIO.OUT)
    GPIO.setup(RIGHT_MOTOR_DATA_ONE, GPIO.OUT)
    GPIO.setup(RIGHT_MOTOR_DATA_TWO, GPIO.OUT)
    GPIO.setup(LEFT_MOTOR_ENABLE_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_MOTOR_ENABLE_PIN, GPIO.OUT)

def get_pwm_imstance():
    """Returns a PWM instance"""
    return GPIO.PWM(LEFT_MOTOR_ENABLE_PIN, PWM_FREQUENCY), GPIO.PWM(RIGHT_MOTOR_ENABLE_PIN, PWM_FREQUENCY)

def start_pwm(left_pwm, right_pwm):
    """Starts the PWM with the initial duty cycle"""
    left_pwm.start(INITIAL_PWM_DUTY_CYCLE)
    right_pwm.start(INITIAL_PWM_DUTY_CYCLE)

def change_pwm_duty_cycle(left_pwm, right_pwm, duty_cycle):
    """Change the PWM duty cycle"""
    left_pwm.ChangeDutyCycle(duty_cycle)
    right_pwm.ChangeDutyCycle(duty_cycle)
    
# set_gpio_pins();
# set_left_mode()
# GPIO.cleanup()

