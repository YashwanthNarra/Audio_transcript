import soundfile as sf
from datasets import load_dataset

print("Fetching noisy Telugu sample from Kathbath...")

# Load Kathbath dataset for Telugu in streaming mode (no full download needed)
ds = load_dataset(
    "ai4bharat/Kathbath", "te", split="test", streaming=True, trust_remote_code=True
)

# Grab the first audio sample
sample = next(iter(ds))

# Extract raw audio array and sampling rate
audio_array = sample["audio"]["array"]
sampling_rate = sample["audio"]["sampling_rate"]
transcription = sample.get("transcription", "N/A")

# Save as WAV file
sf.write("telugu_noisy_sample.wav", audio_array, sampling_rate)

print("Saved: telugu_noisy_sample.wav")
print(f"Transcript: {transcription}")