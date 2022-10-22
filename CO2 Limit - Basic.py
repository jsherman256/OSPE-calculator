import streamlit as st
from lib import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## CO2 Limit - Basic")
    st.markdown("Find the expected steady-state CO2 level for an ASHRAE-compliant room.")
    st.markdown("---")

    # Create UI input elements
    st.markdown("### Room")
    room = st.selectbox(label='Room Type', options=vent.index, index=default_room)

    st.markdown("### People")
    left, right = st.columns(2)
    with left:
        age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_age)
    with right:
        activity = st.selectbox(label="Activity", options=activities.index, index=default_activity)

    # Look up Met from activity
    met = activities.loc[activity].Met

    # Do calculations
    vent_per_capita = vent.loc[room]['Total People Rate (lps/person)']
    co2_per_capita = co2_gen.loc[age][met]
    max_co2 = outdoor_co2 + co2_per_capita*1000000 / vent_per_capita

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Outdoor airflow per person**| | $ = {vent_per_capita} {u.lps_per_person}$|
    |**CO2 generated per person**| | $ = {round(co2_per_capita, 5)} {u.lps_per_person}$|
    |**Steady State CO2**|${outdoor_co2}{u.ppm} + \\frac{{ {round(co2_per_capita, 5)}{u.lps_per_person}}} {{ {vent_per_capita}{u.lps_per_person}}} \\cdot {u.mega}$|$ = {int(max_co2)}{u.ppm}$
    """)

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display_v2(
        max_co2,
        details={
            "Room:": room, 
            "Average Age:": age,
            "Activity:": activity
        }
    )