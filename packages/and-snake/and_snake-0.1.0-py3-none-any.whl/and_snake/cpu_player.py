#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 17:32:44 2023

@author: ahorpeda
"""

import pygame
import random
import sys

import game_client

class CPUPlayer(game_client.GameClient):
    
    
    def __init__(self, s_client):
        super().__init__(s_client.game_screen, s_client.client, s_client.snake_color, s_client.food_color)
        self.s_client = s_client   
        self.previous_direction = ''
   
    
    def control_snake(self):
        x_difference = self.s_client.snake_head[0] - self.s_client.x_position_food
        y_difference = self.s_client.snake_head[1] - self.s_client.y_position_food
        
        if self.previous_direction != self.s_client.last_botton_pressed: 
            self.previous_direction = self.s_client.last_botton_pressed
        
        if abs(x_difference) > abs(y_difference):
            if x_difference < 0 and self.s_client.last_botton_pressed != 'LEFT':
                self.s_client.last_botton_pressed = 'RIGHT'
            elif x_difference > 0 and self.s_client.last_botton_pressed != 'RIGHT':
                self.s_client.last_botton_pressed = 'LEFT'
            else:
                if self.find_valid_direction() == 'ALL':
                    self.s_client.last_botton_pressed = random.choice(['UP', 'DOWN'])
                else:
                    self.s_client.last_botton_pressed = self.find_valid_direction()
        else:
            if y_difference < 0 and self.s_client.last_botton_pressed != 'UP':
                self.s_client.last_botton_pressed = 'DOWN'
            elif y_difference > 0 and self.s_client.last_botton_pressed != 'DOWN':
                self.s_client.last_botton_pressed = 'UP'
            else:
                if self.find_valid_direction() == 'ALL':
                   self.s_client.last_botton_pressed = random.choice(['LEFT', 'RIGHT'])
                else:
                    self.s_client.last_botton_pressed = self.find_valid_direction()
        
        self.await_move()


    def await_move(self):
        waiting = True
        wait_count = 0
        while waiting:
            if self.calc_next_postion() in self.s_client.snake_coordinates[1:] and wait_count <= 1000:
                valid_direction = self.find_valid_direction()
                if valid_direction == 'ALL':
                    possible_moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
                    possible_moves.remove(self.s_client.last_botton_pressed)
                    self.s_client.last_botton_pressed = random.choice(possible_moves)
                else:
                    self.s_client.last_botton_pressed = valid_direction
            else:
                waiting = False
            
            wait_count += 1
            
                
    def calc_next_postion(self):
        if self.s_client.last_botton_pressed == 'UP':
            return [self.s_client.snake_head[0], self.s_client.snake_head[1] - 50, 50, 50]
        if self.s_client.last_botton_pressed == 'DOWN':
            return [self.s_client.snake_head[0], self.s_client.snake_head[1] + 50, 50, 50]   
        if self.s_client.last_botton_pressed == 'LEFT':
            return [self.s_client.snake_head[0] - 50, self.s_client.snake_head[1], 50, 50]
        if self.s_client.last_botton_pressed == 'RIGHT':
            return [self.s_client.snake_head[0] + 50, self.s_client.snake_head[1], 50, 50]

        
    def find_valid_direction(self) -> str:
        if self.s_client.snake_head[0] - 50 < 0:
            if self.s_client.last_botton_pressed == 'LEFT' and self.s_client.snake_head[1] - 50 < 0:
                return 'DOWN'
            if self.s_client.last_botton_pressed == 'LEFT' and self.s_client.snake_head[1] + 50 >= self.s_client.y_size:
                return 'UP'
            if self.s_client.last_botton_pressed == 'UP':
                return 'RIGHT'
            if self.s_client.last_botton_pressed == 'DOWN':
                return 'RIGHT'
        
        if self.s_client.snake_head[0] + 50 >= self.s_client.x_size:
          if self.s_client.last_botton_pressed == 'RIGHT' and self.s_client.snake_head[1] - 50 < 0:
              return 'DOWN'
          if self.s_client.last_botton_pressed == 'RIGHT' and self.s_client.snake_head[1] + 50 >= self.s_client.y_size:
              return 'UP'
          if self.s_client.last_botton_pressed == 'UP':
              return 'LEFT'
          if self.s_client.last_botton_pressed == 'DOWN':
              return 'LEFT'
        
        if self.s_client.snake_head[1] - 50 < 0:
            if self.s_client.last_botton_pressed == 'UP' and self.s_client.snake_head[0] - 50 < 0:
                return 'RIGHT'
            if self.s_client.last_botton_pressed == 'UP' and self.s_client.snake_head[0] + 50 >= self.s_client.y_size:
                return 'LEFT'
            if self.s_client.last_botton_pressed == 'RIGHT':
                return 'DOWN'
            if self.s_client.last_botton_pressed == 'LEFT':
                return 'DOWN'
        
        if self.s_client.snake_head[1] + 50 >= self.s_client.y_size:
            if self.s_client.last_botton_pressed == 'DOWN' and self.s_client.snake_head[0] -50 < 0:
                return 'RIGHT'
            if self.s_client.last_botton_pressed == 'DOWN' and self.s_client.snake_head[0] +50  >= self.y_size:
                return 'LEFT'
            if self.s_client.last_botton_pressed == 'RIGHT':
                return 'UP'
            if self.s_client.last_botton_pressed == 'LEFT':
                return 'UP'

        return 'ALL'
    
    
    def move_snake(self):
        if self.s_client.last_botton_pressed == 'UP':
            self.s_client.erase_snake()
            self.s_client.snake_head[1] -= 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        if self.s_client.last_botton_pressed == 'DOWN':
            self.s_client.erase_snake()
            self.s_client.snake_head[1] += 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        if self.s_client.last_botton_pressed == 'LEFT':
            self.s_client.erase_snake()
            self.s_client.snake_head[0] -= 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
        if self.s_client.last_botton_pressed == 'RIGHT':
            self.s_client.erase_snake()
            self.s_client.snake_head[0] += 50
            self.s_client.snake_coordinates.insert(0, list(self.s_client.snake_head))
            if self.s_client.growing == False:
                self.s_client.snake_coordinates.pop()
            self.s_client.draw_snake()
    
    