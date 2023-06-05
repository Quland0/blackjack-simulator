import random
import tkinter
from tkinter.font import BOLD
import pygame
from PIL import Image, ImageTk

# функция для получения изображений карт с устройства
def getCardImages(card_images):
    suits = ['h', 'c', 'd', 's']

    for suit in suits:
        # добавление числовых карт от 1 до 10
        for card in range(1, 11):
            name = 'ccards/{}{}.png'.format(suit, card)
            image = tkinter.PhotoImage(file=name)
            card_images.append(('{}_of_{}'.format(card, suit), image))

        # добавление карт с лицами (валет, дама, король)
        faceCards = ['j', 'q', 'k']
        for card in faceCards:
            name = 'ccards/{}{}.png'.format(suit, card)
            image = tkinter.PhotoImage(file=name)
            card_images.append(('{}_of_{}'.format(card, suit), image))

# Инициализация pygame
pygame.init()

# Загрузка звуковых файлов
sound_win = pygame.mixer.Sound("sounds/win.wav")
sound_loss = pygame.mixer.Sound("sounds/loss.wav")

wins = 0
losses = 0

outcome_label = None

def getCard(frame):
    # берем карту сверху колоды
    next_card = deck.pop(0)
    # и добавляем ее в конец колоды
    deck.append(next_card)
    # показываем изображение карты в виджете Label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    # возвращаем карту
    return next_card


# Функция для подсчета общего значения карт в списке
def calcScore(hand):
    score = 0
    ace = False
    for next_card in hand:
        card_name = next_card[0]
        card_value = card_name.split('_')[0]

        if card_value == '1' and not ace:
            ace = True
            card_value = 11
        elif card_value in ['j', 'q', 'k']:
            card_value = 10
        else:
            card_value = int(card_value)

        score += card_value

        if score > 21 and ace:
            score -= 10
            ace = False

    return score

def showOutcomeImage(outcome):
    global outcome_label
    if outcome_label:
        outcome_label.destroy()
    
    if outcome == "win":
        image_path = "images/win.png"
    elif outcome == "loss":
        image_path = "images/loss.png"
    elif outcome == "draw":
        image_path = "images/draw.png"

    # Загрузите изображение
    image = Image.open(image_path)

    # Объект PhotoImage для отображения изображения в Tkinter
    photo = ImageTk.PhotoImage(image)

    # Создание виджета Label для отображения изображения
    outcome_label = tkinter.Label(gameWindow, image=photo)
    outcome_label.image = photo
    outcome_label.place(x=600, y=110)  # Координаты расположения изображения на экране
    update_stats(outcome)
    
    player_button.config(state="disabled")
    dealer_button.config(state="disabled")

    new_game_button.config(state="normal")

def update_stats(outcome):
    global wins
    global losses

    if outcome == "win":
        wins += 1
    elif outcome == "loss":
        losses += 1

    stats_label.config(text="Победы: {}  Поражения: {}".format(wins, losses))

