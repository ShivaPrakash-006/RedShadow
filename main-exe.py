#MODULES
import pygame
import pygame.constants
import random
import time
import pickle
import pymysql
#INITIALISATION
pygame.init()
pygame.display.init()
pygame.font.init()

#SCREEN SETTINGS
WININFO = pygame.display.Info()
WIDTH, HEIGHT = WININFO.current_w, WININFO.current_h

#VARIABLES
PLAYER_W = 64
PLAYER_H = 64
PLAYER_V = 10
PLAYER_D = 200
PLAYER_P = 3

BUTTON_W = 200
BUTTON_H = 50

STAR_W = 5
STAR_H = 5
STAR_V = 5

BULLET_H = 10
BULLET_W = 7
BULLET_V = 15

ENEMY_H = 32
ENEMY_W = 32
ENEMY_V = 2.5

AMBUSH_H = 16
AMBUSH_W = 16
AMBUSH_V = 15

COIN_H = 8
COIN_W = 8
COIN_V = 1

PAUSE_H = 32
PAUSE_W = 32

PAUSEBOX_H = HEIGHT/2
PAUSEBOX_W = WIDTH/4

#PICTURES
BG = pygame.transform.scale(pygame.image.load("_internal/Background.png"), (WIDTH,HEIGHT))
PAUSE = pygame.image.load("_internal/PauseButton.png")
CRYSTAL = pygame.image.load("_internal/SpaceShips/Crystal/Crystal.png")
ARROW = pygame.image.load("_internal/SpaceShips/ArrowHead/ArrowHead.png")
HELIX = pygame.image.load("_internal/SpaceShips/Helix/Helix.png")
SHIP1 = CRYSTAL
SHIP2 = pygame.image.load("_internal/SpaceShips/Enemy.png")

