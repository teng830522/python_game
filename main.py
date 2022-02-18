#操作 sprite
from winreg import REG_OPTION_BACKUP_RESTORE
import pygame #導入遊戲模組
import random #導入隨機模組
import os #導入作業系統操作呼叫模組

#宣告變數
FPS = 60
WHITE = (255,255,255)
WIDTH = 500
HEIGHT = 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0 , 255)

pygame.init() #遊戲初始化
pygame.mixer.init() #音樂初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #宣告視窗長寬
pygame.display.set_caption("太空生存戰") #設定視窗名稱
clock = pygame.time.Clock() #宣告變數為 遊戲模組跟蹤時間

#載入圖片 再用.convert()轉換成pygame容易讀取的格式 *需要先初始化遊戲*
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() #os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img) #設定視窗名稱
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_imgs = [] #石頭有7種 因此宣告物件為陣列
for i in range(7): #執行 7次迴圈, 變數i 帶入執行次數 
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert()) #新增圖片到陣列內, 在字串前面加上f 後面方可加上變數
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (74, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    play_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    play_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(play_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()

#載入音樂,音效
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))#os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))#os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))#os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))#os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")) ,#os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav")) #os.path.join為 呼叫作業系統 取出相對位置(資料夾位置,檔案名稱) 
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg")) #帶入背景聲音
pygame.mixer.music.set_volume(0.4) #降低背景聲音

#font_name = pygame.font.match_font('arial') #尋找電腦內要導入的字體
font_name = os.path.join("font.ttf") #設定中文字
def draw_text(surf, text, size, x, y): #新增涵式(要帶入的資料)
    font = pygame.font.Font(font_name, size) #創建一個文字的物件
    text_surface = font.render(text , True, WHITE)
    text_rect = text_surface.get_rect() #文字定位
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0 :
        hp = 0
    BAR_LENGTH = 100 #生命條長度
    BAR_HETGHT = 10 #生命條高度
    fill = (hp/100) * BAR_LENGTH #剩餘生命
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HETGHT) #宣告外部矩形的屬性
    fill_rect = pygame.Rect(x, y, fill, BAR_HETGHT) #宣告內部矩形的屬性
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2) #第四個參數為外框

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0)) #設定背景圖片 (R,G,B)
    draw_text(screen, '太空生存戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← → 移動飛船 空白鍵發射飛彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '案任意鍵開始遊戲', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting :
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():   #迴圈 當按下關閉視窗關閉迴圈
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite): #創建Player類別 繼承 pygame內建Sprite類別
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self) #初始化內建涵式, 生成 image & rect
        #self.image = pygame.Surface((50, 40))
        self.image = pygame.transform.scale(player_img, (50, 38)) #將玩家圖片 修改(寬度,長度) 帶入變數
        self.image.set_colorkey(BLACK) #圖片中去除指定顏色
        self.rect = self.image.get_rect() #將image 加外框
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2 #設定rect 的x座標
        self.rect.bottom = HEIGHT - 10 #設定rect 的y座標
        self.speedx = 8 #設定按下鍵盤 物件x座標變化幅度
        self.health = 100 #宣告玩家生命
        self.live = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000 :
            self.gun -= 1
            self.gun_time = now

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2 #設定rect 的x座標
            self.rect.bottom = HEIGHT - 10 #設定rect 的y座標

        key_pressed = pygame.key.get_pressed() #先告變數為 鍵盤上按鍵回傳的布林值為陣列
        if key_pressed[pygame.K_LEFT]: #當按下a時 rect的 x座標扣除先前宣告的變數
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_RIGHT]: #當按下d時 rect的 x座標增加先前宣告的變數
            self.rect.x += self.speedx
        #self.rect.x += 2 #將rect設定x座標+2 執行後會因為迴圈持續增加
        if self.rect.right > WIDTH: #設定 rect 右邊界超過畫面時, 鎖定數值
            self.rect.right = WIDTH
        if self.rect.left < 0: #設定 rect 左邊界超過畫面時, 鎖定數值
            self.rect.left = 0
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1 :
                bullet = Bullet(self.rect.centerx, self.rect.top) #執行 Bullet類別 帶入子彈要生成x,y座標數值, 產生子彈圖片物件
                all_sprites.add(bullet) #新增子彈物件到全部群組中
                bullets.add(bullet) #新增子彈物件到子彈群組中
                shoot_sound.play()
            elif self.gun >=2 :
                bullet1 = Bullet(self.rect.left, self.rect.centery) #執行 Bullet類別 帶入子彈要生成x,y座標數值, 產生子彈圖片物件
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1) #新增子彈物件到全部群組中
                all_sprites.add(bullet2) #新增子彈物件到全部群組中
                bullets.add(bullet1) #新增子彈物件到子彈群組中
                bullets.add(bullet2) #新增子彈物件到子彈群組中
                shoot_sound.play()
    def hide (self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite): #創建Rock 繼承 內建類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call 內建初始涵式 共兩個屬性 image & rect
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(RED)
        self.image_ori = random.choice(rock_imgs) #隨機取出石頭物件裡的圖片
        self.image_ori.set_colorkey(BLACK) #去除圖片顏色
        #self.image_ori = rock_img
        self.image = self.image_ori.copy() #複製取出的石頭圖片
        self.rect = self.image.get_rect() #將image 的變數加外框
        self.radius = int(self.rect.width * 0.85 / 2)   #判定子彈石頭碰撞 宣告半徑為物件寬度除2
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)  #宣告物件生成的 座標x 
        self.rect.y = random.randrange(-180 , -100) #宣告變數生成的 座標y 
        self.speedx = random.randrange(-3 , 3) #宣告變數 座標x 向左或右移動 , 隨機增加減少-3 ~ 3 的值 
        self.speedy = random.randrange(2 , 5) #宣告變數 座標y 向下移動 , 隨機增加2 ~ 5 的值 
        self.total_degree = 0 #宣告石頭目前旋轉的角度
        self.rot_degree = random.randrange(-3 , 3) #宣告石頭增加旋轉的角度 , 隨機增加減少-3 ~ 3 的值 

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()  
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100 , -40)
            self.speedx = random.randrange(-3 , 3)
            self.speedy = random.randrange(2 , 10)

class Bullet(pygame.sprite.Sprite): #創建Bullet 繼承 內建類別
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #call 內建初始涵式 共兩個屬性 image & rect
        #self.image = pygame.Surface((10, 20))
        #self.image.fill(BLUE)
        self.image = bullet_img
        self.image.set_colorkey(BLACK) #去除圖片顏色
        self.rect = self.image.get_rect() #將變數 的圖片加外框
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy   
        if self.rect.bottom < 0:
            self.kill()     

class Explosion(pygame.sprite.Sprite): #創建Bullet 繼承 內建類別
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self) #call 內建初始涵式 共兩個屬性 image & rect
        self.size= size
        self.image = expl_anim[self.size][0]
        self.image.set_colorkey(BLACK) #去除圖片顏色
        self.rect = self.image.get_rect() #將變數 的圖片加外框
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks() #初始化到現在的毫秒數
        self.frame_rate = 50 #設定播放圖片間格的毫秒數

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()     
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite): #創建Bullet 繼承 內建類別
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self) #call 內建初始涵式 共兩個屬性 image & rect
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK) #去除圖片顏色
        self.rect = self.image.get_rect() #將變數 的圖片加外框
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy   
        if self.rect.top > HEIGHT:
            self.kill()     

pygame.mixer.music.play(-1)

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group() #創建全部的群組 
        rocks = pygame.sprite.Group() #創建石頭的群組 
        bullets = pygame.sprite.Group() #創建子彈的群組 
        powers = pygame.sprite.Group() #創建火力的群組
        player = Player() #宣告變數繼承 設定好的類別
        all_sprites.add(player) #將玩家圖片加入到全部群組內  
        for i in range(8):    
            new_rock()
        score = 0 #宣告分數為0
        
    #設定迴圈1s/60次數
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():   #迴圈 當按下關閉視窗關閉迴圈
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #更新遊戲
    all_sprites.update() #執行"群組"內每一個物件的update涵式
    #判斷石頭 子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) #當子彈碰到石頭 刪除子彈及石頭 
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius #將石頭半徑加到分數上
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9 : 
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    #判斷石頭 飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits :
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_rock()
        if player.health <= 0 :
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.live -= 1
            player.health = 100
            player.hide()
            # running = False

    #判斷寶物 飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True, )
    for hit in hits :
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun' :
            player.gunup() 
            gun_sound.play()       

    if player.live == 0 and not(death_expl.alive()): #且die 完成不存在時, 在執行關閉
        show_init = True

    #畫面顯示
    screen.fill(WHITE) #設定畫面顏色 (R,G,B)
    screen.blit(background_img, (0,0)) #設定背景圖片 (R,G,B)
    all_sprites.draw(screen) # 將all_sprites 畫到畫面上
    draw_text(screen, str(score), 18, WIDTH/2 , 10)
    draw_health(screen, player.health, 5 , 15)
    draw_lives(screen, player.live, player_mini_img, WIDTH - 100, 15)
    pygame.display.update() #更新畫面

pygame.quit()