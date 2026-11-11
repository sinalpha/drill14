import random

from pico2d import *
import game_framework


# ---- 딱따구리 비행 물리 값 -------------------------------------------------
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel = 30 cm (수업 예제와 동일)
FLY_SPEED_KMPH_MIN = 21.0       # 시속 21 ~ 24 km
FLY_SPEED_KMPH_MAX = 24.0


class Bird:
    image = None

    # 스프라이트 시트(918x506) 분할 정보: 5 + 5 + 4 = 14 프레임
    CELL_W = 182
    ROWS = [(0, 170), (170, 170), (340, 166)]  # (위에서부터의 y, 높이)
    FRAMES_PER_ROW = [5, 5, 4]
    SHEET_H = 506
    MARGIN = 45  # 화면 가장자리에서 방향을 바꾸는 여백(px)

    def __init__(self, x=400, y=300, dir=1):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.dir = dir  # +1: 오른쪽, -1: 왼쪽
        # 새마다 21~24 km/h 사이의 속도를 가진다
        self.speed_kmph = random.uniform(FLY_SPEED_KMPH_MIN, FLY_SPEED_KMPH_MAX)
        self.speed_mps = self.speed_kmph * 1000.0 / 3600.0   # 약 5.83 ~ 6.67 m/s
        self.speed_pps = self.speed_mps * PIXEL_PER_METER    # 약 194 ~ 222 px/s
        self.frame = random.uniform(0, 14)  # 새마다 날갯짓 위상을 다르게

    def update(self):
        # 임시 값: 초당 14프레임 (물리 값은 이후 커밋에서 적용)
        self.frame = (self.frame + 14 * game_framework.frame_time) % 14
        self.x += self.dir * self.speed_pps * game_framework.frame_time

        # 가장자리에 닿으면 방향 전환
        right = get_canvas_width() - Bird.MARGIN
        if self.x > right:
            self.x, self.dir = right, -1
        elif self.x < Bird.MARGIN:
            self.x, self.dir = Bird.MARGIN, 1

    def draw(self):
        index = int(self.frame)
        row = 0
        while index >= Bird.FRAMES_PER_ROW[row]:
            index -= Bird.FRAMES_PER_ROW[row]
            row += 1
        top, h = Bird.ROWS[row]
        bottom = Bird.SHEET_H - top - h
        w_dst, h_dst = Bird.CELL_W // 2, h // 2
        if self.dir == 1:  # 시트의 새는 오른쪽을 본다
            Bird.image.clip_draw(index * Bird.CELL_W, bottom, Bird.CELL_W, h,
                                 self.x, self.y, w_dst, h_dst)
        else:  # 왼쪽으로 날 때는 수평 반전
            Bird.image.clip_composite_draw(index * Bird.CELL_W, bottom,
                                           Bird.CELL_W, h, 0, 'h',
                                           self.x, self.y, w_dst, h_dst)
