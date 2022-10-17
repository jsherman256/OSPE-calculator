import streamlit as st
from converters import cfm_to_cubic_meters_per_hour, lps_to_cubic_meters_per_hour
from lib import *
from converters import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')


st.markdown("# OSPE Air Quality Calculator")
st.markdown("## Air Changes from Filtration")
st.markdown("Find the number of air changes per hour provided by an air purifier.")
st.markdown("---")

st.markdown("### Room")
# Room parameters
left, right = st.columns([1,1])
with left:
    room_volume = st.number_input(label='Room Volume', step=1, min_value=1, value=200)
with right:
    volume_unit = st.selectbox(label='Volume Unit', options=['cubic meters', 'cubic feet'])

st.markdown("### Filtration")
# Filtration
left, right = st.columns([1,1])
with left:
    max_cadr = st.number_input(label='Clear Air Delivery Rate (CADR)', step=1, min_value=1, value=250)
with right:
    cadr_unit = st.selectbox(label="CADR Unit", options=['CFM', 'lps', 'm^3/h'])

# Convert CADR to cubic meters per hour (if necessary)
if cadr_unit == 'm^3/h':
    max_cadr_m3ph = max_cadr
elif cadr_unit == 'CFM':
    max_cadr_m3ph = cfm_to_cubic_meters_per_hour(max_cadr)
elif cadr_unit == 'lps':
    max_cadr_m3ph = lps_to_cubic_meters_per_hour(max_cadr)

# Convert room volume to cubic meters
if volume_unit == 'cubic meters':
    volume_m3 = room_volume
elif volume_unit == 'cubic feet':
    volume_m3 = cubic_feet_to_cubic_meters(room_volume)

# This *should* always be true, but best to double check
if volume_m3 > 0:
    ach = max_cadr_m3ph / volume_m3
    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Air Changes per Hour**| $ \\frac{{\\text{{CADR}}}}{{\\text{{Volume}}}} = \\frac{{{round(max_cadr_m3ph,2)} {u.m3ph}}}{{{round(volume_m3,2)} {u.cubic_m}}} $ | $ = {round(ach,2)} $ |
    """)
    display_ach(ach)