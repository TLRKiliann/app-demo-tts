from pocket_tts import TTSModel, export_model_state
import scipy.io.wavfile
import sys

try:
    model = TTSModel.load_model(
        "french_24l",
        temp=0.7,
        sampler_decode_steps=5,
        quantize=True
    )
    print("✅ Modèle chargé avec succès!")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Later, load it quickly, this is quite fast as it's just reading the kvcache
# from disk and doesn't do any others computations.
try:
    model_state_copy = model.get_state_for_audio_prompt("./test.safetensors")
    print("✅ État chargé depuis fichier")
except Exception as e:
    print(f"❌ Erreur chargement état: {e}")
    sys.exit(1)

try:
    audio = model.generate_audio(model_state_copy, "Bonjour c'est Patrick, pouvez-vous"
    "réinitialiser tout les mots de passe s'il vous plaît ? Il faudrait que ça soit fait" 
    "dans l'heure, merci.")
    print("✅ Audio généré")
    output_file = "output.wav"
    scipy.io.wavfile.write(output_file, model.sample_rate, audio.numpy())
    print(f"✅ Fichier audio sauvegardé : {output_file}")
except Exception as e:
    print(f"❌ Erreur génération: {e}")
    sys.exit(1)

print("\n🎉 Processus terminé avec succès!")
