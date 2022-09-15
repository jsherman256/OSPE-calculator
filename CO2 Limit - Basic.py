import streamlit as st
from lib import *

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

form_container = st.empty()

with form_container.container():
    st.markdown("# OSPE Air Quality Calculator")
    st.markdown("## CO2 Limit - Basic")
    st.markdown("Find the maximum CO2 level for an ASHRAE-compliant room.")
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

    with st.expander("More info"):
        st.latex(f"vent_{{\\text{{per capita}}}} = {vent_per_capita}\\text{{ L/s/p}}")
        st.latex(f"co2_{{gen}} = {round(co2_per_capita, 5)}\\text{{ L/s/p}}")
        st.latex(f"co2_{{max}} = {int(max_co2)}\\text{{ ppm}} = {outdoor_co2}\\text{{ ppm}} + \\frac{{ {round(co2_per_capita, 5)} \\cdot 10^6 \\text{{ L/s/p}}}} {{ {vent_per_capita}  \\text{{ L/s/p}}}}")

    submitted = st.button('Print')

if submitted:
    form_container.empty()
    display(max_co2, room)