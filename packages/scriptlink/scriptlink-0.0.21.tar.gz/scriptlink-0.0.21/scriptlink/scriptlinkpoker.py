#Description
#Developer:
#pckgs attrs==21.4.0  py==1.11.0 pytest==7.0.0 pluggy==1.0.0 iniconfig-1.1.1 atomicwrites-1.4.0 hypothesis==3.43.1 coverage==6.3.1
#requirements  GPUtil==1.4.0,psutil==5.9.0
from scriptlink import *
import random
#import pokercalclib as pkl
import ctypes, ctypes.util
pkl = ctypes.CDLL(str.lower(os.path.join(os.path.dirname(__file__), 'pokercalclibctypes.dll')))
Poker_ev7=pkl.poker_ev7
Poker_evomaha=pkl.poker_evomaha
Poker_evomahalow=pkl.poker_evomahalow
def poker_holdem_equity(h1,h2,boardcards,num_opponents=1,handrange=0):
    cards=[0]*5
    cards[:len(boardcards)] = boardcards
    pct=pkl.poker_holdem_equity(h1,h2,len(boardcards),num_opponents,handrange,cards[0],cards[1],cards[2],cards[3],cards[4]);
    return pct/10;
def poker_omaha_equity(h1,h2,h3,h4,boardcards,num_opponents=1,handrange=0):
    cards=[0]*5
    cards[:len(boardcards)] = boardcards
    pct=pkl.poker_omaha_equity(h1,h2,h3,h4,len(boardcards),num_opponents,handrange,cards[0],cards[1],cards[2],cards[3],cards[4]);
    return pct/10;
def poker_omahahl_equity(h1,h2,h3,h4,boardcards,num_opponents=1,handrange=0):
    cards=[0]*5
    cards[:len(boardcards)] = boardcards
    pct=pkl.poker_omahahl_equity(h1,h2,h3,h4,len(boardcards),num_opponents,handrange,cards[0],cards[1],cards[2],cards[3],cards[4]);
    return pct/10;

rank_map = {
    "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
    "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}
suit_map = {
    "C": 0, "D": 1, "H": 2, "S": 3,
    "c": 0, "d": 1, "h": 2, "s": 3
}
# fmt: on

rank_reverse_map = {value: key for key, value in rank_map.items()}
suit_reverse_map = {value: key for key, value in suit_map.items() if key.islower()}
def id_to_card(id):
    r=rank_reverse_map[id // 4]
    s=suit_reverse_map[id%4]
    return r+s

def getdeck(n):
    numbers = list(range(0, 52))
    random.shuffle(numbers)
    return numbers[:n]
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def card_to_id(card):
    rank, suit, *_ = tuple(card)
    return rank_map[rank] * 4 + suit_map[suit]
def evaluate_omaha_cards(*cards):
    
    int_cards = list(map(card_to_id, cards))
    hand_size = len(cards)

    h = int_cards[:4]
    cc = int_cards[4:]
    return cd.poker_evomaha(cc[0],cc[1],cc[2],cc[3],cc[4],h[0],h[1],h[2],h[3]);
def evaluate_omaha_cardslow(*cards):
    
    int_cards = list(map(card_to_id, cards))
    hand_size = len(cards)

    h = int_cards[:4]
    cc = int_cards[4:]
    return cd.poker_evomahalow(cc[0],cc[1],cc[2],cc[3],cc[4],h[0],h[1],h[2],h[3]);
def omaharunout(handr=0,*cards):
    int_cards = list(map(card_to_id, cards))
    hand_size = len(cards)

    h = int_cards[:4]
    cc = int_cards[4:]
    pct=poker_omaha_equity(h[0],h[1],h[2],h[3],cc,handrange=handr)
    return pct;
def omahahlrunout(handr=0,*cards):
    int_cards = list(map(card_to_id, cards))
    hand_size = len(cards)

    h = int_cards[:4]
    cc = int_cards[4:]
    pct=poker_omahahl_equity(h[0],h[1],h[2],h[3],cc,handrange=handr)
    return pct;
def holdemrunout(handr=0,*cards):
    int_cards = list(map(card_to_id, cards))
    hand_size = len(cards)

    h = int_cards[:2]
    cc = int_cards[2:]
    pct=poker_holdem_equity(h[0],h[1],cc,handrange=handr)
    return pct;

def pkpoker_holdem_equity(h1,h2,boardcards,num_opponents=1,handrange=0):
    cards=[0]*5
    cards[:len(boardcards)] = boardcards
    pct=pkl.poker_holdem_equity(h1,h2,len(boardcards),num_opponents,handrange,cards[0],cards[1],cards[2],cards[3],cards[4]);
    return pct/10;



    
    
