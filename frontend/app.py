
import requests
import streamlit as st


BACKEND_URL = "http://backend:7860"

st.title("ExtraaLearn – Lead Conversion Predictor")
st.write("Enter a lead's details to see how likely they are to become a paying customer.")

# ---- Inputs ----
age = st.number_input("Age", min_value=18, max_value=70, value=40)
occupation = st.selectbox("Current occupation", ["Professional", "Unemployed", "Student"])
first_interaction = st.selectbox("First interaction", ["Website", "Mobile App"])
profile = st.selectbox("Profile completed", ["High", "Medium", "Low"])
visits = st.number_input("Website visits", min_value=0, max_value=50, value=3)
time_spent = st.number_input("Time spent on website (seconds)", min_value=0, max_value=3000, value=700)
page_views = st.number_input("Page views per visit", min_value=0.0, max_value=20.0, value=3.0)
last_activity = st.selectbox("Last activity", ["Email Activity", "Phone Activity", "Website Activity"])
print1 = st.selectbox("Saw newspaper ad?", ["No", "Yes"])
print2 = st.selectbox("Saw magazine ad?", ["No", "Yes"])
digital = st.selectbox("Saw digital ad?", ["No", "Yes"])
edu = st.selectbox("Heard via educational channels?", ["No", "Yes"])
referral = st.selectbox("Came through a referral?", ["No", "Yes"])

lead = {
    "age": age, "current_occupation": occupation, "first_interaction": first_interaction,
    "profile_completed": profile, "website_visits": visits, "time_spent_on_website": time_spent,
    "page_views_per_visit": page_views, "last_activity": last_activity,
    "print_media_type1": print1, "print_media_type2": print2, "digital_media": digital,
    "educational_channels": edu, "referral": referral,
}

# ---- Predict ----
if st.button("Predict"):
    try:
        r = requests.post(f"{BACKEND_URL}/v1/lead", json=lead, timeout=30)
        if r.status_code == 200:
            out = r.json()
            st.success(f"{out['prediction']}  (probability: {out['conversion_probability']:.1%})")
        else:
            st.error(f"Backend error: {r.status_code} – {r.text}")
    except Exception as e:
        st.error(f"Could not reach the backend: {e}")
