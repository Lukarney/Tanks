
# CITATION: I got the cmu_112_graphics from 
# 15-112 website https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#Missile and tank sprites came from DYLESTORM
#on gamedevmarket https://www.gamedevmarket.net/member/dylestorm/
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
        self.armLength=15
        self.aimingArmLength=50
        self.armX2Aiming=self.x+self.aimingArmLength
        self.armY2Aiming=self.y-18
        self.newAimingArmXDistance=0
        self.newAimingArmYDistance=0
        self.armY2Aiming=0
        self.armX2Aiming=0
        self.armWidth=10
        tacoURL='https://i.imgur.com/sQSdSo8.png'
        tacoImage=self.mode.loadImage(tacoURL)
        self.tacoImage=self.mode.scaleImage(tacoImage,1/10)
        self.tacoImage=self.tacoImage.rotate(math.degrees(self.angle))
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
        tankUrl='https://i.imgur.com/zEwkCY6.png'
        self.tankImage=self.mode.loadImage(tankUrl)
        self.tankImage=self.mode.scaleImage(self.tankImage,1.5)
    

    def move(self,cordinate):
        if cordinate=="Right":
            self.x=self.x+self.dx
            if self.direction=="Left":
                self.tankImage=self.tankImage.transpose(Image.FLIP_LEFT_RIGHT)
            self.direction=cordinate
            self.tacoImage=self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        if cordinate=="Left":
            self.x=self.x-self.dx
            if self.direction=="Right":
                self.tankImage=self.tankImage.transpose(Image.FLIP_LEFT_RIGHT)
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
                        if self.mode.ammo["Bullet"]>0:
                            self.mode.ammo["Bullet"]=self.mode.ammo.get("Bullet")-1
                            self.mode.bullets.append(Bullet(self.mode,self.x,self.y,
                            self.direction,self.angle))
                    if self.mode.BulletTypes[self.mode.BulletTypeIndex]=="Bomb":
                        if self.mode.ammo["Bomb"]>0:
                            self.mode.ammo["Bomb"]=self.mode.ammo.get("Bomb")-1
                            self.mode.bullets.append(Bomb(self.mode,self.x,self.y,
                            self.direction,self.angle))
                    if self.mode.BulletTypes[self.mode.BulletTypeIndex]=="Missile":
                        if self.mode.ammo["Missile"]>0:
                            self.mode.ammo["Missile"]=self.mode.ammo.get("Missile")-1
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
        self.newAimingArmXDistance=self.aimingArmLength*math.cos(math.radians(self.angle))
        self.newAImingArmYDistance=self.aimingArmLength*math.sin(math.radians(self.angle))
        
        bottomAngle=0
        self.armX1=self.x
        self.armY1=self.y-10
        #sets up the barrel(arm) of the tank to move around
        if self.direction=="Right":
            self.armX2=self.armX1+self.newArmXDistance
            self.armX2Aiming=self.armX1+self.newAimingArmXDistance
            self.armImageX=self.x+self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            self.armX2=self.armX1-self.newArmXDistance
            self.armX2Aiming=self.armX1-self.newAimingArmXDistance
            self.armImageX=self.x-self.newArmXDistance/2
            self.tacoImage.transpose(Image.FLIP_LEFT_RIGHT)
        #sets up the y position of the arm to move around
        self.armY2=self.armY1-self.newArmYDistance
        self.armY2Aiming=self.armY1-self.newAImingArmYDistance
        self.armX3=self.armX1-6
        self.armY3=self.armY1-12
        self.armX4=self.armX2-6
        self.armY4=self.armY2-12
        self.armImageY=self.y-10-self.newArmYDistance/2

    def drawShootingLine(self,canvas):
        canvas.create_line(self.armX1,self.armY1,
        self.armX2Aiming,self.armY2Aiming,fill='red')
        
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
                if(self.x>self.mode.app.width):
                    self.x-=self.dx
                if self.x<0:
                    self.x+=self.dx
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
                if self.mode.aimingOn==True:
                    self.drawShootingLine(canvas)
                # canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
                # fill='green')
                # canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
                # self.armX4,self.armY4,self.armX3,self.armY3,fill='green')
                canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.tankImage))
            #draw lives in the top right
            for i in range(self.lives):
                canvas.create_image(self.mode.app.width-(1+i)*50, 40,
            image=ImageTk.PhotoImage(self.heart))
            # canvas.create_image(self.armImageX,
            # self.armImageY,image=ImageTk.PhotoImage(self.tacoImage))

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
        self.aimingArmLength=50
        self.armX2Aiming=self.x+self.aimingArmLength
        self.armY2Aiming=self.y-18
        self.newAimingArmXDistance=0
        self.newAimingArmYDistance=0
        self.armY2Aiming=0
        self.armX2Aiming=0
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
        enemyUrl='https://i.imgur.com/CHxzZj7.png'
        self.enemyImage=self.mode.loadImage(enemyUrl)
        self.enemyImage=self.mode.scaleImage(self.enemyImage,1.5)
        zombieUrl='https://i.imgur.com/WZzxkEo.png'
        self.zombieImage=self.mode.loadImage(zombieUrl)
        self.zombieImage=self.mode.scaleImage(self.zombieImage,1.5)
        if self.direction=="Left":
            self.enemyImage=self.enemyImage.transpose(Image.FLIP_LEFT_RIGHT)
            self.zombieImage=self.zombieImage.transpose(Image.FLIP_LEFT_RIGHT)

        #for angle in range(0,180)
        #self.tacoDict
        def __eq__(self,other):
            return isinstance(other,Enemy)

    def timerFired(self):
        if self.bulletTimer>3:
                self.bulletTimer=0
                if self.alive==True:
                    otherTankX=self.mode.tank1.x
                    otherTankY=self.mode.app.height//2
                    self.mode.bullets.append(EnemyBullet(self.mode,self.x,self.y,
                    self.direction,otherTankX,otherTankY))
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
            self.mode.points+=25
            self.timeDied=self.mode.totalTime
    
    def draw(self, canvas):
        if self.alive==True:
            if(self.mode.isGameOver==False):
                pass
                # canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
                # fill='red')
                # canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
                # self.armX4,self.armY4,self.armX3,self.armY3,fill='red')
            if (isinstance(self,ZombieFriend)):
                canvas.create_text(self.x,self.y-30,text=self.countDownTillDeath//10)
                canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.zombieImage))
            else:
                canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.enemyImage))



