# DOTA Ward Finder

A project to identify heavily warded areas in DOTA2 based on game objectives. 

For an interactive implementation see this link:
https://share.streamlit.io/nadimkawwa/dotawardfinder/main/appWardObjectives.py

For the previous iteration of this project:
https://share.streamlit.io/nadimkawwa/dotawardfinder/main/appWardFinder.py

## Use Cases
By looking at gaming through a data science perspective, we can infer the game style of more experienced players. Indeed, regardless of skill level, <b>vision</b> remains a crucial aspect of DOTA2. In addition, it's possible to reverse engineer how services like [Dota Plus](https://www.dota2.com/plus) make their suggestions.

## What Are Objectives in DOTA2?
You win the game by destroying the enemy team's ancient (fort). In order to be able to hit the fort you need to clear out all the towers in one of the 3 map lanes. Each lane has 3 towers and the fort has 2 towers attached to it. In DOTA2 terminilogy <b><i>capturing an objective</i></b> means destroying a particular building. I highly recommend playing some DOTA2 games to gain a better understanding of this project and to appreciate the game's complexity. 

## Getting Started

This project is written purely in python 3.6 and packages used are:
- streamlit
- pandas
- numpy
- matplotlib
- Pillow
- scikit-learn

## Data Collection

Data is collected from opendota.com using its API. An example is provided in this [sample query](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/ward_logs_pro_matches.sql).
The raw data need to be ingested and massaged into a format that suits this project's need. 
To see how nested JSON data is ingested, refer to [Notebook #5](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/05_ConsolidatedObjectivesData.ipynb) which uses [helper classes](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/HelperClasses.py).


## Methodology

### Towers
Since the overall strategy changes based on captured objectives, the clustering is segmented based on what towers are still standing. Assuming that the JSON file has been parsed, the workflow is as follows:
1) Filter data based on what towers are still standing.
2) Partition the data in subdivisions based on Team+Type. <br>
  2.1 Radiant + Observer <br>
  2.2 Radiant + Sentry <br>
  2.3 Dire + Obsever <br>
  2.4 Dire + Sentry <br>
3) Find clusters for each subdivision.
4) Calculcate centroid of each cluster.
5) Plot map reflecting warding status

### Roshan
Same as the previous section with two modifications:
- Only look at wards in upper left quadrant of map.
- Partially color towers to show on average what percentage is still alive.

## Trying it Locally
The main class used is [WardFinder](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/07_WardCircles.ipynb) found in notebook #7. It is made to resemble the implementations of scikit learn with a fit method and built in plotting functions. 


```python
# instantiate the class 
wards = WardFinder(obs_data_path = 'df_obs_obj.csv', #observer wards
                   sen_data_path = 'df_sen_obj.csv', #sentry wards
                   map_img = 'maps/map_detailed_723.jpeg', #background map
                   exclude_pregame=False #exclude wards planted before 0:00?
                  )
# what's the most recently captured objective?
# enter 0 to say that all towers ar
wards.get_filtered_wards(radiant_top = 1, 
                         radiant_mid =1, 
                         radiant_bot = 1, 
                         dire_top =2 , 
                         dire_mid = 1, 
                         dire_bot=1
                        )

# fit to existing data 
# anytime the get_filtered_wards is called the status is reset to most recent input
wards.fit_clusters()

# plot it and save it somewhere
wards.plot_wards(save_path = os.path.join('tower_combos','test_map.png'),
                 show_plot=True)

```


## Interactive Web App

The result is the web app below hosted on streamlit:
https://share.streamlit.io/nadimkawwa/dotawardfinder/main/appWardObjectives.py

You will be asked to specify what objectives are captured and when done the app will show the plots.

## Sample Plots

### Towers

The map below shows the last standing towers as listed below. 
- Radiant Top T2 
- Radiant Mid T2 
- Radiant Bot T3
- Dire Top T1
- Dire Mid T1
- Dire Bot T1

This is a very advantegeous position for Dire who have not lost a single tower. Hence almost all warding is done the Radiabnt safe jungle and triangle.

![Captured Towers](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/maps/A1_B1_C2_D0_E0_F0.png)


### Roshan

Getting Roshan can be done more than once. The image below shows the 1st attempt where all entrances need to be secured.
In some very rare cases, taking Roshan is done before attacking the enemy highground (T3 towers). However, most players agree it's a better idea to secure the Aegis before pushing for highground.

![Rosh Attempt #1](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/maps/rosh_attempt_01.png)


