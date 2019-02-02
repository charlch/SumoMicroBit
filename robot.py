import radio
from microbit import *


def set_motor_speeds(left_speed, right_speed):
    """
    Set both motor speeds. Speeds are floats in the range [-1.0, 1.0]
    """
    left_motor(left_speed)
    right_motor(right_speed)


def left_motor(speed):
    """
    Set left motor speed. Speed is a float in the range [-1.0, 1.0]
    """
    _set_motor(speed, pin12, pin8, pwm_index=0)


def right_motor(speed):
    """
    Set the right motor speed. Speed is a float in the range [-1.0, 1.0]"""
    _set_motor(speed, pin16, pin0, pwm_index=1)



# These counters are the globals used to keep track
# of the pwm (pulse width modulation) signals used to set motor
# speed to non binary values.
_pwm_counters = [0, 0]


def _set_motor(speed, forward_pin, backward_pin, pwm_index):
    #  Increments the counter by the speed, if the counter goes over 1
    #  then turn the motor on and reset the counter. 
    is_going_forward = speed > 0
    is_going_backwards = speed < 0
    is_motor_on = False
    _pwm_counters[pwm_index] += abs(speed)
    if _pwm_counters[pwm_index] > 1:
        is_motor_on = True
        _pwm_counters[pwm_index] -= 1
    _set_pin(forward_pin, is_going_forward & is_motor_on)
    _set_pin(backward_pin, is_going_backwards & is_motor_on)


def _set_pin(pin, value):
    pin.write_digital(value)


def main():
    channel = 0
    channel_set = False

    while not channel_set:
        sleep(100)
        if button_a.is_pressed() and button_b.is_pressed():
	        channel_set = True
        elif button_a.is_pressed():
            channel = channel - 1
        elif button_b.is_pressed():
            channel = channel + 1

        channel = channel % 10
        display.show(str(channel), wait=False, loop=True)

    display.show(Image.HAPPY, wait=True)
    sleep(500)
    display.show(str(channel), wait=False, loop=True)

    radio.config(channel=channel)
    radio.on()

    while True:
        sleep(10)
        try:
            incoming = radio.receive()
        except:
            pass
        display.show(str(incoming), wait=False, loop=False)
        if incoming == 'stop' or incoming is None:
            set_motor_speeds(0.0,0.0)
        elif incoming == 'left':
            set_motor_speeds(1.0,-1.0)
        elif incoming == 'right':
            set_motor_speeds(-1.0,1.0)
        elif incoming == 'both':
            set_motor_speeds(1.0,1.0)



main()
