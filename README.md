# DOTA Ward Finder

A project to identify heavily warded areas in DOTA2.

For an interactive implementation see this link:
https://share.streamlit.io/nadimkawwa/dotawardfinder/main/appWardFinder.py

## Use Cases
By looking at gaming through a data science perspective, we can infer the game style of more experienced players. Indeed, regardless of skill level, <b>vision</b> remains a crucial aspect of DOTA2. In addition, it's possible to reverse engineer how services like [Dota Plus](https://www.dota2.com/plus) make their suggestions.

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

## Methodology

Since the overall strategy changes based on how long the game has been running, the clustering is segmented based on time. In addition, DBSCAN is the algorithm of choise for finding clusters.
Therefore, the main paramters for this project are:
- Time frame
- Epsilon
- Min number of samples

## Sample Plots

### Very Early Game
Before the first creep waves leave the base, players compete for gold runes. Therefore, players place observer wards near the center of the map at the river in order to see what the enemy is doing. Moreover, some place observer wards deep in the enemy jungle before the enemy has time to deward it. 
Lastly, the sentry wards shown in red correspond to economical warfare. Indeed, a sentry ward placed inside the bounding box of a neutral creep camp prevents the latter from spawning. Hence the enemy team is denied gold and the ability to pull the creep wave.

![Wards Before Game Start](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/plots/Wards_Placed_Before_Minute_0_00.png)


### Mid to Late Game

In the mid to late game, teams can turn their attention to Roshan's pit. This is represented by the hilltops near the pit being populated with obsever wards and sentry wards placed at the entrance to detect an attempt to snatch the aegis.

![Mid to Late Game](https://github.com/NadimKawwa/DOTAWardFinder/blob/main/plots/Wards_Placed_From_30_00_to_40_00.png)
