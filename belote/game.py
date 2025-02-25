# game.py
import random
import numpy as np

from belote.cards import Deck, Hand, Suit
# Supposons que Trick et GameState soient définis ici ou importés
# Par exemple :
class Trick:
    def __init__(self, trump: Suit):
        self.trump = trump
        self.played_cards = []  # Liste de tuples (player, card)

    def add_card(self, player, card):
        self.played_cards.append((player, card))

    def determine_winner(self):
        if not self.played_cards:
            raise ValueError("Aucune carte jouée dans ce trick")
        lead_suit = self.played_cards[0][1].suit
        # Si des atouts ont été joués, seuls ceux-ci sont considérés.
        trump_cards = [(p, c) for (p, c) in self.played_cards if c.suit == self.trump]
        if trump_cards:
            candidates = trump_cards
        else:
            # Sinon, seules les cartes de la couleur demandée comptent.
            candidates = [(p, c) for (p, c) in self.played_cards if c.suit == lead_suit]
        winner, winning_card = max(candidates, key=lambda pc: pc[1].get_points(self.trump))
        return winner

class GameState:
    def __init__(self, trump: Suit = None):
        self.trump = trump
        self.current_trick = None
        self.completed_tricks = []

############################################
# Classe DealSimulator dans game.py
############################################

