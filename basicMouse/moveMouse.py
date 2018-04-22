import pyautogui as pag	#library to run function related to mouse function

def moveMouse(x,y,(lbx,lby),(rbx,rby),(ubx,uby),(dbx,dby)):
    waitTime = 0.05
    moveSpace = 10
    rbx = rbx-lbx
    x = x - lbx
    dby = dby-uby
    y = y - uby
    print('rbx:'+str(rbx)+'x:'+str(x))
    if x < 0.25*rbx:
        pag.moveRel(moveSpace,0,duration = waitTime)
    if x > 0.75*rbx:
        pag.moveRel(-moveSpace,0,duration = waitTime)
    if y < 0.25*dby:
        pag.moveRel(0,-moveSpace,duration = waitTime)
    if y > 0.75*dby:
        pag.moveRel(0,moveSpace,duration = waitTime)

