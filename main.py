import pygame
import random
import os

#win conditions dont work
#delaer takes more cards than suposed to
#test if compiter has blackjack already
#more money for if blackjack
#logic for aces

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
title_font = pygame.font.SysFont('Comic Sans MS', 70)
button_font = pygame.font.SysFont('Comic Sans MS', 60)
normal_font = pygame.font.SysFont('Comic Sans MS', 35)
bet_font = pygame.font.SysFont('Comic Sans MS', 30)

active_screen = 1
card_index = { 52: '2_of_clubs.png', 1: '3_of_clubs.png', 2: '4_of_clubs.png', 3: '5_of_clubs.png', 4: '6_of_clubs.png', 5: '7_of_clubs.png', 6: '8_of_clubs.png', 7: '9_of_clubs.png', 8: '10_of_clubs.png', 9: 'jack_of_clubs.png', 10: 'queen_of_clubs.png', 11: 'king_of_clubs.png', 12: 'ace_of_clubs.png', 13: '2_of_diamonds.png', 14: '3_of_diamonds.png', 15: '4_of_diamonds.png', 16: '5_of_diamonds.png', 17: '6_of_diamonds.png', 18: '7_of_diamonds.png', 19: '8_of_diamonds.png', 20: '9_of_diamonds.png', 21: '10_of_diamonds.png', 22: 'jack_of_diamonds.png', 23: 'queen_of_diamonds.png', 24: 'king_of_diamonds.png', 25: 'ace_of_diamonds.png', 26: '2_of_hearts.png', 27: '3_of_hearts.png', 28: '4_of_hearts.png', 29: '5_of_hearts.png', 30: '6_of_hearts.png', 31: '7_of_hearts.png', 32: '8_of_hearts.png', 33: '9_of_hearts.png', 34: '10_of_hearts.png', 35: 'jack_of_hearts.png', 36: 'queen_of_hearts.png', 37: 'king_of_hearts.png', 38: 'ace_of_hearts.png', 39: '2_of_spades.png', 40: '3_of_spades.png', 41: '4_of_spades.png', 42: '5_of_spades.png', 43: '6_of_spades.png', 44: '7_of_spades.png', 45: '8_of_spades.png', 46: '9_of_spades.png', 47: '10_of_spades.png', 48: 'jack_of_spades.png', 49: 'queen_of_spades.png', 50: 'king_of_spades.png', 51: 'ace_of_spades.png' }
faces = 'jqk'
deck = []
index = 0
playerCard_X = 10
playerCard_Y = 390
dealerCard_X = 658
dealerCard_Y = 55
money = 0
bet = 10
canBet = True
stick = False
score = 0
computer_score = 0
game_over = False
player_win = None
no_more_cards = False
tie = False
dealer_turn = False

with open('stats.txt', 'r') as file:
    for line in file.readlines():
        money = int(line.strip())

class Card():
    def __init__(self,path,x,y,hidden):
        self.value = path[0]

        if hidden == 'None':
            img = pygame.image.load(os.path.join('cards', path))
        
        if hidden == 'back.png':
            img = pygame.image.load(os.path.join('cards', hidden))
            self.alterImg = pygame.image.load(os.path.join('cards', path))
            self.alterImg = pygame.transform.scale(self.alterImg,(132,200))
        self.img = pygame.transform.scale(img,(132,200))

        self.x = x
        self.y = y
    
    def draw(self):
        screen.blit(self.img,(self.x,self.y))

def shuffle():
    global deck
    global index
    index = 0
    deck = random.sample(range(1,53),52)

shuffle()

player_cards = []
dealer_cards = []

def new_card(player,amount,hidden):
    global playerCard_X
    global dealerCard_X
    global index
    for i in range(amount):
        if player:
            player_cards.append(Card(card_index[deck[index]],playerCard_X,playerCard_Y,'None'))
            playerCard_X += 100
            index += 1
        elif not player:
            if hidden:
                dealer_cards.append(Card(card_index[deck[index]],dealerCard_X,dealerCard_Y,'back.png'))
            elif not hidden:
                dealer_cards.append(Card(card_index[deck[index]],dealerCard_X,dealerCard_Y,'None'))
            dealerCard_X -= 100
            index += 1

def start_menu():
    screen.fill((43, 102, 57))

    title_text = title_font.render('Blackjack!', False, (255,255,255))
    text_rect = title_text.get_rect(center=(SCREEN_WIDTH/2,100))
    screen.blit(title_text, text_rect)

    pygame.draw.rect(screen, (0,0,0),(200,200,400,75))
    pygame.draw.rect(screen, (255,255,255),(205,205,390,65))

    start_text = button_font.render('Start',False,(0,0,0))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2,232.5))
    screen.blit(start_text,start_rect)

