import streamlit as st
import requests
import io
import pandas as pd
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import DBSCAN


#this line must come first
st.set_page_config(layout="wide")

#colors used in plotting
colors = [
    #'b', 
          #'g', 
          'r', 
          'c', 
          'm', 
          'y', 
          'darkorange', 
          'peru', 
          'gold', 
          'silver', 
          'indigo',
          'navy', 
          'crimson', 
          'darkmagenta', 
          'lime'
         ]


@st.cache(persist=True)
def load_data():
    """
    Loads data from public S3 bucket
    
    """
    #read from S3
    df_obs = pd.read_csv('https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/df_obs.csv')
    df_sen = pd.read_csv('https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/df_sentry.csv')
    
    
    #background image to be used
    img_url = 'https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/map_detailed_723.jpeg'
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content))
    
    
    #apply translation of coordinates
    df_obs['x'] = df_obs['x'] - 64
    df_obs['y'] = df_obs['y'] - 64
    df_sen['x'] = df_sen['x'] - 64
    df_sen['y'] = df_sen['y'] - 64

    #convert time to minutes
    df_obs['time'] = df_obs['time']/60
    df_sen['time'] = df_sen['time']/60

    
    return df_obs, df_sen, img



def getLabels(df, eps=3, min_samples=100):
    """
    Returns the labels of a dataframe after dbscan clustering
    
        Parameters
    ----------
    
    df: Pandas dataframe
        Data to be used for fitting. Must have columns 'x' and 'y'
    
    eps : float, default=0.5
        The maximum distance between two samples for one to be considered
        as in the neighborhood of the other. This is not a maximum bound
        on the distances of points within a cluster. This is the most
        important DBSCAN parameter to choose appropriately for your data set
        and distance function.
        
        
    
    """
    #instantiate dbscan
    db = DBSCAN(eps=eps, 
                min_samples=min_samples, 
                metric='euclidean', 
                n_jobs=-1
               )
    
    #fit and predict to data
    db.fit_predict(df[['x', 'y']])
    
    #Returns the sorted unique elements of an array
    labels_unique = np.unique(db.labels_)
    #drop the -1 labels which are unlabeled
    labels_unique = labels_unique[labels_unique != -1]
    
    
    return db.labels_, labels_unique

def populateSubPlot(df,
                    eps=3,
                    min_samples=50,
                    fig=None, 
                    axs=None, 
                    row=None, 
                    col=None,
                    title='Some Ward',
                    img=Image.open('maps/map_detailed_723.jpeg')
                   ):
    
        """
    Populates the subplots to show clustering for each kind
    
        Parameters
    ----------
    
    df: Pandas dataframe
        Data to be used for fitting. Must have columns 'x' and 'y'
    
    eps : float, default=0.5
        The maximum distance between two samples for one to be considered
        as in the neighborhood of the other. This is not a maximum bound
        on the distances of points within a cluster. This is the most
        important DBSCAN parameter to choose appropriately for your data set
        and distance function.
        
    axs: pyplot object, default=None
        Axis of pyplot
        
    fig: pyplot object, default=None
        Figure of subplots
        
    row: integer, default=None
        Row of subplot to be filled
        
    col: integer, default=None
        Column of subplot to be filled
        
    title: string, default=None
        Title of subplot
        
    img: string, default=presaved image
        Image to be filled in background
        
        
        
    
    """
        #assign labels to data and get unique labels
        db_labels, unique_labels = getLabels(df,
                                             eps=eps, 
                                             min_samples=min_samples)
    
        #set the title
        axs[row,col].set_title(title)
        
        #slap image on background
        axs[row,col].imshow(img, extent=[0, 128, 0, 128])

        #for each label and color
        for label, color in zip(unique_labels, colors):
            #places where label matches
            label_arg = np.argwhere(db_labels==label).ravel()
            #reduced version of where labels occur
            df_label_cluster = df.iloc[label_arg]
            #add scatter to plot
            axs[row,col].scatter(df_label_cluster['x'],
                                 df_label_cluster['y'], label=str(label),
                                 color=color)
    
    
    
    



