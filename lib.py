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

def display(max_co2):
    st.markdown('---')

    st.markdown(f"<center><span style='font-size:80px;'>Maximum CO2</style></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:250px;'>{int(max_co2)}</style></center>", unsafe_allow_html=True)