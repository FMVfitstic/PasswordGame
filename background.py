import pygame
import math
import random

class BackGround:
    def __init__(self, screen):
        self.displaced_verteces = 0
        self.screen = screen
        self.lattice = []
        self.SQRT_3 = 1.73205080757
        self.NUM_ROWS = 12
        self.SIDE = screen.get_height()/(self.NUM_ROWS-1)
        skew = self.SIDE/self.SQRT_3
        for i in range(int(screen.get_width()/self.SIDE+2)):
            h_offset = (i-0.7)*2/self.SQRT_3*self.SIDE
            self.lattice.append([])
            for j in range(self.NUM_ROWS+3):
                v_offset = (j-1.5)*self.SIDE
                c1 = pygame.Color('#000000')
                c2 = pygame.Color('#000000')
                colors = [c1, c2]
                for c in colors:
                    if random.random() > 0.5:
                        #arancione
                        c.r = int(random.uniform(200, 255))
                        c.g = int(random.uniform(100, c.r//1.5))
                        c.b = int(random.uniform(30, c.g//2))
                    else:
                        #azzurro
                        c.b = int(random.uniform(200, 255))
                        c.g = int(random.uniform(100, c.b//1.5))
                        c.r = int(random.uniform(30, c.g//2))
                
                self.lattice[i].append({'x':h_offset - (skew if j%2==1 else 0), 'y':v_offset, 'dx':0, 'dy':0, 'vx':0, 'vy':0, 'up':c1, 'down':c2})


    def drawTriangle(self, p1, p2, p3, c):
        pygame.draw.polygon(self.screen, c, [p1, p2, p3])

    def draw(self, dt):
        chaos_level = self.displaced_verteces/len(self.lattice)/len(self.lattice[0])
        self.displaced_verteces = 0

        for x in range(len(self.lattice)):
            for y in range(len(self.lattice[x])):
                if x < len(self.lattice)-1 and y < len(self.lattice[x])-1 and y%2==0:
                    p1 = (self.lattice[x][y]['x'] + self.lattice[x][y]['dx'], self.lattice[x][y]['y'] + self.lattice[x][y]['dy'])
                    p2 = (self.lattice[x][y+1]['x'] + self.lattice[x][y+1]['dx'], self.lattice[x][y+1]['y'] + self.lattice[x][y+1]['dy'])
                    p3 = (self.lattice[x+1][y+1]['x'] + self.lattice[x+1][y+1]['dx'], self.lattice[x+1][y+1]['y'] + self.lattice[x+1][y+1]['dy'])
                    p4 = (self.lattice[x+1][y]['x'] + self.lattice[x+1][y]['dx'], self.lattice[x+1][y]['y'] + self.lattice[x+1][y]['dy'])
                    p5 = (self.lattice[x][y+2]['x'] + self.lattice[x][y+2]['dx'], self.lattice[x][y+2]['y'] + self.lattice[x][y+2]['dy'])
                    p6 = (self.lattice[x+1][y+2]['x'] + self.lattice[x+1][y+2]['dx'], self.lattice[x+1][y+2]['y'] + self.lattice[x+1][y+2]['dy'])
                    self.drawTriangle(p1, p2, p3, self.lattice[x][y]['down'])
                    self.drawTriangle(p1, p4, p3, self.lattice[x+1][y+1]['up'])
                    self.drawTriangle(p2, p3, p5, self.lattice[x][y+2]['up'])
                    self.drawTriangle(p3, p5, p6, self.lattice[x+1][y+1]['down'])
                dx = self.lattice[x][y]['x'] + self.lattice[x][y]['dx']
                dy = self.lattice[x][y]['y'] + self.lattice[x][y]['dy']
                mouse_force = 0.3
                home_force = 0.03
                neighbor_force = 0.05
                deltaT = dt/100
                friction = 0.06
                mouse_coord = pygame.mouse.get_pos()
                if math.sqrt( math.pow(dx-mouse_coord[0], 2) + math.pow(dy-mouse_coord[1], 2) ) < self.SIDE/1.2:
                    self.lattice[x][y]['vx'] += deltaT*(mouse_coord[0]-dx)*mouse_force
                    self.lattice[x][y]['vy'] += deltaT*(mouse_coord[1]-dy)*mouse_force

                self.lattice[x][y]['vx'] += deltaT*(-self.lattice[x][y]['dx'])*home_force
                self.lattice[x][y]['vy'] += deltaT*(-self.lattice[x][y]['dy'])*home_force

                if x!=0 and y!=0 and x!=len(self.lattice)-1 and y!=len(self.lattice[x])-1:
                    neighbors = []
                    if y%2==0:
                        try:
                            neighbors.append(self.lattice[x][y-1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x+1][y-1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x+1][y])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x+1][y+1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x][y+1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x-1][y])
                        except:
                            pass
                    else:
                        try:
                            neighbors.append(self.lattice[x-1][y-1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x][y-1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x+1][y])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x][y+1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x-1][y+1])
                        except:
                            pass
                        try:
                            neighbors.append(self.lattice[x-1][y])
                        except:
                            pass

                    for n in neighbors:
                        ndx = n['x'] + n['dx']
                        ndy = n['y'] + n['dy']
                        mod = math.sqrt(math.pow(ndx-dx, 2) + math.pow(ndy-dy, 2))
                        scalar = 1
                        if mod > self.SIDE:
                            scalar = self.SIDE/mod
                        self.lattice[x][y]['vx'] += (ndx-dx)*neighbor_force*scalar
                        self.lattice[x][y]['vy'] += (ndy-dy)*neighbor_force*scalar

                if abs(self.lattice[x][y]['vx']) > friction:
                    self.lattice[x][y]['vx'] += math.copysign(friction, -self.lattice[x][y]['vx'])
                else:
                    self.lattice[x][y]['vx'] *= math.pow(friction, 2)

                if abs(self.lattice[x][y]['vy']) > friction:
                    self.lattice[x][y]['vy'] += math.copysign(friction, -self.lattice[x][y]['vy'])
                else:
                    self.lattice[x][y]['vy'] *= math.pow(friction, 2)
                
                self.lattice[x][y]['dx'] += deltaT*self.lattice[x][y]['vx']
                self.lattice[x][y]['dy'] += deltaT*self.lattice[x][y]['vy']

                displacement = math.sqrt(self.lattice[x][y]['dx']*self.lattice[x][y]['dx'] + self.lattice[x][y]['dy']*self.lattice[x][y]['dy'])
                disp_limit = self.SIDE*1.3*(1-chaos_level)
                if displacement > disp_limit/2:
                    self.displaced_verteces += 1
                    self.lattice[x][y]['vx'] *= math.pow(friction, 2)
                    self.lattice[x][y]['vy'] *= math.pow(friction, 2)
                if displacement > disp_limit:
                    self.lattice[x][y]['dx'] *= disp_limit/displacement
                    self.lattice[x][y]['dy'] *= disp_limit/displacement