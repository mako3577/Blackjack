import random
import tkinter
from tkinter import *
from PIL import ImageTk, Image


width = 1900
height = 1000

def load_images_buttons(dictname):
    global width, height
    buttons = ['bet_minus', 'bet_plus', 'check', 'double', 'draw', 'lock_in', 'new_game', 'make_bet']
    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    for button in buttons:
        path = f'images/buttons/{button}.{extension}'
        key = button
        image = Image.open(path)
        button = image.resize((int(width / 7) + 2, int(height * 1 / 12) + 5), Image.ANTIALIAS)
        button = ImageTk.PhotoImage(button)
        dictname[key] = button


def load_images(card_images):
    suits = ['hearts', 'clubs', 'diamonds', 'spades']
    face_cards = ['jack', 'queen', 'king']
    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = f'cards/{card}_of_{suit}.{extension}'
            image = Image.open(name)
            image = image.resize((int(width / 14), int(height / 5)), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            card_images.append((card, image,))

            # next the face cards
        for card in face_cards:
            name = f'cards/{card}_of_{suit}.{extension}'
            image = Image.open(name)
            image = image.resize((int(width / 14), int(height / 5)), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            card_images.append((10, image,))


def deal_card(frame):
    # pop the next card off the deck
    next_card = deck.pop(0)
    # add the image to a Label and display the Label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    # calculate the total score of all cards n the list
    # only one ace can have the value 11, and this will be reduce to 1 if the hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we bust, check if there is an ace
        if score > 21 and ace is True:
            score -= 10
            ace = False
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    player_score = score_hand(player_hand)
    m = money.get()
    b = bet_value.get()
    while 0 <= dealer_score <= 17 and dealer_score < player_score:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)

    if player_score > 21:
        result_text.set("Dealer wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
        money.set(m + 2 * b)
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
    else:
        result_text.set("Draw!")
        money.set(m + b)
    result_frame()
    player_button['state'] = 'disabled'
    dealer_button['state'] = 'disabled'
    new_game_button['state'] = 'disabled'
    bet_double['state'] = 'disabled'
    bet_in['state'] = 'normal'


def deal_player():
    player_score = score_hand(player_hand)
    if player_score < 21:
        player_hand.append(deal_card(player_card_frame))
        player_score = score_hand(player_hand)
    if player_score > 21:
        player_button['state'] = 'disabled'
        result_text.set("Dealer win")
        dealer_button['state'] = 'disabled'
        bet_double['state'] = 'disabled'
        bet_in['state'] = 'normal'
    player_score_label.set(player_score)
    new_game_button['state'] = 'disabled'


def resetb():
    global cards, deck
    dealer_hand.clear()
    player_hand.clear()
    for widget in player_card_frame.winfo_children():
        widget.destroy()
    for widget in dealer_card_frame.winfo_children():
        widget.destroy()
    dealer_score_label.set(0)
    player_score_label.set(0)
    # create new deck
    cards = []
    print(len(deck))
    load_images(cards)
    deck = list(cards)
    print(len(deck))
    random.shuffle(deck)

    # 2 cards for player and 1 for dealer at start of new game
    m = money.get()
    b = bet_value.get()
    if m - b >= 0:                       # if player has enough money
        money.set(m - b)                 # lock bet value for next game
        # deal start cards
        player_hand.append(deal_card(player_card_frame))
        player_hand.append(deal_card(player_card_frame))
        dealer_hand.append(deal_card(dealer_card_frame))
        # check score
        player_score = score_hand(player_hand)
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
        player_score_label.set(player_score)
        result_text.set('')
        # changing value of bet cannot be allowed during the game
        player_button['state'] = 'normal'
        dealer_button['state'] = 'normal'
        new_game_button['state'] = 'disabled'
        bet_button_increase['state'] = 'disabled'
        bet_button_decrease['state'] = 'disabled'
        bet_in['state'] = 'disabled'
        bet_double['state'] = 'normal'
    else:
        result_text.set('Not enough money to make a bet. Try again.')


def betincrease():
    """increase bet value by 100"""
    b = bet_value.get()
    bet_value.set(b + 100)


def betdecrease():
    """decrease bet value by 100"""
    b = bet_value.get()
    if b >= 100:
        bet_value.set(b - 100)
    else:
        result_text.set("Bet Value must be positive")


def unlock_keys():
    b = bet_value.get()
    m = money.get()
    if bet_in['text'] == 'Make a bet!':
        bet_in['text'] = "lock in your bet"
        bet_in['image'] = button_images['lock_in']
        bet_button_decrease['state'] = 'normal'
        bet_button_increase['state'] = 'normal'
        new_game_button['state'] = 'disabled'

    elif b <= m:
        bet_in['text'] = 'Make a bet!'
        bet_in['image'] = button_images['make_bet']
        bet_button_decrease['state'] = 'disabled'
        bet_button_increase['state'] = 'disabled'
        new_game_button['state'] = 'normal'
    else:
        result_text.set("Not enough money")
        bet_value.set(0)


def double_bet():
    b = bet_value.get()
    m = money.get()
    player_score = score_hand(player_hand)
    if b <= m:
        bet_value.set(2 * b)
        money.set(m - b)
        deal_player()
        player_score = score_hand(player_hand)
        if player_score < 22:
            deal_dealer()
        bet_double['state'] = 'disabled'
        bet_value.set(b)

    else:
        result_text.set("You have not enough money")
    player_score_label.set(player_score)


def result_frame():
    """creates result frame and places result of the game in it"""
    result = tkinter.Label(mainWindow)
    result.place(rely=1/30, relx=10/27, relwidth=1/3, relheight=1/13)
    result.config(textvariable=result_text, background='green', fg='black', font=f'arial {int(height / 25)} bold')


def money_add():                  # todo delete function and all usages of it before release
    m = money.get()
    money.set(m + 1000)


def run_game():              # allows to run game from another python file
    mainWindow.mainloop()


mainWindow = tkinter.Tk()

green_background = tkinter.PhotoImage(file='images/green_background.png')

green_background_label = tkinter.Label(mainWindow, image=green_background)
green_background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set up the screen and frames for the dealer and player

mainWindow.title("Black Jack")
mainWindow.geometry(f"{width}x{height}")
mainWindow.minsize(height=int(8 / 10 * height), width=int(8 / 10 * width))
mainWindow.maxsize(height=height, width=width)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.pack(side=LEFT, fill='both', expand=True)
card_frame.place(relheight=1 / 2, relwidth=35 / 50, relx=1 / 40, rely=5 / 40)

result_text = tkinter.StringVar()

result = tkinter.Label(mainWindow)
result.place(rely=1 / 30, relx=10 / 27, relwidth=1 / 4, relheight=1 / 13)
result.config(textvariable=result_text, background='green', fg='black', font=f'arial {int(height / 40)} bold')

dealer_score_label = tkinter.IntVar()
label_dealer = tkinter.Label(card_frame, text='Dealer', font=f'arial {int(height / 50)}', background='green',
                             fg='white')
label_dealer.pack(side=LEFT)
label_dealer.place(rely=2 / 9)

dealer_score = tkinter.Label(card_frame, textvariable=dealer_score_label, font=f'arial {int(height / 50)}',
                             background='green', fg='white')
dealer_score.pack(side=LEFT)
dealer_score.place(rely=27 / 90)

# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green', pady=height / 200, padx=width / 50)
dealer_card_frame.place(rely=4 / 70, relx=15 / 150)

player_score_label = tkinter.IntVar()

label1 = tkinter.Label(card_frame, text='Player', background='green', fg='white', font=f'arial {int(height / 50)}')
label1.pack(side=LEFT)
label1.place(rely=7 / 11)
label2 = tkinter.Label(card_frame, textvariable=player_score_label, font=f'arial {int(height / 50)}',
                       background='green', fg='white')

label2.place(rely=8 / 11)

# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background='green', pady=height / 200, padx=width / 50)
player_card_frame.place(rely=6 / 11, relx=15 / 150)

button_frame = tkinter.Frame(mainWindow, background='purple')
button_frame.pack(side=BOTTOM, fill='x', pady=5)
button_frame.place(rely=75 / 100, relheight=1 / 12, relwidth=1)

bet_value = tkinter.IntVar()
bet_value.set(100)
money = tkinter.IntVar()
money.set(1000)

money_frame = tkinter.Frame(mainWindow, borderwidth=1, background='green')
money_frame.place(relx=75 / 100, rely=2 / 10, relheight=1 / 5, relwidth=1 / 6)

money_frame.columnconfigure(0, weight=1)

tkinter.Label(money_frame, text='Money: ', background='green',
              font=f'arial {int(height / 60)}').grid(row=0, column=0, pady=(int(height / 150), 0))
tkinter.Label(money_frame, textvariable=money, background='green',
              font=f'arial {int(height / 60)}').grid(row=1, column=0)
tkinter.Label(money_frame, text='Current Bet: ', background='green',
              font=f'arial {int(height / 60)}').grid(row=2, column=0, pady=(int(height / 25), 0))
tkinter.Label(money_frame, background='green', textvariable=bet_value,
              font=f'arial {int(height / 60)}').grid(row=3, column=0)

button_images = {}
load_images_buttons(button_images)

dealer_button = tkinter.Button(button_frame, image=button_images['check'], activebackground='purple',
                               command=deal_dealer, highlightthickness=0, bd=0)
dealer_button.pack(expand=True)
dealer_button.place(relx=0, relheight=1)

player_button = tkinter.Button(button_frame, highlightcolor='purple', activebackground='purple',
                               image=button_images['draw'], command=deal_player, highlightthickness=0, bd=0)
player_button.place(relx=1 / 7, relheight=1)


new_game_button = tkinter.Button(button_frame, highlightthickness=0, bd=0, activebackground='purple',
                                 image=button_images['new_game'], command=lambda: [score_hand(dealer_hand), resetb(), ])

new_game_button.place(relx=2 / 7, relheight=1)

bet_button_increase = tkinter.Button(button_frame, image=button_images['bet_plus'],
                                     activebackground='purple', command=betincrease, highlightthickness=0, bd=0)

bet_button_increase.place(relx=3 / 7, relheight=1)

bet_button_decrease = tkinter.Button(button_frame, image=button_images['bet_minus'], command=betdecrease,
                                     activebackground='purple', highlightthickness=0, bd=0)
bet_button_decrease.place(relx=4 / 7, relheight=1)

bet_in = tkinter.Button(button_frame, image=button_images['lock_in'], command=unlock_keys,
                        activebackground='purple', highlightthickness=0, bd=0)
bet_in.place(relx=5 / 7, relheight=1)

bet_double = tkinter.Button(button_frame, image=button_images['double'], command=double_bet,
                            activebackground='purple', highlightthickness=0, bd=0)
bet_double.place(relx=6 / 7, relheight=1)

button_money_add = tkinter.Button(mainWindow, background='gold', command=money_add,         # todo delete with money_add
                                  text='Money+1000', font=f'arial {int(height / 50)}')
button_money_add.place(rely=9 / 10, relx=9 / 10, relheight=1 / 10, relwidth=1 / 10)         # todo delete with money_add

player_button['state'] = 'disabled'
dealer_button['state'] = 'disabled'
bet_double['state'] = 'disabled'
new_game_button['state'] = 'disabled'
cards = []
load_images(cards)

# create a new deck of cards and shuffle them
deck = list(cards)
random.shuffle(deck)

# create a list to store dealers and players hands
dealer_hand = []
player_hand = []

# if running as a main, run_game() function is not necessary to start the game
if __name__ == '__main__':
    mainWindow.mainloop()
