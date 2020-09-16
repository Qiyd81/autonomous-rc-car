#!/usr/bin/env python
"""Interactive control for the car"""
import time
import io
import pygame
import pygame.font
import picamera
import configuration
import helpers.motor_driver as motor_driver_helper
import helpers.image as image_helper
import RPi.GPIO as GPIO
#import CV2
import matplotlib.pyplot as plt
from PIL import Image

UP = DOWN = LEFT = RIGHT = ACCELERATE = DECELERATE = False

def get_keys(direction):
    """Returns a tuple of (UP, DOWN, LEFT, RIGHT, change, ACCELERATE,
    DECELERATE, stop) representing which keys are UP or DOWN and
    whether or not the key states changed.
    """
    change = False
    #stop = False 
    key_to_global_name = {
        pygame.K_ESCAPE: 'QUIT',
        pygame.K_q: 'QUIT',
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',        
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_w: 'ACCELERATE',
        pygame.K_s: 'DECELERATE'
    }
    for event in pygame.event.get():
        if event.type in {pygame.K_q, pygame.K_ESCAPE}:
            #stop = True
            direction = key_to_global_name[event.key]
        elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
            down = (event.type == pygame.KEYDOWN)
            up = (event.type == pygame.KEYUP)
            change = (event.key in key_to_global_name)
            #if event.key in key_to_global_name:
            if change and down:
                direction = key_to_global_name[event.key]
            elif change and up:
                direction = "IDLE"
            else:
                pass
        else:
            pass
    return direction

def interactive_control():
    """Runs the interactive control"""
    setup_interactive_control()
    clock = pygame.time.Clock()
    with picamera.PiCamera() as camera:
        camera.resolution = configuration.PICAMERA_RESOLUTION
        camera.framerate = configuration.PICAMERA_FRAMERATE
        time.sleep(configuration.PICAMERA_WARM_UP_TIME)
        #GPIO.output(LEFT_MOTOR_ENABLE_PIN, GPIO.HIGH)
        #GPIO.output(RIGHT_MOTOR_ENABLE_PIN, GPIO.HIGH)        
        left_pwm, right_pwm = motor_driver_helper.get_pwm_imstance()
        motor_driver_helper.start_pwm(left_pwm, right_pwm)

        duty_cycle = configuration.INITIAL_PWM_DUTY_CYCLE
        direction = "IDLE"
        while True:
            direction = get_keys(direction)
            if direction == "QUIT":
                motor_driver_helper.set_idle_mode()
                print("quit mode")
            
            elif direction == "ACCELERATE":
                duty_cycle = duty_cycle + 3 if (duty_cycle + 3) <= 100 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(left_pwm, right_pwm, duty_cycle)
                print("speed: " + str(duty_cycle))
            elif direction == "DECELERATE":
                duty_cycle = duty_cycle - 3 if (duty_cycle - 3) >= 0 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(left_pwm, right_pwm, duty_cycle)
                print("speed: " + str(duty_cycle))
            elif direction == 'UP':
                motor_driver_helper.set_forward_mode()
                print("up" + str(duty_cycle))
            elif direction == 'DOWN':
                motor_driver_helper.set_reverse_mode()
                print("down" + str(duty_cycle))  
            elif direction == 'LEFT':
                motor_driver_helper.set_left_mode()
                print("left" + str(duty_cycle))
            elif direction == 'RIGHT':
                motor_driver_helper.set_right_mode()
                print("right" + str(duty_cycle))
            else:
                motor_driver_helper.set_idle_mode()
                print("no input")
                pass
            #print(direction)
            # 打开预览
            #camera.start_preview()
            # 垂直翻转
            camera.vflip = True
            # 水平翻转
            camera.hflip = True
            # 是否旋转
            #camera.rotation = 0
            # 控制摄像头亮度
            #camera.brightness = 60

            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            image_helper.save_image_with_direction(stream, direction)
            #image = stream.array
            #image_resize = CV2.rezie(image, (320,240))
#             stream.seek(0)
#             image = Image.open(stream)
#             plt.imshow(image)
            stream.flush()
            #GPIO.cleanup() 
            #clock.tick(10)
        pygame.quit()
        left_pwm.stop()
        right_pwm.stop()

def setup_interactive_control():
    """Setup the Pygame Interactive Control Screen"""
    pygame.init()
    display_size = (300, 400)
    screen = pygame.display.set_mode(display_size)
    background = pygame.Surface(screen.get_size())
    color_white = (255, 255, 255)
    display_font = pygame.font.Font(None, 40)
    pygame.display.set_caption('RC Car Interactive Control')
    text = display_font.render('Use arrows to move', 1, color_white)
    text_position = text.get_rect(centerx=display_size[0] / 2)
    background.blit(text, text_position)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def main():
    """Main function"""
    motor_driver_helper.set_gpio_pins()
    interactive_control()

if __name__ == '__main__':
    main()
