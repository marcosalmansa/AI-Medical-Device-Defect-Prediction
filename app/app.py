import streamlit as st
import pandas as pd
import joblib
import os


# Ruta del modelo 
model_path = os.path.join(
    os.path.dirname(__file__),
    "../models/medical_device_quality_AI.pkl"
)

# Cargar modelo
model_package = joblib.load(model_path)

model = model_package["model"]
threshold = model_package["threshold"]

# Título
st.title("Medical Device Manufacturing Quality AI")

st.write(
    """
    Predictive AI system for detecting potential manufacturing defects
    in medical devices based on process parameters.
    """
)


# Entrada de parámetros

temperature = st.number_input(
    "Temperature (ºC)",
    min_value=50.0,
    max_value=100.0,
    value=75.0
)

pressure = st.number_input(
    "Pressure (bar)",
    min_value=1.0,
    max_value=8.0,
    value=4.0
)

cycle_time = st.number_input(
    "Cycle time (min)",
    min_value=10.0,
    max_value=60.0,
    value=35.0
)

machine_speed = st.number_input(
    "Machine speed (rpm)",
    min_value=50.0,
    max_value=200.0,
    value=120.0
)

vibration = st.number_input(
    "Vibration (mm)",
    min_value=0.0,
    max_value=0.2,
    value=0.05
)

humidity = st.number_input(
    "Humidity (%)",
    min_value=10.0,
    max_value=90.0,
    value=45.0
)


# Predicción

if st.button("Predict quality"):

    input_data = pd.DataFrame({

        "temperature_C": [temperature],
        "pressure_bar": [pressure],
        "cycle_time_min": [cycle_time],
        "machine_speed_rpm": [machine_speed],
        "vibration_mm": [vibration],
        "humidity_percent": [humidity]

    })


    probability = model.predict_proba(
        input_data
    )[0][1]


    prediction = (
        probability >= threshold
    )


    st.subheader("Prediction result")


    if prediction:

        st.error(
            f"⚠️ Potential defect detected\n\n"
            f"Defect probability: {probability:.1%}"
        )

    else:

        st.success(
            f"✅ Product quality accepted\n\n"
            f"Defect probability: {probability:.1%}"
        )