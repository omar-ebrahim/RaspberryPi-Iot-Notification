import RPi.GPIO as GPIO
import RGB1602
import time

# initialise the LCD - 16 columns 2 rows
lcd = RGB1602.RGB1602(16, 2)

colour_red = (255, 0, 0)
colour_green = (0, 255, 0)
colour_blue = (0, 0, 255)

lcd.clear()

time.sleep(1)
lcd.show_cursor()
lcd.setCursor(0, 0)
lcd.printout("new message")

lcd.setCursor(0, 1)
lcd.printout("qwertyuiopasdfghjklzxcvbnm")

time.sleep(1)
lcd.setCursor(1,1)
time.sleep(1)
lcd.scrollLeft()
time.sleep(1)
lcd.scrollLeft()

