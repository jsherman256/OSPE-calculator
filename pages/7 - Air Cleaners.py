import streamlit as st
from converters import cfm_to_cubic_meters_per_hour, lps_to_cubic_meters_per_hour
from lib import *
from converters import *
import units as u
import math 

# Given an integer between 0 and 100 (inclusive)
# return the inverse percentage as a float
# For example, input of 80 returns output of 0.20
def inv_percent(n):
    return (100 - n) / 100

st.set_page_config(page_title='OSPE Air Quality Calculator', page_icon='💨')


st.markdown("# OSPE Air Quality Calculator")
st.markdown("## Estimating Clean Air Delivery")
st.markdown("Find the clean air delivery rate (CADR) provided by an air cleaner.")

from_ach, from_percent, from_log = st.tabs(['From ACH', 'From % Reduction', 'From log reduction'])

with from_ach:
    st.markdown("### Calculate CADR from Air Changes per Hour")
    # Room parameters
    left, middle_left, middle_right, right = st.columns([1,1,1,2])
    with left:
        rated_ach = st.number_input(label='ACH', step=1, min_value=1, value=2)
    with middle_left:
        volume_known = st.checkbox(label='Room Volume Known', value=False)
    with middle_right:
        room_volume = st.number_input(label='Room Volume', step=1, min_value=1, value=10, disabled=(not volume_known))
    with right:
        volume_unit = st.selectbox(label='Volume Unit', options=['cubic meters', 'cubic feet'])

    # Convert room volume to cubic meters
    if volume_unit == 'cubic meters':
        volume_m3 = room_volume
    elif volume_unit == 'cubic feet':
        volume_m3 = cubic_feet_to_cubic_meters(room_volume)

    if not volume_known:
        st.error("The effectiveness cannot be calculated without the volume of the room. Often items can have very high air change rates in small rooms and are ineffective in larger rooms.")
    else:
        # Convert CADR to Liters per second
        # 1000 Liters in a cubic meter. 3600 seconds in an hour
        cadr_lps = volume_m3 * rated_ach * (1000 / 3600)

        st.markdown("### Results")
        st.markdown(f"""
        ||||
        |-|-|-|
        |**Clean Air Delivery Rate**| $ \\text{{Volume}} \\cdot \\text{{ACH}} \\cdot {u.m3ph_over_lps} $ | $ = {round(volume_m3, 2)} {u.cubic_m} \\cdot {rated_ach} \\cdot {u.m3ph_over_lps} $ | $ = {round(cadr_lps, 2)} {u.lps} $
        """)

        display_cadr(cadr_lps)

with from_percent:
    st.markdown("### Calculate CADR from % Reduction")
    left, middle_left, middle_right, right = st.columns(4)
    with left:
        test_percent = st.number_input("Test %", min_value=0, max_value=100, value=80)
    with middle_left:
        control_percent = st.number_input("Control %", min_value=0, max_value=100, value=0)
    with middle_right:
        chamber_volume = st.number_input(f"Volume of chamber (m³)", min_value=0)
    with right:
        test_time = st.number_input("Test duration (min)", min_value=0)

    if control_percent > test_percent:
        st.error("Control % reduction is higher than test reduction. Please check the values")
    elif chamber_volume == 0 or test_time == 0:
        st.error("The effectiveness cannot be calculated without the volume of the chamber and the duration of test.")
    else:
        # Convert CADR to Liters per second
        # 1000 Liters in a cubic meter. 3600 seconds in an hour
        cadr_lps = (chamber_volume / test_time) * math.log(inv_percent(control_percent) / inv_percent(test_percent)) * 60 * (1000 / 3600)

        st.markdown("### Results")
        if control_percent == 0:
            st.warning("Since it is unknown how much is removed when the unit is off (control %), the actual CADR is likely to be less than shown here")

        st.markdown(f"""
        ||||
        |-|-|-|
        |**CADR**| $ \\frac{{\\text{{volume}}}}{{\\text{{time}}}} \\cdot {u.min_per_hour} \\cdot \\ln\\left({{\\frac{{1 - \\text{{c}}}}{{1 - \\text{{t}}}}}}\\right) \\cdot {u.m3ph_over_lps} $ | $ = \\frac{{{chamber_volume} {u.cubic_m}}}{{{test_time} {u.minutes}}} \\cdot {u.min_per_hour} \\cdot \\ln\\left({{\\frac{{{round(1 - (control_percent / 100), 2)}}}{{{round(1 - (test_percent / 100), 2)}}}}}\\right) \\cdot {u.m3ph_over_lps} $ |""")

        display_cadr(cadr_lps)

with from_log:
    st.markdown("### Calculate CADR from log Reduction")
    left, middle_left, middle_right, right = st.columns(4)
    with left:
        test_log = st.number_input("Test log reduction", min_value=0.0, value=2.0, step=0.1)
    with middle_left:
        control_log = st.number_input("Control log reduction", min_value=0.0, value=0.0, step=0.1)
    with middle_right:
        chamber_volume = st.number_input(f"Volume of chamber (m³)", min_value=0, key="log_chamber_volume")
    with right:
        test_time = st.number_input("Test duration (min)", min_value=0, key="log_test_time")

    # TODO is this an error?
    if round(control_log, 1) > round(test_log, 1):
        st.error("Control log reduction is higher than test reduction. Please check the values")
    elif chamber_volume == 0 or test_time == 0:
        st.error("The effectiveness cannot be calculated without the volume of the chamber and the duration of test.")
    else:
        # Convert CADR to Liters per second
        # 1000 Liters in a cubic meter. 3600 seconds in an hour
        cadr_lps = (chamber_volume / test_time) * math.log(10**(test_log - control_log)) * 60 * (1000 / 3600)

        st.markdown("### Results")
        if control_log == 0:
            st.warning("Since it is unknown how much is removed when the unit is off (control log reduction), the actual CADR is likely to be less than shown here")

        st.markdown(f"""
        ||||
        |-|-|-|
        |**CADR**| $ \\frac{{\\text{{volume}}}}{{\\text{{time}}}} \\cdot {u.min_per_hour} \\cdot \\ln\\left({{10^{{t-c}}}}\\right) \\cdot {u.m3ph_over_lps} $ | $ = \\frac{{{chamber_volume} {u.cubic_m}}}{{{test_time} {u.minutes}}} \\cdot {u.min_per_hour} \\cdot \\ln\\left({{10^{{{round(test_log, 1)} - {round(control_log, 1)}}}}}\\right) \\cdot {u.m3ph_over_lps} $ |""")

        display_cadr(cadr_lps)
