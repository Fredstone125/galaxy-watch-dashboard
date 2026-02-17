import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Galaxy Watch Performance Dashboard",
    layout="wide"
)

DATA_PATH = "data/"

# -----------------------------
# DATA LOADER
# -----------------------------
def load_csv(filename):
    try:
        df = pd.read_csv(DATA_PATH + filename)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        st.warning(f"Could not load {filename}")
        return None

# -----------------------------
# LOAD DATA
# -----------------------------
calories = load_csv("calories.csv")
activity = load_csv("activity.csv")
heart = load_csv("heart_rate.csv")
sleep = load_csv("sleep.csv")
stress = load_csv("stress.csv")
energy = load_csv("energy.csv")
spo2 = load_csv("spo2.csv")
bp = load_csv("bp.csv")
ecg = load_csv("ecg.csv")
falls = load_csv("falls.csv")
body = load_csv("body_comp.csv")
antiox = load_csv("antioxidants.csv")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Dashboard Role")
role = st.sidebar.selectbox(
    "Select View",
    ["Athlete", "Coach", "Trainer", "Team Doctor"]
)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def line_chart(df, y, title):
    fig = px.line(df, x="timestamp", y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

# =============================
# ATHLETE VIEW
# =============================
if role == "Athlete":
    st.title("Athlete Overview")

    col1, col2, col3 = st.columns(3)

    if energy is not None:
        col1.metric("Energy Score", int(energy["energy_score"].iloc[-1]))

    if calories is not None:
        col2.metric("Calories Burned", int(calories["calories"].iloc[-1]))

    if activity is not None:
        col3.metric("Active Minutes", int(activity["active_minutes"].iloc[-1]))

    if sleep is not None:
        sleep["sleep_score"] = sleep[["deep", "light", "rem"]].sum(axis=1)
        line_chart(sleep, "sleep_score", "Sleep Quality")

    if stress is not None:
        line_chart(stress, "stress_score", "Stress Trend")

    if antiox is not None:
        st.metric("Antioxidant Index", round(antiox["carotenoid_index"].iloc[-1], 2))

# =============================
# COACH VIEW
# =============================
elif role == "Coach":
    st.title("Coach Performance Dashboard")

    if calories is not None:
        line_chart(calories, "calories", "Calories Burned")

    if activity is not None:
        line_chart(activity, "active_minutes", "Active Minutes")

    if heart is not None:
        line_chart(heart, "bpm", "Heart Rate")

    if energy is not None:
        line_chart(energy, "energy_score", "Readiness Score")

# =============================
# TRAINER VIEW
# =============================
elif role == "Trainer":
    st.title("Trainer Conditioning & Recovery")

    if heart is not None:
        heart["zone"] = pd.cut(
            heart["bpm"],
            bins=[0, 100, 120, 140, 160, 220],
            labels=["Z1", "Z2", "Z3", "Z4", "Z5"]
        )
        zone_counts = heart["zone"].value_counts().sort_index()
        fig = px.bar(zone_counts, title="Heart Rate Zones")
        st.plotly_chart(fig, use_container_width=True)

    if body is not None:
        line_chart(body, "body_fat", "Body Fat %")
        line_chart(body, "muscle_mass", "Muscle Mass")

    if sleep is not None:
        fig = px.area(
            sleep,
            x="timestamp",
            y=["deep", "light", "rem"],
            title="Sleep Stages"
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================
# TEAM DOCTOR VIEW
# =============================
elif role == "Team Doctor":
    st.title("Medical Monitoring")

    if heart is not None:
        line_chart(heart, "bpm", "Heart Rate")

    if ecg is not None:
        st.metric(
            "ECG Abnormal Events",
            int(ecg["abnormal_flag"].sum())
        )

    if spo2 is not None:
        line_chart(spo2, "oxygen_percent", "Blood Oxygen (SpO₂)")

    if bp is not None:
        fig = px.line(
            bp,
            x="timestamp",
            y=["systolic", "diastolic"],
            title="Blood Pressure"
        )
        st.plotly_chart(fig, use_container_width=True)

    if falls is not None:
        st.subheader("Fall Events")
        st.dataframe(falls[falls["fall_detected"] == 1])

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Galaxy Watch Performance System • Demo Data")
