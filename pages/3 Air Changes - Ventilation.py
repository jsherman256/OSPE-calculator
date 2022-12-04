import streamlit as st
from converters import cfm_to_cubic_meters_per_hour, lps_to_cubic_meters_per_hour
from lib import *
from converters import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

st.markdown("# OSPE Air Quality Calculator")
st.markdown("## Air Changes from Ventilation")
st.markdown("Estimate the number of outdoor air changes based on indoor CO2 levels.")
st.markdown("---")

st.markdown("### Room")
# Room parameters
left, right = st.columns(2)
with left:
    room_volume = st.number_input(label='Room Volume', step=1, min_value=1, value=200)
with right:
    volume_unit = st.selectbox(label='Volume Unit', options=['cubic meters', 'cubic feet'])

st.markdown("### People")
# People parameters
left, center, right = st.columns([1,1,3])
with left:
    people = st.number_input(label="Number Occupants", min_value=1, value=25)
with center:
    age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_age)
with right:
    activity = st.selectbox(label="Activity", options=activities.index, index=default_activity)

st.markdown("### CO₂")
left, right = st.columns(2)
with left:
    outdoor_co2_actual = st.number_input(label='Outdoor CO2', step=5, min_value=350, value=outdoor_co2)
with right:
    indoor_co2 = st.number_input(label='Steady-State Indoor CO2', step=5, min_value=350, value=900)

# Convert room volume to cubic meters
if volume_unit == 'cubic meters':
    volume_m3 = room_volume
elif volume_unit == 'cubic feet':
    volume_m3 = cubic_feet_to_cubic_meters(room_volume)

if indoor_co2 <= outdoor_co2_actual:
    st.error("Indoor CO2 must be greater than outdoor CO2. Please check your numbers.")

# This *should* always be true, but best to double check
if volume_m3 > 0 and indoor_co2 > outdoor_co2_actual:
    # Look up Met from activity
    met = activities.loc[activity].Met

    # Do calculations
    co2_per_capita = co2_gen.loc[age][met]
    vent_per_capita = co2_per_capita * 1000000 / (indoor_co2 - outdoor_co2_actual)
    total_vent_lps = vent_per_capita * people
    ach = 3.6 * total_vent_lps / volume_m3

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**CO2 generated per person**| | $ = {round(co2_gen.loc[age][met], 5)}{u.lps_per_person} $|
    |**Outdoor airflow per person**| $ \\frac{{{round(co2_per_capita, 5)} {u.lps_per_person}}}{{{indoor_co2}{u.ppm} - {outdoor_co2_actual}{u.ppm}}} \\cdot {u.mega} $ | $ = {round(vent_per_capita, 1)}{u.lps_per_person} $ |
    |**Total outdoor airflow**| $ {round(vent_per_capita, 1)}{u.lps_per_person} \\cdot {people}{u.people} $ | $ = {round(total_vent_lps, 1)}{u.lps} $|
    |**Air changes per hour**| $ 3.6 \\cdot \\frac{{{round(total_vent_lps, 1)}{u.lps}}}{{{round(volume_m3, 1)}{u.cubic_m}}} $ | $ = {round(ach, 2)}{u.ach} $ |
    """)
    display_ach(ach)