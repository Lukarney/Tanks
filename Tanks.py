from cmu_112_graphics import *
from tkinter import*
from PIL import Image #
import math
class Tank(object):
    def __init__(self,mode):
        self.mode=mode
        self.lives=3
        self.x=self.mode.app.width//2
        self.y=self.mode.app.width//2
        self.dx=10
        self.direction="Right"
        self.angle=0
        self.armLength=25
        self.armWidth=10
        tacoURL='https://i.imgur.com/sQSdSo8.png'
        tacoImage=self.mode.loadImage(tacoURL)
        self.tacoImage=self.mode.scaleImage(tacoImage,1/10)
        self.armX1=self.x
        self.armY1=self.y-10
        self.armX2=self.x+self.armLength
        self.armY2=self.y-18
        self.armX3=self.armX1-3
        self.armY3=self.armY1-4
        self.armX4=self.armX2-3
        self.armY4=self.armY2-4
        self.newArmXDistance=0
        self.newArmYDistance=0
        self.armImageX=0
        self.armImageY=0
        heartURL=('https://cdn.pixabay.com/photo/2017/09/23/16/33/'+
        'pixel-heart-2779422_1280.png')
        heart=self.mode.loadImage(heartURL)
        self.heart=self.mode.scaleImage(heart,1/30)

    def move(self,cordinate):
        if cordinate=="Right":
            self.x=self.x+self.dx
            self.direction=cordinate
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        if cordinate=="Left":
            self.x=self.x-self.dx
            self.direction=cordinate
        if cordinate=="Up":
            self.angle+=5
            if self.angle>90:
                self.angle=90
        if cordinate=="Down":
            self.angle-=5
            if self.angle<-30:
                self.angle=-30
        print(self.angle)
        if cordinate=="Space":
            self.mode.bullets.append(Bullet(self.mode,self.x,self.y,
            self.direction,self.angle))
        if(self.x>self.mode.app.width):
            self.x-=self.dx
        if self.x<0:
            self.x+=self.dx

    def moveTankArm(self):
        self.tacoImage.rotate(2*math.radians(self.angle))
        
        #if we want the arm to follow the mouse cursor
        deltaY=self.mode.cursor[1]-self.armY1
        deltaX=self.mode.cursor[0]-self.armX1
        if deltaX<2:
            deltaX=2
        
        theta=math.atan(deltaY/deltaX)
        self.newArmXDistance=self.armLength*math.cos(math.radians(self.angle))
        self.newArmYDistance=self.armLength*math.sin(math.radians(self.angle))
        bottomAngle=0
        self.armX1=self.x
        self.armY1=self.y-10
        if self.direction=="Right":
            self.armX2=self.armX1+self.newArmXDistance
            self.armImageX=self.x+self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            self.armX2=self.armX1-self.newArmXDistance
            self.armImageX=self.x-self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        self.armY2=self.armY1-self.newArmYDistance
        self.armX3=self.armX1-6
        self.armY3=self.armY1-12
        self.armX4=self.armX2-6
        self.armY4=self.armY2-12
        self.armImageY=self.y-10-self.newArmYDistance/2
        

    def checkBulletCollisions(self):
        bulletsToKeep=[]
        for i in range(len(self.mode.bullets)):
            if self.mode.bullets[i].containsPoint(self.x,
            self.y) and isinstance(self.mode.bullets[i],Bullet):
                self.lives-=1
            else:
                bulletsToKeep+=[self.mode.bullets[i]]
        self.mode.bullets=bulletsToKeep
    
    def timerFired(self):
        self.checkBulletCollisions()
        self.moveTankArm()


    def draw(self, canvas):
        if(self.mode.isGameOver==False):
            canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
            fill='green')
            canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
            self.armX4,self.armY4,self.armX3,self.armY3,fill='green')
        #draw lives in the top right
        for i in range(self.lives):
            canvas.create_image(self.mode.app.width-(1+i)*50, 40,
        image=ImageTk.PhotoImage(self.heart))
        canvas.create_image(self.armImageX,
        self.armImageY,image=ImageTk.PhotoImage(self.tacoImage))

class Block(object):
    pass
