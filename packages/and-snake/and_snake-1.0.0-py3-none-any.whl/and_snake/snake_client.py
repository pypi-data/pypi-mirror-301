#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 19:42:50 2023

@author: ahorpeda
"""

import pygame
import random
import sys
from typing import List, Tuple, TypeAlias
import game_client

class SnakeClient(game_client.GameClient):
    
    
    def __init__(self, game_screen, game_client, snake_color, food_color):
        super().__init__(game_client.x_size, game_client.y_size, game_client.background_color, game_client.caption)
        self.game_screen = game_screen
        self.client = game_client
        self.snake_color = snake_color
        self.food_color = food_color
        self.snake_coordinates = [[100, 100, 50, 50]]
        self.snake_head = [100, 100, 50, 50]
        self.last_botton_pressed = 'RIGHT'
        self.growing = False
        self.score = 0
        self.gameover = False
        self.player = ''
        
    # Må flyttes
    def initialize_snake_game(self, client) -> None:
        client.draw_blank_screen(self.game_screen)
        self.draw_snake()
        self.spawn_food()
    
    # Må flyttes
    def draw_snake(self) -> None:
        for coordinates in self.snake_coordinates:
            pygame.draw.rect(self.game_screen, self.snake_color,(coordinates))

    # Må flyttes
    def erase_snake(self) -> None:
        for coordinates in self.snake_coordinates:
            pygame.draw.rect(self.game_screen, self.background_color,(coordinates))

    # Må flyttes
    def check_if_gameover(self) -> bool:
        if self.snake_head[0] < 0 or self.snake_head[1] < 0:
            self.gameover = True
            return False
        elif self.snake_head[0] >= self.x_size or self.snake_head[1] >= self.y_size:
            self.gameover = True
            return False
        elif self.snake_head in self.snake_coordinates[1:]:
            self.gameover = True
            return False
        return True
    
    # Må flyttes
    def spawn_food(self) -> None:
        food_spawned = False
        while not food_spawned:
            self.x_position_food = random.randrange(0, self.x_size, 50)
            self.y_position_food = random.randrange(0, self.y_size, 50)
            if [self.x_position_food, self.y_position_food] in [cord[:2] for cord in self.snake_coordinates]:
                continue
            food_spawned = True
        pygame.draw.rect(self.game_screen, self.food_color,(self.x_position_food, self.y_position_food, 50, 50))
        
    # Må flyttes
    def food_interaction(self) -> None:
        self.growing = False 
        if self.snake_head[:2] == [self.x_position_food, self.y_position_food]:
             self.growing = True
             self.score += 1
             self.spawn_food()
        
    
    def draw_score(self, score: str, text_size: int, text_font: str, text_color: tuple[str]) -> None:
        score_img = game_client.GameClient.return_text_image(score, text_size, text_font, text_color)
        x_pos = 0
        y_pos = 0
        self.client.delete_and_draw_text_image(self.game_screen, score_img, x_pos, y_pos)

    
    def draw_text_on_screen(self, text_list: list[str], text_size: int, text_font: str, text_color: tuple[str]) -> None:
        for index, text in enumerate(text_list):
            img = game_client.GameClient.return_text_image(text, text_size, text_font, text_color)
            x_pos = self.x_size/2 - img.get_width()/2
            y_pos = self.y_size/5 + index * self.y_size * 2/text_size
            self.client.delete_and_draw_text_image(self.game_screen, img, x_pos, y_pos)
        
    
    def registrer_name(self) -> None:
        self.draw_blank_screen(self.game_screen)
        text_lines = ['Game over!', f'Your score: {self.score}', 'Please enter your name and press ENTER to proceed.', 'Name: ']
        self.draw_text_on_screen(text_lines, 35, 'arialblack', (255, 255, 255))
        
        while True:
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.player = self.player[:-1]
                    else:
                        character = chr(event.key).upper()
                        self.player += character

            self.draw_blank_screen(self.game_screen)
            self.draw_text_on_screen(text_lines[:-1] + [text_lines[-1] + self.player], 35, 'arialblack', (255, 255, 255))
            pygame.display.update()

    
    @staticmethod
    def screen_awaiter(quit_events: list[str], proceed_events: list[str]) -> bool:
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key in quit_events:
                        return False
                    if event.key in proceed_events:
                        return True
            pygame.display.update()

        
        
        