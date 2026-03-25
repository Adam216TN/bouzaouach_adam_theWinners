import numpy as np
import random
from .steering import Steering
from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent


class Agent7(KartAgent):
    def __init__(self, env, path_lookahead=3, steps=0): #Ajout d'une variable step
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.steps = steps
        self.name = "Bouzaouach Adam" # replace with your chosen name
        self.pilote = Steering() # Ajout d'un agent de pilotage
        self.dist = 0

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []
        self.pilote.reset()
        self.dist = 0

    def endOfTrack(self):
        return self.isEnd

    def choose_action(self, obs):
        
        points = obs['paths_start']
        points2 = obs['center_path']
        target = points[2]
        target2 = points[0]
        gx = target[0]
        gz = target[2]
        gx2 = target2[0]
        gz2 = target2[2]

        if self.steps <= 200:
            print(f" Pas de temps : {self.steps}") #Affichage du nombre de pas de temps
        #print(f"distance : {obs['distance_down_track']}")
        
        brake = False

        
        
        # Si on est à moins de 200 pas de temps on avance à fond en utilisant notre fonction pure_pursuit
        if self.steps <= 200:
            acceleration = 0.5
            steering = self.pilote.pilote(gx,gz)
            distance = obs['distance_down_track']
            self.dist = distance

        # Si on a parcouru le double de la distance depuis le demarrage de la marche arrière, c'est qu'on est revenu à la ligne de départ
        elif obs['distance_down_track'] <= self.dist*2: 
            # Pour faire une marche arrière, on mets brake à true et accel à 0
            brake = True
            acceleration = 0.0
            steering = self.pilote.pilote(gx2,gz2)
            steering = steering * 0.1
            #steering = steering*-1
            #print(f" Pas de temps : {self.steps}")
        
        # Quand on est revenu sur la ligne de départ, on coupe les gaz totalement
        else:
            acceleration = 0.0
            brake = False
            steering = 0.0

        if self.steps == 200:
            print("Fin des 200 pas de temps")

        #print(f"Steering {steering}")
        action = {
            "acceleration": acceleration,
            "steer": steering,
            "brake": brake, # bool(random.getrandbits(1)),
            "drift": False,
            "nitro": False,
            "rescue":False,
            "fire": False,
        }
        return action
