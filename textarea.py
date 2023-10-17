
import pygame
import sys

class TextArea:

    margin = 10

    def __init__(self, x, y, w, h, relative, c1, c2, screen, text, font_size):

        self.base_font = pygame.font.Font(None, font_size)
        self.font_size = font_size
        self.user_text = text

        self.relative = relative

        self.w = w
        self.x=x
        self.y=y
        self.h=h

        self.input_rect = pygame.Rect(x, y, w, h)
		
        self.screen = screen

        self.color_active = c1

        self.color_passive = c2
        self.color = self.color_passive

        self.visible = True

    def setVisibility(self, value):
        self.visible = value
    
    def isVisible(self):
        return self.visible

    def updateText(self, text):
        self.user_text = text

    def updateWidth(self, width):
        self.w = width
        self.input_rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def calcPos(self, beg, end):
        text_surface = self.base_font.render(self.user_text[beg:end], True, (255, 255, 255))
        return text_surface.get_width()
    
    def drawText(self):
        beg = 0
        end = 0
        prevend = 0
        lines = 0
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))

        while end < len(self.user_text):
            end = prevend
            end+=1
            while True:
                while end < len(self.user_text) and self.user_text[end] != ' ' and self.user_text[end] != '\n' and self.user_text[end] != '\t':
                    end+=1
                size = self.calcPos(beg, end)
                if(end>=len(self.user_text)):
                    text_surface = self.base_font.render(self.user_text[beg:], True, (255, 255, 255))
                    self.screen.blit(text_surface, (self.input_rect.x + TextArea.margin, self.input_rect.y + lines*self.font_size))
                    break
                if(self.user_text[end] =='\n' and size<=self.input_rect.w-2*TextArea.margin):
                    text_surface = self.base_font.render(self.user_text[beg:end], True, (255, 255, 255))
                    prevend = end
                    self.screen.blit(text_surface, (self.input_rect.x + TextArea.margin, self.input_rect.y + lines*self.font_size))
                    break
                if(size>self.input_rect.w-2*TextArea.margin):
                    text_surface = self.base_font.render(self.user_text[beg:prevend], True, (255, 255, 255))
                    self.screen.blit(text_surface, (self.input_rect.x + TextArea.margin, self.input_rect.y + lines*self.font_size))
                    break
                prevend = end
                end+=1
            lines+=1
            beg=prevend+1

    def draw(self):
		
        if self.visible:
            self.color = self.color_active
            
            if self.relative:
                self.input_rect = pygame.Rect(self.screen.get_width()*self.x/100 - self.w/2, self.screen.get_height()*self.y/100 - self.h/2, self.w, self.h)

            pygame.draw.rect(self.screen, self.color, self.input_rect)
            
            self.drawText()