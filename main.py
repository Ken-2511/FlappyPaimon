# 这是程永康在2022年4月16日开始编写的FlappyPaimon程序
# 这个程序是为了改进之前写的。因为觉得之前写的程序有点乱，所以想改得更有条理一点
# 希望在这个程序编写好之后我还能编写出一个会玩这个游戏的人工智能。
# 加油，尽自己所能编写吧。加油，康康！
# 4月20日：放弃变换的窗口大小了，放弃调速了，把这两项写死
# 5月1日，要把游戏开始和重来界面做好
# 5月2日，改进消息机制，更换派蒙图片
# 5月8日，要将游戏掉帧的原因找出来
# 2023年4月12日，把地面的贴图合成一个，规范化代码，增加了config文件

import pygame
from pygame import mixer
import sys
import Sprites
import Text
from config import *

pygame.init()

# initialize window
icon = pygame.image.load("GenshinImpact.ico")
pygame.display.set_icon(icon)
pygame.display.set_caption("Flappy Paimon")
window = pygame.display.set_mode(WINDOW_SIZE)

# load music
mixer.music.load("music/bg_music.mp3")
mixer.music.set_volume(MUSIC_VOLUME)
jump = mixer.Sound("music/jump.wav")
jump.set_volume(MUSIC_VOLUME)
hit = mixer.Sound("music/hit.mp3")
hit.set_volume(MUSIC_VOLUME)

# load sprites
paimon = Sprites.Paimon()
pillars = Sprites.PillarGroup(window, 300)
grass = Sprites.Grass()


# other vars
class TimeManager:
    # 其实pygame.time.Clock有这个功能
    # 一个用于游戏计时的类，通过逐帧累加精确计时
    def __init__(self):
        self.count = 0

    def get_time(self):
        return self.count * TIMESPAN

    def step(self):
        self.count += 1


time_manager = TimeManager()
clock = pygame.time.Clock()


def greeting():
    run = True
    while run:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Text.in_start():
                    run = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 画
        window.fill((0, 0, 0))
        pos = pygame.mouse.get_pos()
        bias = (-(pos[0] - WINDOW_SIZE[0] // 2) // 20, -(pos[1] - WINDOW_SIZE[1] // 2) // 20)
        Text.flappy_paimon(window, bias)
        Text.start(window, bias)
        pygame.display.flip()
        clock.tick(FPS)


def prepare():
    mixer.music.play()
    run = True
    while run:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    jump.play()
                    paimon.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                jump.play()
                paimon.jump()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 画
        window.fill((130, 150, 200))
        t = time_manager.get_time()
        paimon.prepare(window, t)
        grass.update(window, t)
        pygame.display.flip()
        time_manager.step()
        clock.tick(FPS)


def start():
    run = True
    while run:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump.play()
                    paimon.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                jump.play()
                paimon.jump()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 画
        window.fill((130, 150, 200))
        t = time_manager.get_time()
        pillars.update()
        paimon.start(window, t)
        grass.update(window, t)
        # noinspection PyTypeChecker
        check1 = pygame.sprite.spritecollideany(paimon, pillars, pygame.sprite.collide_rect_ratio(0.8))
        # noinspection PyTypeChecker
        check2 = pygame.sprite.collide_rect(paimon, grass)
        if check1 or check2:
            hit.play()
            paimon.kill()
            run = False
        pygame.display.flip()
        time_manager.step()
        clock.tick(FPS)


def end():
    mixer.music.stop()
    while paimon.rect.bottom <= WINDOW_SIZE[1] - grass.size[1]:
        paimon.image.get_masks()
        window.fill((130, 150, 200))
        pillars.end()
        t = time_manager.get_time()
        paimon.end(window, t)
        grass.end(window, t)
        pygame.display.flip()
        time_manager.step()
        clock.tick(FPS)
    pygame.time.delay(800)


if __name__ == '__main__':
    prepare()
    start()
    end()
    pygame.quit()
