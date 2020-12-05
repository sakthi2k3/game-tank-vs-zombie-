import pgzrun
WIDTH = 1200
HEIGHT = 720
player=Actor("tank2")
enemy=Actor("enemy")
player.y=HEIGHT-120
player_speed = 10
bullet_speed=8
level=1
bullets=[]
enemys=[]
jump=False
j=10
b=0
d=0
a=0
c=0
p="1"
s=[]
game_over=False
fires=[]
coins=[]
x=0
gameover=Actor("game over")
gameover.x=600
gameover.y=360
score=100000
bonus=0
total=0

def draw():
   if level<6:     
        screen.blit("b2",(0,0))
        draw_enemy()
        draw_player()
        draw_bullets()
        draw_fire()
        draw_coin()
        draw_lightning()
        draw_score()
        for t in s:
            t.draw()
        if game_over:
            gameover.draw()
   elif level==6:
       screen.blit("b4",(0,0))
       draw_total_score()
            
    
def update():
   if not game_over and level<6: 
        player_move()
        move_bullets()
        move_enemy()
        check_bullet_collision()
        check_boundries()
        check_nxtlvl()
        player_collision()
        move_fire()
        coin_collected()
        move_lightning()
        check_shock()
        update_score()
        check_player_boundries()
   elif level==6:
       total_score()



def check_player_boundries():
   if player.left<0:
      player.left=0

def update_score():
   global score
   score=score-2

def draw_coin():
    for coin in coins:
        coin.draw()       

def coin_collected():
    global p,bonus
    for coin in coins:
        if coin.colliderect(player):
            sounds.coin.play()
            coins.remove(coin)
            bonus+=500
            if level==3:
                p="2"
                bonus+=1000
   
def draw_total_score():
   screen.draw.text("You Win", (WIDTH/2-120, HEIGHT /4-20), fontsize=100, color="grey")
   screen.draw.text("Score: "+str(score), (WIDTH/2-100, HEIGHT /2-20), fontsize=50, color="grey")
   screen.draw.text("Bonus: "+str(bonus), (WIDTH/2-100, HEIGHT /2+50), fontsize=50, color="grey")
   screen.draw.text("Final Score: "+str(total), (WIDTH/2-270, HEIGHT/2+150), fontsize=100, color="grey")

   
def total_score():
   global total,score,bonus
   if total <= score+bonus:
      total+=100
   
def check_boundries():
    
        for bullet in bullets:
            if bullet.left>WIDTH:
                remove_bullet(bullet)

def player_move():
    
        global j,jump
        if keyboard.left:
            player.x -= player_speed
        if keyboard.right:
            player.x += player_speed
        if not(jump):
            if keyboard.x:
               jump=True
        else:
            if j>=-10:
                player.y-=(j*abs(j))*0.5
                j-=1
            else:
                j=10
                jump=False


def draw_bullets():
    
        for bullet in bullets:
            bullet.draw()

def move_bullets():
    
        for bullet in bullets:
            bullet.x += bullet_speed

def create_bullet():
   
        if len(bullets)<2:
                sounds.shoot.play()
                bullet = Actor("bullet"+p)
                bullet.x=player.x+109.5
                bullet.y=player.y-26
                bullets.append(bullet)  
    
def on_key_down(unicode):
  
       if unicode:
               if unicode == "z":
                    create_bullet()

    
def check_nxtlvl():
    
        global level
        if player.left>WIDTH:
            level+=1
            player.left=3
            create_enemy()
            create_coin()
        if level>5:
            game_over=True
            sounds.music2.play()
            
def draw_player():
    
  
        player.draw()
   
    
def draw_lightning():
    global x
    if level==5 and len(s)<1 and x==0:
        x=1
        sounds.thunder.play()
        thunder=Actor("lightning")
        thunder.x=WIDTH-180
        thunder.y=0
        s.append(thunder)
        
       
          
def move_lightning():
    for t in s:
        t.y+=1

