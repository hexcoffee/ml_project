r"""
This module holds the basic data structure.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from .common import *

import numpy as np
#import msmtools.analysis
import pandas as pd

import math


class MatchData:

    # TODO: Support of multiple sheets
    def __init__(self, filename, format='excel'):
        """Create new data container for a match.

        Parameters:
            path: filename of the data file -> needs to be in the same folder!
            format: must be excel currently, TODO: planning to to csv as well
            """
        file = pd.ExcelFile(filename)
        if file is None:
            print("Loading failed!")
        self._raw_table = file.parse()
        
    """Print description of the current dataframe stored using pandas' function describe().

    Parameters:
        """
    def describe(self):
        descr = self._raw_table.describe()
        print(descr)

    #TODO        
    """Return trajectory with customizable data, which can be put directly into TICA/DMD.

    Parameters:
        player_id: if a player id is given, then make a trajectory for this single player. 
        If None (default), make trajectory for whole team(s) (an x- and y-dimension for each player)
        team_id: Must be 0, 1 or None (default). If given, the trajectory will only contain
        the players of one team. If None, both teams are considered. If player_id is given,
        then team_id has no effect.
        ball: Whether the ball should be a dimension/column in the data. Default: True
        distinguish_teams: If trajectory is created for both teams, if this Boolean is set to
        True, the coordinates of the second team are set to negative values. Default: False
        """
    def trajectory(self, player_id=None, team_id=None, ball=True, distinguish_teams=False):
        return None
    # shot clock, game clock, off_status=True, ... are in Basketball class!!
    #TODO    
    """Return list of the ids of the players.

    Parameters:
        """
    def player_ids(self):
        return None
        
class BballData(MatchData):
        
    def __init__(self, filename, format='excel'):
        MatchData.__init__(self, path, format='excel')
        if self._raw_table.empty is False:
            self._game_id = self._raw_table['GAME_CODE'][0]
        else
            print("Dataframe is empty! Can not initialize BballData")
            return None
    
    #TODO
    """Return trajectory with customizable data, which can be put directly into TICA/DMD.

    Parameters:
        player_id: if a player id is given, then make a trajectory for this single player. 
        If None (default), make trajectory for whole team(s) (an x- and y-dimension for each player)
        team_id: Must be 0, 1 or None (default). If given, the trajectory will only contain
        the players of one team. If None, both teams are considered. If player_id is given,
        then team_id has no effect.
        ball: Whether the ball should be a dimension/column in the data. Default: True
        distinguish_teams: If trajectory is created for both teams, if this Boolean is set to
        True, the coordinates of the second team are set to negative values. Default: False
        quarters: list of quarters to be included (they are just concatenated in the data matrix).
        If None (default), all quarters are taken.
        cur_quarter: Adds a column with the information, which quarter currently is (from 1 to 4)
        off_status: Whether to include a 0/1-column, whether team 0 is currently attacking.
        Default: False
        shot_clock: Whether to include the shot (24-second-) clock information as a dimension
        game_clock: Whether to include the game (720-second-) clock information as a dimension.
        720 seconds is the duration of one quarter.
        """
    def trajectory(self, player_id=None, team_id=None, ball=True, distinguish_teams=False, 
    quarters=None, cur_quarter=None, off_status=False, shot_clock=False, game_clock=False):
        return None
    
    @property
    def _game_id(self):
        return self._game_id
        
        
        
        
        
        # if not self.is_stochastic_matrix(transition_matrix):
            # raise InvalidValue('Transition matrix must be stochastic')

        # self._lagtime = lagtime


    # @property
    # def states(self):
        # return list(self._states)

    # @property
    # def lagtime(self):
        # return self._lagtime

    # @property
    # def communication_classes(self):
        # """The set of communication classes of the state space.
        
        # Returns: [CommunicationClass]
            # List of communication classes sorted by size descending.
        # """
        # if self._communication_classes is None:
            # self._communication_classes = [
                # CommunicationClass(sorted(c), component_is_closed(c, self.transition_matrix))
                # for c in strongly_connected_components(self.transition_matrix)
            # ]
        # self._communication_classes.sort(key=lambda c: len(c.states), reverse=True)
        # return self._communication_classes

    # @property
    # def stationary_distribution(self):
        # """The unique stationary distribution. The Markov chain must be irreducible.
        
        # Type: pandas.Series
        # """
        # if self._stationary_distribution is None:
            # self._stationary_distribution = self._find_stationary_distribution()
        # return self._stationary_distribution
       

    # def left_eigenvectors(self, k=None):
        # """Computes the first k left eigenvectors for largest eigenvalues
        
        # Arguments:
        # k: int
            # How many eigenvectors should be returned. Defaults to None, meaning all.
        
        # Returns: pandas.DataFrame
            # DataFrame containing the eigenvectors as columns
        # """
        # if k is None:
            # k = len(self.transition_matrix)
        # return self.left_eigen[1].iloc[:,:k]