class Bullet(object):
    def __init__(self,mode,x,y,direction,angle):
        self.mode=mode
        #initial x and y
        self.x=x
        self.y=y-10
        self.direction=direction
        self.angle=math.radians(angle)
        self.change=(0,0)
        self.gravity=9.81
        self.velocity=50
        self.initialDistanceXAdded=self.mode.tank1.armLength*2*math.cos(self.angle)
        #15 is a random distance, but it will be the size of the tank ?arm?
        self.initialDistanceYAdded=self.mode.tank1.armLength*2*math.sin(self.angle)
        self.time=0
        #the change in x and y and the position of the bullet
        self.dy=0
        self.dx=0
        if self.direction=="Right":
            self.x+=self.initialDistanceXAdded
            self.y-=self.initialDistanceYAdded
        else:
            self.x-=self.initialDistanceXAdded
            self.y-=self.initialDistanceYAdded

    def __eq__(self,other):
        return isinstance(other,Bullet)
    
    def __hash__(self):
        return hash(self.x,self.y,self.direction,self.angle)
    
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5
    #checks if the item contains the point
    def containsPoint(self,x,y):
        return self.distance(self.dx,self.dy,x,y)<11

    def convertAngle(self):
        return (self.velocity*math.cos(self.angle),self.velocity*math.sin(self.angle))
    
    def fireBullet(self,direction):
        vx=self.velocity*math.cos(self.angle)
        vy=self.velocity*math.sin(self.angle)
        self.time+=.1
        if self.direction=="Right":
            self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
            self.dx=self.x+vx*self.time
        if self.direction=="Left":
            self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
            self.dx=self.x-vx*self.time

        
    def timerFired(self):
        self.fireBullet(self.direction)
        self.change=self.convertAngle()
        # if self.direction=="Right":
        #     self.x+=self.change[0]
        #     self.y-=self.change[1]
        # else:
        #     self.x-=self.change[0]
        #     self.y-=self.change[1]

    def draw(self,canvas):
        canvas.create_oval(self.dx+5,self.dy+5,self.dx-5,self.dy-5,
        fill='black')
class GameMode(Mode):
    def appStarted(mode):
        mode.cursor=[-1,-1]
        mode.bullets=[]
        mode.hearts=[]
        mode.tank1=Tank(mode)
        #creates enemy cactus in cacti dictionary
        
        #sets up functions for the end game
        mode.died=False
        mode.isGameOver=False
    #checks to see if a key is pressed
    def keyPressed(mode,event):
        mode.tank1.move(event.key)
        if (event.key=='h'):
            mode.app.setActiveMode(mode.app.helpMode)
        
        #checks to see if game is over and sets up for end game screen
        if(mode.isGameOver==True):
            if event.key=="r":
                mode.appStarted()
    #moves cursor with mouse
    def mouseMoved(mode,event):
        # mode.app._root.configure(cursor='none')
        mode.cursor=[event.x,event.y]
    #collects hear when mouse is pressed
    def mousePressed(mode,event):
        for heart in mode.hearts:
            if heart.containsPoint(event.x+mode.scrollX,event.y):
                mode.draggingHeart=heart
    def mouseReleased(mode,event):
        pass
    def mouseDragged(mode,event):
        mode.cursor=[event.x,event.y]
        pass
        # if not mode.draggingHeart is None:
        #     mode.draggingHeart.x=event.x+mode.scrollX
        #     mode.draggingHeart.y=event.y

    def timerFired(mode):
        mode.tank1.timerFired()
        for bullet in mode.bullets:
            bullet.timerFired()
        if(mode.isGameOver==False):
            pass
        #changes isGameOver if player died
        if(mode.died==True):
            mode.isGameOver=True
         
    def redrawAll(mode,canvas):
        mode.tank1.draw(canvas)
        for bullet in mode.bullets:
            bullet.draw(canvas)
        if(mode.isGameOver==True):
            if(mode.died==True):
                font = 'Arial 26 bold'
                canvas.create_text(mode.width/2, 150, 
                text="You did not make it :(\n press r to restart", font=font)   
            else:
                font = 'Arial 26 bold'
                text=('WINNER!\n'+
                'press r to restart')
                canvas.create_text(mode.width/2, 150,text=text, font=font)

class SplashScreenMode(Mode):
    def appStarted(mode):
        pass
    def redrawAll(mode, canvas):
        pass
    def keyPressed(mode, event):
        pass
class HelpMode(Mode):
    def appStarted(mode):
        pass
    #draws background
    def redrawAll(mode, canvas):
        pass
    #if any key is pressed the game starts
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
#holds all the game functions
class MyModalApp(ModalApp):
    def appStarted(app):
        #app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        #app.helpMode = HelpMode()
        app.setActiveMode(app.gameMode)
        #app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50
 
def runTanks():
    MyModalApp(width=600,height=600)
runTanks()