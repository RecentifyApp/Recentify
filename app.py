import streamlit as st
import pandas as pd
from openai import OpenAI
import io

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AITA Instagram Story Generator",
    layout="wide"
)

st.title("🔥 AITA Instagram Story Generator")
st.write("Generate viral AITA stories involving Instagram follower tracker apps (without sounding like ads).")

# =====================================
# SIDEBAR SETTINGS
# =====================================

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
        "Cheating Suspicion",
        "Trust Issues",
        "Jealousy",
        "Ex Drama",
        "Family Conflict",
        "Friends Betrayal",
        "Work Affair",
        "Public Confrontation",
        "Secrets Revealed",
        "Double Life",
        "Church / Community",
        "Social Media Obsession"
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

mode = st.sidebar.radio(
    "Digital Framing Mode",
    ["Subtle (Recommended)", "Direct"]
)

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File (must contain story text column)",
    type=["csv"]
)

# =====================================
# GENERATE FUNCTION
# =====================================

def generate_stories(df, api_key, num_stories, categories, tone, mode):

    client = OpenAI(api_key=api_key)

    sample_data = df.sample(min(15, len(df))).to_string()

    # Framing control
    if mode == "Subtle (Recommended)":
        digital_instruction = """
        Every story MUST mention using an Instagram follower tracker app.
        The app must be mentioned only once.
        The narrator must feel embarrassed, guilty, or slightly ashamed for using it.
        Never praise the app.
        Never explain how it works.
        Focus on emotional consequences, not the technology.
        """
    else:
        digital_instruction = """
        Every story MUST clearly mention using an Instagram follower tracker app.
        Mention it only once.
        Do NOT praise it.
        Do NOT explain how it works.
        Keep the tone realistic, not promotional.
        """

    prompt = f"""
You are a professional Reddit AITA storyteller.

Study the viral examples below and learn:
- Human imperfection
- Emotional pacing
- Suspicion build-up
- Moral gray endings

DATA:
{sample_data}

Generate {num_stories} completely new AITA stories.

MANDATORY RULES:
1. Every story MUST involve Instagram.
2. Every story MUST mention using an Instagram follower tracker app.
3. Mention the app only once.
4. No marketing tone.
5. No promotion.
6. No instructions.
7. Must feel 100% human.
8. 450-750 words.
9. Start with "Throwaway because..."
10. End with a clear AITA question.

Category focus: {categories}
Tone: {tone}

{digital_instruction}

Format each story like this:

===== STORY =====
TITLE:
FULL STORY:

TIMELINE:
- Event 1
- Event 2
- Escalation
- Discovery
- Confrontation
- Final Dilemma
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,
    )

    return response.choices[0].message.content


# =====================================
# MAIN BUTTON
# =====================================

if st.button("🚀 Generate Stories"):

    if not api_key:
        st.error("Please enter your OpenAI API Key.")
    elif not uploaded_file:
        st.error("Please upload a CSV file.")
    else:
        try:
            df = pd.read_csv(uploaded_file)

            with st.spinner("Generating high-viral Instagram stories..."):
                stories_text = generate_stories(
                    df,
                    api_key,
                    num_stories,
                    categories,
                    tone,
                    mode
                )

            st.success("Stories generated successfully ✅")

            st.text_area("Generated Stories", stories_text, height=600)

            # Split stories for CSV export
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
                file_name="generated_instagram_aita_stories.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("Built for Viral Instagram Suspicion Story Strategy 🚀")
