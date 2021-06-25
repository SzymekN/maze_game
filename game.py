from A_star import A_Star
from player import Player
import sys
import pygame
from math import floor

from settings import Settings
from maze import *
from A_star import A_Star


class MazeGame():

    def __init__(self):
        """Initialize needed objects"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Maze runner")

        self.rows = floor(
            self.settings.screen_size[1] / self.settings.cell_width)
        self.cols = floor(
            self.settings.screen_size[0] / self.settings.cell_width)

        print(self.cols)
        print(self.rows)

        # initialize player
        self.player = Player(self)
        self.maze = Maze(self)
        self.a_star = A_Star(self)


    def run_game(self):
        """Run game"""
        FPS = self.settings.FPS
        while True:

            if not self.settings.solve:
                pygame.time.Clock().tick(FPS)

            self._check_events()

            if self.settings.play:
                self.player.update()

            self._update_screen()
 
    def _check_events(self):
        """Respond if event occurs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Check keydown event triggered"""
        if event.key == pygame.K_RIGHT:
            self.player.move_r = True
        if event.key == pygame.K_LEFT:
            self.player.move_l = True
        if event.key == pygame.K_UP:
            self.player.move_u = True
        if event.key == pygame.K_DOWN:
            self.player.move_d = True
        if event.key == pygame.K_f:
            self.settings.FOV = not self.settings.FOV
        if event.key == pygame.K_p:
            self.player.reset()
            self.settings.play = not self.settings.play
        if event.key == pygame.K_s:
            self.a_star.reset()
            self.settings.solve = not self.settings.solve
        if event.key == pygame.K_q:
            self.a_star.reset()
            self.settings.q_solve = not self.settings.q_solve
            self.a_star.qucik_find()
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        """Chceck triggered key upevent"""
        if event.key == pygame.K_RIGHT:
            self.player.move_r = False
        if event.key == pygame.K_LEFT:
            self.player.move_l = False
        if event.key == pygame.K_UP:
            self.player.move_u = False
        if event.key == pygame.K_DOWN:
            self.player.move_d = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.maze.draw_maze()
        self.player.draw_player()

        if self.settings.solve:
            self.a_star.find_path()

        self.player.draw_route()
        # generate_maze(self, self.current)
        pygame.display.flip()


if __name__ == "__main__":
    mg = MazeGame()
    mg.run_game()
