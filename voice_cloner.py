#!/usr/bin/env python3
"""
Script de clonage vocal avec Pocket TTS
Utilisation: python3 voice_cloner.py chemin/vers/ma_voix.wav
"""

import sys
import os
import argparse
from pathlib import Path
from pocket_tts import TTSModel, export_model_state

# Configuration par défaut
DEFAULT_TEXT = "Bonjour Pierette, veuillez effectuer le versement comme convenu. En vous remerciant."
DEFAULT_LANGUAGE = "french_24l"
DEFAULT_TEMPERATURE = 0.5
DEFAULT_LSD_STEPS = 5
DEFAULT_OUTPUT = "./last3_test.wav"

def validate_audio_file(file_path):
    """Vérifie que le fichier audio existe et est valide"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Fichier audio introuvable : {file_path}")

    valid_extensions = ['.wav', '.mp3', '.flac', '.m4a']
    ext = Path(file_path).suffix.lower()
    if ext not in valid_extensions:
        print(f"⚠️  Extension {ext} non standard. Assurez-vous que c'est un fichier audio valide.")

    return True

def get_output_paths(input_path):
    """Génère les noms de fichiers de sortie"""
    base_name = Path(input_path).stem
    safetensors_path = f"{base_name}.safetensors"
    wav_output = f"./{base_name}_generated.wav"
    return safetensors_path, wav_output

def export_voice(model, audio_path, output_path):
    """Exporte l'empreinte vocale depuis un fichier audio"""
    print(f"📤 Exportation de la voix depuis : {audio_path}")
    try:
        voice_state = model.get_state_for_audio_prompt(audio_path)
        export_model_state(voice_state, output_path)
        print(f"✅ Voix exportée avec succès vers : {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'exportation : {e}")
        return False

def generate_speech(voice_path, text, language, temperature, lsd_steps, output_path):
    """Génère la parole avec la voix clonée"""
    print(f"🔊 Génération de la parole...")
    print(f"   Texte : {text}")
    print(f"   Voix : {voice_path}")
    print(f"   Langue : {language}")
    print(f"   Température : {temperature}")
    print(f"   Étapes LSD : {lsd_steps}")

    # Construction de la commande
    import subprocess
    cmd = [
        "pocket-tts", "generate",
        "--quantize",
        "--text", text,
        "--voice", voice_path,
        "--language", language,
        "--temperature", str(temperature),
        "--lsd-decode-steps", str(lsd_steps),
        "--output-path", output_path
    ]

    try:
        # Exécution de la commande en filtrant NNPACK
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Filtrage des messages NNPACK
        filtered_output = '\n'.join(
            line for line in result.stdout.split('\n') 
            if "NNPACK" not in line
        )

        if result.stderr:
            filtered_error = '\n'.join(
                line for line in result.stderr.split('\n') 
                if "NNPACK" not in line
            )
            if filtered_error:
                print(f"⚠️  Messages d'erreur :\n{filtered_error}")

        if filtered_output:
            print(f"📝 Sortie :\n{filtered_output}")

        print(f"✅ Audio généré avec succès vers : {output_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False

def main():
    # Configuration du parser d'arguments
    parser = argparse.ArgumentParser(
        description="Cloneur vocal Pocket TTS - Génère de la parole avec une voix clonée",
        epilog="Exemple : python3 voice_cloner.py ma_voix.wav"
    )

    parser.add_argument(
        "audio_file",
        type=str,
        help="Chemin vers le fichier audio de la voix à cloner (WAV, MP3, FLAC, M4A)"
    )

    parser.add_argument(
        "--text", "-t",
        type=str,
        default=DEFAULT_TEXT,
        help=f"Texte à générer (défaut : '{DEFAULT_TEXT}')"
    )

    parser.add_argument(
        "--language", "-l",
        type=str,
        default=DEFAULT_LANGUAGE,
        choices=['french_24l', 'french', 'english', 'english_2026-01', 'english_2026-04', 
                 'german_24l', 'portuguese_24l', 'italian_24l', 'spanish_24l'],
        help=f"Modèle de langue (défaut : {DEFAULT_LANGUAGE})"
    )

    parser.add_argument(
        "--temperature", "-T",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Température de génération (défaut : {DEFAULT_TEMPERATURE})"
    )

    parser.add_argument(
        "--lsd-steps", "-s",
        type=int,
        default=DEFAULT_LSD_STEPS,
        help=f"Nombre d'étapes de décodage LSD (défaut : {DEFAULT_LSD_STEPS})"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Chemin de sortie pour l'audio généré (défaut : nom_original_generated.wav)"
    )

    parser.add_argument(
        "--keep-voice", "-k",
        action="store_true",
        help="Conserver le fichier .safetensors après la génération"
    )

    args = parser.parse_args()

    # Vérification du fichier audio
    try:
        validate_audio_file(args.audio_file)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # Génération des chemins de sortie
    safetensors_path, default_wav = get_output_paths(args.audio_file)
    output_wav = args.output if args.output else default_wav

    print("🚀 Démarrage du clonage vocal Pocket TTS")
    print("=" * 50)
    print(f"📁 Fichier source : {args.audio_file}")
    print(f"📁 Sortie audio : {output_wav}")
    print(f"📁 Empreinte vocale : {safetensors_path}")
    print("=" * 50)

    # Chargement du modèle
    print(f"🔄 Chargement du modèle {args.language}...")
    try:
        model = TTSModel.load_model(language=args.language)
        print("✅ Modèle chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        sys.exit(1)

    # Exportation de la voix
    if not export_voice(model, args.audio_file, safetensors_path):
        print("❌ Échec de l'exportation de la voix")
        sys.exit(1)

    # Génération de la parole
    if not generate_speech(
        safetensors_path,
        args.text,
        args.language,
        args.temperature,
        args.lsd_steps,
        output_wav
    ):
        print("❌ Échec de la génération audio")
        sys.exit(1)

    # Nettoyage (optionnel)
    if not args.keep_voice:
        try:
            os.remove(safetensors_path)
            print(f"🧹 Fichier temporaire supprimé : {safetensors_path}")
        except:
            pass

    print("=" * 50)
    print("🎉 Clonage vocal terminé avec succès !")
    print(f"📁 Audio généré : {output_wav}")
    if args.keep_voice:
        print(f"📁 Empreinte vocale conservée : {safetensors_path}")

if __name__ == "__main__":
    main()
