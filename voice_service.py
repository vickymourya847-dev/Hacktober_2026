
import io
import wave
from pathlib import Path

from faster_whisper import WhisperModel
from piper import PiperVoice


BASE_DIR = Path(__file__).resolve().parent

VOICE_PATH = (
    BASE_DIR
    / "voices"
    / "en_US-lessac-medium.onnx"
)

_whisper = None
_piper = None


def get_whisper():
    global _whisper

    if _whisper is None:
        _whisper = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return _whisper


def get_piper():
    global _piper

    if _piper is None:
        if not VOICE_PATH.is_file():
            raise FileNotFoundError(
                f"Piper voice not found: {VOICE_PATH}"
            )

        _piper = PiperVoice.load(
            str(VOICE_PATH)
        )

    return _piper


def transcribe_audio(audio_path):
    model = get_whisper()

    segments, info = model.transcribe(
        str(audio_path),
        beam_size=1,
        vad_filter=True
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    return {
        "text": transcript,
        "language": info.language
    }


def generate_speech(text):
    voice = get_piper()

    output = io.BytesIO()

    with wave.open(output, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    output.seek(0)
    return output.getvalue()
