import sensor, image, time, math
from pyb import UART

# Camera Setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

# UART Setup
uart = UART(3, 115200)
clock = time.clock()

def degrees(radians):
    return (180 * radians) / math.pi

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(),
        degrees(tag.z_rotation()))
        uart.write("X,%f,Y,%f,Z,%f,R,%f\r\n" % print_args)

