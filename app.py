import streamlit as st
import pandas as pd
from openai import OpenAI
import io
import time

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AITA Instagram Story Generator",
    layout="wide"
)

st.title("🔥 AITA Instagram Story Generator")
st.write("Generate short viral AITA stories involving Instagram follower tracker apps (max 1400 characters).")

# =====================================
# SIDEBAR SETTINGS
# =====================================

st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

num_stories = st.sidebar.slider(
    "Number of Stories",
    1,
    10,
    3
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
# SINGLE STORY GENERATOR
# =====================================

def generate_single_story(client, sample_data, tone, mode):

    if mode == "Subtle (Recommended)":
        digital_instruction = """
        The narrator must mention using an Instagram follower tracker app once.
        The narrator must feel slightly embarrassed, insecure, or guilty for using it.
        Never praise the app.
        Never explain how it works.
        Focus on emotional consequences.
        """
    else:
        digital_instruction = """
        The narrator must clearly mention using an Instagram follower tracker app once.
        Do not praise it.
        Do not explain how it works.
        Keep it realistic.
        """

    prompt = f"""
You are writing a Reddit AITA post.

Study the style below:
{sample_data}

Write ONE new AITA story.

STRICT RULES:
- Maximum 1400 characters total.
- Include a TITLE.
- Then write the STORY.
- No timeline.
- Must feel 100% human and imperfect.
- Slight emotional instability is realistic.
- Involve Instagram.
- Must mention using an Instagram follower tracker app once.
- No marketing tone.
- No instructions.
- Start story with "Throwaway because..."
- End with a clear AITA question.

Tone: {tone}

{digital_instruction}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.05,
    )

    return response.choices[0].message.content.strip()


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
            sample_data = df.sample(min(10, len(df))).to_string()

            client = OpenAI(api_key=api_key)

            stories = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("Generating stories..."):

                for i in range(num_stories):

                    status_text.text(f"Generating story {i+1} of {num_stories}...")

                    story = generate_single_story(
                        client,
                        sample_data,
                        tone,
                        mode
                    )

                    stories.append(story)

                    progress_bar.progress((i + 1) / num_stories)
                    time.sleep(0.2)

            status_text.text("✅ All stories generated!")

            final_output = "\n\n====================\n\n".join(stories)

            st.success("Done 🚀")

            st.text_area("Generated Stories", final_output, height=600)

            # CSV Export
            export_df = pd.DataFrame({
                "Generated Story": stories
            })

            csv_buffer = io.StringIO()
            export_df.to_csv(csv_buffer, index=False)

            st.download_button(
                label="⬇ Download Stories as CSV",
                data=csv_buffer.getvalue(),
                file_name="short_instagram_aita_stories.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("Built for Viral Instagram Suspicion Strategy 🚀")