def draw_game():
    screen.fill((43, 102, 57))
    
    pygame.draw.rect(screen,(0,0,0),(10,290,40,40))
    pygame.draw.rect(screen,(255,255,255),(12,292,36,36))
    down_text = bet_font.render('-',False,(0,0,0))
    down_rect = down_text.get_rect(center=(30,310))
    screen.blit(down_text,down_rect)

    pygame.draw.rect(screen,(0,0,0),(60,290,150,40))
    pygame.draw.rect(screen,(255,255,255),(62,292,146,36))
    bet_text = bet_font.render(f'${bet}',False,(0,0,0))
    bet_rect = bet_text.get_rect(center=(135,310))
    screen.blit(bet_text,bet_rect)

    pygame.draw.rect(screen,(0,0,0),(220,290,40,40))
    pygame.draw.rect(screen,(255,255,255),(222,292,36,36))
    down_text = bet_font.render('+',False,(0,0,0))
    down_rect = down_text.get_rect(center=(240,310))
    screen.blit(down_text,down_rect)

    pygame.draw.rect(screen,(0,0,0),(270,290,150,40))
    pygame.draw.rect(screen,(255,255,255),(272,292,146,36))
    placeBet_text = bet_font.render('Place Bet',False,(0,0,0))
    placeBet_rect = placeBet_text.get_rect(center=(345,310))
    screen.blit(placeBet_text,placeBet_rect)

    pygame.draw.rect(screen,(0,0,0),(710,290,80,40))
    pygame.draw.rect(screen,(255,255,255),(712,292,76,36))
    placeBet_text = bet_font.render('Stick',False,(0,0,0))
    placeBet_rect = placeBet_text.get_rect(center=(750,310))
    screen.blit(placeBet_text,placeBet_rect)

    pygame.draw.rect(screen,(0,0,0),(640,290,60,40))
    pygame.draw.rect(screen,(255,255,255),(642,292,56,36))
    placeBet_text = bet_font.render('Hit',False,(0,0,0))
    placeBet_rect = placeBet_text.get_rect(center=(670,310))
    screen.blit(placeBet_text,placeBet_rect)

    playerCards_text = normal_font.render('Your cards:', False, (255,255,255))
    screen.blit(playerCards_text, (10,340))

    cpuCards_text = normal_font.render('Computer cards:', False, (255,255,255))
    screen.blit(cpuCards_text, (520,1))

    money_text = normal_font.render(f'Money: ${money}', False, (255,255,255))
    screen.blit(money_text,(5,0))

    for card in player_cards:
        card.draw()

    for card in reversed(dealer_cards):
        card.draw()

def loose_screen():
    box = pygame.draw.rect(screen,(0,0,0),(200,237.5,400,75))
    pygame.draw.rect(screen,(255,255,255),(202,239.5,396,71))

    playAgain_text = normal_font.render('Play Again', False, (0,0,0))
    playAgain_rect = playAgain_text.get_rect(center=box.center)
    screen.blit(playAgain_text,playAgain_rect)
    
def updateScore():
    global score
    global computer_score

    score = 0
    for card in player_cards:
        try:
            score += int(card.value)
        except:
            if card.value in faces:
                score += 10
            
            elif card.value == 'a':
                score += 11
                #add logic for ace latter
    
    computer_score = 0
    for card in dealer_cards:
        try:
            computer_score += int(card.value)
        except:
            if card.value in faces:
                computer_score += 10
            
            elif card.value == 'a':
                computer_score += 11
                #add logic for ace latter

def check_win():
    global player_win
    global game_over
    global tie

    if score > 21:
        player_win = False
        game_over = True
    elif score <= 21 and computer_score > 21:
        player_win = True
        game_over = True
    elif score > computer_score and no_more_cards:
        player_win = True
        game_over = True
    elif score < computer_score and no_more_cards:
        player_win = False
        game_over = True
    elif score == computer_score and no_more_cards:
        tie = True
        game_over = True

def reset():
    global index,playerCard_X,playerCard_Y,dealerCard_X,dealerCard_Y,bet,canBet,stick,score,computer_score,game_over,player_win,no_more_cards,tie,dealer_turn,player_cards,dealer_cards
    shuffle()
    player_cards = []
    dealer_cards = []
    index = 0
    playerCard_X = 10
    playerCard_Y = 390
    dealerCard_X = 658
    dealerCard_Y = 55
    bet = 10
    canBet = True
    stick = False
    score = 0
    computer_score = 0
    game_over = False
    player_win = None
    no_more_cards = False
    tie = False
    dealer_turn = False

running = True
while running:
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 200 <= mouse_x <= 600 and 200 <= mouse_y <= 275 and active_screen == 1:
                active_screen = 2
            
            if 10 <= mouse_x <= 50 and 290 <= mouse_y <= 330 and active_screen == 2 and bet != 10 and canBet:
                bet -= 10
            elif 220 <= mouse_x <= 260 and 290 <= mouse_y <= 330 and active_screen == 2 and (bet + 10) <= money and canBet:
                bet += 10
            elif 270 <= mouse_x <= 420 and 290 <= mouse_y <= 330 and active_screen == 2 and canBet:
                canBet = False
                new_card(True,2,False)
                new_card(False,1,False)
                new_card(False,1,True)
            elif 640 <= mouse_x <= 700 and 290 <= mouse_y <= 330 and active_screen == 2 and not canBet and stick == False and score <= 21:
                new_card(True,1,False)
            elif 710 <= mouse_x <= 790 and 290 <= mouse_y <= 330 and active_screen == 2 and not canBet and stick == False:
                dealer_cards[1].img = dealer_cards[1].alterImg
                stick = True
                dealer_turn = True
            elif 200 <= mouse_x <= 600 and 237.5 <= mouse_y <= 312.5 and active_screen == 3:
                reset()
                active_screen = 2

        if event.type == pygame.QUIT:
            with open ('stats.txt', 'w') as file:
                file.write(str(money))
            running = False

    if active_screen == 1:
        start_menu()

    elif active_screen == 2:
        check_win()

        if player_win == False:
            print('loose')
            active_screen = 3
            money -= bet
        
        elif player_win == True:
            print('win')
            active_screen = 3
            money += bet
        
        elif tie == True:
            print('tie')
            active_screen = 3

        if computer_score < 17 and dealer_turn:
            new_card(False,1,False)

        elif computer_score > 17 and dealer_turn:
            no_more_cards == True
            
        updateScore()
        draw_game()
    
    elif active_screen == 3:
        updateScore()
        draw_game()
        loose_screen()

    if index == 51:
        shuffle()

    pygame.display.flip()
    pygame.display.set_caption('Blackjack')

pygame.quit()