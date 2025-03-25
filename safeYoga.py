import streamlit as st

st.title("AI-Powered Yoga Guidance")


st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #fffeed; }
    html, body, [class*="st-"] { color: black !important; }

    /* Fix buttons */
    button {
        background-color: #ff5555 !important;  
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    button:hover { background-color: #ff2222 !important; }

    /* Fix input fields */
    textarea, input, select {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
    }

    /* Improve dropdown menu */
    div[data-baseweb="select"] {
        background-color: white !important; /* Ensuring dropdown has a white background */
        color: black !important;
    }

    /* Fix dropdown options */
    div[data-baseweb="select"] > div {
        background-color: white !important; /* Light background */
        color: black !important;
        border: 1px solid black !important;
    }

    /* Ensure options in dropdown are readable */
    div[data-baseweb="menu"] {
        background-color: white !important;
        border: 1px solid black !important;
    }
    
    div[data-baseweb="menu"] li {
        background-color: white !important;
        color: black !important;
        padding: 8px;
    }

    div[data-baseweb="menu"] li:hover {
        background-color: #f0f0f0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize session state variables
if "selected_pose" not in st.session_state:
    st.session_state.selected_pose = "Child’s Pose"  # Set a default pose

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 0

# Initialize session state
if "chat_step" not in st.session_state:
    st.session_state.chat_step = 0
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Initialize safe and unsafe poses in session state
if "safe_poses" not in st.session_state:
    st.session_state.safe_poses = [
        "Child’s Pose", "Bound Angle Pose", "Cat-Cow Pose",
        "Downward Facing Dog Pose", "Mountain Pose", "Angle Pose"
    ]
if "unsafe_poses" not in st.session_state:
    st.session_state.unsafe_poses = ["Example Unsafe Pose 1", "Example Unsafe Pose 2"]

# Step 0: Welcome Message + Food & Water Precautions
if st.session_state.chat_step == 0:
    with st.chat_message("assistant"):
        st.write("Welcome to your AI Yoga Guide! Let's begin.")
        
        st.write("### 🍎 Food & Water Precautions")
        st.write("- Avoid eating heavy meals 2-3 hours before yoga.")
        st.write("- Stay hydrated, but avoid drinking too much water just before the session.")
        st.write("- Light snacks (fruits, nuts) are okay 30 minutes before yoga.")
        
        if st.button("Start Chat"):
            st.session_state.chat_step = 1
            st.rerun()


# Step 1: Ask for yoga level
if st.session_state.chat_step == 1:
    with st.chat_message("assistant"):
        st.write("What is your level in yoga?")
        yoga_level = st.selectbox("Choose your level:", ["Beginner", "Intermediate", "Advanced", "No Idea"])
        if st.button("Submit"):
            st.session_state.user_data["yoga_level"] = yoga_level
            st.session_state.chat_step = 2
            st.rerun()

# Step 2: Show beginner videos if applicable
if st.session_state.chat_step == 2:
    with st.chat_message("assistant"):
        if st.session_state.user_data["yoga_level"] in ["Beginner", "No Idea"]:
            st.write("Since you're a beginner, here are some easy poses to start with:")
            st.video("https://www.youtube.com/watch?v=NYhH8Gr35cI")  # Mountain Pose
            st.video("https://www.youtube.com/watch?v=y39PrKY_4JM")  # Cat-Cow Pose
            st.video("https://www.youtube.com/watch?v=eqVMAPM00DM")  # Child's Pose
        else:
            st.write("You're experienced! Let's move on.")
        if st.button("Next"):
            st.session_state.chat_step = 3
            st.rerun()

# Step 3: Collect User Information
if st.session_state.chat_step == 3:
    with st.chat_message("assistant"):
        st.write("Before we start, let's check some health precautions.")

    if "age" not in st.session_state.user_data:
        age = st.text_input("Enter your age:", key="age_input")
        if age:
            st.session_state.user_data["age"] = age
            st.rerun()
    elif "injuries" not in st.session_state.user_data:
        injuries = st.text_area("List any injuries (if any):", key="injury_input")
        if st.button("Next"):
            st.session_state.user_data["injuries"] = injuries
            st.rerun()
    elif "medical_conditions" not in st.session_state.user_data:
        conditions = st.multiselect(
            "Do you have any medical conditions?",
            ["None", "Pregnancy", "Sciatica", "Herniated Disc", "Hypertension", "Arthritis"],
            key="medical_condition_input"
        )
        if st.button("Next"):
            st.session_state.user_data["medical_conditions"] = conditions
            st.rerun()

    elif "sub_conditions" not in st.session_state.user_data:
        sub_conditions = {}
        if "Hypertension" in st.session_state.user_data["medical_conditions"]:
            sub_conditions["Hypertension"] = st.selectbox(
                "Which type of Hypertension do you have?",
                ["Essential Hypertension", "Secondary Hypertension"],
                key="hypertension_sub"
            )
        if "Sciatica" in st.session_state.user_data["medical_conditions"]:
            sub_conditions["Sciatica"] = st.selectbox(
                "What kind of Sciatica do you have?",
                ["Acute Sciatica", "Chronic Sciatica"],
                key="sciatica_sub"
            )
        if "Herniated Disc" in st.session_state.user_data["medical_conditions"]:
            sub_conditions["Herniated Disc"] = st.selectbox(
                "Which region is affected?",
                ["Cervical Herniation (Neck)", "Lumbar Herniation (Lower Back)"],
                key="herniated_sub"
            )
        if st.button("Submit Health Info"):
            st.session_state.user_data["sub_conditions"] = sub_conditions
            st.session_state.chat_step = 4
            st.rerun()

# Step 5: Select Yoga Pose and Display Precautions
if st.session_state.chat_step == 4:
    st.write("### Safe & Unsafe Poses Based on Your Condition")

    # Define initial safe poses
    all_poses = {
        "Child’s Pose": True,
        "Bound Angle Pose": True,
        "Cat-Cow Pose": True,
        "Downward Facing Dog Pose": True,
        "Mountain Pose": True,
        "Angle Pose": True,
    }

    # Retrieve user medical conditions and injuries
    conditions = st.session_state.user_data.get("medical_conditions", [])
    injuries = st.session_state.user_data.get("injuries", [])

    # Apply Restrictions
    if "Pregnancy" in conditions:
        all_poses["Child’s Pose"] = False
        all_poses["Downward Facing Dog Pose"] = False
        all_poses["Angle Pose"] = False
    if "Sciatica" in conditions:
        all_poses["Bound Angle Pose"] = False
    if "Herniated Disc" in conditions:
        all_poses["Bound Angle Pose"] = False
    if "Hypertension" in conditions:
        all_poses["Child’s Pose"] = False
        all_poses["Downward Facing Dog Pose"] = False
    if "Arthritis" in conditions:
        all_poses["Bound Angle Pose"] = False

    # Injury-based restrictions
    if "knee" in injuries:
        all_poses["Child’s Pose"] = False
        all_poses["Angle Pose"] = False
    if "wrist" in injuries:
        all_poses["Downward Facing Dog Pose"] = False
        all_poses["Cat-Cow Pose"] = False

    # Filter safe and unsafe poses
    safe_poses = [pose for pose, is_safe in all_poses.items() if is_safe]
    unsafe_poses = [pose for pose, is_safe in all_poses.items() if not is_safe]

    # Store safe poses in session state
    st.session_state.safe_poses = safe_poses

    st.write("✅ **Safe Poses:**", ", ".join(safe_poses) if safe_poses else "None available")
    st.write("🚫 **Unsafe Poses:**", ", ".join(unsafe_poses) if unsafe_poses else "None available")

    # Ensure session state is initialized before the widget
    if "selected_pose" not in st.session_state:
        st.session_state.selected_pose = safe_poses[0] if safe_poses else ""

    # Assign selectbox value directly to session state using key
    if safe_poses:
        selected_pose = st.selectbox("Choose a pose to perform:", safe_poses, key="selected_pose")
    else:
        st.write("No safe poses available based on your conditions. Please consult a professional.")

    if st.button("Show Pre-Asana Precautions") and safe_poses:
        st.session_state.chat_step = 5  # Move to the next step
        st.rerun()

# Step 6: Display Pre-Asana Precautions
if st.session_state.chat_step == 5 and st.session_state.selected_pose:
    pose = st.session_state.selected_pose

    precautions = {
        "Child’s Pose": [
            "Avoid if you have knee injuries or severe back pain.",
            "People with high blood pressure should avoid keeping their head too low.",
        ],
        "Bound Angle Pose": [
            "If you have a hip injury, avoid pressing the knees too hard.",
            "People with lower back pain should sit with support under the hips.",
        ],
        "Cat-Cow Pose": [
            "Avoid if you have a neck injury or pain.",
            "People with herniated discs should avoid deep backbends.",
        ],
    }

    st.write(f"### ✅ Pre-Asana Precautions for {pose}:")
    for point in precautions.get(pose, ["No specific precautions available."]):
        st.write(f"- {point}")

    if st.button("Lets start the streches and yoga pose"):
        st.session_state.chat_step = 6
        st.rerun()

# Step 7: Warm-up Stretches (Common for all levels)
if st.session_state.chat_step == 6:
    st.write("### 🏃 Warm-Up Stretches")
    st.video("https://www.youtube.com/watch?v=2q3HwR-HILc")  # General Warm-up Stretches
    st.video("https://www.youtube.com/watch?v=DCQwQYRwBWE")  # Neck & Shoulder Warm-up
    st.video("https://www.youtube.com/watch?v=IMzxosIffag")  # Spinal & Full Body Warm-up

    if st.button("Proceed to Yoga Pose"):
        st.session_state.chat_step = 7
        st.rerun()

# Step 8: Show final yoga session videos
if st.session_state.chat_step == 7:
    with st.chat_message("assistant"):
        st.write("You're all set! Follow along with your personalized yoga session:")

        pose_videos = {
            "Child’s Pose": "https://www.youtube.com/watch?v=eqVMAPM00DM",
            "Bound Angle Pose": "https://www.youtube.com/watch?v=B6tb4TncKhY",
            "Cat-Cow Pose": "https://www.youtube.com/watch?v=y39PrKY_4JM",
            "Downward Facing Dog": "https://www.youtube.com/watch?v=j97SSGsnCAQ",
            "Mountain Pose": "https://www.youtube.com/watch?v=NYhH8Gr35cI",
            "Angle Pose": "https://www.youtube.com/watch?v=0lfzG9jH6cM"
        }

        # Retrieve safe poses from session state
        safe_poses = st.session_state.get("safe_poses", [])
        
        for pose, url in pose_videos.items():
            if pose in safe_poses:
                st.write(f"### {pose}")
                st.video(url)

        st.write("Enjoy your session! 😊")