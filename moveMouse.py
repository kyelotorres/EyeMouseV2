import pyautogui as pag	#library to run function related to mouse function

xscreen,yscreen = pag.size() #get screen size and print it
print('Xscreen: '+ str(xscreen).rjust(4)+' Yscreen:' + str(yscreen).rjust(4) )
try:
	while True:
		#print the posiition of the mouse coordinates
		x,y = pag.position()
		print('X: '+ str(x).rjust(4)+' Y:' + str(y).rjust(4) )
		#make the mouse move based on key 'a' 's' 'd' 'w'
		inputs = raw_input('move:')
		if inputs == 'a':
			pag.moveRel(-50,0,duration = 0.5)
		elif inputs == 'd':
			pag.moveRel(50,0,duration = 0.5)
		elif inputs == 's':
			pag.moveRel(0,50,duration = 0.5)
		elif inputs == 'w':
			pag.moveRel(0,-50,duration = 0.5)
		else:
			print("invalid")
except KeyboardInterrupt:
	print('\nDone')
