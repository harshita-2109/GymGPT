from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(input_prompt, user_data):
    response = model.generate_content([input_prompt, user_data])
    return response.text

def user_data_combine_input_prompt(name, goal, weight, height, food, age, gender):
    text = (f"Hi I am {name}, I’m a {age}-year-old {gender}, {height} cm tall, weighing {weight} kg. "
            f"I want to {goal} and maintain a balanced diet. I prefer {food} food. "
            "Please provide a detailed and accurate response based on my info. "
            "If I withheld dietary preference or training style, IGNORE IT and carry on with a generic response. "
            "Do not give me any extra info, just respond as the trainers or a mix of trainers and give the workout plan "
            "and the philosophy along with some things to research if needed and quotes from the trainers if there are any. "
            "Be extremely detailed and straight to the point.")
    return text

input_prompt = """
You are an AI Nutritionist, designed to provide personalized dietary advice, meal plans, and nutritional information to users. Your goal is to help users achieve their health and wellness goals through proper nutrition.
Calculate the calories intake he/she required according to their body and health goals. Give the diet plan for 1 week by indicating calories each food item required. 
Tasks:
Personalized Dietary Advice:
Collect and analyze user information such as name, weight, height, age, gender, dietary preferences, and health goals.
Provide customized dietary recommendations based on the user's profile and goals.
Meal Planning:
Create balanced and nutritious meal plans tailored to the user's preferences and dietary needs.
Suggest recipes based on whether the user is veg or non-veg, portion sizes, and shopping lists.
Nutritional Information:
Offer detailed information about the nutritional content of various foods.
Explain the benefits of different nutrients and how they contribute to health.
Interaction Style:
Empathetic and Supportive: Show understanding and support for users' challenges and goals.
Clear and Informative: Provide information in a clear, concise, and easy-to-understand manner.
Encouraging: Motivate users to adopt healthier eating habits and stay on track with their goals.
Respectful of Preferences: Always respect users' dietary preferences, restrictions, and cultural considerations.
Example Interaction:
response should be in the given manner
User Query:
"Hi I am Harshita, I’m a 30-year-old woman, 5'6" tall, weighing 50 kg. I want to lose 10 pounds and maintain a balanced diet. I prefer vegetarian food. Can you help me with a meal plan?"
AI Response:
"Hello Harshita! I'd be happy to help you achieve your weight loss and dietary goals. Based on your information, I’ll create a personalized vegetarian meal plan for you. It will focus on providing balanced nutrition while promoting weight loss. Let's start with some questions to fine-tune your plan:
Meal plan:
Breakfast: Greek yogurt with honey and mixed berries.
Morning Snack: A handful of almonds.
Lunch: Quinoa salad with chickpeas, tomatoes, cucumbers, and a lemon-tahini dressing.
Afternoon Snack: Apple slices with almond butter.
Dinner: Stir-fried tofu with broccoli, bell peppers, and a gluten-free soy sauce.
I'll also provide recipes and a shopping list for each day, just let me know!
Use suitable emojis in the whole response to motivate the user.
"""

####### Streamlit initialization ########
st.set_page_config(
    page_title="Nutritionist Doctor",
    page_icon="🧑‍⚕️",
    layout="centered",
)

st.sidebar.image("doctor.png", use_column_width=True)
# Set up the sidebar inputs
st.sidebar.header("User details window")

# Input box for the name
name = st.sidebar.text_input("Name")

# User Input for Workout Goals
goal = st.sidebar.selectbox('Choose Your Fitness Goal', ['Weight Loss', 'Muscle Gain', 'Maintenance'])

# Number input for weight
weight = st.sidebar.number_input("Weight (kg)", format="%.2f")

# Number input for height
height = st.sidebar.number_input("Height (cm)", min_value=0, max_value=250, step=1)

# Select box for gender
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

# Select box for food preference
food = st.sidebar.selectbox("Food Preference", ["Veg", "Non-veg", "Vegan"])

# Number input for age
age = st.sidebar.number_input("Age", min_value=0, max_value=110, step=1)

# Submit button
submit = st.sidebar.button("Give me diet plan :) ")

st.title("")
st.title('AI-Nutritionist Doctor 💪❤️ ')

st.markdown("""
Welcome to GymGPT—where your dream body isn’t built overnight, but through epic dedication. Forget quick fixes; we’re all about hard work, smart choices, and a no-nonsense attitude. 
Whether you want superhero strength or just to look awesome, we’re here to fuel your journey. Ready to embrace the grind? Let’s get started!
""")

if submit:
    # Perform actions when the submit button is pressed
    if not name or not goal or not weight or not height or not gender or not food or not age:
        st.error('Please fill all required fields (Height, Weight, Age, and Activity Level) before generating the plan.')
    else:
        user_input = user_data_combine_input_prompt(name, goal, weight, height, food, age, gender)
        response = get_gemini_response(input_prompt, user_input)
        st.write("---------------------------------------------------------------------------------------------------")
        st.markdown('---')  # This creates a horizontal line to act as a visual separator
        st.write(response)
            
    # Create a download button for the generated plan
    st.download_button(
        label="Download Your Plan",
        data=response,
        file_name="generated_plan.txt",
        mime="text/plain"
    )


st.header('')  # This will create a header with no text

# Use Markdown for a divider
st.markdown('---')  # This creates a horizontal line to act as a visual separator

st.markdown('''
    Developed by HARSHITA BHARDWAJ🤓
''')
link = 'CONNECT WITH ME : [LinkedIn](https://www.linkedin.com/in/harshita-bhardwaj-755871312/)'
st.markdown(link, unsafe_allow_html=True)
