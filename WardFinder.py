import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

from sklearn.cluster import DBSCAN

%matplotlib inline


class WardFinder:
    def __init__(self, df_obs, df_sen, img):
        
        #read and store data
        self.df_obs = df_obs
        self.df_sen = df_sen
        self.img = img
        
        #OBSEVER apply translation of coordinates + time conversion
        self.df_obs['x'] = self.df_obs['x'] - 64
        self.df_obs['y'] = self.df_obs['y'] - 64
        self.df_obs['time'] = self.df_obs['time']/60
        
        #SENTRY apply translation of coordinates + time conversion
        self.df_sen['x'] = self.df_sen['x'] - 64
        self.df_sen['y'] = self.df_sen['y'] - 64
        self.df_sen['time'] = self.df_sen['time']/60
        
        
        
        #separate between

        