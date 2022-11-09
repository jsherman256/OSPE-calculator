import streamlit as st
from lib import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')


form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## CO2 Limit - Advanced")
    st.markdown("Find the expected steady-state CO2 level for an ASHRAE-compliant room.")
    st.markdown("---")

    st.markdown("### Room")
    # Room parameters
    left, right = st.columns([3,1])
    with left:
        room = st.selectbox(label='Room Type', options=vent.index, index=default_room)
    with right:
        room_size = st.number_input(label='Room Size (sq m)', min_value=1, value=75)

    st.markdown("### People")
    # People parameters
    left, center, right = st.columns([1,1,3])
    with left:
        people = st.number_input(label="Number Occupants", min_value=1, value=25)
    with center:
        age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_age)
    with right:
        activity = st.selectbox(label="Activity", options=activities.index, index=default_activity)

    # Look up Met
    met = activities.loc[activity].Met

    # Do calculations
    vent_params = vent.loc[room]
    vent_needed = (vent_params['People Rate'] * people) + (vent_params['Area Rate'] * room_size)

    co2_created = co2_gen.loc[age][met] * people
    max_co2 = outdoor_co2 + co2_created*1000000 / vent_needed
    co2_half_cap = (max_co2 + outdoor_co2) / 2

    room_volume_estimate = room_size * 2.7 # Assume 2.7m ceilings
    outdoor_ach = vent_needed * 3.6 / room_volume_estimate
    extra_ach = 6 - outdoor_ach
    vent_only_co2_limit = outdoor_co2 + co2_created * 1000000 / (vent_needed*(6/outdoor_ach))

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Total outdoor airflow**| $ ({vent_params['People Rate']}{u.lps}\\cdot {people}{u.people}) + ({vent_params['Area Rate']}{u.lps} \\cdot {room_size}{u.sq_m}) $ | $ = {round(vent_needed,2)} {u.lps}$|
    |**Total CO2 generated**| $ {co2_gen.loc[age][met]}{u.lps_per_person} \\cdot {people}{u.people} $ | $ = {round(co2_created,5)}{u.lps} $ |
    |**Steady State CO2**| $ {outdoor_co2}{u.ppm} + \\frac{{{round(co2_created, 5)} {u.lps}}}{{{round(vent_needed,2)}{u.lps}}} \\cdot {u.mega} $ | $ = {int(max_co2)}{u.ppm} $ |
    |**ACH of outdoor air**| $ ({round(vent_needed,2)}{u.lps} \cdot 3.6) \div ({room_size}{u.sq_m} \cdot 2.7{u.meter}) $ | $ = {round(outdoor_ach, 1)}{u.ach} $ |
    """
    )

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display_v2_std(
        max_co2,
        co2_half_cap,
        outdoor_ach,
        extra_ach,
        vent_only_co2_limit,
        details={
            "Room:": room, 
            "Average Age:": age,
            "Activity:": activity
        }
    )