import streamlit as st
from lib import *
import units as u

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## Residential Buildings")
    st.markdown("Find the expected steady-state CO2 level for a residential building.")
    st.markdown("---")

    # Create UI input elements
    # Room parameters
    st.markdown("### Building")
    left, right = st.columns(2)
    with left:
        bedrooms = st.selectbox(label='Number Bedrooms', options=residential.columns)
    with right:
        floor_space = st.selectbox(label='Floor Space (sq m)', options=residential.index)

    st.markdown("### People")
    left, right = st.columns(2)
    with left:
        people_count_a = st.number_input(label="Number People", min_value=1, step=1, value=2, key="num_people_a")
        people_count_b = st.number_input(label="Number People", min_value=0, step=1, key="num_people_b")
        people_count_c = st.number_input(label="Number People", min_value=0, step=1, key="num_people_c")
    with right:
        age_a = st.selectbox(label="Age", options=co2_gen.index, index=co2_gen.index.get_loc("30 to <40"), key="age_a")
        age_b = st.selectbox(label="Age", options=co2_gen.index, index=co2_gen.index.get_loc("16 to < 21"), key="age_b", disabled=(people_count_b == 0))
        age_c = st.selectbox(label="Age", options=co2_gen.index, index=co2_gen.index.get_loc("3 to <6"), key="age_c", disabled=(people_count_c == 0))

    # Assume Met of 1.3
    met = 1.3

    # Do calculations
    co2_created = (
        co2_gen.loc[age_a][met] * people_count_a
        + co2_gen.loc[age_b][met] * people_count_b
        + co2_gen.loc[age_c][met] * people_count_c
    )
    vent_needed = residential.loc[floor_space][bedrooms]
    max_co2 = outdoor_co2 + co2_created*1000000 / vent_needed
    co2_half_cap = (max_co2 + outdoor_co2) / 2

    st.markdown("### Results")
    st.markdown(f"""
    ||||
    |-|-|-|
    |**Total outdoor airflow**| | $ = {vent_needed} {u.lps}$|
    |**Total CO2 generated**| | $ = {round(co2_created, 5)} {u.lps}$|
    |**Steady State CO2**| ${outdoor_co2}{u.ppm} + \\frac{{{round(co2_created, 5)} {u.lps}}}{{{round(vent_needed,2)}{u.lps}}} \\cdot {u.mega} $ | $ = {int(max_co2)}{u.ppm} $ |
    """)

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    details = {
        "Bedrooms:": bedrooms, 
        f"Floor Space:": f"{floor_space} m²",
        f"Ages {age_a}:": f"{people_count_a} people",
    }
    if people_count_b > 0:
        details[f"Ages {age_b}:"] = f"{people_count_b} people"
    if people_count_c > 0:
        details[f"Ages {age_c}:"] = f"{people_count_c} people"
    display_v2_residential(
        max_co2,
        co2_half_cap,
        details
    )