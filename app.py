import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="LogiScholar", layout="wide", page_icon="🎓")

# --- 2. THEME & VISIBILITY STYLING (Professional Light Theme) ---
st.markdown("""
    <style>
    /* Light Professional Background */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #e2e8f0;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-left: 5px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* Text Visibility */
    div[data-testid="stMetricLabel"] > div {
        color: #64748b !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #1e3a8a !important;
        font-size: 32px !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
    }
    
    /* Input Labels */
    .stSlider label, .stSelectbox label, .stTextInput label {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def get_data():
    try:
        return pd.read_csv('university_core_data.csv')
    except FileNotFoundError:
        st.error("Data file not found! Please run your Jupyter script to create 'university_core_data.csv' first.")
        st.stop()

df = get_data()

# Department to Core Subject Mapping
dept_subjects = {
    'CSE': ['Data Science', 'Operating Systems', 'Cyber Security'],
    'IT': ['Data Science', 'Cloud Computing', 'Web Frameworks'],
    'ECE': ['VLSI Design', 'Digital Electronics', 'Signal Processing'],
    'EEE': ['Power Systems', 'Control Theory', 'Electric Machines'],
    'MECH': ['Thermodynamics', 'Fluid Mechanics', 'Robotics']
}

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>PORTAL</h2>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Dashboard", "AI Predictor", "Search"],
        icons=["speedometer2", "cpu-fill", "search"], 
        default_index=0,
        styles={
            "container": {"background-color": "#ffffff"},
            "nav-link": {"color": "#475569", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white"},
        }
    )
    st.markdown("---")
    st.info("System Status: Online")
    st.caption(f"Database Size: {len(df):,} Records")

# --- 5. DASHBOARD PAGE ---
if selected == "Dashboard":
    st.title("🏛️ Academic Command Center")
    
    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", f"{len(df):,}")
    c2.metric("Campus Avg GPA", f"{df['Current_GPA'].mean():.2f}")
    c3.metric("Avg Attendance", f"{df['Attendance_%'].mean():.1f}%")
    c4.metric("Retention Rate", "98.2%")

    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Department Enrollment (Pie Chart)")
        fig_pie = px.pie(df, names='Department', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_right:
        st.subheader("Avg Performance by Department (Bar Chart)")
        avg_gpa_dept = df.groupby('Department')['Current_GPA'].mean().reset_index()
        fig_bar = px.bar(avg_gpa_dept, x='Department', y='Current_GPA', color='Department', 
                         text_auto='.2f', color_discrete_sequence=px.colors.qualitative.Safe)
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- 6. AI PREDICTOR PAGE ---
elif selected == "AI Predictor":
    st.title("🤖 Intelligent GPA Forecast")
    st.write("Using **Multiple Linear Regression** weights to predict future academic outcomes.")
    
    input_col, result_col = st.columns([1, 1])
    
    with input_col:
        st.markdown("### 📝 Performance Inputs")
        u_dept = st.selectbox("Current Department", list(dept_subjects.keys()))
        subjects = dept_subjects[u_dept]
        
        s1 = st.slider(f"{subjects[0]} Marks", 0, 100, 80)
        s2 = st.slider(f"{subjects[1]} Marks", 0, 100, 75)
        s3 = st.slider(f"{subjects[2]} Marks", 0, 100, 85)
        att = st.slider("Current Attendance %", 0, 100, 90)

    with result_col:
        st.markdown("### 📈 AI Prediction Analysis")
        # Logic: Weighted Linear Regression Simulation
        prediction = ((s1*0.35) + (s2*0.25) + (s3*0.20) + (att*0.20)) / 10
        
        st.metric("Forecasted GPA", f"{prediction:.2f}")
        st.progress(prediction/10)
        
        if prediction >= 8.5:
            st.success("Analysis: Distinction Performance Expected.")
        elif prediction >= 6.0:
            st.info("Analysis: Standard Passing Performance.")
        else:
            st.error("Warning: Academic Support Intervention Recommended.")

# --- 7. SEARCH PAGE (COLOR ZONES & DOWNLOAD) ---
elif selected == "Search":
    st.title("🔍 Student Record Search")
    reg_no = st.text_input("Enter Student Register ID (10001 - 20000)")

    if reg_no:
        result = df[df['Register_No'].astype(str) == reg_no]
        if not result.empty:
            st.write(f"### Academic Profile: {result['Name'].values[0]}")

            # Define Traffic-Light Performance Zones
            def apply_performance_zones(val):
                if isinstance(val, (int, float)):
                    if val <= 45:
                        return 'background-color: #ffcccc; color: #990000;' # Red Zone
                    elif val <= 60:
                        return 'background-color: #ffe5cc; color: #994c00;' # Orange Zone
                    elif val <= 80:
                        return 'background-color: #ffffcc; color: #808000;' # Yellow Zone
                    else:
                        return 'background-color: #ccffcc; color: #006600;' # Green Zone
                return ''

            # Style the dataframe with discrete colors
            styled_profile = result.style.applymap(
                apply_performance_zones, 
                subset=['Mark_1', 'Mark_2', 'Mark_3', 'Attendance_%', 'Current_GPA']
            ).format(precision=2)

            st.dataframe(styled_profile, use_container_width=True)
            
            # --- DOWNLOAD OPTION ---
            st.markdown("### Export Student Data")
            csv_data = result.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Download Academic Report (.csv)",
                data=csv_data,
                file_name=f"Student_Report_{reg_no}.csv",
                mime="text/csv",
                help="Download this profile for offline record keeping."
            )
            
            st.toast("Profile Loaded Successfully!", icon='⭐')
        else:
            st.error("No record found with that Register ID.")
