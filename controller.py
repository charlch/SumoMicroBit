import radio
from microbit import display, Image, button_a, button_b, sleep


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
        if button_a.is_pressed() and button_b.is_pressed():
            radio.send('both')
            display.show('b', wait=False, loop=False)
        elif button_a.is_pressed():
            radio.send('left')
            display.show('l', wait=False, loop=False)
        elif button_b.is_pressed():
            radio.send('right')
            display.show('r', wait=False, loop=False)
        else:
            radio.send('stop')
            display.show(str(channel), wait=False, loop=True)

main()
