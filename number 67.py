import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time

# ==========================================
# 1. FUZZY VARIABLES SETUP (3 Inputs, 2 Outputs)
# ==========================================
# Inputs (المدخلات)
dirt = ctrl.Antecedent(np.arange(0, 101, 1), 'dirt')          
grease = ctrl.Antecedent(np.arange(0, 101, 1), 'grease')      
weight = ctrl.Antecedent(np.arange(0, 11, 1), 'weight')       

# Outputs (المخرجات)
wash_time = ctrl.Consequent(np.arange(0, 101, 1), 'wash_time') 
water_temp = ctrl.Consequent(np.arange(0, 101, 1), 'water_temp')

# Triangular Membership Functions (دوال العضوية المتناظرة)
dirt['low'] = fuzz.trimf(dirt.universe, [0, 0, 50])
dirt['medium'] = fuzz.trimf(dirt.universe, [0, 50, 100])
dirt['high'] = fuzz.trimf(dirt.universe, [50, 100, 100])

grease['low'] = fuzz.trimf(grease.universe, [0, 0, 50])
grease['medium'] = fuzz.trimf(grease.universe, [0, 50, 100])
grease['high'] = fuzz.trimf(grease.universe, [50, 100, 100])

weight['light'] = fuzz.trimf(weight.universe, [0, 0, 5])
weight['medium'] = fuzz.trimf(weight.universe, [0, 5, 10])
weight['heavy'] = fuzz.trimf(weight.universe, [5, 10, 10])

wash_time['very_short'] = fuzz.trimf(wash_time.universe, [0, 0, 25])
wash_time['short'] = fuzz.trimf(wash_time.universe, [0, 25, 50])
wash_time['medium'] = fuzz.trimf(wash_time.universe, [25, 50, 75])
wash_time['long'] = fuzz.trimf(wash_time.universe, [50, 75, 100])
wash_time['very_long'] = fuzz.trimf(wash_time.universe, [75, 100, 100])

water_temp['cold'] = fuzz.trimf(water_temp.universe, [0, 0, 50])
water_temp['warm'] = fuzz.trimf(water_temp.universe, [0, 50, 100])
water_temp['hot'] = fuzz.trimf(water_temp.universe, [50, 100, 100])

