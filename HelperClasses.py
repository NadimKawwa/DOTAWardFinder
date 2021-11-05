#! /usr/bin/env python

import os


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


     
####################################################        
####################################################   

class ObjectiveFinder:
    def __init__(self, folder: str ='data_obj'):
        """
        Perform query over JSON folders from OpenDota and extract obejctives.
        All files inside data folder MUST BE JSON
        
        Parameters
        ----------
        folder: string, default= 'data_obj'
                The folder containing the JSON data files
        
        """
        #main folder
        self.folder = folder
        #files inside the folder
        self.files = os.listdir(self.folder)
        #remove anything that starts with a dot
        self.files = [x for x in self.files if not x.startswith('.')]
        
        #assert files are JSON
        if not all (text.lower().endswith('json') for text in self.files):
            raise ValueError(f'All files inside the provided folder "{self.folder}" must be JSON.')

        
    def _getObjectiveTimes(self, match_id, log):
        """
        Reads a log associated with a match and returns a dict of objectives.
        
        Parameters
        ----------
        match_id: int
            ID of match
        
        log: dict
            JSON style entry of match ID associated with player actions
        """
        #empty dict
        d = {}
    
        #keep track of how many rosh kills
        i = 0
    
        #store the match id
        d['match_id'] = match_id
    
        #Extract buildings activity log
        for item in log:
            #check if objective tied to buildings
            if item['type']== 'building_kill':
                d[item['key']] = item['time']
            #check for ROSHAN time killed
            elif item['type'] == 'CHAT_MESSAGE_ROSHAN_KILL':
                #has rosh been killed before?
                if 'ROSHAN_0' not in d:
                    d['ROSHAN_0'] = item['time']
                else:
                    i += 1
                    name= 'ROSHAN_' + str(i)
                    d[name] = item['time']

        return d


    def _getObjectiveDataframe(self, df):
        """
        Ingests dataframe and extracts dictionary of objectives for each row.
        """
        
        #filter by keeping unique match ids
        df_match = df.drop_duplicates(subset='match_id', 
                                      keep='first')

        obj_arr = []
        for row in df_match.itertuples(index=False):
            d = self._getObjectiveTimes(row.match_id, 
                                  row.objectives)
            obj_arr.append(d)

        return pd.DataFrame(obj_arr)



    def getObjectiveData(self):
        """
        Reads files inside folder and returns dataframe of objectives. No arguments needed.
        """
        df_arr = []
        
        for file in self.files:
            #set the path
            data_path = os.path.join(self.folder, file)
            #read data
            df = pd.read_json(data_path)
            #organize
            df_obj = self._getObjectiveDataframe(df)
            #append
            df_arr.append(df_obj)
            
        self.df_obj = pd.concat(df_arr)
                
        
        
        #cosmetic changes to column names
        # TODO: looks too wordy, maybe find a way to shorten it
        self.df_obj.columns = self.df_obj.columns.str.replace('npc_dota_goodguys','radiant')
        self.df_obj.columns = self.df_obj.columns.str.replace('npc_dota_badguys','dire')
        
        return self.df_obj
            
            
####################################################        
####################################################   



