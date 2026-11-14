import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# إعداد الصفحة وعنوان التطبيق في واجهة Streamlit
st.set_page_config(page_title="Fuzzy Washing Machine", layout="wide")

st.title("🧺 Smart Washing Machine Controller")
st.markdown("Mamdani Fuzzy Inference System (FIS)")

# ==========================================
# 1. تعريف المتغيرات (المدخلات والمخرجات)
# ==========================================
# المدخلات (Antecedents): نسبة الأوساخ، نسبة الدهون، وحجم الحمولة
dirtiness = ctrl.Antecedent(np.arange(0, 101, 1), "dirtiness")
grease = ctrl.Antecedent(np.arange(0, 101, 1), "grease")
load = ctrl.Antecedent(np.arange(0, 10.1, 0.1), "load")

# المخرجات (Consequents): وقت الغسيل، ودرجة حرارة الماء
wash_time = ctrl.Consequent(np.arange(0, 61, 1), "wash_time")
water_temp = ctrl.Consequent(np.arange(0, 101, 1), "water_temp")

# ==========================================
# 2. تعريف دوال العضوية (Membership Functions)
# ==========================================
# دوال العضوية للأوساخ (قليلة، متوسطة، كثيرة)
dirtiness["low"] = fuzz.trimf(dirtiness.universe, [0, 0, 50])
dirtiness["medium"] = fuzz.trimf(dirtiness.universe, [25, 50, 75])
dirtiness["high"] = fuzz.trimf(dirtiness.universe, [50, 100, 100])

# دوال العضوية للدهون (قليلة، متوسطة، كثيرة)
grease["low"] = fuzz.trimf(grease.universe, [0, 0, 50])
grease["medium"] = fuzz.trimf(grease.universe, [25, 50, 75])
grease["high"] = fuzz.trimf(grease.universe, [50, 100, 100])

# دوال العضوية لحجم الحمولة (خفيفة، متوسطة، ثقيلة)
load["light"] = fuzz.trimf(load.universe, [0, 0, 5])
load["medium"] = fuzz.trimf(load.universe, [2, 5, 8])
load["heavy"] = fuzz.trimf(load.universe, [5, 10, 10])

# دوال العضوية لوقت الغسيل (قصير، عادي، طويل)
wash_time["short"] = fuzz.trimf(wash_time.universe, [0, 0, 30])
wash_time["normal"] = fuzz.trimf(wash_time.universe, [15, 30, 45])
wash_time["long"] = fuzz.trimf(wash_time.universe, [30, 60, 60])

# دوال العضوية لدرجة حرارة الماء (بارد، دافئ، حار)
water_temp["cold"] = fuzz.trimf(water_temp.universe, [0, 0, 40])
water_temp["warm"] = fuzz.trimf(water_temp.universe, [30, 50, 70])
water_temp["hot"] = fuzz.trimf(water_temp.universe, [60, 100, 100])

