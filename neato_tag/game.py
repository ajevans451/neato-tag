
import numpy as np

#Color Calibrations
LOWER_PINK = np.array([116,0,69])
UPPER_PINK = np.array([255,73,150])
LOWER_BLUE = np.array([0,52,80])
UPPER_BLUE = np.array([26,104,255])
LOWER_YELLOW = np.array([123,137,0])
UPPER_YELLOW = np.array([194,203,69])
LOWER_GREEN = np.array([28,103,50])
UPPER_GREEN = np.array([98,255,92])
CALIBRATION_MATRIX = np.array([[584.9932,0,0], [0, 584.6622,0], [377.3949,225.2839,1]])
FOCAL_Y = CALIBRATION_MATRIX[1, 1]
NOTE_HEIGHT = 0.0762
NUM_PIXELS=11943936


player_colors=["PINK", "BLUE", "YELLOW", "GREEN"]
COLOR_TO_MASK = {"PINK":(LOWER_PINK, UPPER_PINK), "BLUE":(LOWER_BLUE, UPPER_BLUE), "YELLOW":(LOWER_YELLOW,UPPER_YELLOW), "GREEN":(LOWER_GREEN,UPPER_GREEN)}


class NeatoTag:
    """
    This class defines the parameters of the game of tag.
    It stores the number and colors of the players in the game.
    """

    def __init__(self, player_colors):
        self.num_players = len(player_colors)
        self.player_colors=player_colors


    def __repr__(self):
        return f"(Number of players: {self.num_players}, Active colors: {self.player_colors})"
    
    
NEATO_TAG=NeatoTag(player_colors)