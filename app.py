import os
import base64
import streamlit as st

# Define the local folders
PODCAST_FOLDER = "podcasts"
QUESTIONS_FOLDER = "questions"

# Function to get all audio files from the folder
def get_podcast_files(folder):
    supported_formats = [".mp3", ".wav"]
    return [f for f in os.listdir(folder) if os.path.splitext(f)[1] in supported_formats]

# Function to parse a single questions file
def parse_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    sections = content.strip().split("\n\n")
    qa_pairs = []
    for section in sections:
        if "**" in section:
            question, *answer = section.split("\n")
            question = question.strip().strip("**")  # Extract question text
            answer = "\n".join(line.strip() for line in answer)  # Combine answer lines
            qa_pairs.append({"question": question, "answer": answer})
    return qa_pairs

# Function to convert the image to a Base64 string
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the local background image
background_image_path = "img/3d-background-with-white-cubes.jpg"
img_base64 = get_base64_image(background_image_path)

# CSS for background image
page_bg_img = f'''
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
}}
</style>
'''

# Inject the CSS into the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load podcasts
podcast_files = get_podcast_files(PODCAST_FOLDER)

# Load questions from all text files in the folder
question_files = [f for f in os.listdir(QUESTIONS_FOLDER) if f.endswith(".txt")]
questions_by_topic = {os.path.splitext(f)[0]: parse_questions(os.path.join(QUESTIONS_FOLDER, f)) for f in question_files}

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["NLP Podcasts", "NLP Q&A"])

if section == "NLP Podcasts":
    # NLP Podcasts Section
    st.title("NLP Podcasts")
    st.write("Browse and listen to podcasts about NLP concepts!")

    if podcast_files:
        for podcast in podcast_files:
            podcast_path = os.path.join(PODCAST_FOLDER, podcast)
            st.subheader(os.path.splitext(podcast)[0])  # Show the podcast title (without extension)
            st.audio(podcast_path)  # Play the podcast
    else:
        st.write("No podcasts available in the folder.")

elif section == "NLP Q&A":
    # NLP Q&A Section
    st.title("NLP Q&A")
    st.write("Select a topic to test your knowledge and learn about NLP concepts!")

    # Topic selection
    topics = list(questions_by_topic.keys())
    selected_topic = st.sidebar.selectbox("Select a topic", topics)

    # Display questions for the selected topic
    if selected_topic:
        st.header(f"Topic: {selected_topic.capitalize()}")
        questions = questions_by_topic[selected_topic]
        for idx, qa in enumerate(questions):
            st.subheader(f"Question {idx + 1}: {qa['question']}")
            with st.expander("Reveal Answer"):
                st.write(qa["answer"])
