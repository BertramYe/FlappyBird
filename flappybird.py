import pygame
import random
from pygame.font import Font,SysFont

class Bird(object):
    """ 定义一个鸟类 """

    def __init__(self):
        """ 鸟的一些初始化参数 """
        self.bird_default_rect = pygame.Rect(65,50,40,30)   # 鸟的矩形，自身占用的活动范围(只是默认的初始化值)
        # 鸟的几种状态， 包括jump，fly和dead
        self.bird_status = [
            pygame.image.load(r".\assets\0.png"),  # 初始形态            
            pygame.image.load(r".\assets\1.png"),  # 煽动翅膀一形态            
            pygame.image.load(r".\assets\2.png"),  # 扇动翅膀二形态            
            pygame.image.load(r".\assets\dead.png"),   # dead形态            
        ]

        # 自定义一个索引列表来获得小鸟真正的状态，默认0表示初始状态
        self.bird_status_code = 0
        # 小鸟的初始坐标
        self.birdX = 120     # X 轴
        self.birdY = 350     # Y 轴
        # 小鸟是否做了跳跃
        self.bird_jump_or_not = False
        # 默认跳跃高度
        self.bird_jump_speed = 15
        # 默认下坠速度,（死亡时不会下坠,此时速度可以修改为 0 ）
        self.bird_gravity = 1
        # 小鸟是否死亡
        self.bird_dead_or_not = False

    def update_bird(self):
        """ 更新小鸟状态，包括位置，飞行姿态等 """
        # 小鸟jump的速度逻辑（越低离Y轴越远）
        if not self.bird_dead_or_not:
            if  self.bird_jump_or_not:
                # print("jump的行为已经被激发")
                # if self.bird_jump_speed > 1:
                self.bird_jump_speed -= 1    # 上升速度依次递减
                self.birdY  -= self.bird_jump_speed
            else:
                self.bird_gravity  += 0.2    # 坠落速度依次递增
                self.birdY   += self.bird_gravity
        else:
            # 小鸟死亡，不会jump，也不会下坠
            self.bird_jump_or_not = False
            self.bird_gravity = 0

        
class Pipple(object):
    """ 定义一个管道类，用来封装管道的属性和功能 """
    def  __init__(self):
        # 管道的初始化坐标，暂时写定值，
        # 之后还可以增加游戏的趣味性，设置不定值用random修改
        self.up_wallx = 200
        self.up_wally = -200
        self.up_pipple = pygame.image.load(r".\assets\top.png")   # 上管道
        self.up_pipple_score = 0            # 通过上管道得分
        # self.up_piple_reset = False        # 上管道是否重置
        self.bird_get_up_pipple_score = False    # 小鸟是否拿到下管道分数

        self.down_wallx = 400
        self.down_wally = 600
        self.down_pipple = pygame.image.load(r".\assets\bottom.png") # 下管道
        self.down_pipple_score = 0         # 通过下管道得分
        # self.down_piple_reset = False     # 下管道是否重置
        self.bird_get_down_pipple_score = False    # 小鸟是否拿到下管道分数

        # 小鸟死亡，管道将不会继续更新，故此时再定义一个bool值，用来控制小鸟死亡时的管道状态
        self.up_pipple_update = True
        self.down_pipple_update = True

        
    def update_up_pipple(self):
        """ 上管道的水平移动  """
        
        # 这里暂时设置为默认值 表示管道移动的速度，当小鸟没有死亡时，移动速度就开始以5像素移动
        # 之后也可以利用random去做随机处理，增加游戏的趣味性
        if self.up_pipple_update:
            self.up_wallx -= 5 

        # 设置小鸟得分,小鸟飞跃管道,并且当管道消失时，分数加 1，并且重置管道（80为管道宽度）
        if ( self.up_wallx - 120 < -98) and not self.bird_get_up_pipple_score :
            # 小鸟已经穿过，还没有得分的话，此时应该开始得分
            self.up_pipple_score = 1
            self.bird_get_up_pipple_score = True
            
        if  (self.up_wallx < -98) and (self.bird_get_up_pipple_score):
            # 如果小鸟已经穿过，并且得分，此时管道开始从窗口消失，将会重置
            self.up_wallx = 200 + 400  # 加的是显示的宽度，这样会使得管道出现得更自然
            self.up_wally = random.randint(-500,-100)  # 游戏的上下伸出部分可以随意设计
            # 重置1管道后小鸟需要重新通过，重新得分故而需要重新复位
            self.bird_get_up_pipple_score = False
            
        

    def update_down_pipple(self):
        """ 下管道水平移动  """
        if self.down_pipple_update:
            self.down_wallx -= 5
        # 得1分 暂时这么设计，在这里面也可以根据小鸟通过的难度设计score的值
        if (self.down_wallx - 120 < -100) and not self.bird_get_down_pipple_score:
            self.down_pipple_score = 1
            self.bird_get_down_pipple_score = True
        
        # 达到一定条件将重置管道
        if (self.down_wallx < -100) and self.bird_get_down_pipple_score:
            self.down_wallx = 400 + 400
            self.down_wally = random.randint(400,700)
            self.bird_get_down_pipple_score = False
        

   
