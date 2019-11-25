
# CITATION: I got the cmu_112_graphics from 15-112 website
from cmu_112_graphics import *
from tkinter import*
from PIL import Image #
import math
import random
class Tank(object):
    def __init__(self,mode,x,y,direction):
        self.mode=mode
        self.lives=3
        self.alive=True
        self.x=x
        self.y=y
        self.dx=10
        self.direction=direction
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
        self.bulletTimer=0
        self.time=0
        self.timeDied=0
        #for angle in range(0,180)
        #self.tacoDict
        heartURL=('https://cdn.pixabay.com/photo/2017/09/23/16/33/'+
        'pixel-heart-2779422_1280.png')
        heart=self.mode.loadImage(heartURL)
        self.heart=self.mode.scaleImage(heart,1/30)

    def move(self,cordinate):
        if cordinate=="Right":
            self.x=self.x+self.dx
            self.direction=cordinate
            self.tacoImage=self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        if cordinate=="Left":
            self.x=self.x-self.dx
            self.direction=cordinate
            self.tacoImage=self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
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
            if self.bulletTimer>=1:
                self.bulletTimer=0
                if self.alive==True:
                    if self.mode.BulletTypes[self.mode.BulletTypeIndex]=="Bullet":
                        self.mode.bullets.append(Bullet(self.mode,self.x,self.y,
                        self.direction,self.angle))
                    if self.mode.BulletTypes[self.mode.BulletTypeIndex]=="Bomb":
                        self.mode.bullets.append(Bomb(self.mode,self.x,self.y,
                        self.direction,self.angle))
                    if self.mode.BulletTypes[self.mode.BulletTypeIndex]=="Missile":
                        self.mode.bullets.append(Missile(self.mode,self.x,self.y,
                        self.direction,self.angle))
        if(self.x>self.mode.app.width):
            self.x-=self.dx
        if self.x<0:
            self.x+=self.dx
    #moves tank arm
    def moveTankArm(self):
        #here to help me figure out how to rotate images
        #self.tacoImage = self.tacoImage.rotate(self.angle)
        #dict[angle]=image
        self.tacoImage.rotate(self.angle)
        
        #if we want the arm to follow the mouse cursor
        deltaY=self.mode.cursor[1]-self.armY1
        deltaX=self.mode.cursor[0]-self.armX1
        if deltaX<2:
            deltaX=2
        theta=math.atan(deltaY/deltaX)
        #uses the angle given by using up and down arrows
        self.newArmXDistance=self.armLength*math.cos(math.radians(self.angle))
        self.newArmYDistance=self.armLength*math.sin(math.radians(self.angle))
        bottomAngle=0
        self.armX1=self.x
        self.armY1=self.y-10
        #sets up the barrel(arm) of the tank to move around
        if self.direction=="Right":
            self.armX2=self.armX1+self.newArmXDistance
            self.armImageX=self.x+self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            self.armX2=self.armX1-self.newArmXDistance
            self.armImageX=self.x-self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        #sets up the y position of the arm to move around
        self.armY2=self.armY1-self.newArmYDistance
        self.armX3=self.armX1-6
        self.armY3=self.armY1-12
        self.armX4=self.armX2-6
        self.armY4=self.armY2-12
        self.armImageY=self.y-10-self.newArmYDistance/2
        
    #check to see if the bullet collided with the tank
    #if it hasn't then it will add to a new list that will then
    #become the list that holds bullets on the screen
    def checkBulletCollisions(self):
        bulletsToKeep=[]
        for i in range(len(self.mode.bullets)):
            direction=self.mode.bullets[i].direction
            if (self.mode.bullets[i].containsPoint(self.x,
            self.y) and isinstance(self.mode.bullets[i],Bomb)):
                self.lives-=1
                if direction=="Right":
                    self.x+=10
                if direction=="Left":
                    self.x-=10
            elif self.mode.bullets[i].containsPoint(self.x,
            self.y) and isinstance(self.mode.bullets[i],Bullet):
                self.lives-=1
            else:
                bulletsToKeep+=[self.mode.bullets[i]]
        self.mode.bullets=bulletsToKeep
    
    def checkIfAlive(self):
        if self.lives==0:
            self.alive=False

    def timerFired(self):
        self.bulletTimer+=.1
        self.time+=1
        self.checkIfAlive()
        if self.alive==True:
            self.checkBulletCollisions()
            self.moveTankArm()
        


    def draw(self, canvas):
        if self.alive==True:
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

