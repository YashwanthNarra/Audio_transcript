from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
import time
from fastapi.responses import PlainTextResponse

from app.services.sarvam import audio_to_english
from app.services.gemini import clean_transcription

router = APIRouter()

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".flac",
    ".webm",
    ".mpeg"
}


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    # Get file extension
    extension = os.path.splitext(file.filename)[1].lower()

    # Validate extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )

    # Save temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp:

        temp.write(await file.read())
        temp_path = temp.name

    try:
        start = time.time()
        try:
            english_text = audio_to_english(temp_path)
            
        except Exception as e:
            print("Sarvam error type: ",type(e))
            print("Sarvam error! ",repr(e))
            print("Sarvam error args: ",e.args)
            raise HTTPException(
                status_code=502,
                detail="Speech translation service failed."
            )
        print("Sarvam time : ", time.time()-start)
        start = time.time()
        try:
            cleaned_text = clean_transcription(english_text)
        except Exception as e:
            print("Gemini error!",repr(e))
            raise HTTPException(
                status_code=502,
                detail="Text processing service failed."
            )

        print("Gemini time : ",time.time()-start)
        
        return {
            'Sucess': True,
            # "transcription": english_text,
            "cleaned_text": cleaned_text
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)