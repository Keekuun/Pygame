import pygame.font
from pygame.sprite import Group
from aliens.plane import Plane


class Score:
    """显示得分的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化得分涉及的属性"""
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 显示得分信息的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始化
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_planes()

    def prep_score(self):
        """将得分转化为渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # 精确到十位数 1000011显示为1,000,000
        score_str = 'Score:{:,}'.format(rounded_score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 0

    def show_score(self):
        """在屏幕上显示分数"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.planes.draw(self.screen)

    def prep_high_score(self):
        """将最高得分转化为渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = 'Record:{:,}'.format(high_score)
        self.high_score_img = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转化为渲染的图像"""
        self.level_str = 'Lv:{}'.format(self.stats.level)
        self.level_img = self.font.render(self.level_str, True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分的下方
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.screen_rect.top + 40

    def prep_planes(self):
        """显示余下游戏次数"""
        self.planes = Group()
        for plane_num in range(self.stats.planes_left):
            plane = Plane(self.ai_settings, self.screen)
            plane.rect.x = plane_num * plane.rect.width + 10
            plane.rect.y = 10
            self.planes.add(plane)
