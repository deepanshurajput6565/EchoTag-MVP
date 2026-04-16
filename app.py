import streamlit as st
import requests

# Set up the page
st.set_page_config(page_title="EchoTag Capture Engine", page_icon="🛡️", layout="centered")

st.title("🛡️ EchoTag: Digital Asset Protection")
st.write("Upload a suspected pirated video frame below. The system will scan for cryptographic watermarks and use AI semantic fallback if the tag is scrambled.")

# File Uploader
uploaded_file = st.file_uploader("Upload Image/Frame", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Target Media", use_container_width=True)
    
    if st.button("Scan Media for Piracy", type="primary"):
        with st.spinner("Initiating EchoTag Webhook..."):
            
            # Send the file to your FastAPI backend
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                response = requests.post("https://echotag-api.onrender.com/api/scan-image", files=files)
                data = response.json()
                
                # Handle the Response visually
                if data.get("status") == "piracy_detected":
                    st.error("🚨 CONFIRMED PIRACY DETECTED")
                    st.success(f"**Action Triggered:** {data['action_triggered']}")
                    st.info(f"**Detection Method:** Cryptographic Watermark")
                    st.code(f"Payload Extracted: {data['payload_extracted']}")
                    
                elif data.get("status") == "piracy_suspected":
                    st.warning("⚠️ SUSPECTED PIRACY DETECTED")
                    st.success(f"**Action Triggered:** {data['action_triggered']}")
                    st.info(f"**Detection Method:** Gemini Semantic Fallback")
                    st.write(f"**AI Analysis:** {data['ai_analysis']}")
                    
                else:
                    st.success("✅ Media is Clean")
                    st.write(data.get("message", "No piracy detected."))
                    
            except requests.exceptions.ConnectionError:
                st.error("Backend server is offline! Make sure your FastAPI server is running on port 8000.")