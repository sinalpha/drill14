from pico2d import *
import game_framework


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
        self.speed_pps = 200  # 임시 값 (px/s)
        self.frame = 0.0

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
