import pandas as pd
import streamlit as st

# Set a reasonable value for outdoor CO2
outdoor_co2 = 420

# Load CSV files
vent = (
    pd
    .read_csv('ASHRAE_62-1_Values.csv')
)
vent = (
    vent
    .assign(Descriptor = vent.Category + " - " + vent["Room Type"])
    .set_index('Descriptor')
)
co2_gen = (
    pd
    .read_csv('CO2_Generation.csv', index_col=0)
    .applymap(lambda x: x / 10000)
)
co2_gen.columns = co2_gen.columns.astype(float)
activities = (
    pd
    .read_csv('Activity-Met.csv', index_col=0)
)
csa = (
    pd
    .read_csv('CSA_Healthcare_Values.csv', index_col=0)
)

# Look up the ordinal index for the default selectbox values
default_room = vent.index.get_loc("Educational Facilities - Classrooms (Ages 9+)")
default_age = co2_gen.index.get_loc("6 to <11")
default_activity = activities.index.get_loc("Sitting tasks, light effort (office work)")

default_health_age = co2_gen.index.get_loc("30 to <40")
default_health_activity = activities.index.get_loc("Standing quietly")

def display(max_co2, room_type, additional=None):
    st.markdown(f"<center><span style='font-size:70px;'>Maximum CO2</style></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:30px;'>{room_type}</style></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:220px;'>{int(max_co2)}</style></center>", unsafe_allow_html=True)
    if additional:
        for key, value in additional.items():
            st.markdown(f"**{key}**  {value}")
    rerun = st.button('Rerun')

    if rerun:
        st.experimental_rerun()

def display_ach(ach):
    # If ACH is within ±0.1 of an integer, just show the integer portion
    # Otherwise, round to the nearest 0.1
    ach = int(ach) if (abs(int(ach) - ach) < .1) else round(ach, 1)

    if ach >= 12:
        rating = "Excellent!"
    if ach < 12 and ach >= 6:
        rating = "Good"
    if ach < 6 and ach >= 4:
        rating = "Ok"
    if ach < 4:
        rating = "Poor"

    st.markdown(f"<center><h1>{ach} ACH</h1></center>", unsafe_allow_html=True)
    st.markdown(f"<center><h1>{rating}</h1></center>", unsafe_allow_html=True)
    