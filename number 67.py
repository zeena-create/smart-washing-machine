import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Fuzzy Washing Machine", layout="wide")
st.title("🧺 Smart Washing Machine (Fuzzy Logic Controller)")

# 1. VARIABLES & MEMBERSHIP FUNCTIONS
dirtiness = ctrl.Antecedent(np.arange(0, 101, 1), "dirtiness")
grease = ctrl.Antecedent(np.arange(0, 101, 1), "grease")
load = ctrl.Antecedent(np.arange(0, 10.1, 0.1), "load")

wash_time = ctrl.Consequent(np.arange(0, 61, 1), "wash_time")
water_temp = ctrl.Consequent(np.arange(0, 101, 1), "water_temp")

dirtiness["low"] = fuzz.trimf(dirtiness.universe, [0, 0, 50])
dirtiness["medium"] = fuzz.trimf(dirtiness.universe, [25, 50, 75])
dirtiness["high"] = fuzz.trimf(dirtiness.universe, [50, 100, 100])

grease["low"] = fuzz.trimf(grease.universe, [0, 0, 50])
grease["medium"] = fuzz.trimf(grease.universe, [25, 50, 75])
grease["high"] = fuzz.trimf(grease.universe, [50, 100, 100])

load["light"] = fuzz.trimf(load.universe, [0, 0, 5])
load["medium"] = fuzz.trimf(load.universe, [2, 5, 8])
load["heavy"] = fuzz.trimf(load.universe, [5, 10, 10])

wash_time["short"] = fuzz.trimf(wash_time.universe, [0, 0, 30])
wash_time["normal"] = fuzz.trimf(wash_time.universe, [15, 30, 45])
wash_time["long"] = fuzz.trimf(wash_time.universe, [30, 60, 60])

water_temp["cold"] = fuzz.trimf(water_temp.universe, [0, 0, 40])
water_temp["warm"] = fuzz.trimf(water_temp.universe, [30, 50, 70])
water_temp["hot"] = fuzz.trimf(water_temp.universe, [60, 100, 100])