#SCREEN SETTING
WIN = pygame.display.set_mode((WIDTH , HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Red Shadow")

#FONTS
FONT = pygame.font.Font("_internal/SourceCodePro-Medium.ttf", 16)
FONT2 = pygame.font.Font("_internal/SourceCodePro-SemiBold.ttf", 20)

#MAIN MENU
def main_menu():
    run = True
    state = "Game"

    #BUTTONS
    class play_button:
        button = pygame.Rect(WIDTH/2-BUTTON_W/2, HEIGHT/2-125 , BUTTON_W, BUTTON_H)
        color = 'white'
        text = 'Play'
        state = 'Game'
    
    class score_button:
        button = pygame.Rect(WIDTH/2-BUTTON_W/2, HEIGHT/2-62.5 , BUTTON_W, BUTTON_H)
        color = 'white'
        text = 'Scores'
        state = 'Scores'
    
    class upgrade_button:
        button = pygame.Rect(WIDTH/2-BUTTON_W/2, HEIGHT/2, BUTTON_W, BUTTON_H)
        color = 'white'
        text = 'Upgrades'
        state = 'Upgrades'
    
    class quit_button:
        button = pygame.Rect(WIDTH/2-BUTTON_W/2, HEIGHT/2+62.5, BUTTON_W, BUTTON_H)
        color = 'white'
        text = 'Quit'
        state = 'Quit'
    
    buttons = [play_button, quit_button, upgrade_button, score_button]

    #DISPLAY UPDATER
    def draw():
        WIN.blit(BG, (0,0))
        for button in buttons:
            pygame.draw.rect(WIN, button.color, button.button)
            text = FONT.render(button.text, 1, 'black')
            WIN.blit(text, (button.button.x + button.button.width/2 - text.get_width()/2, button.button.y + button.button.height/2 - text.get_height()/2))
        pygame.display.update()
    
    #MAIN LOOP
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "Quit"
                run = False
        
        for button in buttons:
            if button.button.collidepoint(pygame.mouse.get_pos()):
                button.color = 'grey'
                if pygame.mouse.get_pressed(3)[0]:
                    state = button.state
                    run = False
            else:
                button.color = 'white'
        
        draw()
    
    return state

#UPGRADES
def upgrades():
    run = True
    state = "Menu"
    with open('_internal/Upgrades/upgrades.dat', 'rb') as f:
        upgrade_data = pickle.load(f)
    ship_list = ["Crystal", "ArrowHead", "Helix"]
    ship_images = [CRYSTAL, ARROW, HELIX]
    upgrade_list = ["Lives","Bullets","Fire Rate","Precision","Shield Time","Fire Time","Dodge","Evasion"]
    ship_no = 0
    ship = ship_list[ship_no]
    ship_image = ship_images[ship_no]
    ship_cost = [1000, 1500, 2000]
    ship_unlocked = upgrade_data[ship][4]
    upgrade_mod = [1, 1, -5, 30, 60, 50, -50, 1]
    upgrade_max = upgrade_data[ship][2]
    upgrade_min = upgrade_data[ship][3]
    upgrade_queue = upgrade_data[ship][0]
    upgrade_unlocked = upgrade_data[ship][1]
    upgrade_cost = [200, 250, 100, 25, 25, 25, 25, 200]
    up_no = 0
    upgrade = upgrade_list[up_no]
    coins = upgrade_data["Coins"]
    
    back_button = pygame.Rect((30,30),(64,64))
    prev_button = pygame.Rect((400,150),(64,64))
    next_button = pygame.Rect((900,150),(64,64))
    up_button = pygame.Rect((100,450),(64,64))
    down_button = pygame.Rect((100,550),(64,64))
    upgrade_button = pygame.Rect((300, 500),(64,64))
    degrade_button = pygame.Rect((200, 500),(64,64))
    class unlock_button:
        button = unlock_button = pygame.Rect((585,325),(BUTTON_W, BUTTON_H))
        color = 'white'
        text = FONT.render(f"Unlock: {ship_cost[ship_no]}", 1, 'black')

    def draw(ship, ship_name, ship_state, data):
        WIN.blit(BG, (0,0))
        #SHIP DISPLAY
        WIN.blit(pygame.transform.scale_by(ship, 3), (WIDTH/2-pygame.transform.scale_by(ship, 3).get_width()/2, 64))
        shipName = FONT.render(ship_name, 1, 'white')
        WIN.blit(shipName, (WIDTH/2 - shipName.get_width()/2, (3*HEIGHT/8) - shipName.get_height()/2))
        #BUTTONS
        WIN.blit(pygame.transform.scale2x(pygame.transform.rotate(pygame.image.load('_internal/Upgrades/ArrowButton.png'), -90)),back_button)
        WIN.blit(pygame.transform.scale2x(pygame.transform.rotate(pygame.image.load('_internal/Upgrades/ArrowButton.png'), 90)), next_button)
        WIN.blit(pygame.transform.scale2x(pygame.transform.rotate(pygame.image.load('_internal/Upgrades/ArrowButton.png'), -90)), prev_button)
        WIN.blit(pygame.transform.scale2x(pygame.image.load('_internal/Upgrades/ArrowButton.png')), down_button)
        WIN.blit(pygame.transform.scale2x(pygame.transform.rotate(pygame.image.load('_internal/Upgrades/ArrowButton.png'), 180)),up_button)
        WIN.blit(pygame.transform.scale2x(pygame.image.load('_internal/Upgrades/UpgradeButton.png')),upgrade_button)
        WIN.blit(pygame.transform.scale2x(pygame.image.load('_internal/Upgrades/DegradeButton.png')),degrade_button)
        if not ship_state:
            unlock_button.text = FONT.render(f"Unlock: {ship_cost[ship_no]}", 1, 'black')
            pygame.draw.rect(WIN, unlock_button.color, unlock_button.button)
            WIN.blit(unlock_button.text, (unlock_button.button.x + unlock_button.button.width/2 - unlock_button.text.get_width()/2, unlock_button.button.y + unlock_button.button.height/2 - unlock_button.text.get_height()/2))

        upgrade_text = FONT.render(upgrade, 1, 'white')
        coin_text = FONT.render(f"Coins: {coins}", 1, 'white')
        cost_text = FONT.render(f"Cost: {upgrade_cost[n]}", 1, 'white')
        WIN.blit(upgrade_text, ((130-upgrade_text.get_width()/2,520)))
        WIN.blit(coin_text, (WIDTH-coin_text.get_width()-10, 10))
        WIN.blit(cost_text, (50, HEIGHT - 50))

        lives_text = FONT2.render(f"Lives: {data[0]}", 1, 'white')
        bullets_text = FONT2.render(f"Bullets: {data[1]}", 1, 'white')
        firerate_text = FONT2.render(f"Fire Rate: {int(data[2]//5)}", 1, 'white')
        slowfuel_text = FONT2.render(f"Precision: {data[3]//30}", 1, 'white')
        shield_text = FONT2.render(f"Shield Time: {data[4]//60}", 1, 'white')
        fire_text = FONT2.render(f"Fire Time: {data[5]//50}", 1, 'white')
        dodgetime_text = FONT2.render(f"Dodge: {data[6]//50}", 1, 'white')
        dodgechance_text = FONT2.render(f"Evasion: {data[7]}", 1, 'white')

        WIN.blit(lives_text, (500, 400))
        WIN.blit(bullets_text, (500, 500))
        WIN.blit(firerate_text, (500, 600))
        WIN.blit(slowfuel_text, (500, 700))
        WIN.blit(shield_text, (1000, 400))
        WIN.blit(fire_text, (1000, 500))
        WIN.blit(dodgetime_text, (1000, 600))
        WIN.blit(dodgechance_text, (1000, 700))

        pygame.display.update()
        
        
    while run:
        upgrade = upgrade_list[up_no]
        n = upgrade_list.index(upgrade)

        if pygame.event.get(pygame.QUIT):
            state = "Quit"
            run = False
        
        if back_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN:
                    state = 'Menu'
                    run = False
        
        if prev_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and ship_no > 0:
                    upgrade_data[ship] = [upgrade_queue, upgrade_unlocked, upgrade_max, upgrade_min, ship_unlocked]
                    ship_no -= 1
                    ship = ship_list[ship_no]
                    ship_image = ship_images[ship_no]
                    ship_unlocked = upgrade_data[ship][4]
                    upgrade_max = upgrade_data[ship][2]
                    upgrade_min = upgrade_data[ship][3]
                    upgrade_queue = upgrade_data[ship][0]
                    upgrade_unlocked = upgrade_data[ship][1]

        if next_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and ship_no < 2:
                    upgrade_data[ship] = [upgrade_queue, upgrade_unlocked, upgrade_max, upgrade_min, ship_unlocked]
                    ship_no += 1
                    ship = ship_list[ship_no]
                    ship_image = ship_images[ship_no]
                    ship_unlocked = upgrade_data[ship][4]
                    upgrade_max = upgrade_data[ship][2]
                    upgrade_min = upgrade_data[ship][3]
                    upgrade_queue = upgrade_data[ship][0]
                    upgrade_unlocked = upgrade_data[ship][1]

        if up_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and up_no < 7:
                    up_no += 1
        
        if down_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and up_no > 0:
                    up_no -= 1
        
        if upgrade_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and ship_unlocked:
                    if upgrade_queue[n] < upgrade_max[n]:
                        if upgrade_unlocked[n] > upgrade_queue[n]:
                            upgrade_queue[n] += upgrade_mod[n]
                        elif upgrade_unlocked[n] == upgrade_queue[n]:
                            if coins > upgrade_cost[n]:
                                coins -= upgrade_cost[n]
                                upgrade_queue[n] += upgrade_mod[n]
                                upgrade_unlocked[n] = upgrade_queue[n]
                        elif upgrade_queue[n] > upgrade_unlocked[n]:
                            upgrade_unlocked[n] = upgrade_queue[n]
                    elif upgrade_queue[n] > upgrade_max[n] and upgrade_mod[n] < 0:
                        if upgrade_unlocked[n] < upgrade_queue[n]:
                            upgrade_queue[n] += upgrade_mod[n]
                        else:
                            if coins > upgrade_cost[n]:
                                coins -= upgrade_cost[n]
                                upgrade_queue[n] += upgrade_mod[n]
                                upgrade_unlocked[n] = upgrade_queue[n]
                        if upgrade_queue[n] < upgrade_unlocked[n]:
                            upgrade_unlocked[n] = upgrade_queue[n]

        if degrade_button.collidepoint(pygame.mouse.get_pos()):
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and ship_unlocked:
                    if upgrade_queue[n] > upgrade_min[n]:
                        upgrade_queue[n] -= upgrade_mod[n]
                    elif upgrade_queue[n] < upgrade_min[n] and upgrade_mod[n] < 0:
                        upgrade_queue[n] -= upgrade_mod[n]
        
        if unlock_button.button.collidepoint(pygame.mouse.get_pos()):
            unlock_button.color = 'grey'
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN and not ship_unlocked and coins >= ship_cost[ship_no]:
                    ship_unlocked = 1
                    coins -= ship_cost[ship_no]
        else:
            unlock_button.color = 'white'


        draw(ship_image, ship, ship_unlocked, upgrade_queue)
    
    with open('_internal/Upgrades/upgrades.dat', 'wb') as f:
        upgrade_data[ship] = [upgrade_queue, upgrade_unlocked, upgrade_max, upgrade_min, ship_unlocked]
        upgrade_data["Coins"] = coins
        if ship_unlocked:
            upgrade_data["Selected"] = ship
        else:
            upgrade_data["Selected"] = "Crystal"
        pickle.dump(upgrade_data, f)
                
    return state

def scores():
    state = "Menu"
    run = True
    db = pymysql.connect(host='localhost',user='shiva',passwd='',database='red_shadow')
    cur = db.cursor()
    cur.execute("SELECT * FROM scores")
    data = cur.fetchall()
    maxno = cur.rowcount
    maxshowno = 6
    startno = 0
    lastno = startno + maxshowno
    sortno = 0
    typeno = 0
    sorting_list = ["playNo", "username", "score", "coins", "time"]
    sort_types = ["ASC", "DESC"]
    sortedby = sorting_list[sortno]
    sorttype = sort_types[typeno]
    search_key = ""

    back_button = pygame.Rect((10, 10),(64,64))
    sort_button = pygame.Rect((back_button.x + 64  + 10, 15), (BUTTON_W, BUTTON_H))
    search_button = pygame.Rect((WIDTH - BUTTON_W - 20, 15),(BUTTON_W, BUTTON_H))


    def draw(scores, search):
        WIN.blit(BG, (0,0))
        title = "%-20s%-20s%-20s%-20s%-20s%-20s"%("Play No", "Username", "Ship", "Score", "Coins", "Time")
        title_text = FONT2.render(title, 1, 'white')
        WIN.blit(title_text, (20, 100))
        for score in scores:
            i = scores.index(score)
            score_text = "%-20s%-20s%-20s%-20s%-20s%-20s"%(score[0],score[1],score[2],score[3],score[4],score[5])
            scores_text = FONT2.render(score_text, 1, 'white')
            WIN.blit(scores_text, (20, 100*(i+2)))
        
        #BUTTONS
        WIN.blit(pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load("_internal/Upgrades/ArrowButton.png")), -90), back_button)
        sort_text = FONT.render(f"Sort By:{sortedby}", 1, 'black')
        pygame.draw.rect(WIN, 'white', sort_button)
        WIN.blit(sort_text, (sort_button.x + sort_button.width/2 - sort_text.get_width()/2, sort_button.y + sort_button.height/2 - sort_text.get_height()/2))
        search_text = FONT.render("Search", 1, 'black')
        pygame.draw.rect(WIN, 'white', search_button)
        WIN.blit(search_text, (search_button.x + search_button.width/2 - search_text.get_width()/2, search_button.y + search_button.height/2 - search_text.get_height()/2))

        searchkey_text = FONT2.render(search, 1, 'white')
        WIN.blit(searchkey_text, (WIDTH - 500, 30))

        pygame.display.update()
         

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "Quit"
                run = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and startno < maxno - maxshowno:
                    startno += 1
                elif event.y > 0 and startno > 0:
                    startno -= 1
            if back_button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                state = "Menu"
                run = False
                break
            if sort_button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                if sortno != 4:
                    if typeno == 1:
                        sortno += 1
                        typeno = 0
                    else:
                        typeno = 1
                else:
                    if typeno == 1:
                        sortno = 0
                        typeno = 0
                    else:
                        typeno = 1
                sortedby = sorting_list[sortno]
                sorttype = sort_types[typeno]
                cur.execute(f"SELECT * FROM scores ORDER BY {sortedby} {sorttype}")
                data = cur.fetchall()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() and len(search_key) < 20:
                    search_key += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    search_key = search_key[:-1]
            if search_button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                cur.execute(f"SELECT * FROM scores WHERE {sortedby} LIKE '{search_key}%'")
                data = cur.fetchall()
                


        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and startno < maxno - maxshowno:
            startno += 0.1
        if keys[pygame.K_UP] and startno > 1:
            startno -= 0.1
        
        lastno = startno + maxshowno
        scores = data[int(startno):int(lastno)]
        draw(scores, search_key)
    
    db.close()
    return state

