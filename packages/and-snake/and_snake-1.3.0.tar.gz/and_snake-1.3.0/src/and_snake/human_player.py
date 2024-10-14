#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:11:07 2023

@author: ahorpeda
"""
from . import snake_client
import pygame

class HumanPlayer(snake_client.SnakeClient):
    
    
    def __init__(self, s_client):
        super().__init__(s_client.game_screen, s_client.client, s_client.snake_color, s_client.food_color)
        self.s_client = s_client
    
    
    def control_snake(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.last_botton_pressed != 'DOWN':
                self.last_botton_pressed = 'UP'
            if event.key == pygame.K_DOWN and self.last_botton_pressed != 'UP':
                self.last_botton_pressed = 'DOWN'
            if event.key == pygame.K_LEFT and self.last_botton_pressed != 'RIGHT':
                self.last_botton_pressed = 'LEFT'
            if event.key == pygame.K_RIGHT and self.last_botton_pressed != 'LEFT':
                self.last_botton_pressed = 'RIGHT'
        
        
    def move_snake(self) -> None:
        if self.last_botton_pressed == 'UP':
            self.s_client.erase_snake()
            self.s_client.snake_head[1] -= 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        
        if self.last_botton_pressed == 'DOWN':
            self.s_client.erase_snake()
            self.s_client.snake_head[1] += 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        
        if self.last_botton_pressed == 'LEFT':
            self.s_client.erase_snake()
            self.s_client.snake_head[0] -= 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        
        if self.last_botton_pressed == 'RIGHT':
            self.s_client.erase_snake()
            self.s_client.snake_head[0] += 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
    
    


