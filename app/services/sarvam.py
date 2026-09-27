import os
import json
import requests

from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)


def audio_to_english(audio_path: str) -> str:

    # 1. Create job
    job = client.speech_to_text_job.create_job( 
        model="saaras:v4",
        mode="translate",
        with_diarization=True, # be careful here
    )

    # 2. Upload
    print("Uploading the audio file...")

    job.upload_files(
        file_paths=[audio_path],
        timeout=300
    )

    # 3. Start
    job.start()

    # 4. Wait
    print("processing the audio file...")

    job.wait_until_complete()

    # 5. Get status
    status = client.speech_to_text_job.get_status(
        job_id=job.job_id
    )

    print("Job state:", status.job_state)

    # 6. Get output filename
    output_file = status.job_details[0].outputs[0].file_name

    print("Output file:", output_file)

    # 7. Get download URL
    download_response = client.speech_to_text_job.get_download_links(
        job_id=job.job_id,
        files=[output_file]
    )

    download_url = download_response.download_urls[
        output_file
    ].file_url

    # 8. Download JSON
    response = requests.get(download_url)
    response.raise_for_status()

    result = response.json()

    # 9. Extract transcript
    if "diarized_transcript" in result:

        entries = result["diarized_transcript"]["entries"]

        transcript_parts = []

        for entry in entries:
            speaker = f"Speaker {entry.get('speaker_id')}"
            text = entry.get("transcript", "")

            transcript_parts.append(
                f"{speaker}: {text}"
            )

        return "\n".join(transcript_parts)

    # If diarization isn't present
    return result.get("transcript", "")