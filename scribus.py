#!/usr/bin/env python3
"""
Scribus — Transcription audio/vidéo via OpenAI Whisper API
Usage : python3 scribus.py fichier.m4a [fichier2.m4a ...]
Les transcripts sont sauvegardés dans le dossier ./transcripts/
"""

import subprocess, sys, os, glob
from openai import OpenAI

# Config
MODEL = "gpt-4o-transcribe"
LANGUAGE = "fr"
OUTPUT_DIR = "transcripts"
MAX_SIZE_MB = 25
COMPRESS_BITRATE = "64k"

def compresser(fichier):
    """Compresse un fichier audio > 25MB via ffmpeg."""
    nom = os.path.splitext(os.path.basename(fichier))[0]
    sortie = f"/tmp/{nom}_compressed.mp3"
    print(f"  ⚙️  Compression ({os.path.getsize(fichier) / 1048576:.1f} MB > {MAX_SIZE_MB} MB)...")
    result = subprocess.run(
        ["ffmpeg", "-i", fichier, "-b:a", COMPRESS_BITRATE, "-y", sortie],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ❌ Erreur ffmpeg : {result.stderr[:200]}")
        sys.exit(1)
    print(f"  ✅ Compressé → {os.path.getsize(sortie) / 1048576:.1f} MB")
    return sortie

def transcrire(fichier, client):
    """Transcrit un fichier audio et sauvegarde le .txt."""
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier}")
        return False

    nom = os.path.splitext(os.path.basename(fichier))[0]
    taille_mb = os.path.getsize(fichier) / 1048576
    print(f"\n📄 {nom} ({taille_mb:.1f} MB)")

    # Compression si nécessaire
    source = fichier
    if taille_mb > MAX_SIZE_MB:
        source = compresser(fichier)

    # Transcription
    print(f"  🎙️  Transcription en cours ({MODEL})...")
    with open(source, "rb") as f:
        result = client.audio.transcriptions.create(
            model=MODEL,
            file=f,
            language=LANGUAGE
        )

    # Sauvegarde
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sortie = os.path.join(OUTPUT_DIR, f"{nom}.txt")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(result.text)

    print(f"  ✅ → {sortie} ({len(result.text)} caractères)")

    # Nettoyage fichier compressé
    if source != fichier and os.path.exists(source):
        os.remove(source)

    return True

def main():
    if len(sys.argv) < 2:
        print("Scribus — Transcription audio/vidéo")
        print("Usage : python3 scribus.py fichier.m4a [fichier2.m4a ...]")
        print("        python3 scribus.py audios/*.m4a")
        print(f"\nLes transcripts sont sauvegardés dans ./{OUTPUT_DIR}/")
        sys.exit(0)

    # Expansion des wildcards (Windows compat)
    fichiers = []
    for arg in sys.argv[1:]:
        expanded = glob.glob(arg)
        if expanded:
            fichiers.extend(expanded)
        else:
            fichiers.append(arg)

    if not fichiers:
        print("❌ Aucun fichier trouvé.")
        sys.exit(1)

    # Vérifier la clé API
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Variable OPENAI_API_KEY non définie.")
        print("   export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"Scribus — {len(fichiers)} fichier(s) à transcrire")
    print(f"Modèle : {MODEL} | Langue : {LANGUAGE}")
    print(f"Sortie : ./{OUTPUT_DIR}/")

    succes = 0
    for f in sorted(fichiers):
        if transcrire(f, client):
            succes += 1

    print(f"\n{'='*40}")
    print(f"Terminé : {succes}/{len(fichiers)} transcrit(s)")

if __name__ == "__main__":
    main()
