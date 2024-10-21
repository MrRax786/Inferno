#libraries
from tkinter import *
import random
import threading

#Initial player coordinates
player_x = 0
player_y = 425

#Boolean for the shield cheat
shield = False

#Instantiating the player name variable before its use in the game
player_name = ' '

#Game resolution constants
GAME_WIDTH = 1600
GAME_HEIGHT = 900

#Image sources
PLAYER_SPRITE_B = "Images/playerB.png"
PLAYER_SPRITE_R = "Images/playerR.png"
PLAYER_SPRITE_G = "Images/playerG.png"
MAIN_SPRITE = ""
PLAYER_SPEED = 20
PLAYER_HEALTH = 100
ENEMY_SPRITE = "Images/enemy.png"
BULLET_SPRITE = "Images/bullet.png"
GAME_BACKGROUND_IMAGE = "Images/grassBackground.png"
MENU_BACKGROUND_IMAGE = "Images/menuBackground.png"
BOSSKEY_BACKGROUND_IMAGE = "Images/bosskey.png"
LOGO_IMAGE = "Images/gameLogo2.png"
POWERUP_IMAGE= "Images/powerup.png"
SHIELD_IMAGE= "Images/shield.png"

#PLAYER CLASS#

class Player:
    def __init__(self):
        #Declaring player attributes and creating the player and bullet sprites.
        global player_x
        global player_y

        player_x = 0
        player_y = 350

        self.pl = PhotoImage(file=MAIN_SPRITE)
        self.p_sprite = main_canvas.create_image(player_x, player_y, image=self.pl, anchor='nw', tag="player_sprite")
        main_canvas.itemconfig(tagOrId="player_sprite", state='hidden')



        self.bullet_img = PhotoImage(file=BULLET_SPRITE)
        self.bullet_img.image = self.bullet_img

    def move(self, event):
        #Allows for player movement
        global player_x
        global player_y

        if event.char == "a":
            main_canvas.move(self.p_sprite, -PLAYER_SPEED, 0)
            player_x -= PLAYER_SPEED
            self.edge_collision()
        elif event.char == "d":
            main_canvas.move(self.p_sprite, PLAYER_SPEED, 0)
            player_x += PLAYER_SPEED
            self.edge_collision()
        elif event.char == "w":
            main_canvas.move(self.p_sprite, 0, -PLAYER_SPEED)
            player_y -= PLAYER_SPEED
            self.edge_collision()
        elif event.char == "s":
            main_canvas.move(self.p_sprite, 0, PLAYER_SPEED)
            player_y += PLAYER_SPEED
            self.edge_collision()

    def moveBullet(self):
        #Function used to move the bullet on the canvas when shot.
        global bullet, bulletloop
        main_canvas.move(bullet,10,0)
        self.bullet_collision(bullet)
        bulletloop = window.after(10,self.moveBullet)



    def shoot(self,event):
        #The shoot function carries out the shooting mechanics when it is triggered.
        global bullet, bulletloop
        try:
            window.after_cancel(bulletloop)
            main_canvas.delete(bullet)
            playerB = main_canvas.bbox(self.p_sprite)
            clR = (playerB[0]+playerB[2])/2
            cTB = (playerB[1] + playerB[3]) / 2
            bullet = main_canvas.create_image(clR,cTB,image= self.bullet_img)
            threading.Thread(target=self.moveBullet).start()


        except NameError:
            playerB = main_canvas.bbox(self.p_sprite)
            clR = (playerB[0]+playerB[2])/2
            cTB = (playerB[1] + playerB[3]) / 2
            bullet = main_canvas.create_image(clR,cTB,image= self.bullet_img)
            threading.Thread(target=self.moveBullet).start()


    def bullet_collision(self,bullet):
        #Checks to see if the bullet has hit the enemy and responds to it
        global score
        a = main_canvas.bbox(bullet)
        for x in enemies:
            b = main_canvas.bbox(x.e_sprite)
            #if b[0] in range(a[0], a[2]) or b[2] in range(a[0], a[2]) and b[1] in range(a[1], a[3]) or b[3] in range(a[1],a[3]):
            if b[0]< a[2] and b[2] > a[0] and b[1] < a[3] and b[3] > a[1]:
                main_canvas.delete(x.e_sprite)
                main_canvas.delete(bullet)
                enemies.remove(x)
                score += 1
                self.enemies_check()
                score_label.config(text="Score:{}".format(score) + " "  + "Health:{}".format(player_health))


                break


    def edge_collision(self):
        #Function contains mechanics for the collision of the player and edge walls in the game, keeping the player in bounds.
        global player_x
        global player_y
        player_bound = main_canvas.bbox(self.p_sprite)
        player_left = player_bound[0]
        player_right = player_bound[2]
        player_top = player_bound[1]
        player_bottom = player_bound[3]

        if player_left < 0:
            main_canvas.move(self.p_sprite,20,0)
            player_x += PLAYER_SPEED
        elif player_right > GAME_WIDTH:
            main_canvas.move(self.p_sprite,-20,0)
            player_x -= PLAYER_SPEED

        elif player_top < 0:
            main_canvas.move(self.p_sprite,0,20)
            player_x += PLAYER_SPEED

        elif player_bottom > GAME_HEIGHT:
            main_canvas.move(self.p_sprite,0,-40)
            player_x -= PLAYER_SPEED

    def enemies_check(self):
        #Checks if there are any enemies, if not then game over
        if not enemies:
            game_over()
        else:
            pass

    def powerup_cheat(self,event):
        #Function for activating the power up cheat when triggered by the player
        global PLAYER_SPEED
        PLAYER_SPEED = 40
        pu_image= main_canvas.create_image(300,45, image=pu, anchor='nw', tag="powerup",state='normal')

    def shield_cheat(self,event):
        #Function for activating the sheild cheat when triggered by the player
        global shield
        shield = True
        sh_image = main_canvas.create_image(400, 600, image=sh, anchor='nw', tag="shield", state='normal')


