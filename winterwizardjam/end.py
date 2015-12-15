import sdl2hl
from pkg_resources import resource_string

import clock
import sys

import ui
import leaderboard


class End(object):

    def __init__(self, renderer, window_size):
        self.renderer = renderer
        self.window_size = window_size

        self.name = ''
        self.max_name_length = 20

        self.button_selected = -1

    def run(self, last_time, best_time, best_time_set, last_ghost, best_ghost):

        scores = leaderboard.get_hi_scores(5)

        texts = []
        buttons = []

        if best_time_set:
            if last_time <= best_time:
                s = 'New personal best! Your time was ' + str(last_time) + ' seconds.'
                best_time = last_time
                best_ghost = last_ghost
            else:
                s = 'Your time was ' + str(last_time) + ' seconds. Your personal best is ' + str(best_time) + ' seconds.'
        else:
            s = 'Your time was ' + str(last_time) + ' seconds.'

        title = ui.Text(0, 100, s, 40)
        title.x = self.window_size[0]/2 - title.width/2
        texts.append(title)

        info_lines = ['Enter your name and submit your score!']
        x = 200
        y = title.y + title.height + 100

        for line in info_lines:
            s = ui.Text(x, y, line, 30)
            texts.append(s)

            y += s.height + 20

        y += 30

        name_text = ui.Text(x + 10, y + 10, self.name, 30)
        texts.append(name_text)

        name_rect = sdl2hl.Rect( x , y, 400, 60)

        y += 100

        submit_text = ui.Text(x + 10, y + 10, 'Submit Score!', 30)
        texts.append(submit_text)
        score_submitted = False
        submit_next_frame = False

        submit_rect = sdl2hl.Rect(x, y, 250, 60)

        begin_text = ui.Text(0, self.window_size[1] - 200, "Press 'Enter' to begin", 30)
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

        if best_time_set:
            t = best_time
        else:
            t = last_time

        s = ui.Text(x + 100, y, 'Personal Best' + ': ' + str(t), 30)
        texts.append(s)
        b = ui.Button(x, y, s.height, s.height)
        buttons.append(b)
        y += s.height + 50

        s = ui.Text(x + 100, y, 'Last Run' + ': ' + str(last_time), 30)
        texts.append(s)
        b = ui.Button(x, y, s.height, s.height)
        buttons.append(b)

        y += s.height + 50

        s = ui.Text(x + 100, y, 'None', 30)
        texts.append(s)
        b = ui.Button(x, y, s.height, s.height)
        buttons.append(b)

        if self.button_selected == -1:
            self.button_selected = len(buttons) - 1

        buttons[self.button_selected].selected = True

        my_clock = clock.clock()
        while True:
            dt = my_clock.tick(60)

            if submit_next_frame and not score_submitted:
                leaderboard.post_score(leaderboard.Score(self.name, last_time, last_ghost))
                score_submitted = True
                submit_text.set_text('Submitted!')

            for event in sdl2hl.events.poll():
                if event.type == sdl2hl.QUIT:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.escape:
                    sdl2hl.quit()
                    sys.exit()
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.return_:
                    if self.button_selected == len(buttons) - 1:
                        return []
                    elif self.button_selected == len(buttons) - 2:
                        return best_ghost
                    elif self.button_selected == len(buttons) - 3:
                        return last_ghost
                    else:
                        return scores[self.button_selected].ghost
                elif event.type == sdl2hl.KEYDOWN and event.keycode == sdl2hl.KeyCode.backspace:
                    if self.name:
                        self.name = self.name[:-1]
                        name_text.set_text(self.name)
                elif event.type == sdl2hl.TEXTINPUT:
                    if len(self.name) <= self.max_name_length:
                        self.name += event.text
                        name_text.set_text(self.name)
                elif event.type == sdl2hl.MOUSEBUTTONDOWN:
                    for i in range(len(buttons)):
                        if buttons[i].intersect_point(event.x, event.y):
                            buttons[self.button_selected].selected = False
                            self.button_selected = i
                            buttons[self.button_selected].selected = True
                        if not submit_next_frame and submit_rect.x < event.x < submit_rect.x + submit_rect.w and submit_rect.y < event.y < submit_rect.y + submit_rect.h:
                            submit_text.set_text('Submitting...')
                            submit_next_frame = True

            self.renderer.draw_color = (0, 0, 0, 255)
            self.renderer.clear()

            for t in texts:
                t.draw(self.renderer)

            for b in buttons:
                b.draw(self.renderer)

            self.renderer.draw_color = (255, 255, 255, 255)
            self.renderer.draw_rect(name_rect)
            self.renderer.draw_rect(submit_rect)

            self.renderer.present()