# 2. RULE BASE (27 RULES)
rules = [
    ctrl.Rule(dirtiness['low'] & grease['low'] & load['light'], [wash_time['short'], water_temp['cold']]),
    ctrl.Rule(dirtiness['low'] & grease['medium'] & load['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirtiness['low'] & grease['high'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['low'] & load['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['medium'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['high'] & load['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['low'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['high'] & grease['medium'] & load['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['high'] & load['light'], [wash_time['long'], water_temp['hot']]),

    ctrl.Rule(dirtiness['low'] & grease['low'] & load['medium'], [wash_time['short'], water_temp['cold']]),
    ctrl.Rule(dirtiness['low'] & grease['medium'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['low'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['low'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['medium'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['low'] & load['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['high'] & grease['medium'] & load['medium'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['hot']]),

    ctrl.Rule(dirtiness['low'] & grease['low'] & load['heavy'], [wash_time['normal'], water_temp['cold']]),
    ctrl.Rule(dirtiness['low'] & grease['medium'] & load['heavy'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['low'] & grease['high'] & load['heavy'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['medium'] & grease['low'] & load['heavy'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['medium'] & load['heavy'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['medium'] & grease['high'] & load['heavy'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['low'] & load['heavy'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['medium'] & load['heavy'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['high'] & load['heavy'], [wash_time['long'], water_temp['hot']])
]

washer_ctrl = ctrl.ControlSystem(rules)

# 3. USER INPUTS
st.markdown("### 🎛️ Controller Inputs")
col1, col2, col3 = st.columns(3)
with col1:
    d_input = st.slider('Dirtiness (%)', 0, 100, 50, 1)
with col2:
    g_input = st.slider('Grease (%)', 0, 100, 50, 1)
with col3:
    l_input = st.slider('Load (kg)', 0.0, 10.0, 5.0, 0.1)

calculate_btn = st.button('🚀 Calculate & Start Washing', use_container_width=True)

# 4. TABS UI
tab1, tab2, tab3, tab4 = st.tabs(["🧺 Simulator", "📊 3D Surface", "⚙️ Defuzzification", "📄 Rules Base"])

with tab1:
    sim = ctrl.ControlSystemSimulation(washer_ctrl)
    
    html_design = ""
    try:
        with open("design.html", "r", encoding="utf-8") as f:
            html_design = f.read()
    except FileNotFoundError:
        pass
    
    st.markdown(html_design, unsafe_allow_html=True)
    
    if calculate_btn:
        placeholder = st.empty()
        
        with placeholder.container():
            st.markdown("""
            <div class="washer-container spinning">
                <div class="washing-machine">
                    <div class="controls-panel">
                        <div class="dispenser"></div>
                        <div class="knobs"><div class="knob"></div><div class="knob"></div></div>
                    </div>
                    <div class="drum-outer"><div class="drum-inner"><div class="clothes"></div></div><div class="door-open"></div></div>
                </div>
                <div class="title-text">🧼 Washing in Progress...</div>
                <div class="subtitle-text">Executing Mamdani FIS</div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(2.0)
        
        sim.input["dirtiness"] = d_input
        sim.input["grease"] = g_input
        sim.input["load"] = l_input
        sim.compute()
        
        placeholder.markdown("""
        <div class="washer-container">
            <div class="washing-machine">
                <div class="controls-panel">
                    <div class="dispenser"></div>
                    <div class="knobs"><div class="knob"></div><div class="knob"></div></div>
                </div>
                <div class="drum-outer"><div class="drum-inner"><div class="clothes"></div></div><div class="door-open"></div></div>
            </div>
            <div class="title-text">✅ Wash Cycle Completed</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"**⏱️ Computed Wash Time:** {sim.output['wash_time']:.1f} minutes")
        st.info(f"**🌡️ Computed Water Temp:** {sim.output['water_temp']:.1f} °C")
    else:
        st.markdown("""
        <div class="washer-container">
            <div class="washing-machine">
                <div class="controls-panel">
                    <div class="dispenser"></div>
                    <div class="knobs"><div class="knob"></div><div class="knob"></div></div>
                </div>
                <div class="drum-outer"><div class="drum-inner"><div class="clothes"></div></div><div class="door-open"></div></div>
            </div>
            <div class="title-text">🧺 Smart Washing Machine Simulator</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 3D Control Surface (Dirtiness vs Load)")
    if st.button("Plot 3D Surface"):
        d_grid = np.linspace(0, 100, 21)
        l_grid = np.linspace(0, 10, 21)
        Z = np.zeros((len(l_grid), len(d_grid)))
        sim_surf = ctrl.ControlSystemSimulation(washer_ctrl)
        
        for i, l_val in enumerate(l_grid):
            for j, d_val in enumerate(d_grid):
                sim_surf.input["dirtiness"] = d_val
                sim_surf.input["grease"] = g_input
                sim_surf.input["load"] = l_val
                sim_surf.compute()
                Z[i, j] = sim_surf.output["wash_time"]
                
        D, L = np.meshgrid(d_grid, l_grid)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(D, L, Z, cmap="plasma", edgecolor="none")
        ax.set_xlabel("Dirtiness (%)")
        ax.set_ylabel("Load (kg)")
        ax.set_zlabel("Wash time (min)")
        ax.set_title("Washing-machine fuzzy controller")
        st.pyplot(fig)

with tab3:
    st.markdown("### ⚙️ Compare Defuzzification Methods")
    
    methods = ["centroid", "bisector", "mom", "som", "lom"]
    results = {}
    
    for method in methods:
        wash_time.defuzzify_method = method
        sim_defuz = ctrl.ControlSystemSimulation(washer_ctrl)
        sim_defuz.input["dirtiness"] = d_input
        sim_defuz.input["grease"] = g_input
        sim_defuz.input["load"] = l_input
        sim_defuz.compute()
        results[method] = sim_defuz.output['wash_time']
        
    wash_time.defuzzify_method = "centroid" 
    
    m_cols = st.columns(len(methods))
    for col, method in zip(m_cols, methods):
        col.metric(label=method.capitalize(), value=f"{results[method]:.1f} min")

with tab4:
    st.markdown("""
    ### 📄 Full 27 Mamdani Rules Matrix
    * **Group 1: Light Load (0 - 5 kg)**
      - IF dirtiness is low AND grease is low AND load is light THEN wash_time is short AND water_temp is cold
      - IF dirtiness is low AND grease is medium AND load is light THEN wash_time is short AND water_temp is warm
      - IF dirtiness is low AND grease is high AND load is light THEN wash_time is normal AND water_temp is warm
      - IF dirtiness is medium AND grease is low AND load is light THEN wash_time is short AND water_temp is warm
      - IF dirtiness is medium AND grease is medium AND load is light THEN wash_time is normal AND water_temp is warm
      - IF dirtiness is medium AND grease is high AND load is light THEN wash_time is long AND water_temp is hot
      - IF dirtiness is high AND grease is low AND load is light THEN wash_time is normal AND water_temp is warm
      - IF dirtiness is high AND grease is medium AND load is light THEN wash_time is long AND water_temp is hot
      - IF dirtiness is high AND grease is high AND load is light THEN wash_time is long AND water_temp is hot
    
    *(Repeated similarly for Medium and Heavy loads)*
    """)
