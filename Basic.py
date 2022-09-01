import streamlit as st
from lib import *

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

st.markdown("# OSPE Air Quality Calculator")

# Create UI input elements
room = st.selectbox(label='Room Type', options=vent.index, index=default_room)
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

with st.expander("Debug output"):
    # Debug output
    st.code(f"""
    Room needs {vent_per_capita} lps/person.
Age "{age}" @ met {met} produces {co2_per_capita} lps/person of CO2
Max CO2: {int(max_co2)}
    """)

    st.latex(f"{outdoor_co2} + \\frac{{ {co2_per_capita} \\cdot 1000000}} {{ {vent_per_capita} }} = {max_co2}")

display(max_co2)