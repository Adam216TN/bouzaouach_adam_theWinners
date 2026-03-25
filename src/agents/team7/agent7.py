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

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def endOfTrack(self):
        return self.isEnd

    def choose_action(self, obs):
        
        points = obs['paths_start']
        target = points[2]
        gx = target[0]
        gz = target[2]

        if self.steps <= 200:
            print(f" Pas de temps : {self.steps}") #Affichage du nombre de pas de temps
        #print(f"distance : {obs['distance_down_track']}")
        
        # Si on est à moins de 200 pas de temps on avance à fond en utilisant notre fonction pure_pursuit
        if self.steps <= 200:
            acceleration = 1.0
            steering = self.pilote.manage_pure_pursuit(gx,gz,7.0)
        
        # Si on est à plus de 200 pas de temps on coupe les gaz et on mets le steering en neutre
        else : 
            acceleration = 0.0
            steering = 0.0

        if self.steps == 200:
            print("Fin des 200 pas de temps")

        #print(f"Steering {steering}")
        action = {
            "acceleration": acceleration,
            "steer": steering,
            "brake": False, # bool(random.getrandbits(1)),
            "drift": False,
            "nitro": False,
            "rescue":False,
            "fire": False,
        }
        return action