def makeQuadSubplots(df_rad_obs, 
                     df_dir_obs, 
                     df_rad_sen, 
                     df_dir_sen, 
                     suptitle='Big title',
                     eps=3, 
                     min_samples=50):
    
    
    """
    Makes 4 subplots and fills each using data from the 4 dataframes.
    
    """
    fig, axs = plt.subplots(2, 2, 
                            figsize=(10,10)
                           )

    fig.suptitle('Clustering Output', fontsize=20)

    populateSubPlot(df=df_rad_obs,
                    eps=eps, 
                    min_samples=min_samples,
                    fig=fig, 
                    axs=axs, 
                    row=0, 
                    col=0, title='Obsever Wards Radiant')


    populateSubPlot(df=df_dir_obs, 
                    eps=eps, 
                    min_samples=min_samples,
                    fig=fig, 
                    axs=axs, 
                    row=0, 
                    col=1, title='Obsever Wards Dire')


    populateSubPlot(df=df_rad_sen, 
                    eps=eps, 
                    min_samples=min_samples,
                    fig=fig, 
                    axs=axs, 
                    row=1, 
                    col=0, title='Sentry Wards Radiant')

    populateSubPlot(df=df_dir_sen, 
                    eps=eps, 
                    min_samples=min_samples,
                    fig=fig, 
                    axs=axs, 
                    row=1, 
                    col=1, title='Sentry Wards Dire')
    
    
    return fig, axs


def timeSeparation(df_rad_obs, 
                   df_dir_obs, 
                   df_rad_sen, 
                   df_dir_sen,
                  t1=0,
                  t2=10):
    
    
    df1 = df_rad_obs[(df_rad_obs['time']>t1) & (df_rad_obs['time']<=t2)]
    df2 = df_dir_obs[(df_dir_obs['time']>t1) & (df_dir_obs['time']<=t2)]
    df3 = df_rad_sen[(df_rad_sen['time']>t1) & (df_rad_sen['time']<=t2)]
    df4 = df_dir_sen[(df_dir_sen['time']>t1) & (df_dir_sen['time']<=t2)]
    
    
    return df1, df2, df3, df4 


### BEGIN CALLING FUNCTIONS & WORK HERE ###

st.title('DOTA2 Ward Explorer')
st.subheader('An Interactive Tool To Explore Vision')



# ASK FOR USER INPUT #

eps_slide_value = st.slider(label = 'Select Range for Epsilon', 
                       min_value=0.0, 
                       max_value=5.0, value=2.0, step=0.5)


t1, t2 = st.slider(label = 'Select Time Frame', 
                        min_value=-5, 
                        max_value=100, value=(10, 20), step=1)

min_samples = st.slider(label = 'Select Minimum Samples Per Cluster', 
                        min_value=0, 
                        max_value=2_000, value=200, step=50)



# READ AND LOAD DATA#

df_obs, df_sen, img = load_data()

#separate by team
df_rad_obs = df_obs[(df_obs['is_radiant']==1)]
df_dir_obs = df_obs[(df_obs['is_radiant']==0)]

df_rad_sen = df_sen[(df_sen['is_radiant']==1)]
df_dir_sen = df_sen[(df_sen['is_radiant']==0)]

# APPLY USER INPUT #

df1, df2, df3, df4 = timeSeparation(df_rad_obs, 
                                    df_dir_obs, 
                                    df_rad_sen, 
                                    df_dir_sen,
                                    t1=t1,
                                    t2=t2)


fig, axs = makeQuadSubplots(df1, 
                            df2, 
                            df3, 
                            df4, 
                            eps=eps_slide_value, 
                            min_samples=50)


st.pyplot(fig)


