# Pocket TTS Clone App

```
# Utilisation la plus simple
python3 voice_cloner.py ma_voix_originale.wav

# Avec votre message personnalisé
python3 voice_cloner.py ma_voix_originale.wav --text "Votre nouveau message ici"

# Avec tous les paramètres
python3 voice_cloner.py ma_voix_originale.wav \
    --text "Bonjour Pierette, veuillez effectuer le versement comme convenu." \
    --language french_24l \
    --temperature 0.7 \
    --lsd-steps 5 \
    --output ./mon_audio.wav \
    --keep-voice
```

```
mon_fichier_original.wav          # Votre voix source
mon_fichier_original.safetensors  # Empreinte vocale (temporaire)
mon_fichier_original_generated.wav # Résultat final
```


