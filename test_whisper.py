
from faster_whisper import WhisperModel

print("Loading Faster-Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Speech recognition model loaded successfully!")
