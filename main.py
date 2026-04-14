from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from dotenv import load_dotenv
from google import genai

# Load the secret API key from your .env file
load_dotenv()

# The new SDK automatically detects the GEMINI_API_KEY in your environment
client = genai.Client()

# Import your working decoder function
from decode import decode

app = FastAPI(title="EchoTag Smart Capture API")

@app.post("/api/scan-image")
async def scan_image(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # STEP 1: Try finding the invisible Echo-Tag watermark
        try:
            secret_message = decode(temp_file_path)
            return {
                "status": "piracy_detected",
                "detection_method": "invisible_watermark",
                "payload_extracted": secret_message,
                "action_triggered": "Automated ad-revenue routing initiated."
            }
            
        except ValueError:
            # STEP 2: Watermark destroyed or missing. Trigger Gemini AI Fallback!
            print("Watermark not found. Triggering Gemini Semantic Fallback...")
            
            # Upload the image using the new SDK
            sample_file = client.files.upload(file=temp_file_path)
            
            # Ask Gemini to analyze the scene
            prompt = "Analyze this image. Does it appear to be a professional sports broadcast? Answer with 'YES' or 'NO' and provide a 1-sentence reason."
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[sample_file, prompt]
            )
            analysis = response.text.strip()
            
            # Clean up the file from Google's servers
            client.files.delete(name=sample_file.name)
            
            if "YES" in analysis.upper():
                return {
                    "status": "piracy_suspected",
                    "detection_method": "semantic_ai_fallback",
                    "ai_analysis": analysis,
                    "action_triggered": "Flagged for manual review."
                }
            else:
                return {
                    "status": "clean",
                    "message": "No watermark found, and AI confirmed no sports broadcast detected."
                }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)