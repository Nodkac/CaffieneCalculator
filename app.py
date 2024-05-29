import streamlit as st

# Define the caffeine content for different drinks
caffeine_content = {
    'Coffee': 95,
    'Espresso': 64,
    'Black Tea': 47,
    'Cola': 22,
    'Energy Drink': 80
}

def calculate_caffeine(initial_amount, hours_passed, half_life=5.5):
    return initial_amount * (0.5 ** (hours_passed / half_life))

st.title('Your Caffeine Journey')
st.markdown('**Effects of Coffee on Your Body:** Coffee increases your adrenaline levels and heart rate, activating the fight-or-flight response and keeping you more alert. It also inhibits the hormone that helps you stay calm and prepared for sleep. Therefore, coffee should be used strategically when you need to stay awake and productive after insufficient sleep...')
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('**On the other hand now that it\'s already too late, find out how much caffeine is there in your system and check if you can fall asleep or not.**')
st.markdown('<br>', unsafe_allow_html=True)

# Ask if the user is a regular coffee consumer
is_regular = st.radio("Have you been consuming coffee regularly for 5 years or more?", ('Yes', 'No'))
st.markdown('<br>', unsafe_allow_html=True)

# Set the threshold based on the user's response
caffeine_threshold = 100 if is_regular == 'Yes' else 30

# User inputs
drink_type = st.selectbox('Select your drink:', list(caffeine_content.keys()))
st.markdown('<br>', unsafe_allow_html=True)
servings = st.number_input('Enter number of servings:', min_value=1, value=1)
st.markdown('<br>', unsafe_allow_html=True)
hours_since_consumption = st.slider('Hours since consumption:', min_value=0.0, max_value=24.0, value=1.0)
st.markdown('<br>', unsafe_allow_html=True)

# Initialize session state for showing tips
if 'show_tips' not in st.session_state:
    st.session_state['show_tips'] = False

if st.button('Can I fall asleep right now?!'):
    total_remaining_caffeine = 0
    for i in range(servings):
        time_since_this_serving = hours_since_consumption - i * 3.5
        serving_caffeine = caffeine_content[drink_type]
        remaining_caffeine_this_serving = calculate_caffeine(serving_caffeine, time_since_this_serving)
        total_remaining_caffeine += remaining_caffeine_this_serving

    st.write(f'Initial caffeine intake per serving: {caffeine_content[drink_type]} mg')
    st.write(f'Total remaining caffeine from all servings: {total_remaining_caffeine:.2f} mg')

    if total_remaining_caffeine > caffeine_threshold:
        st.write("Caffeine level might disrupt your sleep based on your consumption history.")
        st.session_state['show_tips'] = False  # Reset tips state for fresh calculation
        st.session_state['show_tips_button'] = True
    else:
        st.write("Caffeine level is likely not enough to disrupt your sleep.")
        st.session_state['show_tips_button'] = False

# Conditionally display the "Need tips to reduce caffeine?" button
if 'show_tips_button' in st.session_state and st.session_state['show_tips_button']:
    if st.button('Need tips to reduce caffeine?'):
        st.session_state['show_tips'] = True

# Display the tips if the state is set
if st.session_state['show_tips']:
    st.write("To reduce or dilute the amount of caffeine in your system, you can do one of two things: drink a lot of water or exercise to use up your excess energy. And from next time, make sure you calculate beforehand to have a good night's sleep.")
