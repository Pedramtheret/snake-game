import pygame
import sys
import copy
from random import choice


Board_width=600
Board_height=600
Board_margin=10
general_row, general_column=10, 10

class game:

    def __init__(self) :
        pygame.init()

        pygame.display.set_caption('snake game')

        global Board_width
        global Board_height
        global general_row,general_column

        self.screen=pygame.display.set_mode((Board_width,Board_height))
        self.board=Board(Board_width,Board_height,Board_margin, general_column, general_row)
        self.snake=Snake(Board_width, Board_height, Board_margin, general_column, general_row)
        self.fruit=Fruit(Board_width, Board_height, Board_margin, general_column, general_row,Snake)
        self.clock=pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.board.draw(self.screen)
            self.snake.draw(self.screen) 
            self.fruit.draw(self.screen) 
            pygame.display.flip()      
            pygame.display.update()
            self.clock.tick(60)

class Board:
    def __init__(self, Board_width,Board_height, Board_margin,general_column,general_row) :
        self.rowno=general_row
        self.colno=general_column
        self.Board_width=Board_width
        self.Board_height=Board_height
        self.Board_margin=Board_margin
       
    def draw(self,screen):                    
        BLACK = (0, 0, 0)  
        BACKGROUND_COLOR = (178, 190, 195)  # Light gray-blue
        LIGHT_TILE_COLOR = (238, 245, 248)  # Very light gray-blue
        DARK_TILE_COLOR = (207, 219, 223)
        WHITE = (255, 255, 255)  

        screen.fill(BACKGROUND_COLOR)

        
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / self.colno
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / self.rowno

        for col in range(self.colno):
            for row in range(self.rowno):
        # Calculate the position of each tile
                x = self.Board_margin + col * self.tile_W
                y = self.Board_margin + row * self.tile_H
                color = DARK_TILE_COLOR if (row + col) % 2 == 0 else LIGHT_TILE_COLOR
                pygame.draw.rect(screen, color, [x, y, self.tile_W, self.tile_H])#,width=1,border_bottom_left_radius=10) #border_radius=50,)

        '''
        or 
        self.bg_rect[pygam.rect((col+int(row % 2 == 0))*cell siza,row * xell-cize,cell_size,cel_size)
                    for col in range(0,cols,2) for row in range(rows)]
        '''

        

class Snake:
    def __init__(self,Board_width,Board_height,Board_margin, general_column, general_row,start_lentgh=3,start_col=5,start_row=5) :
        self.Board_width=Board_width
        self.Board_height=Board_height
        self.Board_margin=Board_margin
        self.start_lentgh=start_lentgh
        self.start_col=start_col
        self.start_row=start_row
        self.general_column=general_column
        self.general_row=general_row
        self.body=[pygame.Vector2(self.start_col- col,self.start_row) for col in range(self.start_lentgh)]

    def draw(self,screen):
        purple=(128, 0, 128)

        rowno=copy.copy(general_row)
        colno=copy.copy(general_column)
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / colno
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / rowno
        
        for point in self.body:
            rect=pygame.Rect((int(point.x)*self.tile_W) + self.Board_margin,(int(point.y)*self.tile_H) +self.Board_margin,self.tile_W,self.tile_H)
            pygame.draw.rect(screen,purple,rect)

class Fruit:
    def __init__(self,Board_width,Board_height,Board_margin, general_column, general_row,Snake):
        self.Board_width=Board_width
        self.Board_height=Board_height
        self.Board_margin=Board_margin
        self.general_column=general_column
        self.general_row=general_row
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / self.general_column
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / self.general_row
        self.snake=Snake(Board_width,Board_height,Board_margin, general_column, general_row)
        self.set_pos()
    
    def set_pos(self) -> list:

        self.occupied_pos=self.snake.body
        available_pos=[]
        self.positions=[pygame.Vector2(col,row) for col in range(self.general_column) for row in range(self.general_row)]
        for position in self.positions:
            if position not in self.occupied_pos:
                available_pos.append([position.x,position.y])

        self.pos=choice(available_pos)
        return self.pos

    def draw(self,screen):
        orange=(255, 165, 0)
        rect=pygame.Rect((int(self.pos[0])*self.tile_W) + self.Board_margin,
                         (int(self.pos[1])*self.tile_H) + self.Board_margin,
                         self.tile_W,self.tile_H)
        pygame.draw.rect(screen,orange,rect)
         

game().run()