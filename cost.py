import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Cost Estimator", layout="centered") 

# App title
st.title("📞 QuibbleAI Cost Estimator")


col1, col2 = st.columns(2)

with col1:
    # Inputs
    duration = st.slider("⏱️ Call Duration (minutes)", 1, 15, 3)
    calls = st.slider("📞 Calls per Month", 0, 10000, 3000, step=200)
    tokens = st.number_input("🧠 Tokens used per Call", value=700)
    llm_option = st.selectbox("🤖 Choose Language Model", ["GPT-4.1", "GPT-4o", "GPT-4o (latest)"])
    platform_cost = st.number_input("💻 Platform/Infra Cost", value=20)

    # LLM pricing logic
    llm_rate = {
        "GPT-4.1": 0.06,
        "GPT-4o": 0.07,
        "GPT-4o (latest)": 0.14
    }[llm_option]

    # Calculations
    total_minutes = calls * duration
    llm_cost = round((calls * tokens / 1_000_000) * llm_rate, 2)
    inbound_twilio_cost = round(total_minutes * 0.008, 2)
    stt_cost = round(total_minutes * 0.01, 2)
    tts_cost = round(total_minutes * 0.0108, 2)
    infra_cost = platform_cost
    total = round(llm_cost + inbound_twilio_cost + stt_cost + tts_cost + infra_cost, 2)
    cost_per_call = round(total / calls, 2) if calls else 0.00

    # Breakdown
    st.markdown("---")
    st.subheader("📊 Cost Breakdown")
    st.write(f"**Total Call Minutes:** {total_minutes} mins")
    st.write(f"**Inbound Twilio Cost:** ${inbound_twilio_cost}")
    st.write(f"**LLM Cost ({llm_option}):** ${llm_cost}")
    st.write(f"**Speech-to-Text (STT) Cost:** ${stt_cost}")
    st.write(f"**Text-to-Speech (TTS) Cost:** ${tts_cost}")
    st.write(f"**Platform/Infra Cost:** ${infra_cost}")

    st.markdown("---")
    st.success(f"💰 Estimated Monthly Cost: **${total}**")
    st.info(f"📞 Cost per Call: **${cost_per_call}**")

with col2:
    # Pie chart
    labels = ['LLM', 'Twilio (Inbound)', 'STT', 'TTS', 'Infra']
    sizes = [llm_cost, inbound_twilio_cost, stt_cost, tts_cost, infra_cost]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.subheader("📊 Cost Distribution")
    st.pyplot(fig)

    # Downloadable report
    report = f"""
AI Call Cost Estimator Report
-----------------------------
Total Calls: {calls}
Minutes per Call: {duration}
Total Minutes: {total_minutes}
LLM Model: {llm_option}
LLM Cost: ${llm_cost}
Inbound Call Cost: ${inbound_twilio_cost}
STT Cost: ${stt_cost}
TTS Cost: ${tts_cost}
Infrastructure Cost: ${infra_cost}
Total Estimated Monthly Cost: ${total}
Cost per Call: ${cost_per_call}
"""
    st.download_button("📄 Download Report", report, file_name="ai_cost_estimate.txt")

