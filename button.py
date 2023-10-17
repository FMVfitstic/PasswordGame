
import pygame
import math

class Button:

    horiz_offset = 5

    def __init__(self, x, y, w, h, relative, screen, text, react_to_kb, func):
		# basic font for user typed
        self.base_font = pygame.font.Font(None, int(math.floor(h)))
        self.user_text = text

        self.react_to_kb = react_to_kb

        self.relative = relative

        self.w = w
        self.x=x
        self.y=y
        self.h=h

        self.func = func

		# create rectangle
        self.input_rect = pygame.Rect(x, y, w, h)
		
        self.screen = screen

		# color_active stores color(lightskyblue3) which
		# gets active when input box is clicked by user
        self.color_active = pygame.Color('lightskyblue3')

		# color_passive store color(chartreuse4) which is
		# color of input box.
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.is_active = True

    def set_active(self, value):
        self.is_active = value

    def mouse_is_over(self):
        return self.input_rect.collidepoint(pygame.mouse.get_pos())

    def update(self, event):
        if self.is_active:
            if event.type == pygame.KEYDOWN and self.react_to_kb:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.func()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_is_over():
                    self.func()

    def draw(self):

        if self.relative:
            self.input_rect = pygame.Rect(self.screen.get_width()*self.x/100 - self.w/2, self.screen.get_height()*self.y/100 - self.h/2, self.w, self.h)


        if self.mouse_is_over():
            self.color = self.color_active
        else:
            self.color = self.color_passive
			
        pygame.draw.rect(self.screen, self.color, self.input_rect)

        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
		
        self.screen.blit(text_surface, (self.input_rect.x + (self.input_rect.w-(text_surface.get_width()))/2, self.input_rect.y + (self.input_rect.h-self.base_font.get_height())/2))
		
        self.w = max(self.w, text_surface.get_width()+10)