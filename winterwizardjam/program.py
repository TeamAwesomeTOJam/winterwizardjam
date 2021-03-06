import sdl2hl
import game
import title
import end
import leaderboard


class Program(object):

    def __init__(self):
        sdl2hl.init()
        sdl2hl.mixer.init(sdl2hl.mixer.AudioInitFlag.ogg)
        sdl2hl.mixer.open_audio()
        sdl2hl.ttf.init()

        self.window_size = (1920, 1080)

        self.window = sdl2hl.Window(title="Winter Wizard Jam", w=self.window_size[0], h=self.window_size[1])
        # self.renderer = sdl2hl.Renderer(self.window,-1, sdl2hl.RendererFlags.presentvsync)
        self.renderer = sdl2hl.Renderer(self.window)

        self.game = game.game(self.renderer, self.window_size)
        self.title = title.Title(self.renderer, self.window_size)
        self.end = end.End(self.renderer, self.window_size)

        self.best_run_time = 0
        self.best_run_ghost_data = []
        self.best_run_set = False

    def run(self):
        use_mouse, ghost = self.title.run()
        while True:

            run_time, ghost_data = self.game.run(ghost, use_mouse)

            ghost = self.end.run(run_time, self.best_run_time, self.best_run_set, ghost_data, self.best_run_ghost_data)

            if self.best_run_set:
                if run_time < self.best_run_time:
                    self.best_run_time = run_time
                    self.best_run_ghost_data = ghost_data

            else:
                self.best_run_time = run_time
                self.best_run_ghost_data = ghost_data
                self.best_run_set = True
