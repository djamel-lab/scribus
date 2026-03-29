# Scribus

Transcription audio/vidéo via OpenAI Whisper API (GPT-4o Transcribe).

## Installation

```bash
git clone https://github.com/djamel-lab/scribus.git
cd scribus
pip install openai
brew install ffmpeg  # pour la compression auto des fichiers > 25MB
```

## Configuration

```bash
export OPENAI_API_KEY="sk-..."
```

## Utilisation

```bash
# Un fichier
python3 scribus.py mon-audio.m4a

# Plusieurs fichiers
python3 scribus.py audio1.m4a audio2.m4a audio3.m4a

# Tous les fichiers d'un dossier
python3 scribus.py audios/*.m4a
```

Les transcripts sont sauvegardés dans `./transcripts/`.

## Ce que ça gère automatiquement

- Compression ffmpeg si le fichier dépasse 25 MB
- Création du dossier `transcripts/` si inexistant
- Nettoyage des fichiers compressés temporaires
- Batch : traite plusieurs fichiers en une commande

## Formats acceptés

mp3, mp4, m4a, wav, webm, mpeg, mpga, oga, ogg, flac

## Coût

~0.006$/minute. Une vidéo de 15 min coûte ~9 centimes.

## Infos techniques

- **Modèle** : GPT-4o Transcribe
- **Compte** : Organisation "lina" sur platform.openai.com
- **Clé** : projet "Default project", clé `whisper-transcription`
