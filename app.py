import streamlit as st
import pandas as pd
from openai import OpenAI
import io

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="AITA Viral Story Generator Pro",
    layout="wide"
)

st.title("🔥 AITA Viral Story Generator Pro")
st.write("Upload your viral dataset and generate high-converting AITA stories.")

# ===============================
# SIDEBAR SETTINGS
# ===============================

st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

num_stories = st.sidebar.slider(
    "Number of Stories",
    1,
    20,
    3
)

categories = st.sidebar.multiselect(
    "Select Categories",
    [
        "Relationships",
        "Marriage",
        "Dating",
        "Long Distance",
        "Work",
        "Office Drama",
        "Boss Conflict",
        "Family",
        "In-laws",
        "Friends",
        "Jealousy",
        "Money Issues",
        "Trust Issues",
        "Cheating Suspicion",
        "Instagram Conflict",
        "Social Media Secrets",
        "Privacy",
        "Ex Drama",
        "Wedding Drama",
        "Toxic Behavior",
        "Control Issues",
        "Public Confrontation",
        "Hidden Identity",
        "Double Life",
        "Secrets Revealed"
    ]
)

tone = st.sidebar.selectbox(
    "Tone Style",
    [
        "Natural Human",
        "Emotional",
        "Suspenseful",
        "Confessional",
        "Raw & Realistic",
        "Controversial"
    ]
)

digital_mode = st.sidebar.checkbox("Enable Subtle Digital Suspicion Mode", value=True)

# ===============================
# FILE UPLOAD
# ===============================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File (must contain story column)",
    type=["csv"]
)

# ===============================
# GENERATE FUNCTION
# ===============================

def generate_stories(df, api_key, num_stories, categories, tone, digital_mode):

    client = OpenAI(api_key=api_key)

    sample_data = df.sample(min(15, len(df))).to_string()

    digital_instruction = ""
    if digital_mode:
        digital_instruction = """
If digital clues are involved:
- Imply tracking patterns without explaining tools.
- Never name apps.
- Never teach methods.
- Focus on emotional consequences of discovering patterns.
"""

    prompt = f"""
You are a professional Reddit AITA storyteller.

Study the viral dataset below and learn:
- Emotional pacing
- Natural Reddit tone
- Conflict build-up
- Moral ambiguity
- Viral tension structure

DATA:
{sample_data}

Generate {num_stories} brand new AITA stories.

Rules:
- Start with "Throwaway because..."
- 400-700 words each
- Must feel 100% human
- No marketing tone
- Realistic conflict
- Strong viral tension
- Category focus: {categories}
- Tone: {tone}
{digital_instruction}

STRUCTURE EACH STORY LIKE THIS:

===== STORY =====
TITLE:
FULL STORY:

TIMELINE:
- Event 1:
- Event 2:
- Event 3:
- Escalation:
- Turning Point:
- Final Dilemma:

End with AITA question.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,
    )

    return response.choices[0].message.content

# ===============================
# MAIN ACTION
# ===============================

if st.button("🚀 Generate Viral Stories"):

    if not api_key:
        st.error("Please enter OpenAI API Key.")
    elif not uploaded_file:
        st.error("Please upload a CSV file.")
    else:
        try:
            df = pd.read_csv(uploaded_file)

            with st.spinner("Generating high-viral stories..."):
                stories_text = generate_stories(
                    df,
                    api_key,
                    num_stories,
                    categories,
                    tone,
                    digital_mode
                )

            st.success("Stories generated successfully ✅")

            st.text_area("Generated Stories", stories_text, height=600)

            # Convert to CSV
            stories_list = stories_text.split("===== STORY =====")
            stories_list = [s.strip() for s in stories_list if s.strip()]

            export_df = pd.DataFrame({
                "Generated Story": stories_list
            })

            csv_buffer = io.StringIO()
            export_df.to_csv(csv_buffer, index=False)

            st.download_button(
                label="⬇ Download Stories as CSV",
                data=csv_buffer.getvalue(),
                file_name="generated_aita_stories.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.markdown("Built for High-Converting Viral Story Marketing 🚀")
