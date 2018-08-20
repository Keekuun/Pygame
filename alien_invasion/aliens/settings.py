import pygame

class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1024
        self.screen_height = 700
        # (R, G, B)
        self.bg_color = (230, 230, 230)
        self.bg = pygame.image.load('images/bg.jpg')
        self.bg_rect = self.bg.get_rect()

        # 飞机设置(速度)
        self.plane_limit = 3

        # 子弹设置
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人的设置
        self.fleet_drop_speed = 5

        # 增加游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人得分增加的速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.plane_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

        # 积分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人得分"""
        self.plane_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
