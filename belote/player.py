import random
from typing import List
from belote.cards import Card, Hand


class Player:
    def __init__(self, player_id: int, team: int, strategy):
        self.id = player_id
        self.team = team
        self.strategy = strategy  # Instance d'une stratégie (voir ci-après)
        self.hand = Hand()

    def choose_card(self, game_state, allowed_cards: List[Card]) -> Card:
        return self.strategy.decide_card(self, game_state, allowed_cards)

    def accept_candidate(self, candidate: Card, game_state) -> bool:
        return self.strategy.accept_candidate_card(self, candidate, game_state)

    def __str__(self):
        return f"Player {self.id} (Team {self.team})"

# --- Interface Strategy (classe de base) ---

class BaseStrategy:
    def decide_card(self, player: Player, game_state, allowed_cards: List[Card]) -> Card:
        # Par défaut, choisir aléatoirement parmi allowed_cards si disponibles, sinon toute la main.
        choices = allowed_cards if allowed_cards else player.hand.cards
        return random.choice(choices)

    def accept_candidate_card(self, player: Player, candidate: Card, game_state) -> bool:
        # Par défaut, accepter si le joueur a déjà une carte de la même couleur.
        return any(card.suit == candidate.suit for card in player.hand.cards)
