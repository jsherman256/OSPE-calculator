import streamlit as st
from lib import *

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

    with st.expander(label='More info'):
        st.latex(f"vent_{{total}} = {round(vent_needed,2)}\\text{{ L/s}} = ({vent_params['People Rate']}\\text{{ L/s}}\\cdot {people}\\text{{ people}}) + ({vent_params['Area Rate']}\\text{{ L/s}} \\cdot {room_size}\\text{{ }}m^2)")
        st.latex(f"co2_{{gen}} = {round(co2_created,5)}\\text{{ L/s}} = {co2_gen.loc[age][met]}\\text{{ L/s}} \\cdot {people}\\text{{ people}}")
        st.latex(f"co2_{{max}} = {int(max_co2)}\\text{{ ppm}} = {outdoor_co2}\\text{{ ppm}} + \\frac{{{round(co2_created, 5)} \\cdot 10^6\\text{{ L/s}}}}{{{round(vent_needed,2)}\\text{{ L/s}}}}")

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display(max_co2, room)