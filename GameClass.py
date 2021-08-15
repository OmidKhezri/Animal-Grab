import random
import Public


class Animal:
    def __init__(self, _pos_x, _pos_y):
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.size = Public.animal_size
        self.pic = random.randint(10, 50)
        self.grab = 0
        self.delta_x = 0
        self.delta_y = 0

        while self.delta_x == 0 and self.delta_y == 0:
            self.delta_x = random.randint(-1 * Public.animal_speed, Public.animal_speed)
            self.delta_y = random.randint(-1 * Public.animal_speed, Public.animal_speed)

    def calc_new_pos(self):
        self.pos_x += self.delta_x
        self.pos_y += self.delta_y

    def is_click_contain(self, _click_pos_x, _click_pos_y):
        if self.pos_x <= _click_pos_x <= self.pos_x + self.size and self.pos_y <= _click_pos_y <= self.pos_y + self.size:
            self.grab = 1
            return True
        else:
            return False


class Animals:
    def __init__(self):
        self.animals_list = []

    def get_all_animals(self) -> [Animal]:
        return self.animals_list