# Показать победителя, когда игрок останавливается
def staying():
    dealer_score = calcScore(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(getCard(dealer_cardFrame))
        dealer_score = calcScore(dealer_hand)
        dealerScore.set(dealer_score)

    player_score = calcScore(player_hand)
    if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
        sound_loss.play()
        showOutcomeImage("loss")
        
    elif dealer_score > 21 or dealer_score < player_score:
        sound_win.play()
        showOutcomeImage("win")
        
    elif dealer_score == player_score:
        showOutcomeImage("draw")
       

# Показать победителя, когда игрок берет карту
def hitting():
    player_hand.append(getCard(player_card_frame))
    player_score = calcScore(player_hand)

    playerScore.set(player_score)
    if player_score > 21:
        winner.set("Дилер победил!")
        sound_loss.play()
        showOutcomeImage("loss")


def initial_deal():
    hitting()
    dealer_hand.append(getCard(dealer_cardFrame))
    dealerScore.set(calcScore(dealer_hand))
    hitting()

def new_game():
    global dealer_cardFrame
    global player_card_frame
    global dealer_hand
    global player_hand
    global outcome_label
    # Удаление картинки победителя
    winner.set("")

    

    
    # Удаление карт дилера
    for widget in dealer_cardFrame.winfo_children():
        widget.destroy()
        
    # Удаление карт игрока
    for widget in player_card_frame.winfo_children():
        widget.destroy()
    
    # Удаление картинки победителя
    if outcome_label:
        outcome_label.destroy()
    
    player_button.config(state="normal")
    dealer_button.config(state="normal")

    new_game_button.config(state="disabled")
    
    # Создание списков для хранения карт дилера и игрока
    dealer_hand = []
    player_hand = []
    
    # Начальная раздача карт
    initial_deal()

def shuffle():
    random.shuffle(deck)

def exit_game():
    gameWindow.destroy()

gameWindow = tkinter.Tk()

# Настройка окна и фреймов для дилера и игрока
gameWindow.title("Quland`s BJ")
gameWindow.geometry("1600x900")


# Добавление фоновой картинки
background_image = ImageTk.PhotoImage(Image.open("images/background.png"))
background_label = tkinter.Label(gameWindow, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

winner = tkinter.StringVar()
result = tkinter.Label(gameWindow, textvariable=winner, fg="white", bg="#307e61", font=('Verdana', 20, BOLD))
result.place(x=600, y=400)

player_score_frame = tkinter.Frame(gameWindow, bg="#307e61")
player_score_frame.place(x=175, y=400)

tkinter.Label(player_score_frame, text='Ваш счет:', fg='white', bg="#307e61", font=('Verdana', 15, BOLD)).grid(row=0, column=0, sticky=tkinter.E)

playerScore = tkinter.IntVar()
score_label = tkinter.Label(player_score_frame, textvariable=playerScore, fg='white', bg="#307e61", font=('Verdana', 15, BOLD))
score_label.grid(row=0, column=1)

dealer_score_frame = tkinter.Frame(gameWindow, bg="#307e61")
dealer_score_frame.place(x=175, y=90)

tkinter.Label(dealer_score_frame, text='Счет дилера:', fg='white', bg="#307e61", font=('Verdana', 15, BOLD)).grid(row=0, column=0, sticky=tkinter.E)

dealerScore = tkinter.IntVar()
dealer_score_label = tkinter.Label(dealer_score_frame, textvariable=dealerScore, fg='white', bg="#307e61", font=('Verdana', 15, BOLD))
dealer_score_label.grid(row=0, column=1)

stats_label = tkinter.Label(gameWindow, text="Победы: {}  Поражения: {}".format(wins, losses), fg="white", bg="#307e61", font=('Verdana', 15, BOLD))
stats_label.place(x=175, y=830)

# Создание фреймов для карт дилера и игрока
dealer_cardFrame = tkinter.Frame(gameWindow, bg="black")
dealer_cardFrame.place(x=400, y=80)

player_card_frame = tkinter.Frame(gameWindow, bg="black")
player_card_frame.place(x=400, y=350)

# Создание списка для хранения карт
cards = []
getCardImages(cards)

# Создание и перемешивание колоды карт
deck = list(cards)
shuffle()

# Создание списков для хранения карт дилера и игрока
dealer_hand = []
player_hand = []

import tkinter.ttk as ttk

# Создание стиля для кнопок
more_image = ImageTk.PhotoImage(Image.open("images/more.png"))
staying_image = ImageTk.PhotoImage(Image.open("images/staying.png"))
newgame_image = ImageTk.PhotoImage(Image.open("images/newgame.png"))
exit_image = ImageTk.PhotoImage(Image.open("images/exit.png"))

player_button = tkinter.Button(gameWindow, command=hitting, relief="flat")
player_button.place(x=480, y=650)
player_button.config(image=more_image, width=200, height=60)

dealer_button = tkinter.Button(gameWindow, command=staying, relief="flat")
dealer_button.place(x=690, y=650)
dealer_button.config(image=staying_image, width=200, height=60)

new_game_button = tkinter.Button(gameWindow, command=new_game, relief="flat")
new_game_button.place(x=900, y=650)
new_game_button.config(image=newgame_image, width=200, height=60)

exit_button = tkinter.Button(gameWindow, command=exit_game, relief="flat")
exit_button.place(x=1350, y=800)
exit_button.config(image=exit_image, width=200, height=60)



# Начальная раздача карт
initial_deal()

gameWindow.mainloop()