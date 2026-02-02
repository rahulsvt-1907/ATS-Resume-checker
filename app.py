import streamlit as st
from app_extended_functionality import process_uploaded_file, get_fashion_recommendations

st.title("Fashion Stylish AI")
st.text("Get AI-powered outfit recommendations!")

uploaded_file = st.file_uploader("Upload Your Fashion Preference Document (PDF or Image)", type=["pdf", "jpg", "png"])
occasion = st.selectbox("Select the Occasion", ["Casual", "Formal", "Streetwear", "Ethinic"])
name = st.text_input("Enter Your Name (Optional)")
submit = st.button("Get Recommendations")

if submit and uploaded_file:
    user_features = process_uploaded_file(uploaded_file, name)
    if user_features:
        face_shape, skin_color, user_gender = user_features
        
        st.subheader("Detected Features:")
        st.write(f"Face Shape: {face_shape}")
        st.write(f"Skin Color: {skin_color}")
        st.write(f"Gender: {user_gender}")
        
        recommendation, hairstyle, footwear = get_fashion_recommendations(face_shape, skin_color, user_gender, occasion)
        
        st.subheader("Recommended Outfit:")
        st.write(recommendation)
        
        st.subheader("Recommended Hairstyle:")
        st.write(hairstyle)
        
        st.subheader("Recommended Footwear:")
        st.write(footwear)
