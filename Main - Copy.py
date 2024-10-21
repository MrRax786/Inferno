from tkinter import *
import random
import threading

player_x = 0
player_y = 425

player_name = 'Player'

GAME_WIDTH = 1600
GAME_HEIGHT = 900

PLAYER_SPRITE = "Images/playerR.png"
PLAYER_SPEED = 20
PLAYER_HEALTH = 100
ENEMY_SPRITE = "Images/enemy.png"
BULLET_SPRITE = "Images/bullet.png"
BACKGROUND_IMAGE = "Images/grassBackground.png"

class Player:
    def __init__(self):
        global player_x
        global player_y

        player_x = 0
        player_y = 350

        self.pl = PhotoImage(file=PLAYER_SPRITE)
        self.p_sprite = main_canvas.create_image(player_x,player_y,image=self.pl,anchor='nw', tag="player_sprite")



        self.bullet_img = PhotoImage(file=BULLET_SPRITE)
        self.bullet_img.image = self.bullet_img

    def move(self, event):
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
        global bullet, bulletloop
        main_canvas.move(bullet,10,0)
        self.bullet_collision(bullet)
        bulletloop = window.after(10,self.moveBullet)



    def shoot(self,event):
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
        global score
        a = main_canvas.bbox(bullet)
        for x in enemies:
            b = main_canvas.bbox(x.e_sprite)
            #if b[0] in range(a[0], a[2]) or b[2] in range(a[0], a[2]) and b[1] in range(a[1], a[3]) or b[3] in range(a[1],a[3]):
            if b[0]< a[2] and b[2] > a[0] and b[1] < a[3] and b[3] > a[1]:
                main_canvas.delete(x.e_sprite)
                enemies.remove(x)
                score += 1
                self.enemies_check()
                score_label.config(text="Score:{}".format(score) + " "  + "Health:{}".format(player_health))


                break


    def edge_collision(self):
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
        if not enemies:
            game_over()
        else:
            pass





class Enemy:
    def __init__(self):
        self.enemy_x = 1600 #random.randint(0, 1920)
        self.enemy_y = random.randint(0, 900)
        self.enemy_speed = 5

        self.en = PhotoImage(file=ENEMY_SPRITE)
        self.e_sprite = main_canvas.create_image(self.enemy_x, self.enemy_y, anchor='nw', image=self.en)

    def follow(self, player_x, player_y, enemy_x, enemy_y, enemy_speed=5):
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
        global player_x
        global player_y
        global player_health
        self.enemy_move_x, self.enemy_move_y = self.follow(player_x, player_y, self.enemy_x, self.enemy_y, self.enemy_speed)
        self.enemy_x += self.enemy_move_x
        self.enemy_y += self.enemy_move_y
        main_canvas.move(self.e_sprite, self.enemy_move_x, self.enemy_move_y)
        #if self.enemy_x == player_x and self.enemy_y == player_y:
        a= main_canvas.bbox(player.p_sprite)
        b = main_canvas.bbox(self.e_sprite)
        if b[0] < a[2] and b[2] > a[0] and b[1] < a[3] and b[3] > a[1]:
            player_health -= 2
            score_label.config(text="Score:{}".format(score) + " " +"Health:{}".format(player_health))
            if player_health == 0:
                main_canvas.delete(ALL)
                main_canvas.configure(bg='black')
                main_canvas.create_text(main_canvas.winfo_width() / 2, main_canvas.winfo_height() / 2, font=('chiller', 70),text="DEAD", fill="red", tag="dead")
                window.after(5000, lambda:game_over())
        window.after(100, lambda:self.enemyMove())




def check_collisions():
    pass

def game_over():
    global player_name
    global score
    score_label.destroy()
    main_canvas.delete(ALL)
    main_canvas.configure(bg='black')
    main_canvas.create_text(main_canvas.winfo_width() / 2, 100, font=('chiller', 70), text="GAME OVER", fill="red",tag="gameover")

    f = open("Leaderboard.txt", "a")
    f.write(player_name + ":" + str(score))
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



def leaderboard():
    pass




window = Tk()
window.title("Inferno")
window.resizable(True,True)
window.configure(bg='black')

bg = PhotoImage(file=BACKGROUND_IMAGE)

player_health = 100
score = 0

score_label = Label(window, text="Score:{}".format(score) + " " +"Health:{}".format(player_health), font=('chiller', 40), fg= 'red')
score_label.config(bg="black")
score_label.pack()

main_canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH)
main_canvas.pack(fill = "both", expand = True)
main_canvas.create_image(0, 0, image=bg, anchor='nw')
main_canvas.configure(bg='black')

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

player = Player()
window.bind("<Key>", player.move)
window.bind("<space>", player.shoot)

def spawnEnem(enemies,wave_num):
    if wave_num == 0:
        for x in range(5):
            enemies[x].enemyMove()
    else:
        for x in range(5*wave_num):
            enemies[x].enemyMove()

    window.after(10)

enemies = [Enemy() for i in range(5)]

wave_freq =len(enemies)//5
for n in range(wave_freq):
    spawnEnem(enemies,n)





#spawnEnem(enemies)

window.mainloop()




