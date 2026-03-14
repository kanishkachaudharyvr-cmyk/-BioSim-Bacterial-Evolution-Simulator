# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="BioSim - Antibiotic Resistance Simulator",
    page_icon="🧬",
    layout="wide"
)

# ------------------------------------------------
# UI THEME
# ------------------------------------------------
# ------------------------------------------------
# UI THEME
# ------------------------------------------------

# ------------------------------------------------
# UI THEME
# ------------------------------------------------

st.markdown("""
<style>
/* 1. Balanced Top Spacing */
.block-container {
    padding-top: 2rem !important; /* Adjusted for perfect spacing */
    padding-bottom: 1rem !important;
    max-width: 95%;
}

/* 2. Hide Streamlit Chrome */
header[data-testid="stHeader"] {visibility: hidden; height: 0px;}
[data-testid="stToolbar"] {display:none;}
footer {visibility:hidden;}
#MainMenu {visibility:hidden;}

/* 3. Global Background and Text */
.stApp {
    background: linear-gradient(180deg, #f3ffff, #e6fbfb);
    color: #003333;
}

/* 4. Neon Heading Styles */
h1 {
    color: #009e9e !important;
    text-shadow: 0 0 10px #00ffd0;
    margin-top: 0px !important; /* Reset to 0 to prevent overcrowding */
    padding-top: 0px !important;
}

h2, h3 {
    color: #009e9e !important;
    text-shadow: 0 0 6px #00ffd0;
}

/* 5. Metric Card Styling */
[data-testid="metric-container"] {
    background: #f6ffff;
    border: 1px solid #00d6d6;
    border-radius: 12px;
    padding: 12px;
}

/* 6. Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 45px;
    background-color: #f0fdfd;
    border-radius: 4px 4px 0px 0px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("🧫 BioSim – Bacterial Evolution Simulator")

st.info("""
This interactive dashboard demonstrates **how antibiotic resistance evolves**.

Bacteria reproduce extremely quickly. During reproduction:

• Random **mutations** occur  
• Some mutations create **resistant bacteria**  
• Antibiotics kill susceptible bacteria  
• Resistant bacteria survive and dominate the population

This simulator visualizes those evolutionary processes.
""")

# ------------------------------------------------
# SCENARIO PRESETS
# ------------------------------------------------

st.subheader("🧪 Scenario Presets")

scenarios = {
"Balanced Environment":{
"population":150,
"resources":500,
"mutation":0.05,
"antibiotic":"None"
},

"Antibiotic Crisis":{
"population":250,
"resources":300,
"mutation":0.12,
"antibiotic":"High"
},

"Low Mutation":{
"population":150,
"resources":700,
"mutation":0.01,
"antibiotic":"Low"
}
}

# initialize slider state

if "pop" not in st.session_state:
    st.session_state.pop = 150
    st.session_state.res = 500
    st.session_state.mut = 0.05
    st.session_state.ant = "None"

col1,col2,col3 = st.columns(3)

if col1.button("🧬 Balanced Environment"):
    s = scenarios["Balanced Environment"]
    st.session_state.pop = s["population"]
    st.session_state.res = s["resources"]
    st.session_state.mut = s["mutation"]
    st.session_state.ant = s["antibiotic"]

if col2.button("💊 Antibiotic Crisis"):
    s = scenarios["Antibiotic Crisis"]
    st.session_state.pop = s["population"]
    st.session_state.res = s["resources"]
    st.session_state.mut = s["mutation"]
    st.session_state.ant = s["antibiotic"]

if col3.button("🧫 Low Mutation"):
    s = scenarios["Low Mutation"]
    st.session_state.pop = s["population"]
    st.session_state.res = s["resources"]
    st.session_state.mut = s["mutation"]
    st.session_state.ant = s["antibiotic"]

# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1,tab2,tab3,tab4,tab5 = st.tabs([
"🧪 Simulation",
"🧫 Colony Growth",
"💊 Antibiotic Diffusion",
"🧠 AI Prediction",
"📊 Download Report"
])

# ------------------------------------------------
# TAB 1 SIMULATION
# ------------------------------------------------

with tab1:

    st.header("Bacterial Population Simulation")

    st.info("""
This simulation models **bacterial population evolution** over time.

Adjusting parameters changes how bacteria grow and develop resistance.
""")

    population = st.slider(
        "Initial Population",
        50,500,
        key="pop"
    )

    resources = st.slider(
        "Available Resources",
        100,1000,
        key="res"
    )

    mutation = st.slider(
        "Mutation Rate",
        0.0,0.2,
        key="mut"
    )

    antibiotic = st.selectbox(
        "Antibiotic Treatment",
        ["None","Low","High"],
        key="ant"
    )

    steps = st.slider("Simulation Time",50,200,120)

    if st.button("🚀 Run Simulation"):

        pop = population

        genotypeA = pop*0.8
        genotypeB = pop*0.15
        genotypeC = pop*0.05

        results = []

        for t in range(steps):

            growth = 0.05*pop
            pop += growth-(0.02*pop)

            mutation_events = mutation*genotypeA

            genotypeA -= mutation_events
            genotypeB += mutation_events

            if antibiotic=="High":
                genotypeA *= 0.8

            if antibiotic=="Low":
                genotypeA *= 0.9

            resistant = genotypeB+genotypeC
            resistance = (resistant/pop)*100

            resources -= pop*0.01

            results.append([
            t,pop,resources,genotypeA,genotypeB,genotypeC,resistance
            ])

        df = pd.DataFrame(results,columns=[
        "time","population","resources","A","B","C","resistance"])

        st.session_state.simulation_df = df

        c1,c2,c3 = st.columns(3)

        c1.metric("Population",int(df.population.iloc[-1]))
        c2.metric("Resistance %",round(df.resistance.iloc[-1],2))
        c3.metric("Resources",round(df.resources.iloc[-1],2))

        fig1 = px.line(df,x="time",y="population",title="Population Growth")
        st.plotly_chart(fig1,use_container_width=True)

        fig2 = px.line(df,x="time",y=["A","B","C"],title="Genotype Distribution")
        st.plotly_chart(fig2,use_container_width=True)

        fig3 = px.line(df,x="time",y="resistance",title="Resistance Evolution")
        st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# TAB 2 COLONY
# ------------------------------------------------

with tab2:

    st.header("Petri Dish Colony Growth")

    st.info("""
Bacteria grow outward forming colonies on nutrient plates.
This simulation shows colony expansion in **2D and 3D space**.
""")

    size = 40
    grid = np.zeros((size,size))
    grid[size//2,size//2] = 1

    steps = st.slider("Growth Steps",10,80,40)

    if st.button("Simulate Colony"):

        for step in range(steps):

            new = grid.copy()

            for i in range(1,size-1):
                for j in range(1,size-1):

                    if grid[i,j]==1:

                        for n in [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]:

                            if np.random.rand()<0.2:
                                new[n]=1

            grid = new

        fig = px.imshow(grid,color_continuous_scale="Viridis",
        title="Colony Density Heatmap")

        st.plotly_chart(fig,use_container_width=True)

    st.subheader("3D Colony Structure")

    x = np.random.normal(0,1,200)
    y = np.random.normal(0,1,200)
    z = np.random.normal(0,0.5,200)

    fig = go.Figure(data=[go.Scatter3d(
        x=x,y=y,z=z,
        mode='markers',
        marker=dict(size=6,color=z,colorscale="Turbo")
    )])

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# TAB 3 ANTIBIOTIC DIFFUSION
# ------------------------------------------------

with tab3:

    st.header("Antibiotic Diffusion")

    st.info("""
Antibiotics spread through the environment and create
zones where bacteria cannot survive.
""")

    size = 50
    grid = np.zeros((size,size))
    grid[size//2,size//2] = 10

    for step in range(30):

        grid=(grid+
        np.roll(grid,1,0)+
        np.roll(grid,-1,0)+
        np.roll(grid,1,1)+
        np.roll(grid,-1,1))/5

    fig = px.imshow(grid,color_continuous_scale="Magma",
    title="Antibiotic Concentration Map")

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# TAB 4 AI PREDICTION
# ------------------------------------------------

with tab4:

    st.header("AI Resistance Prediction")

    st.info("""
A machine learning model predicts future resistance levels
using simulation data.
""")

    if "simulation_df" not in st.session_state:

        st.warning("Run the simulation first.")

    else:

        df = st.session_state.simulation_df

        X = df[["time"]]
        y = df["resistance"]

        model = LinearRegression()
        model.fit(X,y)

        future = st.slider("Predict Resistance At Time",0,300,150)

        pred = model.predict([[future]])

        st.metric("Predicted Resistance %",round(pred[0],2))

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["resistance"],
        mode="lines",
        name="Simulation"
        ))

        fig.add_trace(go.Scatter(
        x=[future],
        y=[pred[0]],
        mode="markers",
        marker=dict(size=12),
        name="Prediction"
        ))

        st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# TAB 5 DOWNLOAD
# ------------------------------------------------
# --- UPDATE INITIALIZATION (Top of script) ---
if "pop" not in st.session_state:
    st.session_state.pop = 150
    st.session_state.res = 500
    st.session_state.mut = 0.05
    st.session_state.ant = "None"
    st.session_state.simulation_df = None  # Initialize as None

# ... (keep your existing tabs 1, 2, 3, 4) ...

# ------------------------------------------------
# TAB 5 DOWNLOAD (Corrected)
# ------------------------------------------------
# ------------------------------------------------
# TAB 5 DOWNLOAD
# ------------------------------------------------
with tab5:
    st.header("📊 Download Simulation Report")

    # 1. Safely retrieve values from session state to avoid "method" errors
    # We use .get() and float() to ensure these are numbers
    curr_pop = float(st.session_state.get("pop", 150))
    curr_res = float(st.session_state.get("res", 500))
    curr_mut = float(st.session_state.get("mut", 0.05))
    curr_ant = st.session_state.get("ant", "None")
    curr_steps = int(steps) # 'steps' is defined at the top of the script

    if st.button("Generate & Download Report"):
        report_results = []
        
        # Initial local variables for the calculation loop
        gA = curr_pop * 0.8
        gB = curr_pop * 0.15
        gC = curr_pop * 0.05
        temp_pop = curr_pop
        temp_res = curr_res

        for t in range(curr_steps):
            # Population Growth Logic
            growth = 0.05 * temp_pop
            death = 0.02 * temp_pop
            temp_pop = temp_pop + growth - death
            
            # Mutation Logic
            m_events = curr_mut * gA
            gA -= m_events
            gB += m_events
            
            # Resource depletion
            temp_res -= temp_pop * 0.01

            # Competition Index based on Antibiotic Treatment
            if curr_ant == "High":
                comp_idx = 0.8
                gA *= 0.8
            elif curr_ant == "Low":
                comp_idx = 0.4
                gA *= 0.9
            else:
                comp_idx = 0.1

            # Calculate safe densities (prevent division by zero)
            denom = temp_pop if temp_pop > 0 else 1
            
            # Append data with the EXACT column names from your image
            report_results.append({
                "time_step": t,
                "total_pop": round(max(0, temp_pop), 2),
                "resource_concentration": round(max(0, temp_res), 2),
                "genotype_density": round(gB / denom, 4),
                "mutation_frequency": round(m_events / denom, 4),
                "cooperation_index": round((gB + gC) / denom, 4),
                "competition_index": comp_idx
            })

        # Create DataFrame
        df_report = pd.DataFrame(report_results)
        
        # Display a preview
        st.write("### Preview of Data")
        st.dataframe(df_report.head())
        
        # Convert to CSV
        csv_data = df_report.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Click here to download CSV",
            data=csv_data,
            file_name="simulation_metrics.csv",
            mime="text/csv"
        )
    else:
        st.info("Click the button above to process the current data for download.")