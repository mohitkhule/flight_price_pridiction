import streamlit as st
import pickle, base64
import pandas as pd
import sqlite3
from PIL import Image

# Database setup
def init_db():
    conn = sqlite3.connect("flight_predictions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_stops INTEGER,
            journey_day INTEGER,
            journey_month INTEGER,
            dep_hour INTEGER,
            dep_min INTEGER,
            arrival_hour INTEGER,
            arrival_min INTEGER,
            dur_hour INTEGER,
            dur_min INTEGER,
            airline TEXT,
            source TEXT,
            destination TEXT,
            passenger_count TEXT,
            cabin_class TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Load the trained model
model = pickle.load(open("flight_rf.pkl", "rb"))

# Custom CSS for styling and animations
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .header {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #00ffcc;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px #000000;
            animation: fadeIn 2s ease-in-out;
        }
        .sub-header {
            text-align: center;
            font-size: 24px;
            color: #cccccc;
            margin-bottom: 40px;
            animation: slideIn 1.5s ease-in-out;
        }
        .stImage {
            display: block;
            margin: 0 auto;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 255, 204, 0.3);
            animation: zoomIn 1s ease-in-out;
        }
        .form-container {
            background-color: rgba(30, 30, 30, 0.9);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 255, 204, 0.3);
            margin-bottom: 20px;
            animation: fadeIn 1.5s ease-in-out;
        }
        .stButton>button {
            background-color: #00ffcc;
            color: #000000;
            font-size: 18px;
            font-weight: bold;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00ccaa;
        }
        
        .stSelectbox>div>div>select {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 8px;
        }
        .stDateInput>div>div>input {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 8px;
        }
        .stTimeInput>div>div>input {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 8px;
        }
        .stDataFrame {
            background-color: #1e1e1e;
            color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 255, 204, 0.3);
        }
        .stSuccess {
            background-color: #00ffcc;
            color: #000000;
            border-radius: 8px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        @keyframes zoomIn {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(30, 30, 30, 0.9);
            border-radius: 15px;
            margin-top: 40px;
            animation: fadeIn 2s ease-in-out;
        }
        .footer a {
            color: #00ffcc;
            text-decoration: none;
            margin: 0 10px;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .aviation-section {
            background-color: rgba(30, 30, 30, 0.9);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 255, 204, 0.3);
        }
        .aviation-section img {
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .aviation-section h2 {
            color: #00ffcc;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .aviation-section p {
            color: #cccccc;
            font-size: 18px;
            line-height: 1.6;
        }
        .video-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }
        .video-container video {
            min-width: 100%;
            min-height: 100%;
            object-fit: cover;
        }
        .main-content {
            position: relative;
            z-index: 1;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1); /* Light overlay for readability */
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to generate HTML for embedding a background video
def get_video_html(video_path):
    with open(video_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode()

    return f"""
    <div>
    <div class="video-container">
        <video autoplay loop muted>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
    </div>
    </div>
    """

# Path to video
video_path = r"C:\Users\mohit\FLIGHT PRICE PREDICTION\image\3612113-hd_1920_1080_30fps.mp4"

# Inject video background
st.markdown(get_video_html(video_path), unsafe_allow_html=True)

# UI Enhancements
st.image(r"C:\Users\mohit\FLIGHT PRICE PREDICTION\image\DALL·E 2025-03-10 20.10.46 - A professional airline logo with a modern and sleek design, featuring a blue and white color scheme with a flying airplane icon and the name 'SkyWings.webp", use_container_width=True)
st.markdown('<div class="header">✈️ Ready to Take Off?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Experience the future of flight booking with SkyWings.</div>', unsafe_allow_html=True)

# Aviation Trip Section
st.markdown('<div class="aviation-section">', unsafe_allow_html=True)
st.markdown('<h2>✈️ Soar Through the Skies with SkyWings</h2>', unsafe_allow_html=True)
st.image(r"C:\Users\mohit\FLIGHT PRICE PREDICTION\image\d.webp", use_container_width=True)
st.markdown("""
    <p>
        At SkyWings, we believe that every journey should be extraordinary. Whether you're flying for business or leisure, 
        our state-of-the-art aircraft and world-class service ensure a seamless and luxurious experience. 
        From the moment you step on board, you'll be immersed in comfort and elegance, soaring above the clouds 
        with unparalleled views of the world below.
    </p>
    <p>
        Our commitment to excellence extends beyond the skies. With SkyWings, you're not just booking a flight – 
        you're embarking on an adventure. Let us take you to new heights, where the journey is as memorable as the destination.
    </p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Flight Details Form
with st.form("flight_details_form"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From", [ "Delhi", "Kolkata", "Mumbai", "Chennai"])
    with col2:
        destination = st.selectbox("To", [ "Delhi", "New_Delhi", "Hyderabad", "Kolkata"])
    
    col3, col4 = st.columns(2)
    with col3:
        dep_date = st.date_input("Departure Date")
    with col4:
        dep_time = st.time_input("Departure Time")
    
    col5, col6 = st.columns(2)
    with col5:
        arr_date = st.date_input("Arrival Date")
    with col6:
        arr_time = st.time_input("Arrival Time")
    
    Total_stops = st.selectbox("Total Stops", [0, 1, 2, 3, 4])
    airline = st.selectbox("Airline", [
        "Jet Airways", "IndiGo", "Air India", "Multiple carriers", "SpiceJet",
        "Vistara", "GoAir", "Multiple carriers Premium economy", "Jet Airways Business",
        "Vistara Premium economy", "Trujet"
    ])
    
    passenger_count = st.selectbox("Passenger", ["1 Adult", "2 Adults", "3 Adults", "4 Adults"])
    cabin_class = st.selectbox("Cabin Class", ["Economy", "Business", "First Class"])
    
    if st.form_submit_button("Show Flight"):
        st.markdown('</div>', unsafe_allow_html=True)
        dep_datetime = pd.Timestamp.combine(dep_date, dep_time)
        arr_datetime = pd.Timestamp.combine(arr_date, arr_time)
        if arr_datetime <= dep_datetime:
            st.error("Arrival time must be after departure time!")
            st.stop()
        
        duration = arr_datetime - dep_datetime
        dur_hour = duration.seconds // 3600
        dur_min = (duration.seconds % 3600) // 60

        airlines_map = {name: [int(i == j) for i in range(11)] for j, name in enumerate([
            "Jet Airways", "IndiGo", "Air India", "Multiple carriers", "SpiceJet",
            "Vistara", "GoAir", "Multiple carriers Premium economy", "Jet Airways Business",
            "Vistara Premium economy", "Trujet"
        ])}
        airline_encoding = airlines_map.get(airline, [0] * 11)

        source_map = {city: [int(i == j) for i in range(4)] for j, city in enumerate(["NYC", "Delhi", "Kolkata", "Mumbai", "Chennai"])}
        destination_map = {city: [int(i == j) for i in range(5)] for j, city in enumerate(["Dhaka", "Delhi", "New_Delhi", "Hyderabad", "Kolkata"])}
        source_encoding = source_map.get(source, [0] * 4)
        destination_encoding = destination_map.get(destination, [0] * 5)

        features = [
            Total_stops, dep_date.day, dep_date.month, dep_time.hour, dep_time.minute,
            arr_time.hour, arr_time.minute, dur_hour, dur_min,
            *airline_encoding, *source_encoding, *destination_encoding
        ]
        # Predict the base price using the machine learning model
        prediction = model.predict([features])
        base_price = round(prediction[0], 2)  # Round base price to 2 decimal places

        # Adjust price based on passenger count
        num_adults = int(passenger_count.split()[0])  # Extract number of adults
        final_price = base_price * num_adults

        # Adjust price based on cabin class
        if cabin_class == "Business":
            final_price *= 9
        elif cabin_class == "First Class":
            final_price *= 19

        # Round the final price to 2 decimal places
        final_price = round(final_price, 2)

        # Display the final price
        print(f"Final Flight Price: ₹{final_price}")

        # Save prediction to database
        conn = sqlite3.connect("flight_predictions.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO predictions (total_stops, journey_day, journey_month, dep_hour, dep_min,
            arrival_hour, arrival_min, dur_hour, dur_min, airline, source, destination, passenger_count, cabin_class, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (Total_stops, dep_date.day, dep_date.month, dep_time.hour, dep_time.minute,
              arr_time.hour, arr_time.minute, dur_hour, dur_min, airline, source, destination, passenger_count, cabin_class, final_price))
        conn.commit()
        conn.close()
        
        st.success(f"Estimated Flight Price: ₹{final_price}")
        st.write("Your prediction has been saved to the database!")

# Show previous predictions
if st.checkbox("Show Previous Predictions"):
    conn = sqlite3.connect("flight_predictions.db")
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    st.dataframe(df)

# Footer with Company Information and Social Media Handles
st.markdown("""
    <div class="footer">
        <h3>SkyWings Airlines</h3>
        <p>✈️ Fly with Confidence, Fly with SkyWings ✈️</p>
        <p>Contact Us: support@skywings.com | +91 1234567890</p>
        <p>Follow Us: 
            <a href="#">Facebook</a> | 
            <a href="#">Twitter</a> | 
            <a href="#">Instagram</a> | 
            <a href="#">LinkedIn</a>
        </p>
    </div>
    """, unsafe_allow_html=True)