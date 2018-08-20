import sys
import pygame
from aliens.bullet import Bullet
from aliens.alien import Alien
from time import sleep


# 当按钮被按下
def check_keydown_events(event, ai_settings, screen, plane, bullets):
    # 向右移动
    if event.key == pygame.K_RIGHT:
        plane.moving_right = True
    # 向左移动
    elif event.key == pygame.K_LEFT:
        plane.moving_left = True
    # 空格发射子弹
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, plane, bullets)
    # ESC退出
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


# 当按钮被释放
def check_keyup_events(event, ai_settings, screen, plane, bullets):
    # 停止向右移动
    if event.key == pygame.K_RIGHT:
        plane.moving_right = False
    # 停止向左移动
    elif event.key == pygame.K_LEFT:
        plane.moving_left = False


def check_events(ai_settings, screen, stats, score, play_button, plane, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 开始移动
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, plane, bullets)
        # 停止移动
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, plane, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score, play_button, plane, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, score, play_button, plane, aliens, bullets, mouse_x, mouse_y):
    """在玩家点击play按钮时开始游戏"""
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        # 重置游戏的设置
        ai_settings.increase_speed()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        score.prep_level()
        score.prep_score()
        score.prep_high_score()
        score.prep_planes()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()


def update_screen(ai_settings, screen, stats, score, plane, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重复绘制
    screen.blit(ai_settings.bg, ai_settings.bg_rect)

    # 在飞机和外星后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    plane.blitme()
    aliens.draw(screen)
    # 显示得分
    score.show_score()
    # 如果游戏处于非活动状态，就会之Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, score, plane, aliens, bullets):
    """更新子弹的位置，并删除已经消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, score, plane, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, score, plane, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的外星人和子弹
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score.prep_score()
        check_high_score(stats, score)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        # 消灭完外星人等级提高
        stats.level += 1
        score.prep_level()

        create_fleet(ai_settings, screen, plane, aliens)


def check_high_score(stats, score):
    """检查是否诞生了新的最高分数"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()


def fire_bullet(ai_settings, screen, plane, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, plane)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳外星人个数"""
    available_space_x = ai_settings.screen_width - alien_width * 2
    number_aliens_x = int(available_space_x / (alien_width * 2))
    return number_aliens_x


def get_number_aliens_y(ai_settings, plane_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - plane_height)
    number_aliens_y = int(available_space_y / (alien_height * 2))
    return number_aliens_y


def create_alien(ai_settings, screen, aliens, alien_number_x, number_alien_y):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * alien_number_x * 2
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + alien.rect.height * number_alien_y * 2
    aliens.add(alien)


def create_fleet(ai_settings, screen, plane, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳几个
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_aliens_y = get_number_aliens_y(ai_settings, plane.rect.height, alien.rect.height)

    # 创建外星人
    for number_alien_x in range(number_aliens_x):
        for number_alien_y in range(number_aliens_y):
            create_alien(ai_settings, screen, aliens, number_alien_x, number_alien_y)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def plane_hit(ai_settings, screen, stats, score, plane, aliens, bullets):
    """响应被外星人撞到的飞机"""
    if stats.planes_left > 0:
        # 将plane_left减少1
        stats.planes_left -= 1
        # 更新记分牌
        score.prep_planes()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞机放到屏幕中间
        create_fleet(ai_settings, screen, plane, aliens)
        plane.center_plane()

        # 暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, score, plane, aliens, bullets):
    """检测是否有外星人到达了屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 向飞机被撞到一样处理
            plane_hit(ai_settings, screen, stats, score, plane, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, score, plane, aliens, bullets):
    """检测是否有外星人到达屏幕的边缘
    然后更新外星人群中的所有外星人的位置"""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞机之间的碰撞
    if pygame.sprite.spritecollideany(plane, aliens):
        # print('shit hit!!!')
        plane_hit(ai_settings, screen, stats, score, plane, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, score, plane, aliens, bullets)
