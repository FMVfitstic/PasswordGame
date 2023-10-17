
import pygame

class TextBox:

    horiz_offset = 5
    allowedKeys = " qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!()-.?[]_';:@#%^&*+=~£$€|\\/àèéìòùç°§,<>\"a"

    def __init__(self, x, y, w, h, relative, c1, c2, c3, screen):
		# basic font for user typed
        self.base_font = pygame.font.Font(None, h)
        self.user_text = ''

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

        self.color_error = c3
        self.error = False

        self.active = False

        self.cursor_pos = 0
        
        self.delete = False

    def reset(self):
        self.user_text = ""
        self.cursor_pos = 0

    def setError(self, value):
        self.error = value

    def getValue(self):
        return self.user_text
	
    def calcPos(self, pos):
        text_surface = self.base_font.render(self.user_text[:pos], True, (255, 255, 255))
        return text_surface.get_width() + self.input_rect.x + TextBox.horiz_offset

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.error = False
            if self.input_rect.collidepoint(event.pos):					
                self.active = True
                mouse = pygame.mouse.get_pos()[0]
                self.cursor_pos = 0
                min_dist = self.input_rect.w*2
                for i in range(len(self.user_text)+1):
                    pos = self.calcPos(i)
                    if abs(pos-mouse) < min_dist:
                        min_dist = abs(pos-mouse)
                        self.cursor_pos = i
            else:
                self.active = False
                self.delete = False
                self.toDelete = False

        if event.type == pygame.KEYDOWN and self.active:

            self.error = False

            if event.key == pygame.K_BACKSPACE:
                self.delete = True
                self.toDelete = True
                self.deleteTime = pygame.time.get_ticks()
				
            elif event.key == pygame.K_DELETE:
                self.user_text = self.user_text[:self.cursor_pos] + self.user_text[self.cursor_pos+1:]


            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos-1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.user_text), self.cursor_pos+1)

            elif event.unicode in TextBox.allowedKeys and event.unicode != '':
                self.user_text = self.user_text[:self.cursor_pos] + event.unicode + self.user_text[self.cursor_pos:]
                self.cursor_pos += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.delete = False

    def mouse_is_over(self):
        return self.input_rect.collidepoint(pygame.mouse.get_pos())
    
    def draw(self):

        if self.cursor_pos > 0 and self.delete and self.active and ((pygame.time.get_ticks()%2==0 and pygame.time.get_ticks()-self.deleteTime>300) or self.toDelete):
            self.user_text = self.user_text[:self.cursor_pos-1] + self.user_text[self.cursor_pos:]
            self.cursor_pos = max(0, self.cursor_pos-1)
            self.toDelete = False

        def calcCursLocation():
            return self.calcPos(self.cursor_pos)
		
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        if self.error:
            self.color = self.color_error

        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))

        rectW = max(self.w, text_surface.get_width()+2*TextBox.horiz_offset)

        if self.relative:
            self.input_rect = pygame.Rect(self.screen.get_width()*self.x/100 - rectW/2, self.screen.get_height()*self.y/100 - self.h/2, rectW, self.h)

        pygame.draw.rect(self.screen, self.color, self.input_rect)
		
        self.screen.blit(text_surface, (self.input_rect.x + TextBox.horiz_offset, self.input_rect.y + (self.input_rect.h-self.base_font.get_height())/2))
		
        if self.active and pygame.time.get_ticks()%1000>500:
            cursLoc = calcCursLocation()
            pygame.draw.line(self.screen, (255, 255, 255), (cursLoc, self.input_rect.y+self.input_rect.h/6), (cursLoc, self.input_rect.y+self.input_rect.h*5/6))
