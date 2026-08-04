# Pocket TTS Simple Clone

Special thanks to :

`https://github.com/kyutai-labs/pocket-tts`

```
Authors
Manu Orsini*, Simon Rouard*, Gabriel De Marmiesse*, Václav Volhejn, Neil Zeghidour, Alexandre Défossez
```

## App voice_cloner.py

Fichier python maléable à souhait pour optimiser en fonction des besoins.
Le rendu en mode standard très bon.

```
# Utilisation standard
python3 voice_cloner.py ma_voix_originale.wav

# Avec un message personnalisé
python3 voice_cloner.py ma_voix_originale.wav --text "Votre nouveau message ici"

# Avec tous les paramètres
python3 voice_cloner.py ma_voix_originale.wav \
    --text "Some words here..." \
    --language french_24l \
    --temperature 0.7 \
    --lsd-steps 5 \
    --output ./mon_audio.wav \
    --keep-voice

# Processus du script
mon_fichier_original.wav           # Source audio
mon_fichier_original.safetensors   # Voice sample (improve quality)
mon_fichier_original_generated.wav # Final result
```

---

## Install

`python3 -m venv pocket_env`

`source pocket_env/bin/activate`

`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`

`pip install pocket-tts`

- To verify

`python -c "import pocket_tts; print('OK')"`

- Freeze requirements

`pip freeze > requirements.txt`

---

## Huggingface

You need to install it for making a clone of your voice !

`pip install huggingface-hub`

```
	hf auth login
	> login (presser entrer)
	# Verify
	hf auth whoami
```

`pocket-tts generate --text "Test de clonage vocal" --voice "example.wav" --language french_24l`

`aplay tts_output.wav`

---

## Params

`https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/`

```
	pocket-tts generate 
		--text "Some words here..."
		--voice "untitled_fr.safetensors" 
		--language french_24l 
		--temperature 0.5 
		--lsd-decode-steps 5 
		--eos-threshold -5.0 
		--frames-after-eos 5
		--output-path ./last_test.wav
```

## Defaults options

- Quelle longeur de texte assure un rendu optimal avec Pocket TTS ? 

- Quelle longeur de phrase assure un clonage de voix optimal avec Pocket TTS ?

    10-30sec d'enregistrement.

    --config CONFIG_PATH: Path to custom config.yaml (for loading local model files). 
      Incompatible with --language.

    --lsd-decode-steps LSD_DECODE_STEPS: Number of generation steps (default: 1)

    --temperature TEMPERATURE: Temperature for generation (default: 0.7)

    --noise-clamp NOISE_CLAMP: Noise clamp value (default: None)

    --eos-threshold EOS_THRESHOLD: EOS threshold (default: -4.0)

    --frames-after-eos FRAMES_AFTER_EOS: Number of frames to generate after EOS 
      (default: None, auto-calculated based on the text length). Each frame is 80ms.

---

## Uninstall PyTorch & Pocket TTS

`pip uninstall -y torch torchvision torchaudio pocket-tts`

---

Enjoy it !

koala :koala:
