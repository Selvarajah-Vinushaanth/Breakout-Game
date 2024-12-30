import pygame

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(80,175,90)
BLUE=(60,160,200)

pygame.init()
WIDTH=700
HEIGHT=700
FPS=60
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Breakout Game")
clock=pygame.time.Clock()

COLS=10
ROWS=6

class PADDLE:
    def __init__(self):
        self.height=20
        self.width=int(WIDTH/COLS)
        self.x=int(WIDTH/2)-int(self.width/2)
        self.speed=10
        self.y=int(HEIGHT)-20
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
    def draw_paddle(self):
        pygame.draw.rect(win,WHITE,self.rect)
    def move_paddle(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left >0:
            self.rect.x -=self.speed
        if key[pygame.K_RIGHT] and self.rect.right <WIDTH:
            self.rect.x +=self.speed

paddle=PADDLE()


class BALL:
    def __init__(self,x,y):
        self.radius=10
        self.x=x-self.radius+8
        self.y=y-10
        self.dx=3
        self.dy=-3
        self.rect=pygame.Rect(self.x,self.y,self.radius**2,self.radius*2)
        self.game_status=0
    def draw_ball(self):
        pygame.draw.circle(win,BLUE,(self.rect.x,self.rect.y),self.radius)
    def move_ball(self):
        if self.rect.right>WIDTH+90:
            self.dx *=-1
        if self.rect.left <10:
            self.dx *=-1
        if self.rect.top <10:
            self.dy *=-1
        if self.rect.bottom>HEIGHT:
            self.game_status=-1
        self.rect.x+=self.dx
        self.rect.y+=self.dy
        if paddle.rect.colliderect(self.rect):
            self.dy *=-1
            sound=pygame.mixer.Sound("mixkit-martial-arts-fast-punch-2047.wav")
            sound.play()
        all_done = True
        row_no=0
        for row in brick_wall.bricks:
            col_no=0
            for br in row:
                if self.rect.colliderect(br):
                    sound_coll=pygame.mixer.Sound("mixkit-winning-a-coin-video-game-2069.wav")
                    sound_coll.play()
                    brick_wall.bricks[row_no][col_no]=(0,0,0,0)
                    if abs(self.rect.bottom - br.top) <5:
                        self.dy *=-1
                    if abs(self.rect.top -br.bottom)<5:
                        self.dy *=-1
                    if abs(self.rect.left -br.right)<5:
                        self.dx *=-1
                    if abs(self.rect.right -br.left)<5:
                        self.dx *=-1
                if  brick_wall.bricks[row_no][col_no]!=(0,0,0,0):
                    all_done=False

                col_no+=1
            row_no+=1
            if all_done :
                self.game_status=1
        return self.game_status

ball=BALL((paddle.x+paddle.width/2),(HEIGHT-paddle.height-10))


class BRICK:
    def __init__(self):
        self.width=int(WIDTH/COLS)
        self.height=30
    def create_bricks(self):
        self.bricks=[]
        for row in range(ROWS):
            bricks_row=[]
            for col in range(COLS):
                brick_x=col*self.width
                brick_y=row*self.height
                br=pygame.Rect(brick_x,brick_y,self.width,self.height)
                bricks_row.append(br)
            self.bricks.append(bricks_row)
    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(win,GREEN,br)
                pygame.draw.rect(win,BLACK,br,2)


brick_wall=BRICK()
brick_wall.create_bricks()





run = True
while run:
    win.fill(BLACK)
    paddle.draw_paddle()
    paddle.move_paddle()
    ball.draw_ball()
    game_status=ball.move_ball()
    brick_wall.draw_bricks()
    if game_status==-1:
        win.fill(BLACK)
        font=pygame.font.SysFont(None,50)
        text=font.render("Game Over",True,BLUE)
        text_rect=text.get_rect(center=(WIDTH/2,HEIGHT/2))
        win.blit(text,text_rect)
    if game_status==1:
        win.fill(BLACK)
        font=pygame.font.SysFont(None,50)
        text=font.render("You Won",True,BLUE)
        text_rect=text.get_rect(center=(WIDTH/2,HEIGHT/2))
        win.blit(text,text_rect)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()