#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:30:29 2020

@author: pranav
"""

import pygame
import random
import time
import os

pygame.font.init()

#setting window dimensions
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800


#loading all the required images
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "bird3.png")))
    ]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("Game-Images", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5
    
    #x,y represents the starting position of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
    def jump(self):
        self.velocity = -10.5   #here we have a negative velocity for the bird as 0,0 is in the top left of the screen
        self.tick_count = 0     #when we last jumped
        self.height = self.y    #sets the height from where it jumped
        
    def move(self):
        self.tick_count += 1    #one frame went by
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2    #causes the arc when you jump
        
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2
            
        self.y += displacement
        
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
    
    def draw(self, win):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL
        
    def draw(self, win):
       win.blit(self.PIPE_TOP, (self.x, self.top))
       win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
       
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()
    IMG = BASE_IMAGE
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
        
def draw_window(win, bird, pipes, base, score):
    win.blit(BACKGROUND_IMAGE, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
        
    text = STAT_FONT.render("Score : " + str(score), 1, (255,255,255))
    win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()
    
    
def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    clock = pygame.time.Clock()
    
    add_pipe = False
    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        #bird.move()
        add_pipe = False
        
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
            pipe.move()
            
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            
        for r in rem:
            pipes.remove(r)
            
        if bird.y + bird.img.get_height() >= 730:
            pass
            
        base.move()
        draw_window(win, bird, pipes, base, score)
        
        
    pygame.quit()
    quit()
    
    
main()
        