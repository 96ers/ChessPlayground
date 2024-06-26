import pygame
import os.path
import random
from copy import deepcopy
from define import *
from pieces import *
from tools import *
from AI import *
from AI_sunfish import AI_Sunfish


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = BLUE

    def draw_board(self, C):
        pygame.draw.rect(self.screen, C, (0, 0, SCREEN_SIZE, PIECE_SIZE))
        pygame.draw.rect(self.screen, C, (0, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, C, (SCREEN_SIZE-PIECE_SIZE, 0, PIECE_SIZE, SCREEN_SIZE))
        pygame.draw.rect(self.screen, C, (0, SCREEN_SIZE-PIECE_SIZE, SCREEN_SIZE-PIECE_SIZE, PIECE_SIZE))
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.color = WHITE
                else:
                    self.color = ORANGE
                pygame.draw.rect(self.screen, self.color,(PIECE_SIZE*(x+1), PIECE_SIZE*(y+1), PIECE_SIZE, PIECE_SIZE))


class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsansms", 35)
        self.font2 = pygame.font.SysFont("comicsansms", 72)
        board = Board(self.screen)
        pieces = Pieces(self.screen)
        cmate = -1
        cmate = self.Game_player_vs_AI_Minimax(board, pieces)
        self.Game_Over(board, pieces, cmate)

        pygame.quit()

    def Game_player_vs_AI_Minimax(self, board, pieces):

        cplayer = ['w', 'b']
        C = [BLUE, BLACK]
        player, cl, st, cmate = 0, -1, [], -1
        last_pos = ()
        #AI = AI_Minimax(pieces.ar, pieces)
        AI = AI_Sunfish(pieces.ar, pieces)
        AI_random = AI_stupid(pieces.ar, pieces)
        running = True
        while running:
            pos_clicked = ()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if player == 0 and pygame.mouse.get_pressed()[0]:
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue
            if player == 0:
                if pos_clicked != () and not check_valid(pos_clicked[0]-1, pos_clicked[1]-1):
                    cl -= 1
                    continue
                if pos_clicked != () and cl == 0:
                    pieces.selecting(pos_clicked)
                    st.append(pos_clicked)
                if pos_clicked != () and cl == 1:
                    if eq(st[0], pos_clicked):
                        cl -= 1
                        continue
                    if pieces.switch_piece(st[0], pos_clicked):
                        cl, st = -1, []
                        clean_selected(pieces.ar)
                        continue
                    if not pieces.move(pieces.ar, st[0], pos_clicked):
                        cl -= 1
                        continue
                    last_pos = (st[0], pos_clicked)
                    player, cl, st = 1 - player, -1, []
                    if pieces.is_checked(pieces.ar, cplayer[player]):
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False
            else: # player(AI) = 1 ar,pieces,type,alpha,beta,depth, last_move):
                pos = AI.minimax(pieces.ar,pieces,'b',-1000000000,1000000000,3,None,pieces.prev_move)
                if pos[1] == None:
                    p_random = AI_random.find_pos_random(pieces.ar, pieces, 'b')
                    if p_random == None:
                        cmate = 2
                        running = False
                    '''else:
                        print("It's confused\n")
                        pieces.move(pieces.ar, p_random[0], p_random[1])'''
                else:
                    pieces.selecting(pos[1])
                    pieces.move(pieces.ar, pos[1], pos[2])
                    print_ar(pieces.ar)
                    print(AI.eval_board(pieces.ar), pos[0],"\n")
                    last_pos = (pos[1], pos[2])
                    player = 1 - player
                    if pieces.is_checked(pieces.ar, cplayer[player]):
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False
            board.draw_board(C[player])
            pieces.draw_pieces_upgrade(last_pos)

            pygame.display.flip()
            self.clock.tick(20)
        return cmate

    def Game_Over(self, board, pieces, cmate):
        if cmate == -1:
            txt = "-= Never Give Up =-"
        elif cmate == 2:
            txt = "-= Draw =-"
        else:
            txt = "-= PLAYER "+str(cmate+1)+" WON! =-"
        txt = self.font.render(txt, True, GREEN)
        txt_center = (
            SCREEN_SIZE/2 - txt.get_width() // 2,
            50//2 - txt.get_height() // 2
        )
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            board.draw_board(BLUE)
            pieces.draw_pieces()
            self.screen.blit(txt, txt_center)

            pygame.display.flip()
            self.clock.tick(30)



if __name__ == '__main__':
    t = Game()
