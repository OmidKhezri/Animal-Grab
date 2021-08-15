import Public
import GameClass
import random

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition, FadeTransition
from kivy.uix.label import Label, CoreLabel
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

root = ScreenManager()


class SettingWindow(Screen):
    def __init__(self):
        super().__init__()
        self.name = "SettingWindow"
        self.canvas.add(Rectangle(source="pics\\Setting_Background.png", pose=(0, 0), size=(Window.width, Window.height)))
        self.add_widget(Label(text="Easy", font_size=50, pos_hint={"x": .1, "y": .5}, size_hint=(.1, .1)))
        self.add_widget(Label(text="Hard", font_size=50, pos_hint={"x": .8, "y": .5}, size_hint=(.1, .1)))
        self.HardnessPicker = Slider(pos_hint={"x": .25, "y": .48}, size_hint=(.51, .1), min=1, max=100, value=25)
        self.HardnessPicker.bind(value=self.set_hardness)
        self.add_widget(self.HardnessPicker)
        self.add_widget(Button(text="Start Game", font_size=30, pos_hint={"x": .05, "y": .05}, size_hint=(.9, .1), on_press=self.start_game))

    def set_hardness(self, instance, value):
        if 1 <= value <= 25:
            Public.animal_size = 50
            Public.animal_speed = 2
            Public.game_time = 200
        elif 25 < value <= 50:
            Public.animal_size = 50
            Public.animal_speed = 3
            Public.game_time = 170
        elif 50 < value <= 75:
            Public.animal_size = 45
            Public.animal_speed = 4
            Public.game_time = 140
        elif 75 < value <= 100:
            Public.animal_size = 35
            Public.animal_speed = 4
            Public.game_time = 120

#        print(Public.animal_size, Public.animal_speed, Public.game_time)

    def start_game(self, *args):
        root.clear_widgets()
        root.add_widget(GameWindow())
        root.current = "GameWindow"


class GameWindow(Screen):
    def __init__(self):
        super().__init__()
        self.name = "GameWindow"
        self.game_time = Public.game_time
        self.animal_count = 10
        self.container = GameClass.Animals()
        self.score = 0

        self.ScoreLabel = CoreLabel(font_size=40)
        self.TimeLabel = CoreLabel(font_size=40)

        self.game_time_clock = Clock.schedule_interval(self.game_reduce_time, .1)
        self.game_draw_clock = Clock.schedule_interval(self.game_draw, .001)

    def game_reduce_time(self, dt):
        self.game_time -= 1
#        print(self.game_time)

    def game_draw(self, dt):
        if self.game_time == 0:
            self.end_game()

        self.canvas.clear()
        self.canvas.add(Rectangle(source="pics\\jungle.jpg", pos=(0, 0), size=(Window.width, Window.height)))

#        loop for delete animals out of window

        for temp_animal in self.container.get_all_animals():
            if (temp_animal.pos_x <= 0 or temp_animal.pos_x + temp_animal.size >= Window.width) and (temp_animal.pos_y <= 0 or temp_animal.pos_y + temp_animal.size >= Window.height):
                self.container.animals_list.remove(temp_animal)
                self.score -= 10


#        loop for add new animals to list

        while len(self.container.get_all_animals()) < self.animal_count:
            pos_x = random.randint(100, Window.width - 100)
            pos_y = random.randint(100, Window.height - 100)
            self.container.animals_list.append(GameClass.Animal(pos_x, pos_y))


#        loop for draw animals

        for temp_animal in self.container.get_all_animals():

            if temp_animal.grab == 0:
                self.canvas.add(Rectangle(source="pics\\{}.png".format(temp_animal.pic), pos=(temp_animal.pos_x, temp_animal.pos_y), size=(temp_animal.size, temp_animal.size)))
            else:
                if 10 <= temp_animal.pic <= 48:
                    self.canvas.add(Rectangle(source="pics\\spark.png", pos=(temp_animal.pos_x, temp_animal.pos_y), size=(temp_animal.size, temp_animal.size)))

                if temp_animal.pic == 49:
                    self.canvas.add(Rectangle(source="pics\\Star.jpg", pos=(temp_animal.pos_x, temp_animal.pos_y), size=(temp_animal.size, temp_animal.size)))

                if temp_animal.pic == 50:
                    self.canvas.add(Rectangle(source="pics\\Bang.png", pos=(temp_animal.pos_x, temp_animal.pos_y), size=(temp_animal.size, temp_animal.size)))

            temp_animal.calc_new_pos()

        self.ScoreLabel.text = "Score: {}".format(self.score)
        self.ScoreLabel.refresh()

        self.TimeLabel.text = "Remain: {} Seconds".format(self.game_time)
        self.TimeLabel.refresh()

        self.canvas.add(Rectangle(pos=(50, 50), size=self.ScoreLabel.size, texture=self.ScoreLabel.texture))
        self.canvas.add(Rectangle(pos=(Window.width - 400, 50), size=self.TimeLabel.size, texture=self.TimeLabel.texture))

    def end_game(self):
        Clock.unschedule(self.game_time_clock)
        Clock.unschedule(self.game_draw_clock)
        root.clear_widgets()
        root.add_widget(ResultWindow(self.score))
        root.current = "ResultWindow"

    def on_touch_up(self, touch):
        # print(touch.pos[0], touch.pos[1])

        for animal_temp in self.container.get_all_animals():
            if animal_temp.is_click_contain(touch.pos[0], touch.pos[1]):
                self.score += 20
            elif animal_temp.pic == 49:
                self.score += 50
            elif animal_temp.pic == 50:
                self.score -= 50


class ResultWindow(Screen):
    def __init__(self, _score):
        super().__init__()
        self.name = "ResultWindow"
        self.canvas.add(Rectangle(source="pics\\Result_Background.png", pose=(0, 0), size=(Window.width, Window.height)))
        self.ScoreLabel = Label(text="Your score is {}".format(_score), pos_hint={"x": .1, "y": .7}, size_hint=(.8, .1), font_size=40)

        if _score <= 0:
            self.level = "a Weak "
        elif 0 < _score <= 90:
            self.level = "a Regular "
        elif 50 < _score <= 150:
            self.level = "a Good"
        elif _score > 200:
            self.level = "an Excellent "

        self.LevelLabel = Label(text="You are " + self.level + "player", pos_hint={"x": .1, "y": .55}, size_hint=(.8, .1), font_size=40)

        self.add_widget(self.ScoreLabel)
        self.add_widget(self.LevelLabel)

        self.add_widget(Button(text="Restart Game", font_size=20, pos_hint={"x": .01, "y": .05}, size_hint=(.45, .1), on_press=self.restart_game))
        self.add_widget(Button(text="Exit Game", font_size=20, pos_hint={"x": .54, "y": .05}, size_hint=(.45, .1), on_press=self.exit_game))

    def restart_game(self, *args):
        root.clear_widgets()
        root.add_widget(SettingWindow())
        root.current = "SettingWindow"

    def exit_game(self, *args):
        root.clear_widgets()
        exit()


class AnimalGrabApp(App):
    def build(self):
        root.add_widget(SettingWindow())
        root.current = "SettingWindow"
        return root


AnimalGrabApp().run()
