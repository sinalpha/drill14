from pico2d import *
import game_framework


class Bird:
    image = None

    # 스프라이트 시트(918x506) 분할 정보: 5 + 5 + 4 = 14 프레임
    CELL_W = 182
    ROWS = [(0, 170), (170, 170), (340, 166)]  # (위에서부터의 y, 높이)
    FRAMES_PER_ROW = [5, 5, 4]
    SHEET_H = 506

    def __init__(self, x=400, y=300):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0

    def update(self):
        # 임시 값: 초당 14프레임 (물리 값은 이후 커밋에서 적용)
        self.frame = (self.frame + 14 * game_framework.frame_time) % 14

    def draw(self):
        index = int(self.frame)
        row = 0
        while index >= Bird.FRAMES_PER_ROW[row]:
            index -= Bird.FRAMES_PER_ROW[row]
            row += 1
        top, h = Bird.ROWS[row]
        bottom = Bird.SHEET_H - top - h
        Bird.image.clip_draw(index * Bird.CELL_W, bottom, Bird.CELL_W, h,
                             self.x, self.y)
