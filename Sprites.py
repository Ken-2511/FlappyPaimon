# 这个程序用来放置所有的精灵

import pygame
from math import sin
import random
from config import *


class PillarGroup(pygame.sprite.Group):

    def __init__(self, surface, gap):
        super(PillarGroup, self).__init__()
        high_img = pygame.image.load("images/high_tube.png")
        low_img = pygame.image.load("images/low_tube.png")
        self.surface = surface
        self.high_img = high_img
        self.low_img = low_img
        self.gap = gap
        self.last = self.make_new()

    def make_new(self):
        bias = random.randint(50, 300)
        if hasattr(self, "last"):
            left = self.last.rect.left + self.gap
        else:
            left = WINDOW_SIZE[0]
        # make high pillar
        high_pos = (left, -bias)
        high = pygame.sprite.Sprite()
        high.image = self.high_img
        high.rect = pygame.rect.Rect(high_pos, high.image.get_size())
        self.add(high)
        # make low pillar
        low_pos = (left, 520 - bias)
        low = pygame.sprite.Sprite()
        low.image = self.low_img
        low.rect = pygame.rect.Rect(low_pos, low.image.get_size())
        self.add(low)
        return low

    def update(self):
        self.check()
        for sprite in self:
            sprite.rect.left -= BG_DX
            self.surface.blit(sprite.image, sprite.rect)

    def end(self):
        """
        游戏结束后持续刷新最后的图像
        """
        for sprite in self:
            self.surface.blit(sprite.image, sprite.rect)

    def check(self):
        # 在合适的时候杀死对象
        for sprite in self:
            if sprite.rect.right < 0:
                sprite.kill()
        # 在合适的时候创建新的对象
        while self.last.rect.left - BG_DX + self.gap <= WINDOW_SIZE[0]:
            self.last = self.make_new()


class Paimon(pygame.sprite.Sprite):

    def __init__(self):
        super(Paimon, self).__init__()
        # 加载派蒙的图片
        paimon_size = (78, 117)
        self.image1 = pygame.transform.smoothscale(pygame.image.load("images/paimon1.png"), paimon_size)
        self.image2 = pygame.transform.smoothscale(pygame.image.load("images/paimon2.png"), paimon_size)
        self.image3 = pygame.transform.smoothscale(pygame.image.load("images/paimon3.png"), paimon_size)
        self.image4 = pygame.transform.smoothscale(pygame.image.load("images/paimon4.png"), paimon_size)
        self.image = self.image1
        # 设置派蒙的初始位置
        self.ori_pos = ((WINDOW_SIZE[0] - self.image.get_width()) // 2, (WINDOW_SIZE[1] - self.image.get_height()) // 2)
        self.rect = self.image.get_rect()
        self.rect[:2] = self.ori_pos
        self.y_pos = self.rect.top
        self.y_spd = 0

    def jump(self):
        self.y_spd = PAIMON_JUMP_SPD

    def prepare(self, surface, t):
        """
        让派蒙在一定区间内以sin函数的形式上下浮动
        因此速度为cos函数
        """
        self.y_pos = self.ori_pos[1] - sin(3 * t) * 30
        self.rect.top = self.y_pos
        if self.rect.top < self.ori_pos[1]:
            self.image = self.image2
        else:
            self.image = self.image3
        surface.blit(self.image, self.rect)

    def start(self, surface, t):
        self.y_spd += PAIMON_DROP_ACC * TIMESPAN
        self.y_pos += self.y_spd * TIMESPAN
        self.rect.top = self.y_pos
        if self.y_spd < 0:
            self.image = self.image1
        else:
            self.image = self.image2
        surface.blit(self.image, self.rect)

    def end(self, surface, t):
        self.y_spd += PAIMON_DROP_ACC * TIMESPAN
        self.y_pos += self.y_spd * TIMESPAN
        self.rect.top = self.y_pos
        self.image = self.image4
        surface.blit(self.image, self.rect)


class Grass(pygame.sprite.Sprite):

    def __init__(self):
        # 一个循环的长度是113
        super(Grass, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/grass_test.png"), (2000, 100))
        self.size = self.image.get_size()
        self.rect = [0, WINDOW_SIZE[1] - 100, 2000, 100]

    def update(self, surface, t):
        # 草地的图片是重复的，所以只要一张图片在不同位置刷新就行了
        # 这里每次将图片位移一定距离造成草地在向后走的错觉
        self.rect[0] -= BG_DX
        self.rect[0] = self.rect[0] % -113
        surface.blit(self.image, self.rect)

    def end(self, surface, t):
        surface.blit(self.image, self.rect)
