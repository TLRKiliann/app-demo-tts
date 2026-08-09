# 🎤 Demo tts (text to speech)

Ce projet démontre la puissance de `pocket-tts`. 

[https://github.com/kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts)

---

## 🚀 Utilisation

App :snake: => **converter.py + faster_loading.py**

On peut générer un fichier au format `.safetensors` avec le fichier `converter.py`.
C'est ce qui prend le plus de temps. Ensuite, on peut lancer le fichier `faster_loading.py`.

```
python3 converter.py

python3 faster_loading.py
```

---

App :snake: => **voice_cloner.py**

Fichier python maléable à souhait pour optimiser une voix clonée en fonction des besoins.

Le fichier `voice_cloner` en python permet d'optimiser la qualité de la voix clonée, 
grâce aux différentes options de la commande de pocket-tts :

`pocket-tts generate --quantize --text "text" --voice "file.safetensors" --language french_24l --temperature 0.5 --lsd-decode-steps 5 --output-path" result.wav`

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

## ✨ To generate with server

```
# Default params => localhost:8000
pocket-tts serve --language french_24l

# Otherwise
pocket-tts serve --host "localhost" --port 8080 --language french_24l
```

---

## 📦 Install

J'utilise `pip` ci-dessous pour les installations, mais vous pouvez vérifier avec :

`pip -V` 

Si `pip` pointe vers `pyhton3` c'est bon, sinon utilisez `pip3`, plus moderne et sans ambiguïté.

### Simple installation

```
python3 -m venv pocket_env

source pocket_env/bin/activate

git clone https://github.com/TLRKiliann/app-demo-tts.git

pip install -r requirements.txt
```

---

### Complete installation

```
python3 -m venv pocket_env

source pocket_env/bin/activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install pocket-tts

# ⚠️ Version of PyTorch 2.10+ ⚠️
pip install pocket-tts[quantize]

# To verify
python -c "import pocket_tts; print('OK')"

# Freeze requirements
pip freeze > requirements.txt
```

---

## 🤗 Huggingface

- On a besoin de huggingface pour pour se logger avant de cloner sa voix ! (gratuit)

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

## 🎛️ Params

[https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/](https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/)

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

**⚡ Defaults options**

- Quelle longeur de texte assure un rendu optimal avec Pocket TTS ? 

> 1-3 phrases (100-255 caracters)

- Quelle durée d'enregistrement assure un clonage de voix optimal avec Pocket TTS ?

> 20-30 sec (clean & without noise)

    --config CONFIG_PATH: Path to custom config.yaml (for loading local model files). 
      Incompatible with --language.

    --lsd-decode-steps LSD_DECODE_STEPS: Number of generation steps (default: 1)

    --temperature TEMPERATURE: Temperature for generation (default: 0.7)

    --noise-clamp NOISE_CLAMP: Noise clamp value (default: None)

    --eos-threshold EOS_THRESHOLD: EOS threshold (default: -4.0)

    --frames-after-eos FRAMES_AFTER_EOS: Number of frames to generate after EOS 
      (default: None, auto-calculated based on the text length). Each frame is 80ms.

---

## 🗑️ Uninstall

`pip uninstall -y torch torchvision torchaudio pocket-tts torchao`

---

## 🙏 Special thanks to :

```
# Authors
Manu Orsini*, Simon Rouard*, Gabriel De Marmiesse*, Václav Volhejn, Neil Zeghid>
```

---

Enjoy it !

koala :koala:
