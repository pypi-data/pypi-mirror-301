#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 19:42:21 2023

@author: ahorpeda
"""

import pygame

class GameClient:
    def __init__(self, x_size, y_size, background_color, caption):
        self.x_size = x_size
        self.y_size = y_size
        self.background_color = background_color
        self.caption = caption
        
    def draw_game_screen(self):
        pygame.display.set_caption(self.caption)
        game_screen = pygame.display.set_mode((self.x_size, self.y_size))
        game_screen.fill(self.background_color)
        return game_screen
    
    def draw_blank_screen(self, game_screen):
        game_screen.fill(self.background_color)
        return game_screen
        
    def delete_and_draw_text_image(self, game_screen, text_img, x_pos, y_pos):
        text_rect = text_img.get_rect()
        pygame.draw.rect(game_screen, self.background_color,(text_rect))
        GameClient.draw_text_image(game_screen, text_img, x_pos, y_pos)
    
    @staticmethod
    def return_text_image(text_string, text_size, text_font, text_color):
        font = pygame.font.SysFont(text_font, text_size)
        return font.render(text_string, True, text_color)
    
    @staticmethod
    def draw_text_image(surface, text_image, x_pos, y_pos):
        surface.blit(text_image, (x_pos, y_pos))
        
        