def game(game_state):
    #print(1)
    frate = 60
    run = True
    hit = False
    f = open("_internal/Upgrades/upgrades.dat", 'rb')
    data = pickle.load(f)
    
    start = time.time()
    elapsed = 0
    endpoint = 0
    startpoint = 0

    global SHIP1
    ship = data["Selected"]
    Player = pygame.Rect((WIDTH/2, HEIGHT - PLAYER_H - 10), (PLAYER_H, PLAYER_W))
    score = 0
    clock = pygame.time.Clock()
    pause_button =  pause_button = pygame.Rect((WIDTH-PAUSE_W-10, 10),(PAUSE_W, PAUSE_H))
    lives = data[ship][0][0]
    iframes = 120
    dodge_count = 0
    dodge_time = data[ship][0][6]
    evasion = data[ship][0][7]
    

    star_count = 0
    star_time = 100
    stars = []

    bulletNo = data[ship][0][1]
    bullet_time = 0 
    reload_time = data[ship][0][2]
    bullets = []

    enemies1 = []
    enemies_time1 = []

    enemies2 = []
    enemies_time2 = []

    enemies3 = []
    enemies_time3 = []

    enemies4 = []
    enemies_time4 = []

    ambush = False
    enemiesA = []
    ambush_count = 400
    ambush_time = 500

    enemies = [enemies1, enemies2, enemies3, enemies4, enemiesA]
    enemies_time = [enemies_time1, enemies_time2, enemies_time3, enemies_time4]
    enemy_time = 200
    enemy_count = 0

    lebullets = []
    rebullets = []
    vebullets = []
    ebullets = [lebullets, rebullets, vebullets]

    coins = []
    coin_timer = 900
    coin_count = 0
    coin_score = 0

    powerup_list = ('slow_fuel','shield','life','fire','clear')
    powerups = []
    l_powerup = ''
    c_powerup = ''
    shield_time = data[ship][0][4]
    shield_count = 0
    fire_time = data[ship][0][5]
    fire_count = 0
    old_fire_rate = reload_time

    slow_fuel = 300

    dodging = False

    def pause():
        box = pygame.Rect((PAUSEBOX_W*2 - PAUSEBOX_W/2, HEIGHT - PAUSEBOX_H - PAUSEBOX_H/2), (PAUSEBOX_W, PAUSEBOX_H))
        run = True

        class resume_button:
            button = pygame.Rect((box.x + PAUSEBOX_W/2 - BUTTON_W/2, box.y + PAUSEBOX_H/6 - BUTTON_H/2), (BUTTON_W, BUTTON_H))
            color = 'white'
            text = 'Resume'
            state = 'Game'
        class menu_button:
            button = pygame.Rect((box.x + PAUSEBOX_W/2 - BUTTON_W/2, box.y + PAUSEBOX_H/2 - BUTTON_H/2), (BUTTON_W, BUTTON_H))
            color = 'white'
            text = 'Menu'
            state = 'Menu'
        class quit_button:
            button = pygame.Rect((box.x + PAUSEBOX_W/2 - BUTTON_W/2, box.y + (PAUSEBOX_H*5)/6 - BUTTON_H/2), (BUTTON_W, BUTTON_H))
            color = 'white'
            text = 'Quit'
            state = 'Quit'
        buttons = [resume_button, menu_button, quit_button]
        
        def draw():
            pygame.draw.rect(WIN, 'black', box)
            for button in buttons:
                pygame.draw.rect(WIN, button.color, button.button)
                text = FONT.render(button.text, 1, 'black')
                WIN.blit(text, (button.button.x + button.button.width/2 - text.get_width()/2, button.button.y + button.button.height/2 - text.get_height()/2))
            pygame.display.update()
        
        while run:
            draw()
            keys = pygame.key.get_pressed()
            for button in buttons:
                if button.button.collidepoint(pygame.mouse.get_pos()):
                    button.color = 'grey'
                    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                        state = button.state
                        run = False
                        break
                else:
                    button.color = 'white'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "Quit"
                    run = False
        return state

    def draw(player, elapsed_time, Score, Stars, Bullets, EBullets, Enemies, Coins, CoinScore, PauseButton, Lives, Powerups, Powerup):  
        WIN.blit(BG, (0,0))

        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, 'white')
        score_text = FONT.render(f"Score: {Score}", 1, 'white')
        coinScore_text = FONT.render(f"Coins: {CoinScore}", 1, 'white')
        lives_text = FONT.render(f"Lives: {Lives}", 1, 'white')
        power_text = FONT.render(f"Power: {Powerup}", 1, 'white')

        WIN.blit(time_text, (10,20))
        WIN.blit(score_text, (WIDTH-score_text.get_width()-10, 50))
        WIN.blit(coinScore_text, (WIDTH-coinScore_text.get_width()-10, 70))
        WIN.blit(lives_text, (10, 40))
        WIN.blit(power_text, (10, 60))

        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(0)
        s.fill((255, 255, 255))

        for star in Stars:
            pygame.draw.rect(WIN, ['white','grey','light blue','light green'][random.randint(0,3)], star)
        pygame.draw.rect(s, 'red', player)
        WIN.blit(SHIP1, (player.x - 16, player.y))

        for bullet in Bullets:
            pygame.draw.rect(WIN, 'orange', bullet)
        for i in Enemies:
            for enemy in i:
                pygame.draw.rect(s, 'black', enemy)
                WIN.blit(pygame.transform.rotate(SHIP2, 180.0), enemy)
        for coin in Coins:
            pygame.draw.rect(WIN, 'yellow', coin)
        for i in EBullets:
            for ebullet in i:
                pygame.draw.rect(WIN, 'red', ebullet)
        for powerup in Powerups:
            pygame.draw.rect(WIN, 'blue', powerup.box)
        
        pygame.draw.rect(s, 'white', PauseButton)
        WIN.blit(PAUSE, PauseButton)


        WIN.blit(s, (0, 0))
        pygame.display.update()

    def save_score(username, ship, score, coins, time):
        db = pymysql.connect(host='localhost',user='shiva',passwd='',database='red_shadow')
        cursor = db.cursor()
        cursor.execute('SELECT MAX(playNo) FROM scores')
        lastpno = cursor.fetchall()[0][0]
        if lastpno == None:
            pno = 1
        else:
            pno = lastpno + 1
        cursor.execute(f"INSERT INTO scores VALUES({pno}, '{username}', '{ship}', {score}, {coins}, {int(time)})")
        db.commit()
        with open("_internal/Upgrades/upgrades.dat", 'rb') as f:
            data = pickle.load(f)
            data["Coins"] += coins
        with open("_internal/Upgrades/upgrades.dat", 'wb') as f:
            pickle.dump(data, f)
        db.close()
    
    def dodge():
        direction = 0
        t = time.time()
        pygame.init()
        pygame.display.init()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            direction = 1
        elif keys[pygame.K_a]:
            direction = -1
        return direction
    
    def power(enemy):
        ran = random.randint(0,4)
        Powerup = powerup_list[ran]
        class powerup:
            box = pygame.Rect((enemy.x, enemy.y),(COIN_W, COIN_H))
            power = Powerup
        powerups.append(powerup)
     
    f.close()

    while run:
        star_count += clock.tick(frate)
        bullet_time += 1
        enemy_count += 1
        coin_count += 1
        dodge_count += 1