def check_shock():
     for t in s:
         for enemy in enemys:
            if enemy.colliderect(t):
                s.remove(t)
    
def create_enemy():
        global d,level
        if level==1:
           for j in range(3):
                enemy=Actor("enemy3")
                enemy.image ="enemy1"
                enemy.x=WIDTH-100-j*80
                enemy.y=player.y-10
                enemys.append(enemy)
        elif level==2:
            for j in range(5):
                enemy=Actor("enemy3")
                enemy.image ="enemy4"
                enemy.x=WIDTH-100-j*90
                enemy.y=player.y-38
                enemys.append(enemy)
        elif level==3:
              for j in range(3):
                enemy=Actor("enemy3")
                enemy.image ="enemy3"
                enemy.x=WIDTH-100-j*130
                enemy.y=player.y-65
                enemys.append(enemy)
        elif level==4:
            for j in range(5):
                enemy=Actor("enemy3")
                enemy.image ="enemy3"
                enemy.x=WIDTH-100-j*130
                enemy.y=player.y-60
                enemys.append(enemy)
        elif level==5:
                enemy=Actor("enemy3")
                enemy.image ="boss"
                enemy.x=WIDTH-190
                enemy.y=player.y-70
                enemys.append(enemy)
                d=10
                
        
def draw_fire():
    for fire in fires:
        fire.draw()

def move_fire():
    for fire in fires:
        fire.x-=4

def draw_enemy():
          for enemy in enemys:
            enemy.draw()
            
def enemy_fire():
    for enemy in enemys:
            if len(fires)<1:
                fire = Actor("ball")
                fire.x=enemy.x-170
                fire.y=enemy.y+22
                fires.append(fire)
                sounds.zap.play()

def player_collision():
    global game_over  
    for enemy in enemys:
        if enemy.colliderect(player):
                  
                   sounds.explosion.play()
                   player.image="boom"
                   game_over=True
    for fire in fires:
        if fire.colliderect(player):
                   remove_fire(fire)
                   sounds.explosion.play()
                   player.image="boom"
                   game_over=True       
                   
                   
def move_enemy():
     global b
     if level<5:
         for enemy in enemys:
              enemy.x-=0.5
              
     elif level==5:
         for enemy in enemys:
             enemy.x-=0.5
             b+=1
             if b==75:
                b=0
                enemy_fire()
           
             

def check_bullet_collision():
       global a,b,d,bonus
   
        
       for bullet in bullets:
            for enemy in enemys:
                if bullet.colliderect(enemy):
                    a+=1
                    sounds.hit.play()
                    remove_bullet(bullet)
                if a==3+level+d or a>level+3+d:
                    music.pause()
                    sounds.dead.play()
                    remove_enemy(enemy)
                    bonus+=200*level
            for fire in fires:
                if bullet.colliderect(fire):
                    remove_bullet(bullet)
                    remove_fire(fire)

    
def remove_fire(fire):
    fires.remove(fire)
def remove_enemy(enemy):
        global a
  
        a=0
        if enemy in enemys:
            enemys.remove(enemy)
        if level==5:
            game_over==True

def remove_bullet(bullet):
  
    
        if bullet in bullets:
            bullets.remove(bullet)

def draw_score():
    screen.draw.text("Level: "+str(level), (10, 20), fontsize=50, color="green")
    screen.draw.text("Score: "+str(score), (WIDTH-250, 20), fontsize=50, color="yellow")
    screen.draw.text("Bonus: "+str(bonus), (WIDTH-250, 70), fontsize=50, color="orange")

def create_coin():
    global c
    if level==1 or level==2 or level==4:
        for i in range(2):
            coin=Actor("coin")
            coin.x=500+c
            coin.y=400
            if c==0:
                c=525
            else:
                c=0    
            coins.append(coin)
    
    elif level==3:
          for i in range(2):
              coin=Actor("star")
              coin.x=760
              coin.y=400
              coins.append(coin)
    
create_enemy()
create_coin()
pgzrun.go()
