import streamlit as st
from lib import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## Healthcare - Basic")
    st.markdown("Basic calculator for CSA ventilation requirements in healthcare settings.")
    st.markdown("---")

    # Create UI input elements
    st.markdown("### Room")
    room = st.selectbox(label='Room Type', options=csa.index)

    st.markdown("### People")
    left, right = st.columns(2)
    with left:
        age = st.selectbox(label="Average Age", options=co2_gen.index, index=default_health_age)
    with right:
        activity = st.selectbox(label="Activity", options=activities.index, index=default_health_activity)

    # Look up Met from activity
    met = activities.loc[activity].Met

    # Do calculations
    vent_per_capita = csa.loc[room]['Ventilation People Rate (lps/person)']
    total_per_capita = csa.loc[room]['Total People Rate (lps/person)']
    co2_per_capita = co2_gen.loc[age][met]
    max_co2 = outdoor_co2 + co2_per_capita*1000000 / vent_per_capita
    co2_half_cap = (max_co2 + outdoor_co2) / 2

    # Extra info
    extra_ach = round(csa.loc[room]['Total ACH'] - csa.loc[room]['Air Changes per Hour from Ventilation'], 1)
    vent_only_vent_per_capita = total_per_capita
    vent_only_co2_limit = outdoor_co2 + co2_per_capita*1000000 / vent_only_vent_per_capita

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Outdoor airflow per person**| |$ = {round(vent_per_capita, 2)}{u.lps_per_person}$|
    |**CO2 generated per person**| |$ = {round(co2_per_capita, 5)}{u.lps_per_person}$|
    |**Steady State CO2**| $ {outdoor_co2}{u.ppm} + \\frac{{ {round(co2_per_capita, 5)}{u.lps_per_person}}}{{ {round(vent_per_capita, 2)}{u.lps_per_person}}} \\cdot {u.mega} $ | $ = {int(max_co2)}{u.ppm} $|
    """)
    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display_v2_health(
        max_co2,
        co2_half_cap,
        extra_ach=extra_ach,
        outdoor_ach=csa.loc[room]['Air Changes per Hour from Ventilation'],
        vent_only_co2_limit=vent_only_co2_limit,
        details={
            "Room:": room,
            "Required Outdoor CADR per person:": f"{vent_per_capita} lps",
            "Total Required CADR per person:": f"{total_per_capita} lps"
        }
    )
