import streamlit as st
from converters import cfm_to_cubic_meters_per_hour, lps_to_cubic_meters_per_hour
from lib import *
from converters import *

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

st.markdown("# OSPE Air Quality Calculator")
st.markdown("## Air Changes from Ventilation")
st.markdown("Estimate the number of outdoor air changes based on indoor CO2 levels.")
st.markdown("---")

# Room parameters
outdoor, indoor, vol, vol_u = st.columns(4)
with outdoor:
    outdoor_co2_actual = st.number_input(label='Outdoor CO2', step=5, min_value=350, value=outdoor_co2)
with indoor:
    indoor_co2 = st.number_input(label='Steady-State Indoor CO2', step=5, min_value=350, value=900)
with vol:
    room_volume = st.number_input(label='Room Volume', step=1, min_value=1, value=75)
with vol_u:
    volume_unit = st.selectbox(label='Volume Unit', options=['cubic meters', 'cubic feet'])

# People parameters
left, right = st.columns(2)
with left:
    people = st.number_input(label="Number Occupants", min_value=1, value=25)
with right:
    age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_age)

activity = st.selectbox(label="Activity", options=activities.index, index=default_activity)

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

    with st.expander("More info"):
        st.latex(f"co2_{{\\text{{per capita}}}} = {co2_gen.loc[age][met]}\\text{{ L/s}}")
        st.latex(f"vent_{{\\text{{per capita}}}} = \\frac{{{co2_per_capita} \\cdot 10^6}}{{{indoor_co2} - {outdoor_co2_actual}}} = {round(vent_per_capita, 1)}\\text{{ L/s}}")
        st.latex(f"vent_{{total}} = {round(vent_per_capita, 1)} \\cdot {people} = {round(total_vent_lps, 1)}\\text{{ L/s}}")
        st.latex(f"ACH = 3.6 \\cdot \\frac{{{round(total_vent_lps, 1)}}}{{{round(volume_m3, 1)}m^3}} = {round(ach, 1)}")

    display_ach(ach)