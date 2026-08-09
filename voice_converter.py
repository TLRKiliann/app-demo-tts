from pocket_tts import TTSModel, export_model_state
import sys

try:
    model = TTSModel.load_model("french_24l")
    print(f"✅ Loading model success!")
except Exception as e:
    print(f"Error while loading model: {e}")
    sys.exit(1)

try:
    model_state = model.get_state_for_audio_prompt("test.wav")
    print(f"✅ Get state for audio succes!")
except Exception as e:
    print(f"Error get state audio: {e}")
    sys.exit(1)

try:
    export_model_state(model_state, "./test.safetensors")
    print(f"✅ Export model state success!")
except Exception as e:
    print(f"Error during model exportation: {e}")
    sys.exit(1)


print("✅ test.safetensors generated !")
