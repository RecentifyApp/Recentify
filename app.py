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
st.write("Generate short viral AITA stories (max 1400 characters, unlimited angles).")

# =====================================
# SIDEBAR SETTINGS
# =====================================

st.sidebar.header("⚙️ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

num_stories = st.sidebar.slider("Number of Stories", 1, 10, 3)

categories = st.sidebar.multiselect(
    "Select Categories",
    [
        # General
        "Relationships", "Marriage", "Dating", "Family", "Friends", "Work",

        # Relationship
        "Cheating Suspicion", "Trust Issues", "Jealousy", "Long Distance",
        "Secret Ex", "Ex Drama", "Emotional Affair", "Micro-Cheating",
        "Hidden Messages", "Second Account", "Late Night Activity",
        "Toxic Behavior", "Control Issues",

        # Marriage
        "Marriage Conflict", "Spouse Secrecy", "In-Laws Drama",
        "Wedding Drama", "Engagement Doubt",

        # Social Media
        "Instagram Conflict", "Follower Obsession", "Social Media Addiction",
        "Social Media Secrets", "Online Flirting", "Deleted Comments",
        "Privacy", "Public Image vs Private Reality", "Hidden Identity",

        # Friends
        "Best Friend Betrayal", "Friend Group Drama", "Secret Hangouts",

        # Family
        "Sibling Rivalry", "Parent Interference", "Family Loyalty vs Truth",

        # Work
        "Work Affair", "Office Drama", "Office Gossip",
        "Boss Conflict", "Boss Boundary Issues",

        # Psychological
        "Paranoia vs Reality", "Overthinking Spiral", "Obsession",
        "Double Life", "Secrets Revealed",

        # Public
        "Public Confrontation", "Community Scandal", "Event Showdown"
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

# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File (must contain story text column)",
    type=["csv"]
)

# =====================================
# STORY GENERATOR FUNCTION
# =====================================

def generate_single_story(client, sample_data, tone, categories, used_summaries):

    digital_instruction = """
    Mention using an Instagram follower tracking app once.
    Do not explain how it works.
    Do not promote it.
    Keep focus on emotional conflict.
    """

    creativity_instruction = f"""
    Create a completely UNIQUE scenario.

    Avoid repeating themes from:
    {used_summaries}

    You must vary:
    - Main character role (parent, sibling, spouse, coworker, friend, etc.)
    - Type of suspicion
    - Type of discovery
    - Type of confrontation
    - Emotional ending

    Use unexpected twists.
    Make readers divided.
    """

    prompt = f"""
You are writing a Reddit AITA post.

Study this style:
{sample_data}

Write ONE viral AITA story.

STRICT RULES:
- Max 1400 characters
- Include TITLE
- Then STORY
- No timeline
- Messy, imperfect human tone
- Slight overthinking is realistic
- Must involve Instagram
- Must mention using an Instagram follower tracking app once
- No marketing tone
- Start story with "Throwaway because..."
- End with a clear AITA question
- Category focus: {categories}
- Tone: {tone}

{digital_instruction}

{creativity_instruction}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.25
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
            sample_data = df.sample(min(15, len(df))).to_string()

            client = OpenAI(api_key=api_key)

            stories = []
            used_summaries = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(num_stories):

                status_text.text(f"Generating story {i+1} of {num_stories}...")

                story = generate_single_story(
                    client,
                    sample_data,
                    tone,
                    categories,
                    used_summaries
                )

                stories.append(story)
                used_summaries.append(story[:300])

                progress_bar.progress((i + 1) / num_stories)
                time.sleep(0.2)

            status_text.text("✅ All stories generated!")

            final_output = "\n\n====================\n\n".join(stories)

            st.success("Done 🚀")
            st.text_area("Generated Stories", final_output, height=600)

            # CSV export
            export_df = pd.DataFrame({"Generated Story": stories})

            csv_buffer = io.StringIO()
            export_df.to_csv(csv_buffer, index=False)

            st.download_button(
                "⬇ Download Stories as CSV",
                data=csv_buffer.getvalue(),
                file_name="viral_instagram_aita_stories.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown("Unlimited Angles Viral Story Engine 🚀")
