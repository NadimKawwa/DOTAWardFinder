import streamlit as st
import requests
import io
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt


#this line must come first
#st.set_page_config(layout="wide")


### DEFINE FUNCTIONS TO HELP WITH LOADING DATA ###

@st.cache(persist=True)
def load_invalid_combos():
    """
    Loads invalid combos from public S3 bucket
    
    """
    #get the response URL
    response = requests.get('https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/invalid_cases.txt')
    
    #store text 
    text = response.text
    
    #separate by new line character
    invalid_combos = text.split('\n')
    
    return invalid_combos


@st.cache(persist=True)
def load_tower_image(combo):
    """
    Loads the image associated with a tower combo
    """
    img_url = ''.join(['https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/', 
                       combo,
                       '.png'])
    
    
    img_response = requests.get(img_url)
    combo_img = Image.open(BytesIO(img_response.content))
    
    return combo_img
    
    
@st.cache(persist=True)
def load_rosh_image(rosh_attempt):
    """
    Loads the warding in the upper left quadrant 
    """
    img_url = ''.join(['https://nadim-kawwa-dota-bucket.s3.us-west-2.amazonaws.com/rosh_attempt_0', 
                    str(rosh_attempt),
                    '.png'])
    
    
    img_response = requests.get(img_url)
    rosh_img = Image.open(BytesIO(img_response.content))
    
    return rosh_img
    
### BEGIN CALLING FUNCTIONS HERE ###


st.title('DOTA2 Wards & Objectives')
st.subheader('An Interactive Tool To Explore Warding')

st.write('Select the most recently captured objective for each lane. A value of zero means that the tower is still alive.')
st.write('Scroll down to explore warding related to Roshan.')

#load invalid cases
invalid_combos = load_invalid_combos()


# ASK FOR USER INPUT #


rad_top = st.slider(label = 'Radiant Top', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)
rad_mid = st.slider(label = 'Radiant Mid', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)
rad_bot = st.slider(label = 'Radiant Bot', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)
dir_top = st.slider(label = 'Dire Top', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)
dir_mid = st.slider(label = 'Dire Mid', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)
dir_bot = st.slider(label = 'Dire Bot', 
                    min_value=0, 
                    max_value=3, 
                    value=1, 
                    step=1)

#make tuple from user input
user_input_tuple = (rad_top,
                    rad_mid, 
                    rad_bot, 
                    dir_top, 
                    dir_mid, 
                    dir_bot)

#convert each element to string
combo_string_tuple = tuple((str(x) for x in user_input_tuple))

#convert to combo
combo = '_'.join([a+b for a,b in zip('ABCDEF', combo_string_tuple)])

if st.button('Show Wards for Towers'):
    if combo in invalid_combos:
        st.write("Not enough data and/or invalid combo! Try again.")
    else:
        #st.write(combo)
        combo_img = load_tower_image(combo)
        st.image(combo_img)

        
rosh_attempt = st.slider(label = 'Roshan Attempt Number', 
                         min_value=1, 
                         max_value=3, 
                         value=1, 
                         step=1)



        
if st.button('Show Wards for Roshan'):
    rosh_img = load_rosh_image(rosh_attempt)
    st.image(rosh_img)

                 

                 


