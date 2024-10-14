#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:18:14 2023

@author: ahorpeda
"""
from . import snake_client
from . import cpu_player
import pygame
import sys
from . import utils

from . import game_client
from . import human_player

SCREEN_SIZE = (650, 600)
BACKGROUND_COLOR = (178, 107, 53)
CAPTION = 'Snake, by Andreas'
SNAKE_COLOR = (87, 216, 60)
FOOD_COLOR = (255, 0, 0)
START_MENU = ['Welcome to snake!', "Press ENTER to start and ESC to quit."]

def classic_game():
        db = utils.connect_to_db()
        running = True
        pygame.init()
        clock = pygame.time.Clock()
        client = game_client.GameClient(SCREEN_SIZE[0], SCREEN_SIZE[1], BACKGROUND_COLOR, CAPTION)
        screen = client.draw_game_screen()
        my_snake_client = snake_client.SnakeClient(screen, client, SNAKE_COLOR, FOOD_COLOR) 
        player = human_player.HumanPlayer(my_snake_client)
        player.s_client.draw_text_on_screen(START_MENU, 35, 'arialblack', (255,255,255))
        running = snake_client.SnakeClient.screen_awaiter([pygame.K_ESCAPE], [pygame.K_RETURN])
        
        player.s_client.initialize_snake_game(client)
   
        while running:
            running = player.s_client.check_if_gameover()
            player.s_client.draw_score(f'Score: {player.s_client.score}', 35, 'arialblack', (255,255,255))
            for event in pygame.event.get():    
                player.control_snake(event)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False 
            player.move_snake()
            player.s_client.food_interaction()
            pygame.display.update()
            clock.tick(5)
    
            if player.s_client.gameover:
                print('dasdasd')
                player.s_client.registrer_name()
                utils.registrer_new_record(db, player.s_client.player, player.s_client.score)
                top_3 = utils.retrive_top_3_records(db)
                gameover = ['Game over!', f'Your score: {player.s_client.score}', 'Press R to play again and ESC to quit.', '','Highscore:', f'1 {top_3[0][0]}, {top_3[0][1]}', f'2 {top_3[1][0]}, {top_3[1][1]}', f'3 {top_3[2][0]}, {top_3[2][1]}']
                client.draw_blank_screen(screen)
                player.s_client.draw_text_on_screen(gameover, 35, 'arialblack', (255,255,255))
                running = snake_client.SnakeClient.screen_awaiter([pygame.K_ESCAPE], [pygame.K_RETURN, pygame.K_r])
                
                my_snake_client = snake_client.SnakeClient(screen, client, SNAKE_COLOR, FOOD_COLOR)
                player = human_player.HumanPlayer(my_snake_client)
                player.s_client.initialize_snake_game(client)
       
        pygame.quit()

def cpu_game():
    db = utils.connect_to_db()
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    client = game_client.GameClient(SCREEN_SIZE[0], SCREEN_SIZE[1], BACKGROUND_COLOR, CAPTION)
    screen = client.draw_game_screen()
    my_snake_client = snake_client.SnakeClient(screen, client, SNAKE_COLOR, FOOD_COLOR)  
    cpu = cpu_player.CPUPlayer(my_snake_client)
    cpu.s_client.draw_text_on_screen(START_MENU, 35, 'arialblack', (255,255,255))
    running = snake_client.SnakeClient.screen_awaiter([pygame.K_ESCAPE], [pygame.K_RETURN])
    
    my_snake_client.initialize_snake_game(client)
    
    while running:
        running = cpu.s_client.check_if_gameover()
        cpu.s_client.draw_score(f'Score: {cpu.s_client.score}', 35, 'arialblack', (255,255,255))
        for event in pygame.event.get():    
            cpu.control_snake()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 
        
        cpu.control_snake()
        cpu.move_snake()
        cpu.s_client.food_interaction()
        pygame.display.update()
        clock.tick(5)
    
    pygame.quit()

def dual_mode():
    db = utils.connect_to_db()
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    client = game_client.GameClient(SCREEN_SIZE[0], SCREEN_SIZE[1], BACKGROUND_COLOR, CAPTION)
    screen = client.draw_game_screen()
    my_snake_client = snake_client.SnakeClient(screen, client, SNAKE_COLOR, FOOD_COLOR)

    cpu = cpu_player.CPUPlayer(my_snake_client)
    # human = human_player.HumanPlayer(my_snake_client)

    print(cpu)
    print(human)

    # while running:
    #     running = cpu.s_client.check_if_gameover()
    #     cpu.s_client.draw_score(f'Score: {cpu.s_client.score}', 35, 'arialblack', (255,255,255))
    #     for event in pygame.event.get():    
    #         cpu.control_snake()
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 running = False    


    pygame.quit()

if __name__ == '__main__':
    classic_game()
    # cpu_game()
    # dual_mode()