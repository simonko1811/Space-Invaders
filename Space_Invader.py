# space_invaders-like game
# screen set up
import turtle
import os
import math
import random

# set up sreen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Almost Space Invaders")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

# register shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")

# draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup() # so that moving object doesnt draw in window
border_pen.setposition(-300, -300) # go to position to start making white border
border_pen.pendown() # so that it draws in window
border_pen.pensize(3)

for side in range(4): # setting white square inside
    border_pen.fd(600) #  go 600 in line
    border_pen.lt(90) # turn 90%

border_pen.hideturtle()

# set score
score = 0

# draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 273)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))
score_pen.hideturtle()

# create player
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250) #  it will face to the right (0 degree, for up is 90, left is 180, down is 270)
player.setheading(90) # tilt 90 degrees, so it points up

player.speed = 0 # dont move on start

# create number of enemies via list and create list
number_of_enemies = 20
enemies = []
# add enemies to list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x = -230
enemy_start_y = 250
enemy_number = 0

# create an Enemy
for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y

    enemy.setposition(x, y)

    # update enemy_number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.2 # speed of animation

# players bullet to shoot
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.3, 0.3)
bullet.hideturtle()

bulletspeed = 2

# define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# move player left and right
def move_left():
    player.speed = -1.5

def move_right():
    player.speed = 1.5

def move_player():
    x = player.xcor()
    x += player.speed # move to the left by amount of playerspeed
    if x < -280: # boundary check
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # declare bulletstate as global if it needs changed
    global bulletstate

    if bulletstate == "ready":
        # move bullet to the just above the player
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y + 10)
        bullet.showturtle()
        bulletstate = "fire"

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create key-bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# mainloop
while True:

    wn.update()

    move_player()

    for enemy in enemies:
        # move enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # move enemy back and down
        if enemy.xcor() > 280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1 # move in opposite direction with speed of value of enemyspeed * -1

        if enemy.xcor() < -280:
            for e in enemies: # move all down
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        # check for bullet collision
        if isCollision(bullet, enemy):
            # reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,- 400)

            # reset enemy
            #x = random.randrange(-200, 200, 40)
            #y = 250
            enemy.setposition(0, 1000) # move enemy out of screen

            # update score
            score += 1
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))

        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("You Lost")
            break

        if (enemy.ycor() < -250):
            player.hideturtle()
            enemy.hideturtle()
            print("You Lost")
            break

    # move bullet
    if bulletstate == "fire":
        y =bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check if bullet reach top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"