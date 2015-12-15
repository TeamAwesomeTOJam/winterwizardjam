import sdl2hl
from pkg_resources import resource_string
import ui
import leaderboard


import clock
import sys


class Title(object):

    def __init__(self, renderer, window_size):
        self.renderer = renderer
        self.window_size = window_size

    def run(self):
        # draw a blank frame whiel we load scores
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        title = ui.Text(0, 100, 'Loading...', 40)
        title.x = self.window_size[0]/2 - title.width/2
        title.draw(self.renderer)

        self.renderer.present()

        scores = leaderboard.get_hi_scores(5)

        buttons = []
        texts = []

        title = ui.Text(0, 100, 'Winter Wizard Jam', 40)
        title.x = self.window_size[0]/2 - title.width/2
        texts.append(title)

        how_to_play_lines = ['Race to the finish line!',
                             'Position your kite with the mouse or joystick.',
                             'Keep the kite in front of you for maximum speed.',
                             'Try to land smoothly to maintain speed.',
                             "Press 'r' for a quick restart"]

        x = 200
        y = title.y + title.height + 100

        for line in how_to_play_lines:
            s = ui.Text(x, y, line, 30)
            texts.append(s)

            y += s.height + 20

        y += 30

        mouse_text = ui.Text(x + 50, y, 'Mouse', 30)
        texts.append(mouse_text)
        mouse_button = ui.Button(x, y, mouse_text.height, mouse_text.height)
        mouse_button.selected = True

        y += mouse_text.height + 50

        stick_text = ui.Text(x + 50, y, 'Stick', 30)
        texts.append(stick_text)
        stick_button = ui.Button(x, y, stick_text.height, stick_text.height)

        begin_text = ui.Text(0, self.window_size[1] - 200, 'Press any key to begin', 30)
        begin_text.x = self.window_size[0]/2 - begin_text.width/2

        texts.append(begin_text)

        y = title.y + title.height + 100
        x = self.window_size[0]/2 + 300

        s = ui.Text(x, y, 'Pick a ghost', 30)
        texts.append(s)

        y += s.height + 50

        for score in scores:
            s = ui.Text(x + 100, y, score.name + ': ' + str(score.time), 30)
            texts.append(s)
            buttons.append(ui.Button(x, y, s.height, s.height))

            y += s.height + 50

        s = ui.Text(x + 100, y, 'None', 30)
        texts.append(s)
        b = ui.Button(x, y, s.height, s.height)
        b.selected = True
        buttons.append(b)
        button_selected = len(buttons) - 1

        y += s.height + 50

        my_clock = clock.clock()
        while True:
            dt = my_clock.tick(60)

            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.escape:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and (event.keycode == sdl2hl.KeyCode.return_ or event.keycode == sdl2hl.KeyCode.space):
                    if button_selected == len(buttons) - 1:
                        return (mouse_button.selected, [])
                    else:
                        return (mouse_button.selected, scores[button_selected].ghost)
                elif event.type == sdl2hl.MOUSEBUTTONDOWN:
                    for i in range(len(buttons)):
                        if buttons[i].intersect_point(event.x, event.y):
                            buttons[button_selected].selected = False
                            button_selected = i
                            buttons[button_selected].selected = True
                    if mouse_button.intersect_point(event.x, event.y):
                        mouse_button.selected = True
                        stick_button.selected = False
                    if stick_button.intersect_point(event.x, event.y):
                        mouse_button.selected = False
                        stick_button.selected = True

            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()

            for button in buttons:
                button.draw(self.renderer)

            for t in texts:
                t.draw(self.renderer)

            mouse_button.draw(self.renderer)
            stick_button.draw(self.renderer)

            self.renderer.present()