#        print(c_powerup)
        if ambush:
            ambush_count += 1
        if iframes > 0:
            iframes -= 1
        
        elapsed = time.time() - start

        if score < 50:
            endpoint = 0
        elif 50 < score < 200:
            endpoint = 1
            ambush = True
        elif 200 < score < 500:
            endpoint = 2
        elif score > 500:
            endpoint = 3
        
        if score < 150:
            startpoint = 0
        elif 150 < score < 300:
            startpoint = 1
        elif score > 300:
            startpoint = 2
        
        if score < 150:
            enemy_time = 200
        if 150 < score < 300:
            enemy_time = 150
        if 300 < score < 400:
            enemy_time = 100
        if 400 < score < 1000:
            enemy_time = 50
        if 1000 < score < 2000:
            enemy_time = 25
        if 2000 < score < 5000:
            enemy_time = 10
        if 5000 < score < 10000:
            enemy_time = 5
        if 10000 < score < 20000:
            enemy_time = 1
        if score > 20000:
            pass
        
        if c_powerup == 'life':
            lives += 1
            c_powerup = ''
        elif c_powerup == 'clear':
            for i in enemies:
                i.clear()
            c_powerup = ''
        elif c_powerup == 'slow_fuel':
            slow_fuel += 300
            c_powerup = ''
        elif c_powerup == 'fire':
            if fire_count == 0:
                old_fire_rate = reload_time
                reload_time = 2
            fire_count += 1
            if fire_time < fire_count:
                reload_time = old_fire_rate
                fire_count = 0
                c_powerup = ''
        elif c_powerup == 'shield':
            iframes = shield_time


        if star_count > star_time:
            for _ in range(3):
                starx = random.randint(0, WIDTH - STAR_W)
                stary = random.randint(-20, 0)
                star = pygame.Rect((starx, stary), (STAR_W, STAR_H))
                stars.append(star)
            star_count = 0
        
        if enemy_count > enemy_time:
            enx = random.randint(0, WIDTH - ENEMY_W)
            eny = random.randint(-20, 0)
            ent = random.randint(startpoint, endpoint)
            enemy = pygame.Rect((enx, eny), (ENEMY_W, ENEMY_H))
            enemies[ent].append(enemy)
            enemies_time[ent].append(time.time())
            enemy_count = 0
         
        if ambush_count > ambush_time:
            enx = random.randint(Player.x - 50, Player.x + 50)
            eny = random.randint(-20, 0)
            enemy1 = pygame.Rect((enx, eny), (AMBUSH_W, AMBUSH_H))
            enemy2 = pygame.Rect((enx+30, eny), (AMBUSH_W, AMBUSH_H))
            enemy3 = pygame.Rect((enx, eny-30), (AMBUSH_W, AMBUSH_H))
            enemy4 = pygame.Rect((enx+30, eny-30), (AMBUSH_W, AMBUSH_H))
            enemiesA.extend([enemy1, enemy2, enemy3, enemy4])
            ambush_count = 0
            ambush_time = random.randint(300, 600)
        
        if coin_count > coin_timer:
            coin_score += 1
            coin_count = 0
            

        if game_state == "Quit":
            run = False
        
        if game_state == "Menu":
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "Quit"

        keys = pygame.key.get_pressed()
        #Movement + Image Setting
        if keys[pygame.K_k] and slow_fuel > 0:
            frate = 30
            slow_fuel -= 1
            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_P > 0) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d])  and Player.x + PLAYER_W + PLAYER_P < WIDTH): #UPRIGHT
                Player.x += PLAYER_P
                Player.y -= PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/FR.png")
            elif ((keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_P > 0) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_P > 0): #UPLEFT
                Player.x -= PLAYER_P
                Player.y -= PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/FL.png")
            elif ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_P < HEIGHT) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d])  and Player.x + PLAYER_W + PLAYER_P < WIDTH): #DOWNRIGHT
                Player.x += PLAYER_P
                Player.y += PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/DR.png")
            elif ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_P < HEIGHT) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_P > 0): #DOWNLEFT
                Player.x -= PLAYER_P
                Player.y += PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/DL.png")
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_P > 0: #LEFT
                Player.x -= PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/L.png")
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and Player.x + PLAYER_W + PLAYER_P < WIDTH: #RIGHT
                Player.x += PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/R.png")
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_P > 0: #UP
                Player.y -= PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/F.png")
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_P < HEIGHT: #DOWN
                Player.y += PLAYER_P
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/D.png")
            else:
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/I.png")
            
        else:
            frate = 60
            if ((keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_V > 0) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d])  and Player.x + PLAYER_W + PLAYER_V < WIDTH): #UPRIGHT
                Player.x += PLAYER_V
                Player.y -= PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/FR.png")
            elif ((keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_V > 0) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_V > 0): #UPLEFT
                Player.x -= PLAYER_V
                Player.y -= PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/FL.png")
            elif ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_V < HEIGHT) and ((keys[pygame.K_RIGHT] or keys[pygame.K_d])  and Player.x + PLAYER_W + PLAYER_V < WIDTH): #DOWNRIGHT
                Player.x += PLAYER_V
                Player.y += PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/DR.png")
            elif ((keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_V < HEIGHT) and ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_V > 0): #DOWNLEFT
                Player.x -= PLAYER_V
                Player.y += PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/DL.png")
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and Player.x - PLAYER_V > 0: #LEFT
                Player.x -= PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/L.png")
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and Player.x + PLAYER_W + PLAYER_V < WIDTH: #RIGHT
                Player.x += PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/R.png")
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and Player.y - PLAYER_V > 0: #UP
                Player.y -= PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/F.png")
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and Player.y + PLAYER_H + PLAYER_V < HEIGHT: #DOWN
                Player.y += PLAYER_V
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/D.png")
            else:
                SHIP1 = pygame.image.load(f"_internal/SpaceShips/{ship}/I.png")

        if (keys[pygame.K_SPACE] or keys[pygame.K_c]) and bullet_time > reload_time:
            if bulletNo == 1:
                bullet = pygame.Rect((Player.centerx-1.5-BULLET_W/2, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullets.append(bullet)
            elif bulletNo == 2:
                bullet1 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2])
            elif bulletNo == 3:
                bullet1 = pygame.Rect((Player.centerx-1.5-BULLET_W/2, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet3 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2, bullet3])
            elif bulletNo == 4:
                bullet1 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet3 = pygame.Rect((Player.centerx-35, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet4 = pygame.Rect((Player.centerx+25, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2, bullet3, bullet4])
            elif bulletNo == 5:
                bullet1 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet3 = pygame.Rect((Player.centerx-35, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet4 = pygame.Rect((Player.centerx+25, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet5 = pygame.Rect((Player.centerx-1.5-BULLET_W/2, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2, bullet3, bullet4, bullet5])
            elif bulletNo == 6:
                bullet1 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet3 = pygame.Rect((Player.centerx-35, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet4 = pygame.Rect((Player.centerx+25, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet5 = pygame.Rect((Player.centerx-50, Player.top-BULLET_H+20),(BULLET_W, BULLET_H))
                bullet6 = pygame.Rect((Player.centerx+40, Player.top-BULLET_H+20),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2, bullet3, bullet4, bullet5, bullet6])
            elif bulletNo == 7:
                bullet7 = pygame.Rect((Player.centerx-1.5-BULLET_W/2, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet1 = pygame.Rect((Player.centerx-20, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet2 = pygame.Rect((Player.centerx+10, Player.top-BULLET_H),(BULLET_W, BULLET_H))
                bullet3 = pygame.Rect((Player.centerx-35, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet4 = pygame.Rect((Player.centerx+25, Player.top-BULLET_H+10),(BULLET_W, BULLET_H))
                bullet5 = pygame.Rect((Player.centerx-50, Player.top-BULLET_H+20),(BULLET_W, BULLET_H))
                bullet6 = pygame.Rect((Player.centerx+40, Player.top-BULLET_H+20),(BULLET_W, BULLET_H))
                bullets.extend([bullet1, bullet2, bullet3, bullet4, bullet5, bullet6,bullet7])

            bullet_time = 0
        
        if keys[pygame.K_j] and not dodging and dodge_count > dodge_time:
            dodging = True
            direction = dodge()
            Player.x += PLAYER_D * direction
            dodge_count = 0
            dodging = False
            iframes += 12
        
        if keys[pygame.K_l] and l_powerup != '':
            fire_count = 0
            reload_time = old_fire_rate
            iframes = 0
            c_powerup = l_powerup
            l_powerup = ''

        if keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
        
        for bullet in bullets[:]:
            bullet.y -=  BULLET_V
            if bullet.y - BULLET_H < 0:
                bullets.remove(bullet)
        
        for ebullet in vebullets[:]:
            evade = random.randint(0, 20)
            ebullet.y += BULLET_V
            if ebullet.y + BULLET_H > HEIGHT:
                vebullets.remove(ebullet)
            if ebullet.colliderect(Player) and iframes < 1 and evade > evasion:
                vebullets.remove(ebullet)
                hit = True
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
        
        for ebullet in lebullets[:]:
            evade = random.randint(0, 20)
            ebullet.x -= BULLET_V
            if ebullet.x + BULLET_W < 0:
                lebullets.remove(ebullet)
            if ebullet.colliderect(Player) and iframes < 1 and evade > evasion:
                lebullets.remove(ebullet)
                hit = True
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
        
        for ebullet in rebullets[:]:
            evade = random.randint(0, 20)
            ebullet.x += BULLET_V
            if ebullet.x + BULLET_W > WIDTH:
                rebullets.remove(ebullet)
            if ebullet.colliderect(Player) and iframes < 1 and evade > evasion:
                rebullets.remove(ebullet)
                hit = True
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
        
        for star in stars[:]:
            star.y += STAR_V
            if star.y + STAR_H > HEIGHT:
                stars.remove(star)
        
        for enemy in enemies1[:]:
            evade = random.randint(0, 20)
            enemy.y += ENEMY_V
            if enemy.y + ENEMY_H > HEIGHT:
                enemies1.remove(enemy)
            if enemy.colliderect(Player) and iframes < 1 and evade > evasion:
                hit = True
                enemies1.remove(enemy)
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
            for bullet in bullets:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    if enemy in enemies1:
                        enemies1.remove(enemy)
                    score += 10
                    ran = random.randint(0,10)
                    if ran > 2:
                        for i in range(1):
                            coin = pygame.Rect((enemy.x, enemy.y), (COIN_W, COIN_H))
                            coins.append(coin)
                    else:
                        power(enemy=enemy)


        for enemy in enemies2[:]:
            evade = random.randint(0, 20)
            enemy.y += ENEMY_V
            if  time.time() - enemies_time2[enemies2.index(enemy)] > 1:
                ebullet = pygame.Rect((enemy.centerx-BULLET_W/2, enemy.bottom+BULLET_H),(BULLET_W, BULLET_H))
                vebullets.append(ebullet)
                enemies_time2[enemies2.index(enemy)] = time.time()
            if enemy.y + ENEMY_H > HEIGHT:
                enemies2.remove(enemy)
            if enemy.colliderect(Player) and iframes < 1 and evade > evasion:
                hit = True
                enemies2.remove(enemy)
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
            for bullet in bullets:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    if enemy in enemies2:
                        enemies2.remove(enemy)
                    score += 20
                    ran = random.randint(0,10)
                    if ran > 4:
                        for i in range(2):
                            coin = pygame.Rect((enemy.x, enemy.y), (COIN_W, COIN_H))
                            coins.append(coin)
                    else:
                        power(enemy=enemy)
        
        for enemy in enemies3[:]:
            evade = random.randint(0, 20)
            enemy.y += ENEMY_V - 1
            if time.time() - enemies_time3[enemies3.index(enemy)] > 0.5:
                ebulletC = pygame.Rect((enemy.centerx-BULLET_W/2, enemy.bottom+BULLET_H),(BULLET_W,BULLET_H))
                ebulletL = pygame.Rect((enemy.left, enemy.bottom+BULLET_H),(BULLET_W,BULLET_H))
                ebulletR = pygame.Rect((enemy.right-BULLET_W, enemy.bottom+BULLET_H),(BULLET_W,BULLET_H))
                vebullets.extend([ebulletC,ebulletL,ebulletR])
                enemies_time3[enemies3.index(enemy)] = time.time()
            if enemy.y + ENEMY_H > HEIGHT:
                enemies3.remove(enemy)
            if enemy.colliderect(Player) and iframes < 1 and evade > evasion:
                hit = True
                enemies3.remove(enemy)
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
            for bullet in bullets:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    if enemy in enemies3:
                        enemies3.remove(enemy)
                    score += 30
                    ran = random.randint(0,10)
                    if ran > 3:
                        for i in range(3):
                            coin = pygame.Rect((enemy.x, enemy.y), (COIN_W, COIN_H))
                            coins.append(coin)
                    else:
                        power(enemy=enemy)
        
        for enemy in enemies4[:]:
            evade = random.randint(0, 20)
            enemy.y += ENEMY_V
            if time.time() - enemies_time4[enemies4.index(enemy)] > 0.01:
                ebulletL = pygame.Rect((enemy.center),(BULLET_H,BULLET_W))
                ebulletR = pygame.Rect((enemy.center),(BULLET_H,BULLET_W))
                lebullets.append(ebulletL)
                rebullets.append(ebulletR)
                enemies_time4[enemies4.index(enemy)] = time.time()
            if enemy.y + ENEMY_H > HEIGHT:
                enemies4.remove(enemy)
            if enemy.colliderect(Player) and iframes < 1 and evade > evasion:
                hit = True
                enemies4.remove(enemy)
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
            for bullet in bullets:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    if enemy in enemies4:
                        enemies4.remove(enemy)
                    score += 20
                    ran = random.randint(0,10)
                    if ran > 2:
                        for i in range(4):
                            coin = pygame.Rect((enemy.x, enemy.y), (COIN_W, COIN_H))
                            coins.append(coin)
                    else:
                        power(enemy=enemy)
            
        for enemy in enemiesA[:]:
            evade = random.randint(0, 20)
            enemy.y += AMBUSH_V
            if enemy.y + AMBUSH_H > HEIGHT:
                enemiesA.remove(enemy)
            if enemy.colliderect(Player) and iframes < 1 and evade > evasion:
                hit = True
                enemiesA.remove(enemy)
                break
            elif enemy.colliderect(Player) and evade < evasion:
                iframes = 12
            for bullet in bullets:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    if enemy in enemiesA:
                        enemiesA.remove(enemy)
                    score += 10
                    for i in range(1):
                        coin = pygame.Rect((enemy.x, enemy.y), (COIN_W, COIN_H))
                        coins.append(coin)
        
        for coin in coins[:]:
            coin.y += COIN_V
            if coin.y - COIN_H > HEIGHT:
                coins.remove(coin)
            if coin.colliderect(Player):
                coin_score += 1
                coins.remove(coin)
        
        for powerup in powerups[:]:
            powerup.box.y += COIN_V
            if powerup.box.y - COIN_H > HEIGHT:
                powerups.remove(powerup)
            if powerup.box.colliderect(Player):
                l_powerup = powerup.power
                powerups.remove(powerup)

        if hit:
            if lives > 0:
                lives -= 1
                hit = False
                iframes = 120
            else:
                lost_text = FONT.render("You Lost!", 1, 'white')
                WIN.blit(lost_text, (WIDTH/2-lost_text.get_width()/2, HEIGHT/2-lost_text.get_height()/2))
                game_state = "Menu"
                pygame.display.update()
                pygame.time.delay(2000)
                username = ""
                nameput = True
                while nameput:
                    pygame.display.init()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.unicode.isalpha() and len(username) < 20:
                                username += event.unicode
                            elif event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            elif event.key == pygame.K_RETURN:
                                nameput = False
                            elif event.key == pygame.K_ESCAPE:
                                username = " "
                                nameput = False
                                break
                    WIN.blit(BG, (0, 0))
                    hint = FONT.render("Enter Your Username (Press Enter To Save and Escape To Delete The Play)", 1, 'white')
                    name = FONT.render(username, 1, 'white')
                    score_text = FONT.render(f"Score:{score}", 1, 'white')
                    coins_text = FONT.render(f"Coins:{coin_score}", 1, 'white')
                    time_text = FONT.render(f"Time:{int(elapsed)}", 1, 'white')
                    

                    WIN.blit(hint, (WIDTH/2-hint.get_width()/2, 50))
                    WIN.blit(name, (WIDTH/2-name.get_width()/2, HEIGHT/2-name.get_height()/2))
                    WIN.blit(score_text, (WIDTH/2-score_text.get_width()/2, 500))
                    WIN.blit(coins_text, (WIDTH/2-coins_text.get_width()/2, 600))
                    WIN.blit(time_text, (WIDTH/2-time_text.get_width()/2, 700))

                    pygame.display.update()
                if not username.isspace():
                    save_score(username,ship,score,coin_score,elapsed)
                break

        if pause_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(3)[0]:
            game_state = pause()


    
        draw(Player, elapsed, score, stars, bullets, ebullets, enemies, coins, coin_score, pause_button, lives, powerups, l_powerup)
    return game_state

def main():
    run = True
    state = main_menu()

    while run:
        if state == "Menu":
            state = main_menu()

        if state == "Game":
            state = game(state)

        if state == "Quit":
            run = False
        
        if state == "Upgrades":
            state = upgrades()
        
        if state == "Scores":
            state = scores()

    pygame.quit()

if __name__ == "__main__":
    main()