class WardFinder:
    def __init__(self, folder: str ='data_obj'):
        """
        Perform query over JSON folders from OpenDota and extract all observer & sentry wards placed.
        All files inside data folder MUST BE JSON FILES
        
        Parameters
        ----------
        folder: string, default= 'data_obj'
                The folder containing the JSON data files
        """
        #main folder
        self.folder = folder
        #files
        self.files = os.listdir(self.folder)
        #remove anything that starts with a dot
        #avoid reading hidden files
        self.files = [x for x in self.files if not x.startswith('.')]
        
        #assert files are JSON
        if not all (text.lower().endswith('json') for text in self.files):
            raise ValueError(f'All files inside the provided folder "{self.folder}" must be JSON.')
            
            
    def _getSentry(self, df):
        """
        Extract sentry activity inside dataframe.
        """
        #empty array to hold info
        sen_log = []

        #iterate over every row (not super effective)
        for row in df.itertuples(index=False):
            #for every entry in the dict
            for d in row.sen_log:
                #dict to store new rows
                s_log = {}
                s_log['match_id'] = row.match_id #match id not unique
                s_log['start_time'] = row.start_time #record start time
                s_log['hero_id'] = row.hero_id #hero that placed it
                s_log['time'] = d['time'] #time of placement
                s_log['x'] = d['x'] #x coord
                s_log['y'] = d['y'] #y coord
                s_log['z'] = d['z'] #zcoord could be on a hilltop or cliff

                if d['player_slot'] < 128:
                    s_log['is_radiant'] = 1
                else:
                    s_log['is_radiant'] = 0

                sen_log.append(s_log)

        df_sentry = pd.DataFrame.from_dict(sen_log)
        return df_sentry
            
            

    def _getObserver(self, df):
        """
        Extract observer activity inside dataframe
        """
        #empty array to hold info
        obs_log = []

        #iterate over every row (not super effective)
        for row in df.itertuples(index=False):
            #for every entry in the dict
            for d in row.obs_log:
                #dict to store new rows
                o_log = {}
                o_log['match_id'] = row.match_id #match id not unique
                o_log['start_time'] = row.start_time #record start time
                o_log['hero_id'] = row.hero_id #hero that placed it
                o_log['time'] = d['time'] #time of placement
                o_log['x'] = d['x'] #x coord
                o_log['y'] = d['y']
                o_log['z'] = d['z']

                if d['player_slot'] < 128:
                    o_log['is_radiant'] = 1
                else:
                    o_log['is_radiant'] = 0

                obs_log.append(o_log)

        df_obs = pd.DataFrame.from_dict(obs_log)
        return df_obs

        
    def getWardData(self):
        """
        Reads files inside folder and returns dataframe of observer + sentry wards. No arguments needed.
        """
        #instantiate empty arrays
        df_sen_arr = []
        df_obs_arr = []
        
        for file in self.files:
            #set the path
            data_path = os.path.join(self.folder, file)
            #read data
            df = pd.read_json(data_path)
            #organize and call functions on rows
            df_sen = self._getSentry(df)
            df_obs = self._getObserver(df)
            #append dataframe to respective dataframe
            df_sen_arr.append(df_sen)
            df_obs_arr.append(df_obs)
            
        #make into one dataframe
        self.df_sen = pd.concat(df_sen_arr)
        self.df_obs = pd.concat(df_obs_arr)
        
        return self.df_obs, self.df_sen
        
    def seeObserverMap(self):
        """
        Shows a plot of all observer wards placed colored by height. Red box shows map boundaries
        """
        cm = plt.cm.get_cmap('RdYlBu')

        # Create figure and axes
        fig, ax = plt.subplots()

        #very messy but fun to look at
        sc = ax.scatter(self.observerDataframe['x'],
                   self.observerDataframe['y'], 
                   c = self.observerDataframe['z'],
                   cmap=cm)

        plt.title("Scatter of All Obsever Wards")
        plt.xticks(np.arange(50, 250, 50))
        plt.yticks(np.arange(50, 250, 50))

        #draw bounding rectangle
        rect = patches.Rectangle((64, 64), 128, 128, linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        #add the color bar
        plt.colorbar(sc)
        #
        ax.set_facecolor('grey')


        plt.show()
        

    def seeSentryMap(self):
        """
        Shows a plot of all sentry wards placed colored by height. Red box shows map boundaries
        """
        cm = plt.cm.get_cmap('RdYlBu')

        # Create figure and axes
        fig, ax = plt.subplots()

        #very messy but fun to look at
        sc = ax.scatter(self.sentryDataframe['x'],
                   self.sentryDataframe['y'], 
                   c = self.sentryDataframe['z'],
                   cmap=cm)

        plt.title("Scatter of All Obsever Wards")
        plt.xticks(np.arange(50, 250, 50))
        plt.yticks(np.arange(50, 250, 50))

        #draw bounding rectangle
        rect = patches.Rectangle((64, 64), 128, 128, linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        #add the color bar
        plt.colorbar(sc)
        #
        ax.set_facecolor('grey')


        plt.show()     
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        