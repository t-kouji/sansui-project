import time
import RPi.GPIO as gpio

hi_sw_pin = 20
lo_sw_pin = 21
control_out = 18


gpio.cleanup()

gpio.setmode(gpio.BCM)
gpio.setup(hi_sw_pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(lo_sw_pin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(control_out,gpio.OUT)
pwmoutput = gpio.PWM(control_out,50) #GPIO１８をpwmoutputオブジェクトとして作成。50Hzで設定

count = 0

while True:
	print("Hi ",gpio.input(hi_sw_pin ))
	print("Lo ",gpio.input(lo_sw_pin ))
	if (gpio.input(hi_sw_pin )) == (gpio.input(lo_sw_pin )) ==1:
		print("ポンプON！")
		count += 1
		print("count:",count)
		pwmoutput.start(50) #PWMを初期化。また、初期の値を50(duty比)とする。
		time.sleep(5)
		
	if (gpio.input(hi_sw_pin )) == (gpio.input(lo_sw_pin )) ==0:
		print("ポンプOFF！")
		pwmoutput.stop()
	time.sleep(2)