#ENEMY CLASS#

class Enemy:
    def __init__(self):
        #Declaring enemy attributes and creating the enemy sprite.
        self.enemy_x = 1600 #random.randint(0, 1920)
        self.enemy_y = random.randint(0, 900)
        self.enemy_speed = 5

        self.en = PhotoImage(file=ENEMY_SPRITE)
        self.e_sprite = main_canvas.create_image(self.enemy_x, self.enemy_y, anchor='nw', image=self.en, tag='enemy')

    def follow(self, player_x, player_y, enemy_x, enemy_y, enemy_speed=5):
        #This function allows the enemy to follow the player through path finding using pythagoras, allowing the enemies within the game, to constantly follow the player.
        self.diff_x = player_x - self.enemy_x
        self.diff_y = player_y - self.enemy_y

        self.distance = (self.diff_x**2 + self.diff_y**2)**0.5

        if self.distance <= self.enemy_speed:
            return self.diff_x, self.diff_y

        self.normal_x = self.diff_x/self.distance
        self.normal_y = self.diff_y/self.distance

        self.enemy_move_x = self.enemy_speed * self.normal_x
        self.enemy_move_y = self.enemy_speed * self.normal_y

        return self.enemy_move_x, self.enemy_move_y

    def enemyMove(self):
        # This function moves the enemy and constantly checks if an enemy has hit a player and responds, checks the players health, if 0 then load game over screen.
        global player_x
        global player_y
        global player_health
        global shield
        self.enemy_move_x, self.enemy_move_y = self.follow(player_x, player_y, self.enemy_x, self.enemy_y, self.enemy_speed)
        self.enemy_x += self.enemy_move_x
        self.enemy_y += self.enemy_move_y
        main_canvas.move(self.e_sprite, self.enemy_move_x, self.enemy_move_y)
        #if self.enemy_x == player_x and self.enemy_y == player_y:
        a= main_canvas.bbox(player.p_sprite)
        b = main_canvas.bbox(self.e_sprite)
        if b[0] < a[2] and b[2] > a[0] and b[1] < a[3] and b[3] > a[1]:
            if shield == False:
                player_health -= 2
                score_label.config(text="Score:{}".format(score) + " " +"Health:{}".format(player_health))
            if player_health == 0:
                main_canvas.delete(ALL)
                main_canvas.configure(bg='black')
                main_canvas.create_text(main_canvas.winfo_width() / 2, main_canvas.winfo_height() / 2, font=('chiller', 70),text="DEAD", fill="red", tag="dead")
                window.after(5000, lambda:game_over())
        window.after(100, lambda:self.enemyMove())


#GAME BOOT UP CLASS#