class Enemy(Tank):
    def __init__(self,mode,x,y,direction):
        self.mode=mode
        self.lives=3
        self.alive=True
        self.x=x
        self.y=y
        self.dx=10
        self.direction=direction
        self.angle=30
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
        self.bulletTimer=0
        self.time=0
        self.timeDied=0
        #for angle in range(0,180)
        #self.tacoDict

    def timerFired(self):
        if self.bulletTimer>3:
                self.bulletTimer=0
                if self.alive==True:
                    self.mode.bullets.append(Bullet(self.mode,self.x,self.y,
                    self.direction,self.angle))
        self.bulletTimer+=.1
        self.time+=1
        self.checkIfAlive()
        if self.alive==True:
            self.checkBulletCollisions()
            self.moveTankArm()

    def checkIfAlive(self):
        if self.lives==0:
            self.mode.tankEnemyKills+=1
            self.lives-=1
            self.alive=False
            self.mode.points+=15
            self.timeDied=self.mode.totalTime
    
    def draw(self, canvas):
        if self.alive==True:
            if(self.mode.isGameOver==False):
                canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
                fill='red')
                canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
                self.armX4,self.armY4,self.armX3,self.armY3,fill='red')

class ZombieEnemy(Enemy):
    def draw(self, canvas):
        if self.alive==True:
            if(self.mode.isGameOver==False):
                canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
                fill='red')
                canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
                self.armX4,self.armY4,self.armX3,self.armY3,fill='purple')

class ZombieFriend(Tank):
    pass        