# ==========================================
# 3. قاعدة القواعد (Rule Base) - 27 قاعدة
# ==========================================
rules = [
    # المجموعة الأولى: الحمولة الخفيفة (Light Load)
    ctrl.Rule(dirtiness['low'] & grease['low'] & load['light'], [wash_time['short'], water_temp['cold']]),
    ctrl.Rule(dirtiness['low'] & grease['medium'] & load['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirtiness['low'] & grease['high'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['low'] & load['light'], [wash_time['short'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['medium'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['high'] & load['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['low'] & load['light'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['high'] & grease['medium'] & load['light'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['high'] & load['light'], [wash_time['long'], water_temp['hot']]),

    # المجموعة الثانية: الحمولة المتوسطة (Medium Load)
    ctrl.Rule(dirtiness['low'] & grease['low'] & load['medium'], [wash_time['short'], water_temp['cold']]),
    ctrl.Rule(dirtiness['low'] & grease['medium'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['low'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['low'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
ctrl.Rule(dirtiness['medium'] & grease['medium'] & load['medium'], [wash_time['normal'], water_temp['warm']]),
    ctrl.Rule(dirtiness['medium'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['low'] & load['medium'], [wash_time['long'], water_temp['warm']]),
    ctrl.Rule(dirtiness['high'] & grease['medium'] & load['medium'], [wash_time['long'], water_temp['hot']]),
    ctrl.Rule(dirtiness['high'] & grease['high'] & load['medium'], [wash_time['long'], water_temp['hot']]),

    # المجموعة الثالثة: الحمولة الثقيلة (Heavy Load)
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

# ==========================================
# 4. بناء نظام التحكم والمحاكاة
# ==========================================
washer_ctrl = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(washer_ctrl)

# ==========================================
# 5. واجهة المستخدم (المدخلات الجانبية)
# ==========================================
st.sidebar.header("🎛️ Controller Inputs")
d_input = st.sidebar.slider('Dirtiness (%)', 0, 100, 70, 1)    # شريط تمرير للأوساخ
g_input = st.sidebar.slider('Grease (%)', 0, 100, 50, 1)       # شريط تمرير للدهون
l_input = st.sidebar.slider('Load (kg)', 0.0, 10.0, 7.0, 0.1)  # شريط تمرير للحمولة

# تمرير القيم المدخلة إلى نظام المحاكاة وحساب النتيجة النهائية
sim.input["dirtiness"] = d_input
sim.input["grease"] = g_input
sim.input["load"] = l_input
sim.compute()

# ==========================================
# 6. التبويبات لعرض النتائج (Tabs)
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 Simulation Results", 
    "📈 Membership Functions", 
    "📊 3D Surface", 
    "⚙️ Defuzzification", 
    "📄 Rule Base"
])

# --- التبويب الأول: نتائج المحاكاة ---
with tab1:
    st.subheader("Current Evaluation")
    col1, col2 = st.columns(2)
    with col1:
        st.info("### ⏱️ Wash Time")
        # عرض وقت الغسيل المحسوب مع شريط تقدم
        st.title(f"{sim.output['wash_time']:.1f} min")
        st.progress(int(sim.output['wash_time']) / 60)
    with col2:
        st.error("### 🌡️ Water Temp")
        # عرض درجة حرارة الماء المحسوبة مع شريط تقدم
        st.title(f"{sim.output['water_temp']:.1f} °C")
        st.progress(int(sim.output['water_temp']) / 100)

# --- التبويب الثاني: رسم المجموعات الضبابية (Membership Functions) ---
with tab2:
    st.subheader("📈 Fuzzy Sets (Membership Functions)")
    
    # دالة مساعدة لرسم المجموعات الضبابية رياضياً لتجنب تكرار الكود
    def plot_mf(universe, mfs, title, xlabel):
        fig, ax = plt.subplots(figsize=(6, 2.5))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        for (label, params), color in zip(mfs.items(), colors):
            ax.plot(universe, fuzz.trimf(universe, params), color=color, linewidth=2, label=label.upper())
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Membership")
        ax.legend()
        ax.grid(True, alpha=0.3)
        return fig
c1, c2 = st.columns(2)
    with c1:
        st.pyplot(plot_mf(np.arange(0, 101, 1), {'low':[0,0,50], 'medium':[25,50,75], 'high':[50,100,100]}, "Dirtiness", "%"))
        st.pyplot(plot_mf(np.arange(0, 10.1, 0.1), {'light':[0,0,5], 'medium':[2,5,8], 'heavy':[5,10,10]}, "Load", "kg"))
    with c2:
        st.pyplot(plot_mf(np.arange(0, 101, 1), {'low':[0,0,50], 'medium':[25,50,75], 'high':[50,100,100]}, "Grease", "%"))
        st.pyplot(plot_mf(np.arange(0, 61, 1), {'short':[0,0,30], 'normal':[15,30,45], 'long':[30,60,60]}, "Wash Time (Output)", "min"))

# --- التبويب الثالث: الرسم ثلاثي الأبعاد (3D Surface) ---
with tab3:
    st.subheader("📊 3D Control Surface (Dirtiness vs Load)")
    
    # إنشاء شبكة من القيم لتمثيل السطح
    d_grid = np.linspace(0, 100, 21)
    l_grid = np.linspace(0, 10, 21)
    Z = np.zeros((len(l_grid), len(d_grid)))

    sim_surf = ctrl.ControlSystemSimulation(washer_ctrl)
    
    # حساب وقت الغسيل لكل نقطة تقاطع في الشبكة
    for i, l_val in enumerate(l_grid):
        for j, d_val in enumerate(d_grid):
            sim_surf.input["dirtiness"] = d_val
            sim_surf.input["grease"] = g_input # نثبت قيمة الدهون كما هي في الشريط الجانبي
            sim_surf.input["load"] = l_val
            sim_surf.compute()
            Z[i, j] = sim_surf.output["wash_time"]

    # رسم الشكل ثلاثي الأبعاد
    D, L = np.meshgrid(d_grid, l_grid)
    fig = plt.figure(figsize=(9, 5))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(D, L, Z, cmap="viridis", edgecolor="none")
    ax.set_xlabel("Dirtiness (%)")
    ax.set_ylabel("Load (kg)")
    ax.set_zlabel("Wash time (min)")
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
    st.pyplot(fig)

# --- التبويب الرابع: مقارنة طرق فك الضبابية (Defuzzification) ---
with tab4:
    st.subheader("⚙️ Defuzzification Methods Comparison")
    methods = ["centroid", "bisector", "mom", "som", "lom"]
    cols = st.columns(len(methods))

    # تجربة طرق فك الضبابية المختلفة وعرض نتائجها جنباً إلى جنب
    for idx, method in enumerate(methods):
        wash_time.defuzzify_method = method
        sim_defuz = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        sim_defuz.input["dirtiness"] = d_input
        sim_defuz.input["grease"] = g_input
        sim_defuz.input["load"] = l_input
        sim_defuz.compute()
        cols[idx].metric(label=method.upper(), value=f"{sim_defuz.output['wash_time']:.1f} m")

    # إعادة النظام للطريقة الافتراضية للنتائج العامة
    wash_time.defuzzify_method = "centroid"

# --- التبويب الخامس: قاعدة القواعد النصية الكاملة ---
with tab5:
    st.subheader("📄 Full 27 Mamdani Rules")
    st.code("""
# المجموعة الأولى: الحمولة الخفيفة
1. IF dirtiness is low & grease is low & load is light THEN wash_time is short & temp is cold
2. IF dirtiness is low & grease is medium & load is light THEN wash_time is short & temp is warm
3. IF dirtiness is low & grease is high & load is light THEN wash_time is normal & temp is warm
4. IF dirtiness is medium & grease is low & load is light THEN wash_time is short & temp is warm
5. IF dirtiness is medium & grease is medium & load is light THEN wash_time is normal & temp is warm
6. IF dirtiness is medium & grease is high & load is light THEN wash_time is long & temp is hot
7. IF dirtiness is high & grease is low & load is light THEN wash_time is normal & temp is warm
8. IF dirtiness is high & grease is medium & load is light THEN wash_time is long & temp is hot
9. IF dirtiness is high & grease is high & load is light THEN wash_time is long & temp is hot

# المجموعة الثانية: الحمولة المتوسطة
10. IF dirtiness is low & grease is low & load is medium THEN wash_time is short & temp is cold
11. IF dirtiness is low & grease is medium & load is medium THEN wash_time is normal & temp is warm
12. IF dirtiness is low & grease is high & load is medium THEN wash_time is long & temp is warm
13. IF dirtiness is medium & grease is low & load is medium THEN wash_time is normal & temp is warm
14. IF dirtiness is medium & grease is medium & load is medium THEN wash_time is normal & temp is warm
15. IF dirtiness is medium & grease is high & load is medium THEN wash_time is long & temp is hot
16. IF dirtiness is high & grease is low & load is medium THEN wash_time is long & temp is warm
17. IF dirtiness is high & grease is medium & load is medium THEN wash_time is long & temp is hot
18. IF dirtiness is high & grease is high & load is medium THEN wash_time is long & temp is hot

# المجموعة الثالثة: الحمولة الثقيلة
19. IF dirtiness is low & grease is low & load is heavy THEN wash_time is normal & temp is cold
20. IF dirtiness is low & grease is medium & load is heavy THEN wash_time is long & temp is warm
21. IF dirtiness is low & grease is high & load is heavy THEN wash_time is long & temp is hot
22. IF dirtiness is medium & grease is low & load is heavy THEN wash_time is long & temp is warm
23. IF dirtiness is medium & grease is medium & load is heavy THEN wash_time is long & temp is hot
24. IF dirtiness is medium & grease is high & load is heavy THEN wash_time is long & temp is hot
25. IF dirtiness is high & grease is low & load is heavy THEN wash_time is long & temp is hot
26. IF dirtiness is high & grease is medium & load is heavy THEN wash_time is long & temp is hot
27. IF dirtiness is high & grease is high & load is heavy THEN wash_time is long & temp is hot
    """, language="text")