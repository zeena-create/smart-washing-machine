import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

dirt_ctrl = ctrl.Antecedent(np.arange(0, 101, 1), 'dirt')
grease_ctrl = ctrl.Antecedent(np.arange(0, 101, 1), 'grease')
time_ctrl = ctrl.Consequent(np.arange(0, 61, 1), 'time')

dirt_ctrl['Small'] = fuzz.trimf(dirt_ctrl.universe, [0, 0, 50])
dirt_ctrl['Medium'] = fuzz.trimf(dirt_ctrl.universe, [0, 50, 100])
dirt_ctrl['Large'] = fuzz.trimf(dirt_ctrl.universe, [50, 100, 100])

grease_ctrl['NotGreasy'] = fuzz.trimf(grease_ctrl.universe, [0, 0, 50])
grease_ctrl['Medium'] = fuzz.trimf(grease_ctrl.universe, [0, 50, 100])
grease_ctrl['Greasy'] = fuzz.trimf(grease_ctrl.universe, [50, 100, 100])

time_ctrl['VeryShort'] = fuzz.trimf(time_ctrl.universe, [0, 8, 12])
time_ctrl['Short'] = fuzz.trimf(time_ctrl.universe, [8, 12, 20])
time_ctrl['Medium'] = fuzz.trimf(time_ctrl.universe, [12, 20, 40])
time_ctrl['Long'] = fuzz.trimf(time_ctrl.universe, [20, 40, 60])
time_ctrl['VeryLong'] = fuzz.trimf(time_ctrl.universe, [40, 60, 60])

RULES = [
    ("Large",  "Greasy",    "VeryLong"),
    ("Medium", "Greasy",    "Long"),
    ("Small",  "Greasy",    "Long"),
    ("Large",  "Medium",    "Long"),
    ("Medium", "Medium",    "Medium"),
    ("Small",  "Medium",    "Medium"),
    ("Large",  "NotGreasy", "Medium"),
    ("Medium", "NotGreasy", "Short"),
    ("Small",  "NotGreasy", "VeryShort"),
]

fuzzy_rules = []
for d, g, t in RULES:
    fuzzy_rules.append(ctrl.Rule(dirt_ctrl[d] & grease_ctrl[g], time_ctrl[t]))

washing_ctrl = ctrl.ControlSystem(fuzzy_rules)
washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)

st.title("Smart Washing Machine (Fuzzy Logic)")

d_val = st.slider("Dirtiness Level", 0, 100, 50)
g_val = st.slider("Grease Level", 0, 100, 50)

if st.button("Calculate Wash Time"):
    washing_sim.input['dirt'] = d_val
    washing_sim.input['grease'] = g_val
    
    washing_sim.compute()
    
    result = washing_sim.output['time']
    st.success(f"Calculated Wash Time: {result:.1f} minutes")
