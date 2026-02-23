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
st.write("Generate short viral AITA stories (max 1400 characters).")

# =====================================
# SIDEBAR SETTINGS
# =====================================

st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

num_stories = st.sidebar.slider("Number of Stories", 1, 10, 3)

categories = st.sidebar.multiselect(
    "Select Categories",
    [
        # Relationships
        "Cheating Suspicion",
        "Trust Issues",
        "Jealousy",
        "Long Distance",
        "Secret Ex",
        "Emotional Affair",
        "Micro-Cheating",
        "Hidden Messages",
        "Second Account",
        "Late Night Activity",

        # Marriage
        "Marriage Conflict",
        "Spouse Secrecy",
        "In-Laws Drama",
        "Wedding Drama",
        "Engagement Doubt",

        # Social Media
        "Instagram Conflict",
        "Follower Obsession",
        "Social Media Addiction",
        "Online Flirting",
        "Deleted Comments",
        "Public Image vs Private Reality",

        # Friends
        "Best Friend Betrayal",
        "Friend Group Drama",
        "Secret Hangouts",

        # Family
        "Sibling Rivalry",
        "Parent Interference",
        "Family Loyalty vs Truth",

        # Work
        "Work Affair",
        "Office Gossip",
        "Boss Boundary Issues",

        # Psychological
        "Paranoia vs Reality",
        "Overthinking Spiral",
        "Obsession",
        "Control Issues",
        "Double Life",
        "Secrets Revealed",

        # Public
        "Public Confrontation",
        "Community Scandal",
        "Event Showdown"
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
# SINGLE STORY GENERATOR
# =====================================

def generate_single_story(client, sample_data, tone, mode, categories):

    if mode == "Subtle (Recommended)":
        digital_instruction = """
        Mention using an Instagram follower tracking app once.
        The narrator should feel slightly embarrassed or guilty.
        Do not explain how it works.
        Do not promote it.
        Focus on emotional consequences.
        """
    else:
        digital_instruction = """
        Mention using an Instagram follower tracking app once.
        Do not explain how it works.
        Do not promote it.
        Keep tone realistic.
        """

    prompt = f"""
You are writing a Reddit AITA post.

Study the style below:
{sample_data}

Write ONE brand new AITA story.

STRICT RULES:
- Maximum 1400 characters.
- Include a TITLE.
- Then write the STORY.
- No timeline.
- Must feel messy and human.
- Include self-doubt and overthinking.
- Slight emotional instability is realistic.
- Must involve Instagram.
- Mention using an Instagram follower tracking app once.
- No marketing tone.
- Start story with "Throwaway because..."
- End with a clear AITA question.
- Category focus: {categories}
- Tone: {tone}

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
                        mode,
                        categories
                    )

                    stories.append(story)

                    progress_bar.progress((i + 1) / num_stories)
                    time.sleep(0.2)

            status_text.text("✅ All stories generated!")

            final_output = "\n\n====================\n\n".join(stories)

            st.success("Done 🚀")

            st.text_area("Generated Stories", final_output, height=600)

            # CSV Export
            export_df = pd.DataFrame({"Generated Story": stories})

            csv_buffer = io.StringIO()
            export_df.to_csv(csv_buffer, index=False)

            st.download_button(
                "⬇ Download Stories as CSV",
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
