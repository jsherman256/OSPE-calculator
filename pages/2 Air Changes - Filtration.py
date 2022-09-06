import streamlit as st
from converters import cfm_to_cubic_meters_per_hour, lps_to_cubic_meters_per_hour
from lib import *
from converters import *

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')


st.markdown("# OSPE Air Quality Calculator")
st.markdown("## Air Changes from Filtration")
st.markdown("Find the number of air changes per hour provided by an air purifier.")
st.markdown("---")

# Room parameters
left, right = st.columns([1,1])
with left:
    max_cadr = st.number_input(label='Clear Air Delivery Rate (CADR)', step=1, min_value=1, value=250)
with right:
    cadr_unit = st.selectbox(label="CADR Unit", options=['CFM', 'lps', 'm^3/h'])

left, right = st.columns([1,1])
with left:
    room_volume = st.number_input(label='Room Volume', step=1, min_value=1, value=75)
with right:
    volume_unit = st.selectbox(label='Volume Unit', options=['cubic meters', 'cubic feet'])

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
    with st.expander("More info"):
        st.latex(f"\\frac{{{max_cadr_m3ph} \\frac{{m^3}}{{h}}}}{{{volume_m3} m^3}}")
    ach = max_cadr_m3ph / volume_m3

    # If ACH is within ±0.1 of an integer, just show the integer portion
    # Otherwise, round to the nearest 0.1
    ach = int(ach) if (abs(int(ach) - ach) < .1) else round(ach, 1)

    st.markdown(f"<center><h1>{ach} ACH</h1></center>", unsafe_allow_html=True)