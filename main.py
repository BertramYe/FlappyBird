import flappybird
import pygame
import sys
from pygame.font import Font,SysFont
"""  主程序文件 """


if __name__ == "__main__":
    """ 程序执行调用入口  """
    pygame.init()     # 初始化游戏
    size = width,height = 400,680   # 设置游戏窗体的大小
    game_windows = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()     # 设定一个计时器，用来调整轮询的间隙
    backgroud_picture = pygame.image.load(r"assets\background.png")  # 加载背景图片
    # 实例化一个小鸟对象
    bird = flappybird.Bird()
    # 实例化管道对象，为后面画管道做准备
    pipples = flappybird.Pipple()
    # 设置全局变量，用于计算小鸟得分
    score = 0    
    # 用while来操作轮询
    while True:
        clock.tick(20)  # 每秒钟执行5次轮询
        # 创建轮询，用来设置程序的退出动作
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 以下为用户操作的逻辑(如果用户按的空格键或者按下鼠标,并且小鸟还没死的话，小鸟向上跳跃)
            if ((ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE ) or ev.type == pygame.MOUSEBUTTONDOWN) and not bird.bird_dead_or_not:
                bird.bird_jump_or_not = True
                # 初始化跳跃速度
                bird.bird_jump_speed = 15      # 每次鼠标重新点击、或者按键都会给其一个初始化的改变
                # 初始化下坠速度（将下坠速度复原）
                bird.bird_gravity = 1  
        
        flappybird.check_bird_dead_or_not(pipples,game_windows,bird)
        # 如果不退出就有如下动作
        # 创建游戏背景图（包括画小鸟的飞行姿态）
        flappybird.create_map(game_windows,backgroud_picture,bird,pipples)
        # 显示管道(与小鸟飞翔时间同步，可以减少障碍的重影)
        # 当然，前提是小鸟没死
        if not bird.bird_dead_or_not:
            # 计算小鸟得分
            # 上管道
            pipples.update_up_pipple()
            if pipples.bird_get_up_pipple_score:
                score += pipples.up_pipple_score
                pipples.up_pipple_score = 0        # 计算完得分，将分数重新复位
            
            # 下管道
            pipples.update_down_pipple()
            if pipples.bird_get_down_pipple_score:
                score += pipples.down_pipple_score
                pipples.down_pipple_score = 0
        
        # 显示得分
        flappybird.show_score(score,game_windows,bird)
        
            
    
        
       

        



        

       







                

