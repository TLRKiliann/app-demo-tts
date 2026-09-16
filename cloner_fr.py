#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

import scipy.io.wavfile
from pocket_tts import TTSModel, export_model_state

"""
Utilisation
1.
python3 cloner.py clone ma_voix.wav

2.
python3 cloner.py generate voix_esteban.safetensors \
    -t "Bonjour, comment allez-vous ?" \
    -o bonjour.wav
"""

DEFAULT_LANGUAGE = "french_24l"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_LSD_STEPS = 5

VALID_AUDIO_EXTENSIONS = {".wav",".mp3",".flac",".m4a",".ogg"}

def validate_audio_file(audio_path: Path) -> None:
    """Vérifie que le fichier audio existe et possède une extension valide."""

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Fichier audio introuvable : {audio_path}"
        )

    if audio_path.suffix.lower() not in VALID_AUDIO_EXTENSIONS:
        print(
            f"⚠️ Extension {audio_path.suffix} non standard."
        )

def validate_voice_file(voice_path: Path) -> None:
    """Vérifie que le fichier .safetensors existe et n'est pas vide."""

    if not voice_path.is_file():
        raise FileNotFoundError(
            f"Fichier de voix introuvable : {voice_path}"
        )

    if voice_path.stat().st_size == 0:
        raise RuntimeError(
            f"Le fichier de voix est vide : {voice_path}"
        )

def get_voice_path(audio_path: Path) -> Path:
    """Retourne le nom du fichier .safetensors correspondant à l'audio."""

    return audio_path.with_suffix(".safetensors")


def get_output_path(
    voice_path: Path, output_path: Path | None
) -> Path:
    """Détermine le chemin du fichier WAV de sortie."""

    if output_path is not None:
        return output_path

    return voice_path.with_name(
        f"{voice_path.stem}_generated.wav"
    )

def extract_voice(
    model: TTSModel, audio_path: Path,
    voice_path: Path, save_voice: bool,
) -> dict:
    """
    Extrait l'empreinte vocale du fichier audio.

    L'empreinte reste en mémoire pour la génération.
    Elle est sauvegardée en .safetensors uniquement si demandé.
    """

    print()
    print("🎤 Extraction de la voix...")
    print(f"   Source : {audio_path}")

    voice_state = model.get_state_for_audio_prompt(
        audio_path
    )

    print("✅ Empreinte vocale extraite")

    if save_voice:
        print(f"💾 Sauvegarde : {voice_path}")

        export_model_state(
            voice_state,
            str(voice_path),
        )

        validate_voice_file(voice_path)

        print(
            f"✅ Voix sauvegardée "
            f"({voice_path.stat().st_size / 1024:.1f} Ko)"
        )
    return voice_state

def load_voice(model: TTSModel, voice_path: Path) -> dict:
    """Charge une empreinte vocale .safetensors."""

    validate_voice_file(voice_path)

    print()
    print("🎤 Chargement de l'empreinte vocale...")
    print(f"   Voix : {voice_path}")

    voice_state = model.get_state_for_audio_prompt(
        voice_path
    )

    print("✅ Empreinte vocale chargée")
    return voice_state

def generate_speech(
    model: TTSModel,
    voice_state: dict,
    text: str,
    output_path: Path,
) -> None:
    """Génère un fichier WAV à partir du texte et de la voix."""

    if not text.strip():
        raise ValueError(
            "Le texte à générer est vide."
        )

    print()
    print("🔊 Génération audio...")
    print(f"   Texte       : {text}")
    print(f"   Fréquence   : {model.sample_rate} Hz")

    audio = model.generate_audio(
        model_state=voice_state,
        text_to_generate="... " + text,
        copy_state=True,
    )

    if audio.numel() == 0:
        raise RuntimeError(
            "Pocket TTS a retourné un audio vide."
        )

    print(f"   Tensor      : {tuple(audio.shape)}")
    duration = audio.shape[-1] / model.sample_rate
    print(
        f"   Durée       : {duration:.2f} secondes"
    )

    audio_np = audio.detach().cpu().numpy()
    if audio_np.ndim == 2:
        audio_np = audio_np.T
    elif audio_np.ndim != 1:
        raise ValueError(
            f"Format audio inattendu : {audio_np.shape}"
        )

    audio_np = audio_np.astype("float32", copy=False)
    scipy.io.wavfile.write(
        output_path,
        model.sample_rate,
        audio_np,
    )

    if not output_path.is_file():
        raise RuntimeError(
            f"Le fichier n'a pas été créé : {output_path}"
        )

    if output_path.stat().st_size == 0:
        raise RuntimeError(
            f"Le fichier est vide : {output_path}"
        )

    print(
        f"✅ Audio sauvegardé : {output_path} "
        f"({output_path.stat().st_size / 1024:.1f} Ko)"
    )

