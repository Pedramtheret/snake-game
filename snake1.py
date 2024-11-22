import pygame
import sys
import copy
from random import choice
from queue import PriorityQueue


Board_width=600
Board_height=600
Board_margin=10
general_row, general_column=10, 10
player_score=0

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
        
        self.estimation=[]
        self.clock=pygame.time.Clock()
        self.neighbors=[]

        self.player_score=player_score

        self.paused= False
        self.show_path=False    ### to edit(it should change with every space)
        self.path_found= False

        self.move_event=pygame.event.custom_type()
        pygame.time.set_timer(self.move_event,300)

        pygame.font.init()

           

    def h(self,p1,p2):
        x1, y1=p1
        x2, y2=p2
        return abs(x1 - x2) + abs(y1 - y2)
    
    '''
    def reconstruct_path(self,came_from,current):
        path = [current]
        while current in came_from:
            current= came_from[current]
            path.append(current)
            return path[::-1]
    '''

    def algorithm(self):

        if self.path_found:
            return None
        

        head_pos=self.snake.body[0]
        body_pos=self.snake.body[1:]
        fruit_pos=self.fruit.pos

        grid=[[0] * self.board.rowno for _ in range(self.board.colno)]


        for position in body_pos:
            grid[int(position.x)][int(position.y)]=1
        
        print(grid)

        
        counter=0
        openset=PriorityQueue()
        openset.put((0, counter, (int(head_pos.x), int(head_pos.y)))) #importent to use two ()
        came_from={}
        g_score = {(x, y): float('inf') for x in range(len(grid)) for y in range(len(grid[0]))} 
        g_score[(int(head_pos.x), int(head_pos.y))] = int(0)
        f_score = {(x, y): float('inf') for x in range(len(grid)) for y in range(len(grid[0]))}
        f_score[(int(head_pos.x), int(head_pos.y))]= self.h([int(head_pos.x),int(head_pos.y)], [int(fruit_pos[0]), int(fruit_pos[1])])

        openset_hash={(int(head_pos.x),int(head_pos.y))}

        
        while not openset.empty():    

            current=openset.get()[2]
            openset_hash.remove((int(current[0]),int(current[1])))
            current=(int(current[0]), int(current[1]))
            #print(f"Current: {current}")

            neighbors_list=[]
            if (0 <= current[0] + 1 < self.board.rowno
                and 0 <= current[1] < self.board.colno 
                and grid[int(current[0]+1)][int(current[1])] != 1 ):
                neighbors_list.append((current[0]+1,current[1]))

            if (0 <= current[0] - 1 < self.board.rowno
                and 0 <= current[1] < self.board.colno
                and grid[int(current[0] - 1)][int(current[1])] != 1 ):
                neighbors_list.append((current[0] - 1,current[1]))

            if (0 <= current[0] < self.board.rowno
                and 0 <= current[1] + 1 < self.board.colno
                and grid[int(current[0])][int(current[1] + 1)] != 1 ):
                neighbors_list.append((current[0],current[1] + 1))

            if (0 <= current[0] < self.board.rowno
                and 0 <= current[1] - 1 < self.board.colno
                and grid[int(current[0])][int(current[1] - 1)] != 1 ):
                neighbors_list.append((current[0],current[1] - 1))

            #print(f"Current: {current}, Neighbors: {neighbors_list}")
            
            if current == (int(fruit_pos[0]), int(fruit_pos[1])):
                    path = [current]
                    while current in came_from:
                        current = came_from[current]
                        path.append(current)
                    
                    self.path_found = True
                    return path[::-1]
                    
            #openset.remove(current)
                        
                    
                

            for neighbor in neighbors_list:

                    temp_g_score=g_score[(int(current[0]), int(current[1]))] + 1
                    if temp_g_score < g_score[(int(neighbor[0]), int(neighbor[1]))]:
                        came_from[(int(neighbor[0]),int(neighbor[1]))] =  (int(current[0]), int(current[1]))
                        g_score[(int(neighbor[0]), int(neighbor[1]))] = temp_g_score
                        f_score[(int(neighbor[0]), int(neighbor[1]))] = temp_g_score + self.h([int(current[0]),int(current[1])],
                                                                   [int(fruit_pos[0]), int(fruit_pos[1])])
                        if neighbor not in openset_hash:
                            counter += 1
                            openset.put((f_score[(int(neighbor[0]), int(neighbor[1]))], counter, neighbor))
                            openset_hash.add((int(neighbor[0]), int(neighbor[1])))
                            print(f"Neighbor added: {neighbor} with f_score {f_score[neighbor]}")
        
                
        return None
    
    def draw_path(self,screen,path):
        if path:
            self.path_found = False

            for point in path:
                
                Canary=(255, 255, 143)
                rect=pygame.Rect( (int(point[0]) * self.board.tile_W) + self.board.Board_margin, 
                                 (int(point[1]) * self.board.tile_H) + self.board.Board_margin, 
                                 self.board.tile_W, self.board.tile_H)
                pygame.draw.rect(screen, Canary,rect)
            pygame.display.flip()
        print('printed')
        
            
            #pygame.display.update() 
            


    def input(self):
        keys=pygame.key.get_pressed()    #you can't pause with this
        if keys[pygame.K_RIGHT]:
            if self.snake.direction.x != -1:
                self.snake.direction=pygame.Vector2(1,0)
        if keys[pygame.K_LEFT]:
            if self.snake.direction.x != 1:
                self.snake.direction=pygame.Vector2(-1,0)
        if keys[pygame.K_UP]:
            if self.snake.direction.y != 1:
                self.snake.direction=pygame.Vector2(0,-1)
        if keys[pygame.K_DOWN]:
            if self.snake.direction.y != -1:
                self.snake.direction=pygame.Vector2(0,1)

        


            

    def eat(self):
        body_copy=self.snake.body[:]
        new_head=body_copy[0]+ self.snake.direction
        body_copy.insert(0,new_head)
        self.snake.body=body_copy[:]
        self.fruit.set_pos()

    '''
    def estimate_util(self, snake_body):
    
        snake_copy=snake_body[:]        
        counter=0
        possible_direction=[
            pygame.Vector2(1,0),
            pygame.Vector2(-1,0),
            pygame.Vector2(0,1),
            pygame.Vector2(0,-1)           
        ]

        if snake_copy[0]==self.fruit.pos:
            return True
        
        for direction in possible_direction:
            new_head=snake_copy[0] + direction
            if self.snake.is_safe(snake_copy, new_head):
                snake_copy.insert(0 , new_head)
                self.estimation_pos=pygame.Rect((int(new_head.x)*self.snake.tile_W) + self.snake.Board_margin,
                                 (int(new_head.y)*self.snake.tile_H) +self.snake.Board_margin,
                                 self.snake.tile_W,self.snake.tile_H)
                self.estimation.append(self.estimation_pos)               
                if self.estimate_util(snake_copy):
                    return True
                self.estimation.pop()
                snake_copy.pop(0)
            
        return False
    
    def draw_estimate(self):
        Canary=(255, 255, 143)
        for point in self.estimation:
            pygame.draw.rect(self.screen, Canary, point)
    '''

    def score(self):
        
        self.player_score+=1

    def display_score(self, score_textX : int, score_textY : int,screen):
        BLACK = (0, 0, 0) 
        WHITE = (255, 255, 255)
        
        self.score_text=pygame.font.Font('freesansbold.ttf',32)
        self.score_textX=score_textX
        self.score_textY=score_textY

        screen_text= self.score_text.render(f"total score: {self.player_score}",True,BLACK)
        screen.blit(screen_text,(self.score_textX,self.score_textY))
    
    

    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type ==self.move_event and not self.paused:
                    if self.snake.body[0]==self.fruit.pos :
                        self.eat()
                        self.score()
                    else:
                        #self.estimate_util(self.snake.body)
                        self.snake.move()

                   
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #self.show_path = not self.show_path ## Idk should keep it or not
                    print("Spacebar pressed!")
                    self.paused= not self.paused
                    self.show_path= not self.show_path
                    print(self.paused)
                    print(self.show_path)
                     
                
            self.input()

            #updates
            if not self.paused:
    
                if not self.snake.is_safe(self.snake.body, self.snake.body[0]):
                    self.snake.reset()
                    self.player_score=0
            
            #drawing
            self.board.draw(self.screen)
            self.board.draw(self.screen)
            self.display_score(100,100,self.screen)
            self.snake.draw(self.screen) 
            self.fruit.draw(self.screen) 
            #self.draw_estimate()
            

            if self.paused and  self.show_path:
                if not self.path_found:
                    print("Path should be displayed now.")
                    path=self.algorithm()
                
                if path:
                    print(f"Path found: {path}")
                    self.draw_path(self.screen, path)
                    
                else:
                    print("No path found.")
                    

            
            else:
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

        rowno=copy.copy(general_row)
        colno=copy.copy(general_column)
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / colno
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / rowno

        self.body=[pygame.Vector2(self.start_col- col,self.start_row) for col in range(self.start_lentgh)]
        
        self.direction=pygame.Vector2(1,0) #todo: snake should not move before pressing any key

    def move(self):
        body_copy=self.body[:-1]
        new_head=body_copy[0]+ self.direction
        body_copy.insert(0,new_head)
        self.body=body_copy[:]

    def draw(self,screen):
        purple=(128, 0, 128)
        
        for point in self.body:
            rect=pygame.Rect((int(point.x)*self.tile_W) + self.Board_margin,
                             (int(point.y)*self.tile_H) +self.Board_margin,
                             self.tile_W,self.tile_H)
            pygame.draw.rect(screen,purple,rect)

    def reset(self):
        self.body=[pygame.Vector2(self.start_col - col,self.start_row) for col in range(self.start_lentgh)]
        self.direction=pygame.Vector2(1,0) #todo: snake should not move before pressing any key

    def is_safe(self, snake_body, snake_head)  :
                
        body_copy=snake_body[:]
        body_body=body_copy[1:]
        for char in body_body:
            if char==snake_head: #better to write: if body_copy[0] not in body_copy[1:]: return false
                return False
            
        if not self.Board_margin -self.tile_W <= snake_head.x * self.tile_W <= (self.Board_width - self.Board_margin - self.tile_W):
            return False
        if not self.Board_margin - self.tile_H <= snake_head.y * self.tile_H <= (self.Board_height - self.Board_margin - self.tile_W):
            return False
        
        return True
        
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