class ZombieEnemy(Enemy):
    def __eq__(self,other):
        return isinstance(other,ZombieEnemy)
    def draw(self, canvas):
        if self.alive==True:
            if(self.mode.isGameOver==False):
                # canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,
                # fill='purple')
                # canvas.create_polygon(self.armX1,self.armY1,self.armX2,self.armY2,
                # self.armX4,self.armY4,self.armX3,self.armY3,fill='purple')
                canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.zombieImage))

    def checkIfAlive(self):
        if self.lives==0:
            self.mode.tankEnemyKills+=1
            self.lives-=1
            self.alive=False
            self.mode.points+=15
            self.timeDied=self.mode.totalTime
            self.mode.tank3Exist=True
            self.mode.tank3=ZombieFriend(self.mode,
            self.mode.app.width//2-self.mode.app.width//4,self.mode.app.height//1.3,"Right")

class ZombieFriend(Enemy):
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
        self.aimingArmLength=50
        self.armX2Aiming=self.x+self.aimingArmLength
        self.armY2Aiming=self.y-18
        self.newAimingArmXDistance=0
        self.newAimingArmYDistance=0
        self.armY2Aiming=0
        self.armX2Aiming=0
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
        self.mode.tank3Exist=True
        self.color="light purple"
        self.countDownTillDeath=300
        enemyUrl='https://i.imgur.com/CHxzZj7.png'
        self.enemyImage=self.mode.loadImage(enemyUrl)
        self.enemyImage=self.mode.scaleImage(self.enemyImage,1.5)
        zombieUrl='https://i.imgur.com/WZzxkEo.png'
        self.zombieImage=self.mode.loadImage(zombieUrl)
        self.zombieImage=self.mode.scaleImage(self.zombieImage,1.5)

    def __eq__(self,other):
        return isinstance(other,ZombieFriend)
    

    def checkIfAlive(self):
        if self.lives==0:
            self.mode.tankEnemyKills+=1
            self.lives-=1
            self.alive=False
            self.mode.points+=15
            self.mode.tank3Exist=False
            self.timeDied=self.mode.totalTime       

    def timerFired(self):
        if self.bulletTimer>3:
                self.bulletTimer=0
                if self.alive==True:
                    otherTankX=self.mode.tank2.x+10
                    otherTankY=self.mode.app.height//2
                    self.mode.bullets.append(EnemyBullet(self.mode,self.x,self.y,
                    self.direction,otherTankX,otherTankY))
        self.bulletTimer+=.1
        self.time+=1
        self.countDownTillDeath-=1
        if self.time==300:
            self.lives=0
        self.checkIfAlive()
        if self.alive==True:
            self.checkBulletCollisions()
            self.moveTankArm() 

class Player(Tank):

    def __eq__(self,other):
        return isinstance(other,Player)


    def timerFired(self):
        self.bulletTimer+=.1
        self.time+=1
        if len(self.mode.coins)<10 and self.time%100==0:
            for i in range(1):
                randomX=random.randint(10,self.mode.app.width-10)
                randomY=random.randint(self.mode.app.height//2,self.mode.app.height//2+self.mode.app.height//4,)
                self.mode.coins.append(Coin(self.mode,randomX,randomY))
        self.checkIfAlive()
        if self.alive==True:
            self.checkCoinCollisions()
            self.checkBulletCollisions()
            self.moveTankArm()
    
    def checkIfAlive(self):
        if self.lives==0:
            self.alive=False
            self.mode.died=True
            self.mode.endTime=self.mode.totalTime/10

    def checkCoinCollisions(self):
        coinsToKeep=[]
        for i in range(len(self.mode.coins)):
            if (self.mode.coins[i].containsPoint(self.x,
            self.y-5) and isinstance(self.mode.coins[i],Coin)):
                self.mode.points+=50
            else:
                coinsToKeep+=[self.mode.coins[i]]
        self.mode.coins=coinsToKeep

    


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
        return self.distance(self.x,self.y,x,y)<=15
    
            



    def draw(self,canvas):
        canvas.create_oval(self.x-5,self.y-5,self.x+5,self.y+5,fill='yellow')
class Bullet(object):
    def __init__(self,mode,x,y,direction,angle):
        self.mode=mode
        #initial x and y
        self.x=x
        self.y=y-20
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
        return self.distance(self.dx,self.dy,x,y)<=18
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
            if bullet.dy>self.mode.app.height//1.3+15:
                pass
            else:
                bulletsToKeep+=[bullet]
        self.mode.bullets=bulletsToKeep

    def checkCoinCollisions(self):
        coinsToKeep=[]
        for i in range(len(self.mode.coins)):
            if (self.mode.coins[i].containsPoint(self.dx,
            self.dy) and isinstance(self.mode.coins[i],Coin)):
                self.mode.points+=25
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

class EnemyBullet(Bullet):
    def __init__(self,mode,x,y,direction,endX,endY):
        self.mode=mode
        self.direction=direction
        self.x=x
        self.velocity=60
        self.y=y-20
        self.endX=endX
        self.endY=endY
        self.gravity=9.81
        self.dx=0
        self.dy=0
        self.time=0
        self.color='black'
        

    def __eq__(self,other):
        return isinstance(other,EnemyBullet)
    
    def __hash__(self):
        return hash(self.x,self.y,self.direction)

    def fireBullet(self,direction):
        print(("distance",self.endX-self.x))
        X=(self.endX-self.x)
        h=abs(self.endY-self.y)
        if (self.endX-self.x)>0:
            # X=(self.x-self.endX)
            # h=self.y-self.endY
            X=-X
            self.velocity=60
        else:
            # X=(self.endX-self.x)
            # h=(self.endY-self.y)
            self.velocity=60
        # if X<0:
        #     print("X",X)
        #print(X,h)
        phi=math.atan(X/h)
        #print(phi)
        a=((-self.gravity*(X**2))/self.velocity**2)
        #print(a)
        radians=(a+h)/(h**2+X**2)**(1/2)
        #print(radians)
        try:
            if (self.endX-self.x)>0:
                theta=-((math.acos(radians)+phi)/2)
                vx=-self.velocity*math.cos(theta)
            else:
                
                theta=((math.acos(radians)+phi)/2)
                vx=self.velocity*math.cos(theta)
            #theta=(math.acos(radians)+phi)/2
            #theta=.5*math.asin(-self.gravity*X/self.velocity**2)
            # if direction=="Right":
                
            #     theta=math.degrees((math.acos(radians)+phi)/2)
            #     vx=self.velocity*math.cos(theta)
            # else:
            #     theta=math.degrees((math.acos(radians)+phi)/2)
            #     vx=self.velocity*math.cos(theta)
            theta=((math.acos(radians)+phi)/2)
            #vx=self.velocity*math.cos(theta)
            vy=self.velocity*math.sin(theta)
        except:
            if (self.endX-self.x)>0:
                theta=math.radians(30)
                vx=-self.velocity*math.cos(theta)
            else:
                theta=math.radians(30)
                vx=self.velocity*math.cos(theta)
            vy=self.velocity*math.sin(theta)

            # if direction=="Right":
            #     theta=math.radians(30)
            #     vx=self.velocity*math.cos(theta)
            # else:
            #     theta=math.radians(30)
            #     vx=self.velocity*math.cos(theta)
            # vy=self.velocity*math.sin(theta)
        
        
        
        
        #theta=.5*math.asin(-self.gravity*X/self.velocity**2)
        #print("theta: ",theta)
        # vx=self.velocity*math.cos(theta)
        # vy=self.velocity*math.sin(theta)
        self.time+=.1
        #depending on the direction of the tank it changes
        #the x direction of the bullet
        # if self.direction=="Right":
        #     self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
        #     self.dx=self.x+vx*self.time
        # if self.direction=="Left":
        #     self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
        #     self.dx=self.x-vx*self.time
        self.dy=self.y-vy*self.time +(self.gravity/2)*self.time*self.time
        self.dx=self.x-vx*self.time

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
        self.missileImage=self.mode.loadImage('https://i.imgur.com/JVON6yE.png')
        self.missileImage=self.missileImage.rotate(math.degrees(self.angle))
        if self.direction=="Right":
            self.x+=self.initialDistanceXAdded
            self.y-=self.initialDistanceYAdded
        else:
            self.x-=self.initialDistanceXAdded
            self.y-=self.initialDistanceYAdded
            self.missileImage=self.missileImage.transpose(Image.FLIP_LEFT_RIGHT)

    def __eq__(self,other):
        return isinstance(other,Missile)
    

    def draw(self,canvas):
        canvas.create_image(self.dx,self.dy,image=ImageTk.PhotoImage(self.missileImage))


class GameMode(Mode):
    def appStarted(mode):
        mode.cursor=[-1,-1]
        mode.bullets=[]
        mode.hearts=[]
        mode.tank1=Player(mode,mode.app.width//2-mode.app.width//4,
        mode.app.height//1.3,"Right")
        #creates enemy tank
        mode.tank2=Enemy(mode,mode.app.width//2+mode.app.width//4,
        mode.app.height//1.3,"Left")
        mode.BulletTypeIndex=0
        mode.BulletTypes=["Bullet","Bomb","Missile"]
        mode.points=0
        mode.coins=[]
        mode.totalTime=0
        mode.endTime=0
        mode.tankEnemyKills=0
        mode.tank3Exist=False
        mode.name=""
        #the amount of ammo to start off with 
        mode.ammo=dict()
        mode.ammo["Bullet"]=100
        mode.ammo["Bomb"]=10
        mode.ammo["Missile"]=5
        mode.aimingOn=False
        
        for i in range(1):
            randomX=random.randint(10,mode.app.width-10)
            randomY=random.randint(mode.app.height//2+mode.app.height//4,mode.app.height//1.3)
            mode.coins.append(Coin(mode,randomX,randomY))

        
        #sets up functions for the end game
        mode.died=False
        mode.isGameOver=False
    #checks to see if a key is pressed
    def keyPressed(mode,event):
        mode.tank1.move(event.key)
        if (event.key=='h'):
            mode.app.setActiveMode(mode.app.helpMode)
        if event.key=='s':
            mode.app.setActiveMode(mode.app.shopMode)
        
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
        mode.changeAimingOn(event)
        mode.goToShop(event)
    def mouseReleased(mode,event):
        pass
    def mouseDragged(mode,event):
        mode.cursor=[event.x,event.y]
        print(event.x,event.y)
        pass
        # if not mode.draggingHeart is None:
        #     mode.draggingHeart.x=event.x+mode.scrollX
        #     mode.draggingHeart.y=event.y

    def goToShop(mode,event):
        leftX=mode.app.width//100+35
        rightX=mode.app.width//100+35+70
        bottomY=mode.app.height-mode.app.height//100
        topY=mode.app.height-mode.app.height//100-30
        if event.x>leftX and event.x<rightX:
            if event.y<bottomY and event.y>topY:
                mode.app.setActiveMode(mode.app.shopMode)
                
    def changeAimingOn(mode,event):
        leftX=mode.app.width//100
        rightX=mode.app.width//100+30
        bottomY=mode.app.height-mode.app.height//100
        topY=mode.app.height-mode.app.height//100-30
        if event.x>leftX and event.x<rightX:
            if event.y<bottomY and event.y>topY:
                if mode.aimingOn==False:
                    mode.aimingOn=True
                else:
                    mode.aimingOn=False

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
        mode.totalTime
        if mode.totalTime==1800:
            mode.isGameOver=True
        if(mode.isGameOver==False):
            mode.tank1.timerFired()
            mode.tank2.timerFired()
            if mode.tank3Exist:
                mode.tank3.timerFired()
            if mode.tank2.alive==False and (mode.totalTime-mode.tank2.timeDied)==20:
                randomX=random.randint(10,mode.app.width-10)
                #randomY=random.randint(mode.app.height//2-mode.app.height//4,mode.app.height//2)
                if mode.tankEnemyKills%3==0:
                    mode.tank2=ZombieEnemy(mode,mode.app.width//2+mode.app.width//3,
            mode.app.height//1.3,"Left")
                else:
                    if mode.tank1.x-randomX<0:
                        mode.tank2=Enemy(mode,randomX,
                    mode.app.height//1.3,"Left")
                    else:
                        mode.tank2=Enemy(mode,randomX,
                    mode.app.height//1.3,"Right")

            for bullet in mode.bullets:
                bullet.timerFired()
        
        #changes isGameOver if player died
        if(mode.died==True):
            mode.isGameOver=True
            mode.endTime=mode.totalTime
        elif mode.isGameOver==True and mode.tank1.alive==True:
            mode.endTime=mode.totalTime
            mode.tank1.alive=False
            mode.app.setActiveMode(mode.app.endScreenMode)
        if mode.isGameOver==True:
            mode.points+=mode.endTime//10
            mode.app.setActiveMode(mode.app.endScreenMode)





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
        canvas.create_text(rightX2//2,endPointY,
        text=f'{mode.BulletTypes[mode.BulletTypeIndex]}x{mode.ammo[mode.BulletTypes[mode.BulletTypeIndex]]}')
    
    def drawPointsAndTime(mode,canvas):
        canvas.create_text(mode.app.width//2-mode.app.width//10,20,text=mode.points)
        canvas.create_text(mode.app.width//2+mode.app.width//10,20,text=f'time:{mode.totalTime/10}')
    
    def drawAimingBox(mode,canvas):
        if mode.aimingOn==False:
            canvas.create_rectangle(mode.app.width//100,mode.app.height-mode.app.height//100,
            mode.app.width//100+30,mode.app.height-mode.app.height//100-30,)
        else:
            canvas.create_rectangle(mode.app.width//100,mode.app.height-mode.app.height//100,
            mode.app.width//100+30,mode.app.height-mode.app.height//100-30,
            fill='red')
        middlex=(mode.app.width//100+mode.app.width//100+30)//2
        middley=(mode.app.height-mode.app.height//100+
        mode.app.height-mode.app.height//100-30)//2
        canvas.create_text(middlex,middley,text="A",font="Arial 20")

    def drawShopingBox(mode,canvas):
        canvas.create_rectangle(mode.app.width//100+35,mode.app.height-mode.app.height//100,
            mode.app.width//100+35+70,mode.app.height-mode.app.height//100-30,
            fill='purple')
        middlex=(mode.app.width//100+35+mode.app.width//100+35+70)//2
        middley=(mode.app.height-mode.app.height//100+
        mode.app.height-mode.app.height//100-30)//2
        canvas.create_text(middlex,middley,text="Arsenal",font="Arial 15")


    def redrawAll(mode,canvas):
        if mode.isGameOver==False:
            canvas.create_rectangle(0,0,mode.app.width,mode.app.width,fill='light blue')
            canvas.create_rectangle(0,mode.app.height//1.3+10,mode.app.width,mode.app.height,fill='dark green')
            mode.drawPointsAndTime(canvas)
            mode.tank1.draw(canvas)
            mode.tank2.draw(canvas)
            if mode.tank3Exist:
                mode.tank3.draw(canvas)
            for bullet in mode.bullets:
                bullet.draw(canvas)
            for coin in mode.coins:
                coin.draw(canvas)
            mode.drawBulletSelection(canvas)
            mode.drawAimingBox(canvas)
            mode.drawShopingBox(canvas)


            
class EndScreenMode(Mode):
    def appStarted(mode):
        mode.died=mode.app.gameMode.died
        mode.endTime=mode.app.gameMode.endTime
        mode.points=mode.app.gameMode.points
        ES1Url='https://i.imgur.com/xmirSO4.png'
        mode.EndScreen=mode.loadImage(ES1Url)
        mode.EndScreen=mode.scaleImage(mode.EndScreen,1/2.5)

    def keyPressed(mode, event):
        if event.key=='r':
            MyModalApp(width=800,height=500)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.app.width,mode.app.width,fill='light blue')
        canvas.create_rectangle(0,mode.app.height//1.3+10,mode.app.width,mode.app.height,fill='dark green')
        if(mode.died==True):
            font = 'Arial 26 bold'
            canvas.create_text(mode.width/1.3, 150, 
            text="You did not make it :(\n press r to restart", font=font)
            canvas.create_text(mode.app.width//2,mode.app.height//2,
            text=f'{mode.points} points in \n {mode.endTime/10} seconds',font=font)
            #self.name=input("Enter your name: ")
                
        else:
            font = 'Arial 26 bold'
            text=('WINNER!\n'+
            'press r to restart')
            canvas.create_text(mode.width/2, 150,text=text, font=font)
            canvas.create_text(mode.app.width//2,mode.app.height//2,
            text=f'{mode.points} points in \n {mode.endTime/10} time',font=font)

class ShopMode(Mode):
    def appStarted(mode):
        mode.cursor=[-1,-1]
        heartURL=('https://cdn.pixabay.com/photo/2017/09/23/16/33/'+
        'pixel-heart-2779422_1280.png')
        heart=mode.loadImage(heartURL)
        mode.heart=mode.scaleImage(heart,1/20)
        missile=mode.loadImage('https://i.imgur.com/JVON6yE.png')
        mode.missileImage=mode.scaleImage(missile,4)

    def mouseMoved(mode,event):
        # mode.app._root.configure(cursor='none')
        mode.cursor=[event.x,event.y]

    def goBackToGame(mode,event):
        middlex=(mode.app.width//10//2+(mode.app.width//10//2)*5)//2
        middley=(mode.app.height//10//2+(mode.app.height//10//2)*3)//2
        leftX=mode.app.width//10//2
        rightX=(mode.app.width//10//2)*5
        bottomY=(mode.app.height//10//2)*3
        topY=mode.app.height//10//2
        if event.x>leftX and event.x<rightX:
            if event.y<bottomY and event.y>topY:
                mode.app.setActiveMode(mode.app.gameMode)
    def mousePressed(mode,event):
        oneHundredHeight=mode.app.height//(mode.app.height//100)
        thirtyX=mode.app.width//(mode.app.width//10*(1/3))
        mode.goBackToGame(event)
        #buying on the left side
        if event.x>thirtyX and event.x<mode.app.width//2-thirtyX//2:
            #to buy for bomb
            if event.y>oneHundredHeight and event.y<mode.app.height//2+25:
                if mode.app.gameMode.points-5>0:
                    mode.app.gameMode.ammo["Bomb"]=mode.app.gameMode.ammo.get("Bomb")+10
                    mode.app.gameMode.points-=5
            #to buy a life
            if event.y>mode.app.height//2+50 and event.y<mode.app.height-20:
                if mode.app.gameMode.points-25>0:
                    mode.app.gameMode.tank1.lives+=1
                    mode.app.gameMode.points-=25
        #buying on the right side
        if event.x>mode.app.width//2+thirtyX//2 and event.x<mode.app.width-thirtyX:
            #to buy for missile
            if event.y>oneHundredHeight and event.y<mode.app.height-20:
                #if you have the points you can buy a missile
                if mode.app.gameMode.points-50>0:
                    mode.app.gameMode.ammo["Missile"]=mode.app.gameMode.ammo.get("Missile")+10
                    mode.app.gameMode.points-=50
                #mode.app.gameMode.ammo["Missile"]=mode.app.gameMode.ammo.get("Missile")+10
    


    def redrawAll(mode, canvas):
        #gets cursor values
        cursorX,cursorY=mode.cursor
        #overall background
        canvas.create_rectangle(0,0,mode.app.width,mode.app.width,fill='light blue')
        canvas.create_text(mode.app.width//2,mode.app.height//10,text="Arsenal",font="Arial 26")
        #dimensions of the the arsenal based on size of canvas
        oneHundredHeight=mode.app.height//(mode.app.height//100)
        thirtyX=mode.app.width//(mode.app.width//10*(1/3))
        #text for arsenal
        #bomb box
        canvas.create_rectangle(thirtyX,oneHundredHeight,mode.app.width//2-thirtyX//2,mode.app.height//2+25,fill="white")
        canvas.create_text((thirtyX+mode.app.width//2-thirtyX//2)//2,
        oneHundredHeight+oneHundredHeight//10,text="Bomb x10", font="Arial 15")
        canvas.create_text((thirtyX+mode.app.width//2-thirtyX//2)//2,
        mode.app.height//2+25-oneHundredHeight//10,text="5 points", font="Arial 15")
        bombBoxCenterX=(thirtyX+mode.app.width//2-thirtyX//2)//2
        bombBoxCenterY=(oneHundredHeight-thirtyX//2+mode.app.height//2+25)//2
        canvas.create_oval(bombBoxCenterX-20,bombBoxCenterY-20,
        bombBoxCenterX+20,bombBoxCenterY+20,fill='red')
        #extra life box
        canvas.create_rectangle(thirtyX,mode.app.height//2+50,
        mode.app.width//2-thirtyX//2,mode.app.height-20,fill="white")
        canvas.create_text((thirtyX+mode.app.width//2-thirtyX//2)//2,
        mode.app.height//2+50+oneHundredHeight//10,text="Life",font="Arial 15")
        canvas.create_text((thirtyX+mode.app.width//2-thirtyX//2)//2,
        mode.app.height-20-oneHundredHeight//10,text="25 points",font="Arial 15")
        canvas.create_image((thirtyX+mode.app.width//2-thirtyX//2)//2,
        (mode.app.height//2+50+mode.app.height-20)//2,image=ImageTk.PhotoImage(mode.heart))
        #missle box
        canvas.create_rectangle(mode.app.width//2+thirtyX//2,
        oneHundredHeight,mode.app.width-thirtyX,mode.app.height-20,fill="white")
        canvas.create_text((mode.app.width//2+thirtyX//2+mode.app.width-thirtyX)//2,
        oneHundredHeight+oneHundredHeight//10,text="Missile x10",font="Arial 15")
        canvas.create_text((mode.app.width//2+thirtyX//2+mode.app.width-thirtyX)//2,
        mode.app.height-20-oneHundredHeight//10,text="50 points",font="Arial 15")
        canvas.create_image((mode.app.width//2+thirtyX//2+mode.app.width-thirtyX)//2,
        (oneHundredHeight+mode.app.height-20)//2,
        image=ImageTk.PhotoImage(mode.missileImage))
        #draw goback box
        canvas.create_rectangle(mode.app.width//10//2,mode.app.height//10//2,
        (mode.app.width//10//2)*5,(mode.app.height//10//2)*3,fill="navy")
        middlex=(mode.app.width//10//2+(mode.app.width//10//2)*5)//2
        middley=(mode.app.height//10//2+(mode.app.height//10//2)*3)//2
        canvas.create_text(middlex,middley,text="Back",font="Arial 20",fill='white')
    def keyPressed(mode, event):
        if event.key=='s':
            mode.app.setActiveMode(mode.app.gameMode)


class SplashScreenMode(Mode):
    def appStarted(mode):
        SS1Url='https://i.imgur.com/yLLO8FF.png'
        mode.splashScreen=mode.loadImage(SS1Url)
        mode.splashScreen=mode.scaleImage(mode.splashScreen,1/2.5)
    def redrawAll(mode, canvas):
        canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.splashScreen))
        canvas.create_text(mode.app.width//2,mode.app.height//1.1,
        text="Press h to go to the help screen and space to begin",
        font="Arial 15")
        x1=mode.app.width//2-40
        x2=mode.app.width//2+40
        y1=mode.app.height//2-20
    def keyPressed(mode, event):
        if event.key=="h":
            mode.app.setActiveMode(mode.app.helpMode)
        if event.key=="Space":
            mode.app.setActiveMode(mode.app.gameMode)
class HelpMode(Mode):
    def appStarted(mode):
        mode.points=0
        mode.totalTime=0
        mode.slides=0
        
        slide1Url='https://i.imgur.com/8KtW4Cg.png'
        mode.slide1=mode.loadImage(slide1Url)
        mode.slide1=mode.scaleImage(mode.slide1,1/2.5)
        slide2Url='https://i.imgur.com/jLrW3ju.png'
        mode.slide2=mode.loadImage(slide2Url)
        mode.slide2=mode.scaleImage(mode.slide2,1/2.5)
        slide3Url='https://i.imgur.com/qqr9W3w.png'
        mode.slide3=mode.loadImage(slide3Url)
        mode.slide3=mode.scaleImage(mode.slide3,1/2.5)
        slide4Url='https://i.imgur.com/obFJLXk.png'
        mode.slide4=mode.loadImage(slide4Url)
        mode.slide4=mode.scaleImage(mode.slide4,1/2.5)
        slide5Url='https://i.imgur.com/r8923eh.png'
        mode.slide5=mode.loadImage(slide5Url)
        mode.slide5=mode.scaleImage(mode.slide5,1/2.5)
        slide6Url='https://i.imgur.com/ALMzI1P.png'
        mode.slide6=mode.loadImage(slide6Url)
        mode.slide6=mode.scaleImage(mode.slide6,1/2.5)
    

    def drawPointsAndTime(mode,canvas):
        canvas.create_text(mode.app.width//2-mode.app.width//10,20,text=mode.points)
        canvas.create_text(mode.app.width//2+mode.app.width//10,20,text=f'time:{mode.totalTime/10}')
    #draws background
    def redrawAll(mode, canvas):
        if mode.slides%7==0:
            canvas.create_rectangle(0,0,mode.app.width,mode.app.width,fill='light blue')
            canvas.create_rectangle(0,mode.app.height//1.3+10,mode.app.width,mode.app.height,fill='dark green')
            mode.drawPointsAndTime(canvas)
            canvas.create_text(mode.app.width//2,mode.app.height//2,
            text="Press the right and left arrow keys to \n switch the tutorial slides\n press h to start",
            font="Arial 26")
        if mode.slides%7==1:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide1))
        if mode.slides%7==2:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide2))
        if mode.slides%7==3:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide3))
        if mode.slides%7==4:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide4))
        if mode.slides%7==5:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide5))
        if mode.slides%7==6:
            canvas.create_image(mode.app.width//2,mode.app.height//2,image=ImageTk.PhotoImage(mode.slide6))
            


    #if any key is pressed the game starts
    def keyPressed(mode, event):
        if event.key=="Right":
            mode.slides+=1
        elif event.key=="Left":
            mode.slides-=1
        elif event.key=="h":
            mode.app.setActiveMode(mode.app.gameMode)
        else:
            mode.app.setActiveMode(mode.app.splashScreenMode)
#holds all the game functions
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.endScreenMode=EndScreenMode()
        app.shopMode=ShopMode()
        #app.setActiveMode(app.gameMode)
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50
 
def runTanks():
    MyModalApp(width=800,height=500)
runTanks()