class Player(Tank):

    def timerFired(self):
        self.bulletTimer+=.1
        self.time+=1
        if len(self.mode.coins)<10 and self.time%100==0:
            for i in range(1):
                randomX=random.randint(10,self.mode.app.width)
                randomY=random.randint(10,self.mode.app.height//2)
                self.mode.coins.append(Coin(self.mode,randomX,randomY))
        self.checkIfAlive()
        if self.alive==True:
            self.checkBulletCollisions()
            self.moveTankArm()

    


class Coin(object):
    def __init__(self,mode,x,y):
        self.mode=mode
        self.x=x
        self.y=y
        self.time=0
    
    def __eq__(self,other):
        return isinstance(other,Coin)
    
    def __repr__(self):
        return f'{self.x},{self.y}'
    
    def __hash__(self):
        return hash(self.x,self.y)
    #checks the distnce between two points
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5
    #checks if the item contains the point
    def containsPoint(self,x,y):
        return self.distance(self.x,self.y,x,y)<10
    
            



    def draw(self,canvas):
        canvas.create_oval(self.x-5,self.y-5,self.x+5,self.y+5,fill='yellow')
class Bullet(object):
    def __init__(self,mode,x,y,direction,angle):
        self.mode=mode
        #initial x and y
        self.x=x
        self.y=y-10
        self.direction=direction
        self.angle=math.radians(angle)
        self.color='black'
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
        return hash(self.x,self.y,self.direction)
    #checks the distnce between two points
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**.5
    #checks if the item contains the point
    def containsPoint(self,x,y):
        return self.distance(self.dx,self.dy,x,y)<11
    #the physics behind the movement of the bullet
    def fireBullet(self,direction):
        #gets the velocity of X and Y of the the bullet
        vx=self.velocity*math.cos(self.angle)
        vy=self.velocity*math.sin(self.angle)
        self.time+=.1
        #depending on the direction of the tank it changes
        #the x direction of the bullet
        if self.direction=="Right":
            self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
            self.dx=self.x+vx*self.time
        if self.direction=="Left":
            self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
            self.dx=self.x-vx*self.time

    def bulletReachesGround(self):
        bulletsToKeep=[]
        for bullet in self.mode.bullets:
            if bullet.dy>self.mode.app.height//2+20:
                pass
            else:
                bulletsToKeep+=[bullet]
        self.mode.bullets=bulletsToKeep

    def checkCoinCollisions(self):
        coinsToKeep=[]
        for i in range(len(self.mode.coins)):
            if (self.mode.coins[i].containsPoint(self.dx,
            self.dy) and isinstance(self.mode.coins[i],Coin)):
                self.mode.points+=1
            else:
                coinsToKeep+=[self.mode.coins[i]]
        self.mode.coins=coinsToKeep


    def timerFired(self):
        self.fireBullet(self.direction)
        self.bulletReachesGround()
        self.checkCoinCollisions()
        # if self.direction=="Right":
        #     self.x+=self.change[0]
        #     self.y-=self.change[1]
        # else:
        #     self.x-=self.change[0]
        #     self.y-=self.change[1]
    #draws bullet
    def draw(self,canvas):
        canvas.create_oval(self.dx+5,self.dy+5,self.dx-5,self.dy-5,
        fill=self.color)
class Bomb(Bullet):
    def __init__(self,mode,x,y,direction,angle):
        self.mode=mode
        #initial x and y
        self.x=x
        self.y=y-10
        self.direction=direction
        self.angle=math.radians(angle)
        self.color='red'
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
        return isinstance(other,Bomb)

class Missile(Bullet):
    def __init__(self,mode,x,y,direction,angle):
        self.mode=mode
        #initial x and y
        self.x=x
        self.y=y-10
        self.direction=direction
        self.angle=math.radians(angle)
        self.color='white'
        self.gravity=0
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
        return isinstance(other,Missile)
    

    def draw(self,canvas):
        canvas.create_rectangle(self.dx+10,self.dy+5,self.dx-10,self.dy-5, 
        fill=self.color)


class GameMode(Mode):
    def appStarted(mode):
        mode.cursor=[-1,-1]
        mode.bullets=[]
        mode.hearts=[]
        mode.tank1=Player(mode,mode.app.width//2-mode.app.width//4,
        mode.app.height//2,"Right")
        #creates enemy tank
        mode.tank2=Enemy(mode,mode.app.width//2+mode.app.width//4,
        mode.app.height//2,"Left")
        mode.BulletTypeIndex=0
        mode.BulletTypes=["Bullet","Bomb","Missile"]
        mode.points=0
        mode.coins=[]
        mode.totalTime=0
        mode.tankEnemyKills=0
        for i in range(1):
            randomX=random.randint(10,mode.app.width-10)
            randomY=random.randint(10,mode.app.height//2-10)
            mode.coins.append(Coin(mode,randomX,randomY))

        
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
        mode.changeBulletType(event)
    def mouseReleased(mode,event):
        pass
    def mouseDragged(mode,event):
        mode.cursor=[event.x,event.y]
        print(event.x,event.y)
        pass
        # if not mode.draggingHeart is None:
        #     mode.draggingHeart.x=event.x+mode.scrollX
        #     mode.draggingHeart.y=event.y

    def changeBulletType(mode,event):
    
        (leftX1,endPointY,leftX2,y3,rightX1,y2,rightX2,endPointY)=mode.getSelectionTrianglePoints()
        if (event.x<leftX2 and event.x>leftX1 and
            event.y<y3 and event.y>y2):
            mode.BulletTypeIndex=(mode.BulletTypeIndex-1)%len(mode.BulletTypes)
        if (event.x<rightX2 and event.x>rightX1 and
            event.y<y3 and event.y>y2):
            mode.BulletTypeIndex=(mode.BulletTypeIndex+1)%len(mode.BulletTypes)



    def timerFired(mode):
        mode.totalTime+=1
        mode.tank1.timerFired()
        mode.tank2.timerFired()
        if mode.tank2.alive==False and (mode.totalTime-mode.tank2.timeDied)==20:
            if mode.tankEnemyKills%3==0:
                mode.tank2=ZombieEnemy(mode,mode.app.width//2+mode.app.width//3,
        mode.app.height//2,"Left")
            else:
                mode.tank2=Enemy(mode,mode.app.width//2+mode.app.width//4,
            mode.app.height//2,"Left")

        for bullet in mode.bullets:
            bullet.timerFired()
        if(mode.isGameOver==False):
            pass
        #changes isGameOver if player died
        if(mode.died==True):
            mode.isGameOver=True

    def getSelectionTrianglePoints(mode):
        distanceFromTriangelPoint=32
        distanceFromTriangles=125
        leftX1=mode.app.width*.01
        endPointY=mode.app.height//25
        leftX2=leftX1+(distanceFromTriangelPoint//2)*(3)**(1/2)
        y2=endPointY-distanceFromTriangelPoint//2
        y3=endPointY+distanceFromTriangelPoint//2
        rightX1=leftX2+distanceFromTriangles
        rightX2=leftX2+distanceFromTriangles+(distanceFromTriangelPoint//2)*(3)**(1/2)
        return (leftX1,endPointY,leftX2,y3,rightX1,y2,rightX2,endPointY)



    def drawBulletSelection(mode,canvas):
        (leftX1,endPointY,leftX2,y3,rightX1,y2,rightX2,endPointY)=mode.getSelectionTrianglePoints()
        canvas.create_rectangle(leftX2,y2,
        rightX1-1,y3,fill='grey')
        
        canvas.create_polygon(rightX1,y2,
        rightX1,y3,
        rightX2,endPointY,
        fill='yellow',)
        
        canvas.create_polygon(leftX1,endPointY,leftX2,y2,leftX2,y3,fill='yellow')
        canvas.create_text(rightX2//2,endPointY,text=mode.BulletTypes[mode.BulletTypeIndex])
    
    def drawPoints(mode,canvas):
        canvas.create_text(mode.app.width//2-mode.app.width//10,20,text=mode.points)
        canvas.create_text(mode.app.width//2+mode.app.width//10,20,text=f'time:{mode.totalTime/100}')

    def redrawAll(mode,canvas):
        mode.drawPoints(canvas)
        mode.tank1.draw(canvas)
        mode.tank2.draw(canvas)
        for bullet in mode.bullets:
            bullet.draw(canvas)
        for coin in mode.coins:
            coin.draw(canvas)
        mode.drawBulletSelection(canvas)
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
    MyModalApp(width=700,height=700)
runTanks()