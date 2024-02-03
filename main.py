import pygame
import random

pygame.init()

WIN_W = 400
WIN_H = 400

FPS = 60

screen = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption('15 game')

class CUBE():
    def __init__(self, number, x, y):
        if not number == 16:
            self.image = pygame.image.load("%d.png" % (number))
        self.cube_size = 100
        self.number = number
        self.cube_pos = (x * self.cube_size, y * self.cube_size)

    def draw(self):
        if not self.number == 16:
            screen.blit(self.image, self.cube_pos)

    def click(self, pos):
        if self.cube_pos[0] <= pos[0] and self.cube_pos[0] + self.cube_size >= pos[0] and self.cube_pos[1] <= pos[1] and self.cube_pos[1] + self.cube_size >= pos[1]:
            return self.number

    def update(self, new_x, new_y):
        if not new_y:
            if new_x == 1:
                new_x = self.cube_pos[0]/self.cube_size + 1
            else:
                new_x = self.cube_pos[0]/self.cube_size - 1
            self.cube_pos = (new_x * self.cube_size, self.cube_pos[1])
            return
        if not new_x:
            if new_y == 1:
                new_y = self.cube_pos[1]/self.cube_size + 1
            else:
                new_y = self.cube_pos[1]/self.cube_size - 1
            self.cube_pos = (self.cube_pos[0], new_y * self.cube_size)
            return

class InfoText():
    def draw_text(self):
        font1 = pygame.font.Font('GAMERIA.ttf', 60)
        font2 = pygame.font.Font('GAMERIA.ttf', 24)
        text_for_show1 = "YOU WIN"
        text_for_show2 = "your score %d" % (game_engine.moves)
        text1 = font1.render(text_for_show1, True, (51,25,0))
        text2 = font2.render(text_for_show2, True, (51,25,0))
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (WIN_W // 2, WIN_H // 2 - 15)
        textRect2.center = (WIN_W // 2, WIN_H // 2 + 25)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)


class ENGINE():
    def __init__(self):
        self.game_win = False
        self.cube = []
        self.text = InfoText()
        self.board_matrix = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 ]
        self.reset()

    def draw(self):
        for obj in self.cube:
            obj.draw()
        
        if self.game_win:
            self.text.draw_text()

    def check_for_clicked(self, pos):
        for x, obj in enumerate(self.cube):
            a = obj.click(pos)

            if a:
                if not (x - 4 < 0):
                    if self.board_matrix[x - 4] == 16:
                        self.board_matrix[x - 4] = self.board_matrix[x]
                        self.board_matrix[x] = 16
                        self.cube.remove(self.cube[x])
                        self.cube.remove(self.cube[x-4])
                        self.cube.insert(x-4,obj)
                        self.cube.insert(x,self.tmp_obj)
                        obj.update(0, -1)
                        self.moves += 1
                        return
                if not (x - 1 < 0):
                    if self.board_matrix[x - 1] == 16:
                        self.board_matrix[x - 1] = self.board_matrix[x]
                        self.board_matrix[x] = 16
                        self.cube.remove(self.cube[x])
                        self.cube.insert(x-1,obj)
                        obj.update(-1, 0)
                        self.moves += 1
                        return
                if not (x + 4 > len(self.board_matrix) - 1):
                    if self.board_matrix[x + 4] == 16:
                        self.board_matrix[x + 4] = self.board_matrix[x]
                        self.board_matrix[x] = 16
                        self.tmp_obj = self.cube[x+4]
                        self.cube.remove(self.cube[x])
                        self.cube.remove(self.cube[x+3])
                        self.cube.insert(x+3,obj)
                        self.cube.insert(x,self.tmp_obj)
                        obj.update(0, 1)
                        self.moves += 1
                        return
                if not (x + 1 > len(self.board_matrix) - 1):
                    if self.board_matrix[x + 1] == 16:
                        self.board_matrix[x + 1] = self.board_matrix[x]
                        self.board_matrix[x] = 16
                        self.cube.remove(self.cube[x])
                        self.cube.insert(x+1,obj)
                        obj.update(1, 0)
                        self.moves += 1
                        return
        
    def check_win(self):
        self.game_win = True
        for x, obj in enumerate(self.board_matrix):
            if obj != x+1:
                self.game_win = False
                return False

    def reset(self):
        self.game_win = False
        self.cube.clear()
        self.board_matrix.pop()
        random.shuffle(self.board_matrix)
        self.board_matrix.append(16)
        self.moves = 0
        pos_x = 0
        pos_y = 0
        for x in self.board_matrix:
            self.cube.append(CUBE(x, pos_x, pos_y))
            if pos_x == 3:
                pos_x = 0
                pos_y += 1
            else:
                pos_x += 1
            
GAME_CLOCK = pygame.time.Clock()
game_engine = ENGINE()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_engine.reset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_engine.game_win:
                game_engine.check_for_clicked(pygame.mouse.get_pos())
                game_engine.check_win()

    screen.fill((232,78,24))
    game_engine.draw()
    GAME_CLOCK.tick(FPS)
    pygame.display.update()

pygame.quit()
exit()