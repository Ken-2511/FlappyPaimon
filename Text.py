# 这个文件负责管理所有与文字相关的事情

import pygame
from config import *


pygame.font.init()
fp_font = pygame.font.Font("./fonts/zh-cn.ttf", 72)


def flappy_paimon(window: pygame.Surface, bias):
    text = fp_font.render("Flappy Paimon", True, (255, 255, 255))
    rect = text.get_rect()
    rect.left = (WINDOW_SIZE[0] - rect.width) // 2 + bias[0]
    rect.top = (WINDOW_SIZE[1] - rect.height) * 0.618 // 2 + bias[1]
    window.blit(text, rect)


s_font = pygame.font.Font("./fonts/zh-cn.ttf", 32)
s_size = s_font.size("start")
s_original_pos = ((WINDOW_SIZE[0] - s_size[0]) // 2, (WINDOW_SIZE[1] - s_size[1]) * 1.4 // 2)
s_rect = pygame.rect.Rect(s_original_pos, s_size)


def in_start():
    """判断鼠标是否在start文字区域内"""
    pos = pygame.mouse.get_pos()
    return s_rect.left < pos[0] < s_rect.right and s_rect.top < pos[1] < s_rect.bottom


def start(window: pygame.Surface, bias):
    s_rect[:2] = s_original_pos[0] + bias[0], s_original_pos[1] + bias[1]
    if in_start():
        color = (255, 200, 200)
    else:
        color = (255, 255, 255)
    text = s_font.render("start", True, color)
    window.blit(text, s_rect)