def create_parser() -> argparse.ArgumentParser:
    """Crée le parser argparse."""

    parser = argparse.ArgumentParser(
        description="Clonage vocal avec Pocket TTS 2.1.0"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ==========================================================
    # COMMANDE : clone
    # ==========================================================
    clone_parser = subparsers.add_parser(
        "clone",
        help="Extrait une voix depuis un fichier audio.",
    )

    clone_parser.add_argument(
        "audio_file",
        type=Path,
        help="Fichier audio contenant la voix.",
    )

    clone_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help=(
            "Nom du fichier .safetensors. "
            "Par défaut : <nom>.safetensors"
        ),
    )

    # ==========================================================
    # COMMANDE : generate
    # ==========================================================
    generate_parser = subparsers.add_parser(
        "generate",
        help="Génère un WAV avec une voix clonée.",
    )

    generate_parser.add_argument(
        "voice_file",
        type=Path,
        help=(
            "Fichier .safetensors contenant "
            "une voix clonée."
        ),
    )

    generate_parser.add_argument(
        "--text",
        "-t",
        type=str,
        required=True,
        help="Texte à transformer en parole.",
    )

    generate_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Fichier WAV de sortie.",
    )

    generate_parser.add_argument(
        "--language",
        "-l",
        type=str,
        default=DEFAULT_LANGUAGE,
        choices=["french_24l"],
        help=f"Langue (défaut : {DEFAULT_LANGUAGE})",
    )

    generate_parser.add_argument(
        "--temperature",
        "-T",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=(
            f"Température "
            f"(défaut : {DEFAULT_TEMPERATURE})"
        ),
    )

    generate_parser.add_argument(
        "--lsd-steps",
        "-s",
        type=int,
        default=DEFAULT_LSD_STEPS,
        help=(
            f"Nombre d'étapes LSD "
            f"(défaut : {DEFAULT_LSD_STEPS})"
        ),
    )
    return parser

def create_voice(args: argparse.Namespace) -> int:
    """Crée une empreinte .safetensors à partir d'un audio."""

    audio_path: Path = args.audio_file

    validate_audio_file(audio_path)

    voice_path: Path = (
        args.output
        if args.output is not None
        else get_voice_path(audio_path)
    )

    print()
    print("=" * 60)
    print("🎤 Pocket TTS — Création d'une voix clonée")
    print("=" * 60)
    print(f"📁 Audio source : {audio_path}")
    print(f"📁 Voix sortie  : {voice_path}")
    print("⚡ Quantification : INT8")
    print("=" * 60)

    print()
    print("🔄 Chargement du modèle...")

    model = TTSModel.load_model(
        language=DEFAULT_LANGUAGE,
        temp=DEFAULT_TEMPERATURE,
        lsd_decode_steps=DEFAULT_LSD_STEPS,
        quantize=True,
    )

    print("✅ Modèle chargé")

    extract_voice(
        model=model,
        audio_path=audio_path,
        voice_path=voice_path,
        save_voice=True,
    )

    print()
    print("🎉 Empreinte vocale créée !")
    print(f"🎤 Voix : {voice_path}")
    return 0

def generate_from_voice(args: argparse.Namespace) -> int:
    """Génère un fichier WAV avec une empreinte existante."""

    voice_path: Path = args.voice_file

    output_path: Path = get_output_path(
        voice_path,
        args.output,
    )

    print()
    print("=" * 60)
    print("🔊 Pocket TTS — Génération avec voix clonée")
    print("=" * 60)
    print(f"🎤 Voix          : {voice_path}")
    print(f"📁 Sortie        : {output_path}")
    print(f"🌍 Langue        : {args.language}")
    print(f"🌡️ Température   : {args.temperature}")
    print(f"🔢 LSD steps     : {args.lsd_steps}")
    print("⚡ Quantification : INT8")
    print("=" * 60)

    print()
    print("🔄 Chargement du modèle...")

    model = TTSModel.load_model(
        language=args.language,
        temp=args.temperature,
        lsd_decode_steps=args.lsd_steps,
        quantize=True,
    )

    print("✅ Modèle chargé")

    voice_state = load_voice(
        model=model,
        voice_path=voice_path,
    )

    generate_speech(
        model=model,
        voice_state=voice_state,
        text=args.text,
        output_path=output_path,
    )

    print()
    print("=" * 60)
    print("🎉 Génération terminée !")
    print("=" * 60)
    print(f"🔊 Audio : {output_path}")
    print()
    return 0

def main() -> int:
    """Point d'entrée principal du programme."""

    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.command == "clone":
            return create_voice(args)

        if args.command == "generate":
            return generate_from_voice(args)

        parser.error("Commande inconnue.")
    except (
        FileNotFoundError,
        RuntimeError,
        ValueError,
        TypeError,
        OSError,
    ) as error:
        print(f"❌ {error}")
        return 1
    except Exception as error:
        print(f"❌ Erreur inattendue : {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
