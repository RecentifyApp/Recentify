import streamlit as st
import pandas as pd
from openai import OpenAI

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="AITA Viral Story Generator",
    layout="wide"
)

st.title("🔥 AITA Viral Story Generator")
st.write("Upload your viral AITA CSV and generate new human-like stories.")

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
        "Coworker Drama",
        "Family",
        "In-laws",
        "Parenting",
        "Siblings",
        "Friends",
        "Best Friend Drama",
        "Jealousy",
        "Money Issues",
        "Privacy",
        "Trust Issues",
        "Cheating Suspicion",
        "Instagram Conflict",
        "Social Media Secrets",
        "Roommates",
        "Travel Conflict",
        "Wedding Drama",
        "Ex Drama",
        "Toxic Behavior",
        "Control Issues",
        "Public Embarrassment",
        "Secrets Revealed",
        "Boundaries",
        "Career Conflict",
        "Online Lies",
        "Hidden Identity",
        "Double Life",
        "Unexpected Betrayal"
    ]
)

tone = st.sidebar.selectbox(
    "Tone Style",
    [
        "Natural Human",
        "Emotional",
        "Suspenseful",
        "Confessional",
        "Calm Narrative",
        "Raw & Realistic",
        "Controversial"
    ]
)

# ===============================
# FILE UPLOAD
# ===============================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File (must contain story text column)",
    type=["csv"]
)

# ===============================
# GENERATE STORIES FUNCTION
# ===============================

def generate_stories(df, api_key, num_stories, categories, tone):

    client = OpenAI(api_key=api_key)

    sample_data = df.sample(min(15, len(df))).to_string()

    prompt = f"""
You are a professional Reddit AITA storyteller.

Study the viral stories below and learn their:
- Structure
- Emotional pacing
- Natural human tone
- Conflict intensity
- Moral ambiguity

DATA:
{sample_data}

Now generate {num_stories} completely new AITA stories.

RULES:
- Must feel 100% human written
- No marketing tone
- No mention of apps
- Realistic conflicts
- Emotional nuance
- Slight moral gray area
- Viral potential
- Start with "Throwaway because..."
- 400-700 words each
- Category focus: {categories}
- Tone style: {tone}

Separate stories clearly with: ===== STORY =====
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    return response.choices[0].message.content


# ===============================
# MAIN LOGIC
# ===============================

if st.button("🚀 Generate Stories"):

    if not api_key:
        st.error("Please enter your OpenAI API Key.")
    elif not uploaded_file:
        st.error("Please upload a CSV file.")
    else:
        try:
            df = pd.read_csv(uploaded_file)

            with st.spinner("Generating viral stories..."):
                stories = generate_stories(
                    df,
                    api_key,
                    num_stories,
                    categories,
                    tone
                )

            st.success("Stories generated successfully ✅")

            st.text_area(
                "Generated Stories",
                stories,
                height=600
            )

            st.download_button(
                "⬇ Download as TXT",
                stories,
                file_name="aita_generated_stories.txt"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.markdown("Built for Viral AITA Strategy 🚀")