class GameStartUp:
    # Class contains functions for the boot up of the game and all the screens with in the game.
    def __init__(self):
        #Screen 1: The menu screen is created at the instantiation of the class as it is the first screen of the game.
        main_canvas.create_image(0, 0, image=menu_bg, anchor='nw')
        main_canvas.create_image(400, main_canvas.winfo_height() / 2, image=game_logo, anchor='nw', tag="logo")
        self.startBtn = Button(main_canvas, text="START GAME", bg='black', fg='red', font=('chiller', 50),command=self.info_screen)
        self.place = self.startBtn.place(x=600, y=250)

    def info_screen(self):
        #Screen 2: Info screen is after the menu and shows the controls to the user.
        self.startBtn.destroy()
        main_canvas.delete(ALL)
        main_canvas.create_text(main_canvas.winfo_width() / 2, 100, font=('chiller', 70), text="ARE YOU READY FOR THE INFERNO?", fill="red",tag="info")
        main_canvas.create_text(main_canvas.winfo_width() / 2, 300, font=('chiller', 20),text="CONTROLS: (A,W,S,D) TO MOVE PLAYER,(SPACE) TO SHOOT ,(Q/b) TO ACTIVATE BOSS KEY AND (P) OR (I) FOR A SURPRISE", fill="red", tag="infotxt")


        self.infoBtn = Button(main_canvas, text="CONTINUE", bg='black', fg='red', font=('chiller', 50), command= self.nameEnter)
        self.infoBtn.place(x=635, y=400)

    def nameEnter(self):
        #Screen 3: At this screen the user enters their name which will be used later to store their score on the leaderboard.
        self.infoBtn.destroy()
        main_canvas.delete(ALL)
        main_canvas.create_text(main_canvas.winfo_width() / 2, 100, font=('chiller', 70), text="ENTER NAME", fill="red",tag="entername")

        self.name_bx = Entry(window)
        main_canvas.create_window(500, 300, window=self.name_bx)
        self.name_bx.place(x=710,y=350)
        self.nameBtn = Button(main_canvas, text="CONTINUE", bg='black', fg='red', font=('chiller', 50), command= self.selectPlayer)
        self.nameBtn.place(x=635, y=400)

    def selectPlayer(self):
        #Screen 4: On this screen the user can choose a player sprite with three colours to choose from and select the button to choose that sprite..
        global player_name
        if not self.name_bx.get():
            player_name = 'Player'
        else:
            player_name = self.name_bx.get()
        self.name_bx.destroy()
        self.nameBtn.destroy()
        main_canvas.delete(ALL)
        main_canvas.create_text(main_canvas.winfo_width() / 2, 100, font=('chiller', 70), text="SELECT YOUR PLAYER",fill="red", tag="selectplayer")
        self.playerB_btn = Button(main_canvas,bg='black', image = playerB,command= self.blue_player)
        self.playerB_btn.place(x=200, y=200)
        self.playerR_btn = Button(main_canvas,bg='black', image = playerR,command= self.red_player)
        self.playerR_btn.place(x=635, y=200)
        self.playerG_btn = Button(main_canvas,bg='black', image = playerG,command= self.green_player)
        self.playerG_btn.place(x=1050, y=200)

    def blue_player(self):
        #Function if user chooses blue sprite.
        global MAIN_SPRITE
        MAIN_SPRITE = PLAYER_SPRITE_B
        self.difficulty()
    def red_player(self):
        # Function if user chooses red sprite.
        global MAIN_SPRITE
        MAIN_SPRITE = PLAYER_SPRITE_R
        self.difficulty()
    def green_player(self):
        # Function if user chooses green sprite.
        global MAIN_SPRITE
        MAIN_SPRITE = PLAYER_SPRITE_G
        self.difficulty()

    def difficulty(self):
        #Screen 5: This screen allows the player to choose a difficulty for the game which will determine how many enemies will spawn that game. Number of enemies spawn increases with difficulty.
        self.playerB_btn.destroy()
        self.playerR_btn.destroy()
        self.playerG_btn.destroy()
        main_canvas.delete(ALL)
        main_canvas.create_text(main_canvas.winfo_width() / 2, 100, font=('chiller', 70), text="CHOOSE DIFFICULTY", fill="red",tag="difficulty")
        self.easyBtn = Button(main_canvas,width= 20 ,text="EASY ☠", bg='black', fg='red', font=('chiller', 50,),command= self.easy_difficulty)
        self.easyBtn.place(x=500, y=200)
        self.mediumBtn = Button(main_canvas,width= 20, text="MEDIUM ☠☠", bg='black', fg='red', font=('chiller', 50), command= self.medium_difficulty)
        self.mediumBtn.place(x=500, y=370)
        self.hardBtn = Button(main_canvas,width= 20 , text="HARD ☠☠☠", bg='black', fg='red', font=('chiller', 50), command= self.hard_difficulty)
        self.hardBtn.place(x=500, y=550)

    def easy_difficulty(self):
        #Function if user chose easy difficulty
        self.game_bootup(15)
    def medium_difficulty(self):
        # Function if user chose medium difficulty
        self.game_bootup(25)
    def hard_difficulty(self):
        # Function if user chose hard difficulty
        self.game_bootup(45)

    def game_bootup(self,diff):
        #Method sets up the inital bootup of the game and then starts the game.
        global enemies
        global player
        self.easyBtn.destroy()
        self.mediumBtn.destroy()
        self.hardBtn.destroy()
        main_canvas.delete(ALL)
        main_canvas.create_image(0, 0, image=game_bg, anchor='nw')

        enemies = [Enemy() for i in range(diff)]
        player = Player()
        main_game()

    def boss_key(self,event):
        #Function for when boss key is activated.
        self.boss_K = main_canvas.create_image(0, 0, image=boss_bg, anchor='nw')

    def delete_boss_key(self,event):
        #Function to delete the boss key after activation.
        main_canvas.delete(self.boss_K)



