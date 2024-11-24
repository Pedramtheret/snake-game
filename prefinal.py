import pygame
import sys
import copy
from random import choice
from queue import PriorityQueue
from os import walk
from os.path import join
from math import sin


Board_width=800
Board_height=800
Board_margin=0
general_row, general_column=10, 10
player_score=0


class autogame:

    def __init__(self) :
        pygame.init()

        pygame.display.set_caption('snake game')

        global Board_width
        global Board_height
        global general_row,general_column

        self.screen=pygame.display.set_mode((Board_width,Board_height))
        self.board=Board(Board_width,Board_height,Board_margin, general_column, general_row)
        self.snake=Snake(Board_width, Board_height, Board_margin, general_column, general_row)
        self.fruit=Fruit(Board_width, Board_height, Board_margin, general_column, general_row)
        
        self.estimation=[]
        self.clock=pygame.time.Clock()
        self.neighbors=[]

        self.player_score=player_score

        self.paused= False
        self.show_path=False    ### to edit(it should change with every space)
        self.path_found= False
        self.path= None

        self.move_event=pygame.event.custom_type()
        pygame.time.set_timer(self.move_event,4000)
        self.game_active= False


        pygame.font.init()

           

    def h(self,p1,p2):
        x1, y1=p1
        x2, y2=p2
        return abs(x1 - x2) + abs(y1 - y2)
    
    def algorithm(self):

        head_pos=self.snake.body[0]
        body_pos=self.snake.body[1:]
        fruit_pos=self.fruit.pos

        grid=[[0] * self.board.rowno for _ in range(self.board.colno)]

        for position in body_pos:
            grid[int(position.x)][int(position.y)]=1
               
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
            
            if current == (int(fruit_pos[0]), int(fruit_pos[1])):
                    path = [current]
                    while current in came_from:
                        current = came_from[current]
                        path.append(current)
                
                    path=path[:-1]
                    path=path[::-1]
                    return path          

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
                            #print(f"Neighbor added: {neighbor} with f_score {f_score[neighbor]}")
            
        return None
    
    def draw_path(self,screen,path):
        if path:
            #self.path_found = False

            for point in path:
                
                Canary=(255, 255, 143)
                rect=pygame.Rect( (int(point[0]) * self.board.tile_W) + self.board.Board_margin, 
                                 (int(point[1]) * self.board.tile_H) + self.board.Board_margin, 
                                 self.board.tile_W, self.board.tile_H)
                pygame.draw.rect(screen, Canary,rect)
            pygame.display.flip()

            
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

    def auto(self): 
        if self.path:
            next_pos=self.path[0]
            current_pos=self.snake.body[0]

            direction_x=next_pos[0] - current_pos[0]
            direction_y=next_pos[1] - current_pos[1]

            self.snake.direction=pygame.Vector2(direction_x, direction_y)
            self.path.pop(0)

    def eat(self):
        
        body_copy=self.snake.body[:]
        if  (0 <= int(body_copy[0].x+ self.snake.direction.x) < self.board.colno 
             and 0 <= int(body_copy[0].y+ self.snake.direction.y) < self.board.colno ):
            new_head=body_copy[0]+ self.snake.direction
            
        else:

            new_direction= pygame.Vector2(int(self.snake.direction.y),int(self.snake.direction.x))
            if (0 <= int(body_copy[0].x+ new_direction.x) < self.board.colno 
             and 0 <= int(body_copy[0].y+ new_direction.y) < self.board.colno ):
                new_head=body_copy[0]+ new_direction
                
            else:
                new_head=body_copy[0]+ pygame.Vector2(int(new_direction.x) * -1,int(new_direction.y)* -1)
            
        body_copy.insert(0,new_head)
        self.snake.body=body_copy[:]

        #self.snake.new_block = True
        self.fruit.set_pos(self.snake.body)

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
                
                '''
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #self.show_path = not self.show_path ## Idk should keep it or not
                    print("Spacebar pressed!")
                    self.paused= not self.paused
                    self.show_path= not self.show_path
                    print(self.paused)
                    print(self.show_path)
                '''
                if event.type == pygame.KEYDOWN  and not self.game_active:
                    self.game_active=True
            
            if self.snake.body[0]==self.fruit.pos :
                self.eat()
                self.score()
                self.path=self.algorithm()

            else:
                if self.path and self.game_active:            #self.estimate_util(self.snake.body)
                    self.auto()
                    self.snake.move()
                else:
                    self.path=self.algorithm()

            #updates
            if not self.paused:
    
                if not self.snake.is_safe(self.snake.body, self.snake.body[0]):
                    self.snake.reset()
                    self.game_active=False
                    self.player_score=0
                    self.path= None

            #drawing
            self.screen.fill((0, 0, 0)) 
            self.board.draw(self.screen)
            self.board.draw(self.screen)
            
            self.snake.draw(self.screen) 
            self.fruit.draw(self.screen) 
            #self.draw_estimate()

            if self.path:
                self.draw_path(self.screen, self.path)
             

            self.display_score(100,100,self.screen)    
            pygame.display.flip()
            pygame.display.update() 

            self.clock.tick(2)


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
        self.fruit=Fruit(Board_width, Board_height, Board_margin, general_column, general_row)
        
        self.estimation=[]
        self.clock=pygame.time.Clock()
        self.neighbors=[]

        self.player_score=player_score

        self.paused= False
        self.show_path=False    ### to edit(it should change with every space)
        self.path_found= False

        self.move_event=pygame.event.custom_type()
        pygame.time.set_timer(self.move_event,300)
        self.game_active=False

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
                    path=path[1:-1]
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
        self.fruit.set_pos(self.snake.body)

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
                if event.type ==self.move_event and not self.paused and self.game_active:
                    if self.snake.body[0]==self.fruit.pos :
                        self.eat()
                        self.score()
                    else:
                        #self.estimate_util(self.snake.body)
                        self.snake.move()

                   
                elif event.type == pygame.KEYDOWN:
                    if not self.game_active:
                        self.game_active= True
                    if event.key == pygame.K_SPACE:

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
                    self.game_active=False
            
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

        self.surfs= self.import_surfs()
        self.head_surf=self.surfs['head_right']
        self.tail_surf=self.surfs['tail_left']
        self.draw_data = []


        rowno=copy.copy(general_row)
        colno=copy.copy(general_column)
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / colno
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / rowno

        self.body=[pygame.Vector2(self.start_col- col,self.start_row) for col in range(self.start_lentgh)]
        
        self.direction=pygame.Vector2(1,0) #todo: snake should not move before pressing any key

    def update_body(self):
        self.draw_data=[]                    #to just show one_head
        #print(self.surfs)
        for index, part in enumerate(self.body):           ##check
            #position
            x= part.x * self.tile_W
            y=part.y * self.tile_H 
            rect=pygame.Rect(x+self.Board_margin,y+self.Board_margin,self.tile_W,self.tile_H)

            if index==0:
                self.draw_data.append((self.head_surf,rect))      ##should be a tuple
            elif index == len(self.body)-1:
                self.draw_data.append((self.tail_surf,rect))
            else:
                last_part=self.body[index + 1] - part
                next_part=self.body[index - 1] - part
                if last_part.x == next_part.x :
                    self.draw_data.append((self.surfs['body_horizontal'],rect))
                elif last_part.y == next_part.y :
                    self.draw_data.append((self.surfs['body_vertical'],rect))
                else :
                    if last_part.x ==-1 and next_part.y ==-1 or last_part.y==-1 and next_part.x==-1:
                        self.draw_data.append((self.surfs['body_tl'],rect))
                    elif last_part.x ==-1 and next_part.y ==1 or last_part.y==1 and next_part.x==-1:
                        self.draw_data.append((self.surfs['body_bl'],rect))
                    if last_part.x ==1 and next_part.y ==-1 or last_part.y==-1 and next_part.x==1:
                        self.draw_data.append((self.surfs['body_tr'],rect))
                    if last_part.x ==1 and next_part.y ==1 or last_part.y==1 and next_part.x==1:
                        self.draw_data.append((self.surfs['body_br'],rect))




    def import_surfs(self):
        surf_dict={}
        print(1)
        folder_path = "D:\workplace\AP\projects\Snake_NetNinja-main\Snake_NetNinja-main\graphics\snake"
        print(1)
        for folder_path, _, image_names in walk(folder_path):         ##check
            #print(2)
            for image_name in image_names:
                #print('blah')
                full_path= join(folder_path, image_name)
                surface=pygame.image.load(full_path).convert_alpha()      ##check
                surf_dict[image_name.split('.')[0]]=surface
                #print(surf_dict)
            return surf_dict
        
    def update_head(self):
        head_realtion=self.body[1]-self.body[0]
        if head_realtion==pygame.Vector2(-1,0): self.head_surf=self.surfs['head_right']
        elif head_realtion==pygame.Vector2(+1,0): self.head_surf=self.surfs['head_left']
        elif head_realtion==pygame.Vector2(0,-1): self.head_surf=self.surfs['head_down']
        elif head_realtion==pygame.Vector2(0,1): self.head_surf=self.surfs['head_up']

    def update_tail(self):
        tail_relation=self.body[-2]-self.body[-1]
        if tail_relation==pygame.Vector2(-1,0): self.tail_surf=self.surfs['tail_right']
        elif tail_relation==pygame.Vector2(+1,0): self.tail_surf=self.surfs['tail_left']
        elif tail_relation==pygame.Vector2(0,-1): self.tail_surf=self.surfs['tail_down']
        elif tail_relation==pygame.Vector2(0,1): self.tail_surf=self.surfs['tail_up']


    def move(self):
        body_copy=self.body[:-1]
        new_head=body_copy[0]+ self.direction
        body_copy.insert(0,new_head)
        self.body=body_copy[:]

        self.update_head()
        self.update_tail()
        self.update_body()
        

    def draw(self,screen):
        purple=(128, 0, 128)
        for surf, rect in self.draw_data:
            screen.blit(surf, rect)

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
    def __init__(self,Board_width,Board_height,Board_margin, general_column, general_row):
        self.Board_width=Board_width
        self.Board_height=Board_height
        self.Board_margin=Board_margin
        self.general_column=general_column
        self.general_row=general_row
        self.tile_W = (self.Board_width - 2 * self.Board_margin) / self.general_column
        self.tile_H = (self.Board_height - 2 * self.Board_margin) / self.general_row
        self.snake= Snake(Board_width,Board_height,Board_margin, general_column, general_row)
        self.set_pos(self.snake.body)


        apple_path= r"D:\workplace\AP\projects\Snake_NetNinja-main\Snake_NetNinja-main\graphics\apple.png"
        self.surf=pygame.image.load(apple_path).convert_alpha()
    def set_pos(self,snake_body) -> list:

        self.snake_body= snake_body
        self.occupied_pos=self.snake_body
        available_pos=[]
        self.positions=[pygame.Vector2(col,row) for col in range(self.general_column) for row in range(self.general_row)]
        for position in self.positions:
            if position not in self.occupied_pos:
                available_pos.append([position.x,position.y])

        self.pos=choice(available_pos)
        return self.pos

    def draw(self,screen):
        '''
        orange=(255, 165, 0)
        rect=pygame.Rect((int(self.pos[0])*self.tile_W) + self.Board_margin,
                         (int(self.pos[1])*self.tile_H) + self.Board_margin,
                         self.tile_W,self.tile_H)
        pygame.draw.rect(screen,orange,rect)
        '''
        scale = 1 + sin(pygame.time.get_ticks() / 600) / 3
        self.scaled_surf = pygame.transform.smoothscale_by(self.surf, scale)
        self.scaled_rect = self.scaled_surf.get_rect(center = (int(self.pos[0]) * 80 + 80/ 2, int(self.pos[1]) * 80 +80 / 2))

        screen.blit(self.scaled_surf, self.scaled_rect)



autogame().run()