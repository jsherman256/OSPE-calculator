import streamlit as st
import pandas as pd

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')

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
    .read_csv('CO2_Generation.csv', header=[0,1], index_col=0)
    .applymap(lambda x: x / 10000)
)

st.markdown("# OSPE Air Quality Calculator")

(basic_tab, advanced_tab) = st.tabs(['Basic', 'Advanced'])

with basic_tab:
    # Create UI input elements
    room = st.selectbox(label='Room Type', options=vent.index)
    left, right = st.columns(2)
    with left:
        age = st.selectbox(label="Average Age", options=co2_gen.index)
    with right:
        met = st.selectbox(label="Metabolic Rate", options=[m[1] for m in co2_gen.columns if m[0] == 'Met'])

    # Do calculations
    vent_per_capita = vent.loc[room]['Total People Rate (lps/person)']
    co2_per_capita = co2_gen.loc[age][('Met', met)]
    max_co2 = outdoor_co2 + co2_per_capita*1000000 / vent_per_capita

    with st.expander("Debug output"):
        # Debug output
        st.code(f"""
        Room needs {vent_per_capita} lps/person.
Age "{age}" @ met {met} produces {co2_per_capita} lps/person of CO2
Max CO2: {int(max_co2)}
        """)

        st.latex(f"{outdoor_co2} + \\frac{{ {co2_per_capita} \\cdot 1000000}} {{ {vent_per_capita} }} = {max_co2}")

    st.markdown('---')

    st.markdown(f"<center><span style='font-size:80px;'>Maximum CO2</style></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:250px;'>{int(max_co2)}</style></center>", unsafe_allow_html=True)