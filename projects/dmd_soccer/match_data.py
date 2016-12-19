r"""
This module holds the basic data structure.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

#from .common import *

import numpy as np
#import msmtools.analysis
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
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
        self._num_pts = self._raw_table.shape[0]
        
    """Print description of the current dataframe stored using pandas' function describe().

    Parameters:
        """
    def describe(self):
        descr = self._raw_table.describe()
        print(descr)

    #TODO: Write
    # shot clock, game clock, off_status=True, ... are in Basketball class!!
    def trajectory(self, player_id=None, team_id=None, ball=True, distinguish_teams=False):
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
        Returns:
            nd-array (data matrix), txn-dimensional
        """
        return None
        
    #TODO
    def player_ids(self):
        """Return list of the ids of the players.

        Parameters:
        """
        return None
    
    @property
    def num_pts(self):
        return self._num_pts
        
class BballData(MatchData):
        
    # TODO: Work on missing data problem for ball etc.
    # TODO: Split into four tables!
    def __init__(self, filename, format='excel'):
        
        self._raw_table = None
        self._players_table = None
        self._refs_table = None
        self._ball_table = None
        #self._refs_ball_table = None
        self._game_id = None
        self._num_tracked_ppl = 13
        self._num_team_players = 5
        self._num_total_players = 2*self._num_team_players
        self._team_ids = None #ids of the teams and refs
        
        MatchData.__init__(self, filename, format='excel')
        if self._raw_table.empty is False:
            self._game_id = self._raw_table['GAME_CODE'][0]
        else:
            print("Dataframe is empty! Can not initialize BballData")
        
        # Split dataframe into three tables (players, referees, ball)
        team_inds = [self._raw_table.ix[i, 'TEAM'] in np.arange(1,3,1) for i in range(self._raw_table.shape[0])]
        self._players_table = self._raw_table.loc[team_inds, :]
        self._players_table.reset_index(level=0, inplace=True)
        self._refs_table = self._raw_table.loc[lambda df: df.TEAM == 3, :]
        self._refs_table.reset_index(level=0, inplace=True)
        self._ball_table = self._raw_table.loc[lambda df: df.TEAM == 4, :]
        self._ball_table.reset_index(level=0, inplace=True)
    
    # TODO: Cover all cases (currently, the parameters have no effect)
    # TODO: Split up into multiple trajectories, where path is not continuous
    def trajectory(self, player_id=None, pl_id_type='data_id', team_id=None, ball=True, distinguish_teams=False, quarters=None, cur_quarter=None, off_status=False, shot_clock=False, game_clock=False):
        """Return trajectory with customizable data, which can be put directly into TICA/DMD.

        Parameters:
            xxx num_tracked_ppl: Number of objects, for which positional data is available in each
            instance of time. Default: 14 (2*5 players + 3 refs + 1 ball) -> constant of BballData xxx
            player_id: if a player id is given, then make a trajectory for this single player. 
            WHAT IS EXACTLY THE ID OF A PLAYER TO GIVE HERE??? -> we should be able to always take the
            pl_id_type: Must be either 'data_id' (default) or 'slice_at_k'. If 'data_id' is given, then
            a given player_id will be interpreted as the id of a player, given in the data
            (column 'PLAYER_ID'). If 'slice_at_k' is given, then it has to be 0 <= player_id < no. of 
            tracked objects. a single trajectory will be produced, s.t. the trajectory is the tracked
            object from slot "player_id" in the data.
            k'th, but also give multiple trajectories for a player, if we give an exact id (as in the data)
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
        Returns: 
            nd-array (data matrix), txn-dimensional
        """
        if any((self._players_table is None, self._players_table.empty)):
            print("Cannot calculate trajectory matrix, _players_table is empty/None!")
            return None
        ppl_cols = ['X_POSITION', 'Y_POSITION']
        ball_cols = ['X_POSITION', 'Y_POSITION','Z_POSITION']
        length = self._players_table.shape[0]
        exerpts = np.array([self._players_table.ix[np.arange(i, length+i, self._num_total_players), ppl_cols].values for i in range(0, self._num_total_players)])
        X = exerpts.transpose([1,0,2]).reshape((length//(self._num_total_players), len(ppl_cols)*self._num_total_players))
        
        # have players so far, now the ball...
        #print(self._ball_table.shape)
        #print(X.shape)
        #print(self._ball_table)
        #X = np.hstack((X, self._ball_table.ix[:, ball_cols].values))
        return X
    
    @property
    def game_id(self):
        return self._game_id
    
    # TODO: Also plot the ball
    # TODO: Support 'ms'
    def show(self, t, t_type='timestep'):
        """Plots the positions of the players and the ball for a given timestep or time.

        Parameters:
            t: The time, for which the position shall be shown.
            t_type: Can be 'timestep' (default), then the t-th timestep will be plotted, or 'ms', then the
            position after t milliseconds after the start of the game will be shown.
        Returns: 
            
        """
        if t is None:
            print("Specify timestep!")
        traj = self.trajectory()
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.scatter(traj[t][np.arange(0, self._num_team_players*2, 2)], traj[t][np.arange(1, self._num_team_players*2+1, 2)], c='red')
        ax.scatter(traj[t][np.arange(self._num_team_players*2, self._num_total_players*2, 2)], traj[t][np.arange(1 + self._num_team_players*2, 1 + self._num_total_players*2, 2)], c='blue')
        self._format_plot(ax)
        fig.tight_layout()
    
    # TODO: Also plot the ball
    # TODO: Support 'ms'
    def play(self, t_start, t_end, t_type='timestep'):
        """Outputs a play widget to play back certain intervals of the game.

        Parameters:
            t_start: The start time of the video sequence to be shown.
            t_end: The end time of the video sequence to be shown.
            t_type: Can be 'timestep' (default), then the (t_start)-th up to (t_end)-th timestep 
            will be played back, or 'ms', then the time unit is milliseconds.
        Returns: 
            
        """
        if any((t_start is None, t_end is None)):
            print("Specify start and end time!")
        traj = self.trajectory()
        
        step = 10
        play = widgets.Play(
        #     interval=10,
            value=t_start,
            min=t_start,
            max=t_end,
            step=step,
            description="Press play",
            disabled=False
        )
        court_disp = widgets.interactive(self.show, t=(t_start, t_end, step), continuous_update=True)
        widgets.jsdlink((play, 'value'), (court_disp.children[0], 'value'))
        display(play, court_disp)
        
        
    def _format_plot(self, ax):
        """Formats the plots for "show" and "play".

        Parameters:
            ax: Matplotlib axis object
        Returns: 
            
        """
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 50)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_aspect('equal')
        
    #def num_
        
        
        
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