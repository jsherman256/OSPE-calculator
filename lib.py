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
    .read_csv('Activity-Met.csv')
)
activities.Activity = activities.apply(lambda x: f"{x.Activity} - Met {x.Met}", axis=1)
activities = activities.set_index('Activity')
csa = (
    pd
    .read_csv('CSA_Healthcare_Values.csv', index_col=0)
)
residential = (
    pd
    .read_csv('residential.csv', index_col=0)
)

# Look up the ordinal index for the default selectbox values
default_room = vent.index.get_loc("Educational Facilities - Classrooms (Ages 9+)")
default_age = co2_gen.index.get_loc("6 to <11")
default_activity = activities.index.get_loc("Sitting tasks, light effort (office work) - Met 1.5")

default_health_age = co2_gen.index.get_loc("30 to <40")
default_health_activity = activities.index.get_loc("Standing quietly - Met 1.3")

def display(max_co2, room_type, additional=None):
    st.markdown(f"<center><span style='font-size:70px;'>Maximum CO2</span></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:30px;'>{room_type}</span></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:220px;'>{int(max_co2)}</span></center>", unsafe_allow_html=True)
    if additional:
        for key, value in additional.items():
            st.markdown(f"**{key}**  {value}")
    rerun = st.button('Rerun')

    if rerun:
        st.experimental_rerun()

def display_v2_residential(co2, details):
    info_string = """Health Canada recommends maintaining the average CO2 level in your home below 1000 ppm."""
    display_v2(co2, None, details, info_string, activity_warning=False)

def display_v2_std(co2, co2_half_cap, outdoor_ach, extra_ach, vent_only_co2_limit, details):
    info_string = f"""OSPE Indoor Air Quality Advisory Group (IAQAG) recommends 6 air changes per hour (ACH). 
    The ventilation rate from ASHRAE 62.1 is {round(outdoor_ach, 1)} ACH. """
    if extra_ach > 0:
        info_string += f"""An additional {round(extra_ach, 1)} ACH are required to comply with OSPE IAQAG recommendations. 
        <b>If ventilation is the only method used to achieve 6 ACH, CO2 levels should be {int(vent_only_co2_limit)} ppm.</b> 
        Additional air changes can be achieved through ventilation, filtration or ultraviolet germicidal irradiation."""
    display_v2(co2, co2_half_cap, details, info_string)

def display_v2_health(co2, co2_half_cap, outdoor_ach, extra_ach, vent_only_co2_limit, details):
    info_string = f"""OSPE Indoor Air Quality Advisory Group recommends the use of upper room UVGI in healthcare settings. 
    CO2 level is based on {outdoor_ach} ACH of outdoor air from CSA standard Z317.2-2019. 
    An additional {extra_ach} air changes per hour are also required. 
    <b>If ventilation is the only method used, CO2 levels should be {int(vent_only_co2_limit)} ppm.</b>
    Upper room UVGI systems will exceed these requirements."""
    display_v2(co2, co2_half_cap, details, info_string)

def display_v2(co2, co2_half_cap, details, info_string = None, activity_warning=True):
    st.markdown(f"<center><span style='font-size:35px;'>Expected Steady State CO2</span></center>", unsafe_allow_html=True)
    st.markdown(f"<center><span style='font-size:150px;'>{int(co2)}</span></center>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    for (k,v) in details.items():
        st.markdown(f"<span style='font-size:20px;'><strong>{k}</strong> {v}</span>", unsafe_allow_html=True)
    
    disclaimer = ""
    if activity_warning:
        disclaimer += "This is the expected maximum CO2 level when the room is used as described. "
    if co2_half_cap:
        disclaimer += f"If the room is at half capacity, expected CO2 levels would be {int(co2_half_cap)} ppm. "
    if activity_warning:
        disclaimer += "Having higher activity levels could lead to higher CO2 levels. "

    disclaimer += f"""CO2 sensors can have errors on the order of 50 ppm. 
    If the room is consistently above the expected steady state CO2, the ventilation should be investigated or increased as the room is not in compliance with current ventilation requirements.
    """
    st.markdown(f"<br><span style='font-size:12px;'>{disclaimer}</span><br>", unsafe_allow_html=True)

    if info_string:
        st.markdown(f"""
        <br>
        <span style='font-size:12px;'>
        {info_string}
        </span>
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
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
    
def display_cadr(cadr_lps):
    # If within ±0.1 of an integer, just show the integer portion
    # Otherwise, round to the nearest 0.1
    cadr_lps = int(cadr_lps) if (abs(int(cadr_lps) - cadr_lps) < .1) else round(cadr_lps, 1)

    st.markdown(f"<center><h1>{cadr_lps} lps</h1></center>", unsafe_allow_html=True)