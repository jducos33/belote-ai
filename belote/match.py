from collections import defaultdict
from typing import List

from belote.game import DealEngine
from belote.player import Player


class Match:
    def __init__(self, players: List[Player], points_threshold: int):
        self.players = players
        self.points_threshold = points_threshold
        self.global_team_points = defaultdict(int)
        self.current_draft_start_index = 0

    def play_match(self):
        deal_number = 1
        while (self.global_team_points[1] < self.points_threshold and 
               self.global_team_points[2] < self.points_threshold):
            print(f"\n=== Début de la donne {deal_number} ===")
            deal_engine = DealEngine(self.players, self.current_draft_start_index)
            result = deal_engine.run_deal()
            if result is None:
                # Aucun contrat pris, changer le joueur de départ et réessayer.
                self.current_draft_start_index = (self.current_draft_start_index + 1) % len(self.players)
                print("Aucun contrat n'a été pris, nouvelle donne.")
                continue
            # Mise à jour des scores.
            for team, points in result.items():
                self.global_team_points[team] += points
            print(f"Score de la donne {deal_number}: {result}")
            print(f"Score global: {dict(self.global_team_points)}")
            # On peut incrémenter le current_draft_start_index pour la prochaine donne.
            self.current_draft_start_index = (self.current_draft_start_index + 1) % len(self.players)
            deal_number += 1

        if self.global_team_points[1] >= self.points_threshold:
            print("\nL'équipe 1 gagne le match!")
        else:
            print("\nL'équipe 2 gagne le match!")