# MAIN GAME #



def game_over():
    #Last screen which is ran when the user has killed all the enemies or if they have died. Displays the leaderboard.
    global player_name
    global score
    score_label.destroy()
    main_canvas.delete(ALL)
    main_canvas.configure(bg='black')
    main_canvas.create_text(main_canvas.winfo_width() / 2, 200, font=('chiller', 150), text="GAME OVER", fill="red",tag="gameover")

    f = open("Leaderboard.txt", "a")
    f.write("  "+ player_name + ":" + str(score))
    f.close()

    f = open('Leaderboard.txt', 'r')
    leaderboard = [line.replace('\n', '') for line in f.readlines()]
    f.close()

    scoreplace = 425
    main_canvas.create_text(main_canvas.winfo_width() / 2, 350, font=('chiller', 50),text="LEADERBOARD", fill="red", tag="leaderboard")
    for i in leaderboard:
        main_canvas.create_text(main_canvas.winfo_width() / 2, scoreplace, font=('chiller', 30), text=i, fill="red",
                                tag="socres")
        scoreplace -= 5




def spawnEnem(enemies,wave_num):
    #Spawns the enemies in waves.
    if wave_num == 0:
        for x in range(5):
            enemies[x].enemyMove()
    else:
        for x in range(5*wave_num):
            enemies[x].enemyMove()

    window.after(10)

def main_game():
    #contains controls for user and loads the sprites onto the game canvas.
    main_canvas.itemconfig(tagOrId="player_sprite", state='normal')
    window.bind("<Key>", player.move)
    window.bind("<space>", player.shoot)
    window.bind("<q>", game.boss_key)
    window.bind("<b>", game.delete_boss_key)
    window.bind("<p>", player.powerup_cheat)
    window.bind("<i>", player.shield_cheat)

    wave_freq = (len(enemies) // 5) + 1
    for n in range(wave_freq):
        spawnEnem(enemies, n)




#window settings
window = Tk()
window.title("Inferno")
window.resizable(True,True)
window.configure(bg='black')
window.iconbitmap('Images/skull.ico')

#Declaring variables for the PhotoImage source for images.
game_bg = PhotoImage(file=GAME_BACKGROUND_IMAGE)
menu_bg = PhotoImage(file=MENU_BACKGROUND_IMAGE)
game_logo = PhotoImage(file=LOGO_IMAGE)
boss_bg = PhotoImage(file=BOSSKEY_BACKGROUND_IMAGE)
pu= PhotoImage(file=POWERUP_IMAGE)
playerB = PhotoImage(file=PLAYER_SPRITE_B)
playerR = PhotoImage(file=PLAYER_SPRITE_R)
playerG = PhotoImage(file=PLAYER_SPRITE_G)
sh = PhotoImage(file=SHIELD_IMAGE)

#Player health and score
player_health = 100
score = 0

#Score label that shows health percentage and current score.
score_label = Label(window, text="Score:{}".format(score) + " " + "Health:{}".format(player_health),font=('chiller', 40), fg='red')
score_label.config(bg="black")
score_label.pack()

#Canvas setings
main_canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH)
main_canvas.pack(fill = "both", expand = True)
main_canvas.configure(bg='black')

#Decleration of game from GameStartUp class.
game = GameStartUp()




window.update()

#storing sizes of window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")



window.mainloop()