class DealSimulator:
    """
    Simule une donne de belote en découpant le jeu en tricks.
    Réalise la distribution en 3 phases selon les règles officielles (3, puis 2, candidate, puis 2 ou 3 cartes).
    """
    def __init__(self, players, draft_starting_index):
        self.players = players
        self.draft_starting_index = draft_starting_index
        
        # Création et mélange du deck (32 cartes)
        self.deck = Deck()
        self.deck.initialize()  # Assurez-vous que Deck.initialize() initialise un jeu de 32 cartes.
        self.deck.shuffle()
        
        # Réinitialisation des mains des joueurs
        for player in self.players:
            player.hand = Hand()
        
        # Phase 1: Distribuer 3 cartes à chaque joueur
        for player in self.players:
            player.hand.add_cards(self.deck.deal(3))
            print(f"{player}: {player.hand}")
        
        # Phase 2: Distribuer 2 cartes à chaque joueur
        for player in self.players:
            player.hand.add_cards(self.deck.deal(2))
            print(f"{player}: {player.hand}")
        
        # Exposer la candidate (1 carte)
        candidate = self.deck.deal(1)[0]
        print(f"\nCandidate Card: {candidate}")
        accepted = False
        count = len(self.players)
        for i in range(count):
            index = (self.draft_starting_index + i) % count
            player = self.players[index]
            if player.accept_candidate(candidate, None):
                accepted = True
                print(f"{player} accepte la candidate. L'atout sera {candidate.suit.name}.")
                # Le joueur qui accepte reçoit la candidate dans sa main
                player.hand.add_cards([candidate])
                self.accepted_player_id = player.id
                break
        if not accepted:
            # Si aucun joueur n'accepte, on peut fixer l'atout sur la candidate par défaut
            print("Aucun joueur n'a accepté la candidate. On fixe néanmoins l'atout.")
            self.accepted_player_id = None  # ou choisir une stratégie spécifique
        self.trump = candidate.suit
        self.state = GameState(trump=self.trump)
        
        # Phase 3: Compléter la main pour obtenir 8 cartes par joueur
        # Le joueur ayant pris la candidate doit recevoir 2 cartes, les autres 3 cartes.
        for player in self.players:
            current_count = len(player.hand.cards)
            if self.accepted_player_id is not None and player.id == self.accepted_player_id:
                needed = 8 - current_count  # Ce joueur a déjà 6 cartes (3+2+1), il doit recevoir 2.
            else:
                needed = 8 - current_count  # Les autres ont 5 cartes, ils doivent recevoir 3.
            if needed > 0:
                player.hand.add_cards(self.deck.deal(needed))
            print(f"{player}: {player.hand}")
        
        # Initialisation du compteur de tricks et de l'index du joueur qui commence le trick
        self.current_trick_count = 0
        self.current_starting_index = 0

    def get_allowed_cards(self, player, trick):
        """
        Retourne la liste des cartes autorisées à jouer pour le joueur,
        selon la règle : 
         - S'il peut suivre la couleur demandée, il doit le faire.
         - Sinon, s'il possède des atouts, il doit couper.
         - Sinon, aucune contrainte.
        """
        if not trick.played_cards:
            return player.hand.cards.copy()
        lead_suit = trick.played_cards[0][1].suit
        if any(card.suit == lead_suit for card in player.hand.cards):
            return [card for card in player.hand.cards if card.suit == lead_suit]
        elif any(card.suit == self.trump for card in player.hand.cards):
            return [card for card in player.hand.cards if card.suit == self.trump]
        else:
            return player.hand.cards.copy()

    def play_next_trick(self, controlled_agent_id, agent_action=None):
        """
        Joue un trick complet.
        Pour le joueur contrôlé (controlled_agent_id), si un agent_action est fourni,
        il sera utilisé pour choisir la carte parmi les allowed_cards.
        Pour les autres, on choisit aléatoirement.
        
        Retourne (observation, reward, done, info) :
          - observation : vecteur d'observation construit par build_observation().
          - reward : récompense calculée pour le trick.
          - done : True si 8 tricks ont été joués dans la donne.
          - info : informations complémentaires (ex : gagnant du trick).
        """
        trick = Trick(self.trump)
        num_players = len(self.players)
        for i in range(num_players):
            current_index = (self.current_starting_index + i) % num_players
            player = self.players[current_index]
            allowed = self.get_allowed_cards(player, trick)
            if player.id == controlled_agent_id and agent_action is not None:
                action_index = agent_action
                if action_index < 0 or action_index >= len(allowed):
                    action_index = random.randrange(len(allowed))
                chosen = allowed[action_index]
            else:
                chosen = random.choice(allowed)
            player.hand.remove_card(chosen)
            trick.add_card(player, chosen)
            print(f"{player} joue: {chosen}")
        winner = trick.determine_winner()
        print(f"Gagnant du trick {self.current_trick_count + 1}: {winner}")
        self.current_starting_index = self.players.index(winner)
        self.current_trick_count += 1
        # Calcul des points du trick
        trick_points = sum(card.get_points(self.trump) for _, card in trick.played_cards)
        controlled_player = next(p for p in self.players if p.id == controlled_agent_id)
        reward = trick_points if winner.team == controlled_player.team else 0
        observation = self.build_observation(controlled_agent_id, trick, num_players)
        done = self.current_trick_count >= 8
        info = {"trick_winner": winner.id, "trick_points": trick_points}
        return observation, reward, done, info

    def build_observation(self, controlled_agent_id, trick, num_players):
        controlled_player = next(p for p in self.players if p.id == controlled_agent_id)
        allowed = self.get_allowed_cards(controlled_player, trick)
        allowed_ratio = len(allowed) / len(controlled_player.hand.cards) if controlled_player.hand.cards else 0
        tricks_norm = self.current_trick_count / 8
        current_trick_points = sum(card.get_points(self.trump) for _, card in trick.played_cards)
        trick_points_norm = current_trick_points / 100
        hand_size_norm = len(controlled_player.hand.cards) / 8
        current_order = len(trick.played_cards)
        order_norm = current_order / (num_players - 1) if num_players > 1 else 0
        trump_one_hot = [0, 0, 0, 0]
        # On suppose que self.trump.value commence à 1
        trump_one_hot[self.trump.value - 1] = 1
        features = [allowed_ratio, tricks_norm, trick_points_norm, hand_size_norm, order_norm] + trump_one_hot
        return np.array(features, dtype=np.float32)