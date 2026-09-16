# 🎤 Demo tts (text to speech)

Ce projet d'utilisation de `pocket-tts` sur `Raspberry Pi 5`.

[https://github.com/kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts)

---

## 🚀 Utilisation

App :snake: => **cloner_fr.py** ("french_24l")

- commande de base :

```
pocket-tts generate --quantize --language french_24l --text "le texte ici..." --voice test.safetensors --temperature 0.7 --lsd-decode-steps 5 --output-path new.wav
```

- Voir les différentes options:

`pocket-tts generate --help`

- Paramètres

```
python3 voice_cloner.py ma_voix_originale.wav \
    --quantize # optimise par défaut dans ce fichier
    --text "Some words here..." \
    --language french_24l \
    --temperature 0.7 \
    --lsd-steps 5 \
    --output ./mon_audio.wav \
```

---

- cloner_fr.py

```
# Lancer un clone (génère un fichier .safetensors)
python3 cloner_fr.py clone fichier.wav

# Lancer une synthèse vocale (utilisation de fichier.safetensors)
python3 cloner_fr.py generate fichier.safetensors -t "Mon petit texte à générer..." -o output.wav
```

---

## Optimisation

Grâce à ce lien: [https://podcast.adobe.com/en/enhance](https://podcast.adobe.com/en/enhance) 
l'échantillon vocal de base peut être nettoyé et l'option `--quantize` vient optimiser la qualité du rendu.

- `quantize` permet d'améliorer la qualité du rendu audio grâce à `int8`.
- `temperature 0.7` permet d'améliorer le timbre de la voix (émotion).
- `lsd_decode_steps 5` améliore le traitement de la synthèse vocale.

## ✨ Générer une voix clonée avec le server

```
# Default params => localhost:8000
pocket-tts serve --language french_24l

# Autrement
pocket-tts serve --host "localhost" --port 8080 --language french_24l
```

---

## 📦 Installation

J'utilise `pip` ci-dessous pour les installations, mais vous pouvez vérifier avec :

`pip -V` 

Si `pip` pointe vers `pyhton3` c'est bon, sinon utilisez `pip3`, plus moderne et sans ambiguïté.

### Installation complète

```
python3 -m venv pocket_env

source pocket_env/bin/activate

# To fix on CPU
pip install torch torchao --index-url https://download.pytorch.org/whl/cpu
```

`pip install pocket-tts or pocket-tts[quantize]` (voir ci-dessous)

```
# ⚠️ Version of PyTorch 2.10+ required ⚠️
pip install pocket-tts[quantize] # Améliore la qualité !!!

torch==2.14.0+cpu
torchao==0.18.0+cpu

# To verify
python -c "import pocket_tts; print('OK')"

pip list
pip show torch
pip show torchao

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

## 🎛️ Options et paramètres

[https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/](https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/)

```
	pocket-tts generate 
		--text "Some words here..."
		--voice "untitled_fr.safetensors" 
		--language french_24l
		--temperature 0.7
		--lsd-decode-steps 5
		--eos-threshold -4.0
		--frames-after-eos 5
		--output-path ./last_test.wav
```

**⚡ Defaults options**

`pocket-tts generate --help`

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

`pip uninstall -y torch torchao pocket-tts`

---

## 🙏 Special thanks to :

```
# Authors
Manu Orsini*, Simon Rouard*, Gabriel De Marmiesse*, Václav Volhejn, Neil Zeghid>
```

---

Enjoy it !

koala :koala:
