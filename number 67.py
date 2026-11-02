import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ==========================================
# 1. UI TITLE & DESCRIPTION / عنوان الواجهة
# ==========================================
st.title("🚿 Smart Washing Machine (Fuzzy Logic)")
st.write("Mamdani Fuzzy Logic Inference System with 9 IF-THEN Rules for Wash Time & Water Temperature Control.")
st.divider()

# ==========================================
# 2. FUZZY VARIABLES SETUP / إعداد المتغيرات الضبابية
# ==========================================
# Antecedents (Inputs / المدخلات)
dirt = ctrl.Antecedent(np.arange(0, 101, 1), 'dirt')
grease = ctrl.Antecedent(np.arange(0, 101, 1), 'grease')

# Consequents (Outputs / المخرجات)
wash_time = ctrl.Consequent(np.arange(0, 61, 1), 'wash_time')
water_temp = ctrl.Consequent(np.arange(0, 101, 1), 'water_temp')

# Membership Functions / تعريف دوال العضوية
dirt.automf(names=['low', 'medium', 'high'])
grease.automf(names=['low', 'medium', 'high'])
wash_time.automf(names=['very_short', 'short', 'medium', 'long', 'very_long'])
water_temp.automf(names=['cold', 'warm', 'hot'])

# ==========================================
# 3. RULE BASE (9 RULES) / مصفوفة القواعد التسع
# ==========================================
# NOTE / ملاحظة:
# ENG: Full 3x3 matrix covering all combinations of Dirt and Grease.
# AR: مصفوفة كاملة 3x3 تغطي جميع احتمالات الأوساخ والدهون.

rule1 = ctrl.Rule(dirt['low'] & grease['low'], (wash_time['very_short'], water_temp['cold']))
rule2 = ctrl.Rule(dirt['low'] & grease['medium'], (wash_time['short'], water_temp['warm']))
rule3 = ctrl.Rule(dirt['low'] & grease['high'], (wash_time['medium'], water_temp['warm']))

rule4 = ctrl.Rule(dirt['medium'] & grease['low'], (wash_time['short'], water_temp['warm']))
rule5 = ctrl.Rule(dirt['medium'] & grease['medium'], (wash_time['medium'], water_temp['warm']))
rule6 = ctrl.Rule(dirt['medium'] & grease['high'], (wash_time['long'], water_temp['hot']))

rule7 = ctrl.Rule(dirt['high'] & grease['low'], (wash_time['medium'], water_temp['warm']))
rule8 = ctrl.Rule(dirt['high'] & grease['medium'], (wash_time['long'], water_temp['hot']))
rule9 = ctrl.Rule(dirt['high'] & grease['high'], (wash_time['very_long'], water_temp['hot']))

# Control System Setup / إنشاء نظام التحكم
washing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)

# ==========================================
# 4. RULE BASE DISPLAY / عرض القواعد للمناقشة
# ==========================================
with st.expander("📄 View Fuzzy Logic Rules (IF-THEN Rules)"):
    st.markdown("""
    1. **IF** Dirt is Low **AND** Grease is Low **THEN** Time is Very Short **AND** Temp is Cold
    2. **IF** Dirt is Low **AND** Grease is Medium **THEN** Time is Short **AND** Temp is Warm
    3. **IF** Dirt is Low **AND** Grease is High **THEN** Time is Medium **AND** Temp is Warm
    4. **IF** Dirt is Medium **AND** Grease is Low **THEN** Time is Short **AND** Temp is Warm
    5. **IF** Dirt is Medium **AND** Grease is Medium **THEN** Time is Medium **AND** Temp is Warm
    6. **IF** Dirt is Medium **AND** Grease is High **THEN** Time is Long **AND** Temp is Hot
    7. **IF** Dirt is High **AND** Grease is Low **THEN** Time is Medium **AND** Temp is Warm
    8. **IF** Dirt is High **AND** Grease is Medium **THEN** Time is Long **AND** Temp is Hot
    9. **IF** Dirt is High **AND** Grease is High **THEN** Time is Very Long **AND** Temp is Hot
    """)

# ==========================================
# 5. USER INPUTS & CALCULATION / أدوات الإدخال والنتائج
# ==========================================
col1, col2 = st.columns(2)
with col1:
    dirt_input = st.slider('Dirt Level (%)', 0, 100, 50)
with col2:
    grease_input = st.slider('Grease / Fabric Level (%)', 0, 100, 50)

if st.button('Calculate Outputs'):
    # NOTE / ملاحظة:
    # ENG: Fuzzification & Inference process takes place here.
    # AR: هنا تتم عملية تحويل المدخلات وحساب النتائج عبر القواعد.
    washing_sim.input['dirt'] = dirt_input
    washing_sim.input['grease'] = grease_input
    washing_sim.compute()
    
    st.subheader("Calculated Outputs:")
    st.success(f"⏱️ Wash Time: {washing_sim.output['wash_time']:.1f} minutes")
    st.info(f"🌡️ Water Temperature: {washing_sim.output['water_temp']:.1f} °C")

