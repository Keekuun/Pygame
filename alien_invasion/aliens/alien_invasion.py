#!/usr/bin/env/python36
# -*- coding:utf-8 -*-
# author: Keekuun
import pygame
from pygame.sprite import Group
from aliens.settings import Settings
from aliens.plane import Plane
import aliens.game_functions as gf
from aliens.game_stats import GemeStats
from aliens.button import Button
from aliens.score import Score


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 标题
    pygame.display.set_caption('外星人入侵')

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    # 创建用于存储游戏统计信息的实例
    stats = GemeStats(ai_settings)

    # 创建记分牌
    score = Score(ai_settings, screen, stats)

    # 创建一架飞机
    plane = Plane(ai_settings, screen)

    # 创建用于存储的编组
    aliens = Group()
    bullets = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, plane, aliens)

    # 创建按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 开始循环游戏的主程序
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, score, play_button, plane, aliens, bullets)

        if stats.game_active:
            # 每次循环时都重复绘制(R,G,B)
            plane.update()
            gf.update_bullets(ai_settings, screen, stats, score, plane, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, score, plane, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, score, plane, aliens, bullets, play_button)


run_game()
