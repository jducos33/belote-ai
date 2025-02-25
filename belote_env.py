# belote_env.py
import gym
from gym import spaces
import numpy as np

from belote.game import DealSimulator
from belote.player import BaseStrategy, Player


class BeloteEnv(gym.Env):
    """
    Environnement Gym pour simuler une donne de belote de manière incrémentale (trick par trick).
    
    L'agent contrôle un joueur (controlled_agent_id, par défaut 1).
    À chaque appel à step(), un trick complet est joué en utilisant DealSimulator.
    L'observation est construite à partir de l'état du trick et d'autres informations pertinentes.
    
    L'épisode se termine après 8 tricks (fin de la donne).
    """
    metadata = {'render.modes': ['human']}
    
    def __init__(self, controlled_agent_id=1, draft_starting_index=0):
        super(BeloteEnv, self).__init__()
        # L'observation est un vecteur tel que construit par build_observation dans DealSimulator (ici 9 dimensions)
        self.observation_space = spaces.Box(low=0, high=1, shape=(9,), dtype=np.float32)
        # L'action correspond à l'indice de la carte à jouer parmi les allowed_cards (max 8 cartes dans la main)
        self.action_space = spaces.Discrete(8)
        
        self.controlled_agent_id = controlled_agent_id
        self.draft_starting_index = draft_starting_index
        
        self.deal_simulator = None
        self.current_observation = None

    def _create_players(self):
        """
        Crée 4 joueurs répartis en 2 équipes avec une stratégie de base.
        Par exemple : joueurs 1 et 3 dans l'équipe 1, et joueurs 2 et 4 dans l'équipe 2.
        """
        strategy = BaseStrategy()
        return [
            Player(1, 1, strategy),
            Player(2, 2, strategy),
            Player(3, 1, strategy),
            Player(4, 2, strategy)
        ]
        
    def reset(self):
        """
        Réinitialise l'environnement pour démarrer une nouvelle donne.
        - Crée les joueurs.
        - Initialise le DealSimulator avec la distribution initiale, la phase de draft et la distribution finale.
        - Joue le premier trick pour obtenir l'observation initiale.
        """
        players = self._create_players()
        self.deal_simulator = DealSimulator(players, self.draft_starting_index)
        # Jouer le premier trick (sans action forcée pour le joueur contrôlé)
        obs, _, done, info = self.deal_simulator.play_next_trick(self.controlled_agent_id, agent_action=None)
        self.current_observation = obs
        return obs

    def step(self, action):
        """
        Applique l'action (indice de la carte choisie par l'agent pour le joueur contrôlé) pour le prochain trick.
        Renvoie (observation, reward, done, info).
        """
        obs, reward, done, info = self.deal_simulator.play_next_trick(self.controlled_agent_id, agent_action=action)
        self.current_observation = obs
        return obs, reward, done, info

    def render(self, mode='human'):
        """
        Affiche quelques informations utiles sur l'état de la donne.
        """
        print(f"Trick {self.deal_simulator.current_trick_count} / 8")
        # Vous pouvez ajouter d'autres informations (ex. score cumulé, mains restantes, etc.)

