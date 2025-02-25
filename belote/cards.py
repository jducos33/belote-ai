import random
from enum import Enum, auto
from typing import List

# --- Définition des énumérations ---

class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()

class Rank(Enum):
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()

# --- Classe Card ---

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def get_points(self, trump: Suit) -> int:
        """Retourne la valeur de la carte en fonction de l'atout."""
        if self.suit == trump:
            # Valeurs pour l'atout
            if self.rank == Rank.JACK:
                return 20
            elif self.rank == Rank.NINE:
                return 14
            elif self.rank == Rank.ACE:
                return 11
            elif self.rank == Rank.TEN:
                return 10
            elif self.rank == Rank.KING:
                return 4
            elif self.rank == Rank.QUEEN:
                return 3
            else:
                return 0
        else:
            # Valeurs hors atout
            if self.rank == Rank.ACE:
                return 11
            elif self.rank == Rank.TEN:
                return 10
            elif self.rank == Rank.KING:
                return 4
            elif self.rank == Rank.QUEEN:
                return 3
            elif self.rank == Rank.JACK:
                return 2
            else:
                return 0

    def __str__(self):
        return f"{self.rank.name.capitalize()} of {self.suit.name.capitalize()}"

# --- Classe Deck ---

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.initialize()

    def initialize(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, count: int) -> List[Card]:
        if count > len(self.cards):
            raise ValueError("Not enough cards to deal")
        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt

# --- Classe Hand ---

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_cards(self, cards: List[Card]):
        self.cards.extend(cards)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)