def  create_map(game_windows,backgroud_picture,bird,pipples):
    """ 创建地图：画游戏的背景以及相关游戏场景  """
    # 背景图片
    game_windows.blit(backgroud_picture,(0,0))
    # game_windows.blit(backgroud_picture,(398,0))  # 这样可以将屏幕变大  
    # 小鸟的状态
    # 不断更新小鸟状态
    if bird.bird_dead_or_not:   # 小鸟死亡
        bird.bird_status_code = 3
        # print("小鸟已经死亡,游戏结束！")
        game_windows.blit(bird.bird_status[bird.bird_status_code],(bird.birdX,bird.birdY))
        game_windows.blit(pipples.up_pipple,(pipples.up_wallx,pipples.up_wally))   # 上管道
        game_windows.blit(pipples.down_pipple,(pipples.down_wallx,pipples.down_wally))   # 下管道
        pygame.display.update()
    else:
        bird.update_bird()  # 每次状态的转变，小鸟都要飞一遍
        for i in range(0,3):   # 小鸟在飞翔(不改变自身的位置，可以减少重影)
            bird.bird_status_code = i
            # print(bird.bird_status_code)
            game_windows.blit(backgroud_picture,(0,0))  # 为了减小鸟自身由于飞翔造成的重影，每次画背景时将小鸟重新再画一遍
            # game_windows.blit(backgroud_picture,(398,0))   # 这样可以将屏幕变大
            game_windows.blit(bird.bird_status[bird.bird_status_code],(bird.birdX,bird.birdY))
            # 显示管道(与小鸟飞翔时间同步，可以减少障碍的重影)
            game_windows.blit(pipples.up_pipple,(pipples.up_wallx,pipples.up_wally))   # 上管道
            game_windows.blit(pipples.down_pipple,(pipples.down_wallx,pipples.down_wally))   # 下管道
            # 这一行很重要，因为如果不加，小鸟没办法体现飞的状态
            # 并且不要单独拿出来，因为这个逻辑在for循环里面，如果单独拿出来，就体现不出小鸟的飞行状态
            pygame.display.update()  

    # 每点击一次但小鸟更新完状态后，就需要将小鸟跳跃动作复位
    bird.bird_jump_or_not = False
   
def check_bird_dead_or_not(pipples,game_windows,bird):
    """ 检查小鸟是否死亡 """
    # 获取管道的矩形位置信息,Rect(创建矩形区域的时候，是按照 left,top,width,height的顺序 )
    # 上管道   
    # （注意我将得到的图片的width - 10 是为了贴合小鸟本身图片会有部分边缘，故而将 pipple 自身的真实宽度减小，从而形成玩游戏，小鸟装机过程中的更加真实）
    up_pipple_rect = pygame.Rect(pipples.up_wallx,pipples.up_wally,pipples.up_pipple.get_width() - 10,pipples.up_pipple.get_height())
    # print(f"up_pipples_rect:{up_pipple_rect},{bird.bird_rect}")
    # 下管道 
    # (下管道与上管道一样，将得到的图片的width - 10)
    down_pipple_rect = pygame.Rect(pipples.down_wallx,pipples.down_wally,pipples.down_pipple.get_width() - 10,pipples.down_pipple.get_height())
    
    # 获取小鸟的动态的矩形信息，并创建对应的对象
    # bird_rect = pygame.Rect(bird.birdX,bird.birdY,40,30)
    # 此时先通过get_rect()方法获取bird 图片真正的宽高信息，然后利用Rect()重新实例化为Rect对象，减少实际的参数配置，使得游戏后期修改可靠更高
    bird_rect_arg = bird.bird_status[bird.bird_status_code].get_rect()
    bird_rect = pygame.Rect(bird.birdX,bird.birdY,bird_rect_arg[2],bird_rect_arg[3])
    
    # 检测小鸟与上下管子是否碰撞
    if up_pipple_rect.colliderect(bird_rect):
        bird.bird_dead_or_not = True
        # print(f"pop happend,up_pipples_rect:{up_pipple_rect},{bird.bird_rect}")
        # sys.exit()
    if  down_pipple_rect.colliderect(bird_rect):
        bird.bird_dead_or_not = True
        # print(f"down_pipple_rect:{down_pipple_rect},{bird.bird_rect}")
        # sys.exit()

    # 检测小鸟是否飞出边界
    if not game_windows.get_rect().contains(bird_rect):
        bird.bird_dead_or_not = True
       

def show_score(score,game_windows,bird):
    """ 根据小鸟不同的状态打印对应的分数，打印最终成绩 """
    if bird.bird_dead_or_not:
        # 当小鸟死亡时
        final_text_one = "Game Over!"
        final_text_two = f"Your Final Score is : {score} !"
        final_text_one_format = SysFont("Arial",70)    # 第一行字体格式
        final_text_two_format = SysFont("Arial",40)
        final_text_one_render = Font.render(final_text_one_format,final_text_one,1,(242,3,36))
        final_text_two_render = Font.render(final_text_two_format,final_text_two,1,(253,177,6))
        # 设置第一行文字显示位置
        game_windows.blit(final_text_one_render, [game_windows.get_width()/2 - final_text_one_render.get_width()/2,120] )
        # 设置第二行文字显示位置
        game_windows.blit(final_text_two_render, [game_windows.get_width()/2 - final_text_two_render.get_width()/2,200] )
    else:
        # 当小鸟没死时
        game_windows.blit(Font.render(SysFont("Arial",70),str(score),-1,(255,255,255)),(200,50))
    pygame.display.update()