# ==========================================
# 2. RULE BASE (FULL 27 RULES MATRIX)
# ==========================================
rules = [
    # Group 1: Light Weight
    ctrl.Rule(dirt['low'] & grease['low'] & weight['light'], [wash_time['very_short'], water_temp['cold']]),
    ctrl.Rule(dirt['low'] & grease['medium'] & weight['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirt['low'] & grease['high'] & weight['light'], [wash_time['medium'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['low'] & weight['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['medium'] & weight['light'], [wash_time['medium'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['high'] & weight['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['low'] & weight['light'], [wash_time['medium'], water_temp['warm']]),
    ctrl.Rule(dirt['high'] & grease['medium'] & weight['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['high'] & weight['light'], [wash_time['long'], water_temp['hot']]),

    # Group 2: Medium Weight
    ctrl.Rule(dirt['low'] & grease['low'] & weight['medium'], [wash_time['short'], water_temp['cold']]),
    ctrl.Rule(dirt['low'] & grease['medium'] & weight['medium'], [wash_time['medium'], water_temp['warm']]),
    ctrl.Rule(dirt['low'] & grease['high'] & weight['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['low'] & weight['medium'], [wash_time['medium'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['medium'] & weight['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['high'] & weight['medium'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['low'] & weight['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirt['high'] & grease['medium'] & weight['medium'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['high'] & weight['medium'], [wash_time['very_long'], water_temp['hot']]),

    # Group 3: Heavy Weight
    ctrl.Rule(dirt['low'] & grease['low'] & weight['heavy'], [wash_time['medium'], water_temp['cold']]),
    ctrl.Rule(dirt['low'] & grease['medium'] & weight['heavy'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirt['low'] & grease['high'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['medium'] & grease['low'] & weight['heavy'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirt['medium'] & grease['medium'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['medium'] & grease['high'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['low'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['medium'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']]),
    ctrl.Rule(dirt['high'] & grease['high'] & weight['heavy'], [wash_time['very_long'], water_temp['hot']])
]

washing_ctrl = ctrl.ControlSystem(rules)
washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)

# ==========================================
# 3. HTML DESIGN IMPORT (تحميل ملف التصميم)
# ==========================================
try:
    with open("design.html", "r", encoding="utf-8") as f:
        st.markdown(f.read(), unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ==========================================
# 4. USER INPUTS (أدوات التحكم بالمدخلات)
# ==========================================
col1, col2, col3 = st.columns(3)
with col1:
    dirt_input = st.slider('Dirt Level (%)', min_value=0, max_value=100, value=50, step=1)
with col2:
    grease_input = st.slider('Grease Level (%)', min_value=0, max_value=100, value=50, step=1)
with col3:
    weight_input = st.slider('Load Weight (Kg)', min_value=0, max_value=10, value=5, step=1)

calculate_btn = st.button('🚀 Calculate Outputs & Start Washing')

# ==========================================
# 5. EXECUTION & ANIMATION LOGIC (الحساب والتوقف)
# ==========================================
if calculate_btn:
    # 1. تشغيل الحركة وإغلاق الباب
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="washer-container spinning">
            <div class="washing-machine">
                <div class="controls-panel">
                    <div class="dispenser"></div>
                    <div class="knobs">
                        <div class="knob"></div>
                        <div class="knob"></div>
                    </div>
                </div>
                <div class="drum-outer">
                    <div class="drum-inner">
                        <div class="clothes"></div>
                    </div>
                    <div class="door-open"></div>
                </div>
            </div>
            <div class="title-text">🧼 Washing in Progress...</div>
            <div class="subtitle-text">Door Closed - Simulating Fuzzy Logic Calculation</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 2. انتظار 2.5 ثانية (زمن دوران الغسالة)
    time.sleep(2.5)
    
    # 3. حساب نتائج المنطق الضبابي
    washing_sim.input['dirt'] = dirt_input
    washing_sim.input['grease'] = grease_input
    washing_sim.input['weight'] = weight_input
    washing_sim.compute()
    
    # 4. إيقاف الحركة، فتح الباب، وعرض النتائج
    placeholder.markdown("""
    <div class="washer-container">
        <div class="washing-machine">
            <div class="controls-panel">
                <div class="dispenser"></div>
                <div class="knobs">
                    <div class="knob"></div>
                    <div class="knob"></div>
                </div>
            </div>
            <div class="drum-outer">
                <div class="drum-inner">
                    <div class="clothes"></div>
                </div>
                <div class="door-open"></div>
            </div>
        </div>
        <div class="title-text">✅ Wash Cycle Completed</div>
        <div class="subtitle-text">Door Opened - Outputs Calculated Successfully</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Calculated Outputs:")
    st.success(f"⏱️ Wash Time: {washing_sim.output['wash_time']:.1f} minutes")
    st.info(f"🌡️ Water Temperature: {washing_sim.output['water_temp']:.1f} °C")
else:
    # الواجهة الثابتة قبل الضغط
    st.markdown("""
    <div class="washer-container">
        <div class="washing-machine">
            <div class="controls-panel">
                <div class="dispenser"></div>
                <div class="knobs">
                    <div class="knob"></div>
                    <div class="knob"></div>
                </div>
            </div>
            <div class="drum-outer">
                <div class="drum-inner">
                    <div class="clothes"></div>
                </div>
                <div class="door-open"></div>
            </div>
        </div>
        <div class="title-text">🧺 Smart Washing Machine Simulator</div>
        <div class="subtitle-text">Ready - Set values and click Calculate</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. VIEW ALL 27 RULES (عرض القواعد الشاملة)
# ==========================================
with st.expander("📄 View All 27 Fuzzy Logic Rules (Full Matrix)"):
    st.markdown("""
    **🟢 Group 1: Light Weight (0-5 Kg)**
    1. **IF** Dirt is Low **AND** Grease is Low **AND** Weight is Light **THEN** Wash Time is Very Short **AND** Water Temp is Cold
    2. **IF** Dirt is Low **AND** Grease is Med **AND** Weight is Light **THEN** Wash Time is Short **AND** Water Temp is Warm
    3. **IF** Dirt is Low **AND** Grease is High **AND** Weight is Light **THEN** Wash Time is Medium **AND** Water Temp is Warm
    4. **IF** Dirt is Med **AND** Grease is Low **AND** Weight is Light **THEN** Wash Time is Short **AND** Water Temp is Warm
    5. **IF** Dirt is Med **AND** Grease is Med **AND** Weight is Light **THEN** Wash Time is Medium **AND** Water Temp is Warm
    6. **IF** Dirt is Med **AND** Grease is High **AND** Weight is Light **THEN** Wash Time is Long **AND** Water Temp is Hot
    7. **IF** Dirt is High **AND** Grease is Low **AND** Weight is Light **THEN** Wash Time is Medium **AND** Water Temp is Warm
    8. **IF** Dirt is High **AND** Grease is Med **AND** Weight is Light **THEN** Wash Time is Long **AND** Water Temp is Hot
    9. **IF** Dirt is High **AND** Grease is High **AND** Weight is Light **THEN** Wash Time is Long **AND** Water Temp is Hot

    **🟡 Group 2: Medium Weight (5-8 Kg)**
    10. **IF** Dirt is Low **AND** Grease is Low **AND** Weight is Medium **THEN** Wash Time is Short **AND** Water Temp is Cold
    11. **IF** Dirt is Low **AND** Grease is Med **AND** Weight is Medium **THEN** Wash Time is Medium **AND** Water Temp is Warm
    12. **IF** Dirt is Low **AND** Grease is High **AND** Weight is Medium **THEN** Wash Time is Long **AND** Water Temp is Warm
    13. **IF** Dirt is Med **AND** Grease is Low **AND** Weight is Medium **THEN** Wash Time is Medium **AND** Water Temp is Warm
    14. **IF** Dirt is Med **AND** Grease is Med **AND** Weight is Medium **THEN** Wash Time is Long **AND** Water Temp is Warm
    15. **IF** Dirt is Med **AND** Grease is High **AND** Weight is Medium **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    16. **IF** Dirt is High **AND** Grease is Low **AND** Weight is Medium **THEN** Wash Time is Long **AND** Water Temp is Warm
    17. **IF** Dirt is High **AND** Grease is Med **AND** Weight is Medium **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    18. **IF** Dirt is High **AND** Grease is High **AND** Weight is Medium **THEN** Wash Time is Very Long **AND** Water Temp is Hot

    **🔴 Group 3: Heavy Weight (8-10 Kg)**
    19. **IF** Dirt is Low **AND** Grease is Low **AND** Weight is Heavy **THEN** Wash Time is Medium **AND** Water Temp is Cold
    20. **IF** Dirt is Low **AND** Grease is Med **AND** Weight is Heavy **THEN** Wash Time is Long **AND** Water Temp is Warm
    21. **IF** Dirt is Low **AND** Grease is High **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    22. **IF** Dirt is Med **AND** Grease is Low **AND** Weight is Heavy **THEN** Wash Time is Long **AND** Water Temp is Warm
    23. **IF** Dirt is Med **AND** Grease is Med **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    24. **IF** Dirt is Med **AND** Grease is High **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    25. **IF** Dirt is High **AND** Grease is Low **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    26. **IF** Dirt is High **AND** Grease is Med **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    27. **IF** Dirt is High **AND** Grease is High **AND** Weight is Heavy **THEN** Wash Time is Very Long **AND** Water Temp is Hot
    """)
