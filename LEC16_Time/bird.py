from pico2d import *


class Bird:
    image = None

    def __init__(self, x=400, y=300):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        # 시트(918x506)의 첫 프레임: 182x170, 위에서 0 -> 아래 기준 y = 506 - 0 - 170
        Bird.image.clip_draw(0, 336, 182, 170, self.x, self.y)
