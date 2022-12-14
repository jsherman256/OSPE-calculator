import streamlit as st
from lib import *
from converters import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')


form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## Healthcare - Advanced")
    st.markdown("Advanced calculator for CSA ventilation requirements in healthcare settings.")
    st.markdown("---")

    st.markdown("### Room")
    # Room parameters
    left, right = st.columns([3,1])
    with left:
        room = st.selectbox(label='Room Type', options=csa.index)
    with right:
        room_size = st.number_input(label='Room Size (sq m)', min_value=1, value=75)

    st.markdown("### People")
    # People parameters
    left, center, right = st.columns([1,1,3])
    with left:
        people = st.number_input(label="Number Occupants", min_value=1, value=5)
    with center:
        age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_health_age)
    with right:
        activity = st.selectbox(label="Activity", options=activities.index, index=default_health_activity)

    # Look up Met
    met = activities.loc[activity].Met

    # Do calculations
    outdoor_ach_needed = csa.loc[room]['Air Changes per Hour from Ventilation']
    vent_needed = cubic_meters_per_hour_to_lps(
        outdoor_ach_needed * 2.7 * room_size
    )

    co2_created = co2_gen.loc[age][met] * people
    max_co2 = outdoor_co2 + co2_created*1000000 / vent_needed
    co2_half_cap = (max_co2 + outdoor_co2) / 2

    # Air changes needed beyond ventilation
    extra_ach = round(csa.loc[room]['Total ACH'] - csa.loc[room]['Air Changes per Hour from Ventilation'], 1)

    # Ventilation needed and CO2 readings if ventilation is not the only method of air cleaning
    vent_only_vent_needed = cubic_meters_per_hour_to_lps(
        csa.loc[room]['Total ACH'] * 2.7 * room_size
    )
    vent_only_co2_limit = outdoor_co2 + co2_created*1000000 / vent_only_vent_needed

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Total outdoor airflow**|${outdoor_ach_needed}{u.ach} \\cdot {room_size}{u.sq_m} \\cdot 2.7{u.meter} \\cdot {u.m3ph_over_lps}$|$= {round(vent_needed,2)}{u.lps}$|
    |**Total CO2 generated**|${round(co2_gen.loc[age][met], 5)}{u.lps_per_person} \\cdot {int(people)}{u.people}$|$= {round(co2_created, 5)}{u.lps}$|
    |**Steady State CO2**|${outdoor_co2}{u.ppm} + \\left(\\frac{{{round(co2_created, 5)}{u.lps}}}{{{round(vent_needed, 2)}{u.lps}}}\\right) \\cdot {u.mega}$|$ = {int(max_co2)}{u.ppm}$|
    """)

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display_v2_health(
        max_co2,
        co2_half_cap,
        extra_ach=extra_ach,
        vent_only_co2_limit=vent_only_co2_limit,
        outdoor_ach=outdoor_ach_needed,
        details={
            "Room:": room,
            "Required Total Outdoor CADR:": f"{round(vent_needed,2)} L/s",
        }
    )