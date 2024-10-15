# Import the main play functions from each game module
from .Tic_Tac_Toe import play as play_tic_tac_toe
from .Air_Hockey import play as play_air_hockey
from .Dodge_Ball import play as play_dodge_ball

# Expose them at the package level
__all__ = ['play_tic_tac_toe', 'play_air_hockey', 'play_dodge_ball']
