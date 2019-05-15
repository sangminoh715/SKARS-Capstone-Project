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
        x_tag = tag.x_translation()
        y_tag = tag.y_translation()
        z_tag = tag.z_translation()
        
        x_rot = tag.x_rotation()
        y_rot = tag.y_rotation()
        z_rot = tag.z_rotation()
        
        #Trig
        x = math.cos(y_rot)*x_tag - math.sin(y_rot)*z_tag
        y = math.sin(x_rot)*math.sin(y_rot)*x_tag + math.cos(x_rot)*y_tag + math.cos(y_rot)*math.sin(x_rot)*z_tag
        z = math.cos(x_rot)*math.sin(y_rot)*x_tag - math.sin(x_rot)*y_tag + math.cos(x_rot)*math.cos(y_rot)*z_tag
        
        print_args = (x, y, z, z_rot)
        uart.write("X,%f,Y,%f,Z,%f,R,%f\r\n" % print_args)
