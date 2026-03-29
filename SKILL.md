---
name: scribus
description: >
  Transcrit des fichiers audio ou vidéo en texte via scribus.py (OpenAI Whisper API). Déclenche ce skill IMMÉDIATEMENT dès que l'utilisateur mentionne "transcrire", "transcription", "scribus", "audio en texte", "convertir l'audio", "transformer en texte", "retranscrire", "passer en texte", "extraire le texte de l'audio", "speech to text", "whisper", ou toute demande impliquant la conversion d'un fichier audio/vidéo en texte écrit. Produit un prompt Cowork (via claudus) ou Claude Code prêt à exécuter. Ne PAS déclencher pour la génération d'audio (utiliser NotebookLM via speed-learner), la lecture ou l'analyse de transcripts existants, ni la création de sous-titres vidéo.
---

# Scribus — Transcription audio/vidéo

## Rôle

Quand une transcription audio/vidéo est demandée, préparer un prompt d'exécution qui utilise le script `scribus.py` du repo `djamel-lab/scribus`. Le prompt est formaté pour Cowork (via la skill claudus) ou pour Claude Code selon le contexte.

## Infos techniques

- **Repo** : `djamel-lab/scribus` → cloné dans `~/scribus`
- **Script** : `scribus.py`
- **Modèle** : GPT-4o Transcribe (OpenAI)
- **Langue** : français par défaut (modifiable avec `LANGUAGE` dans le script)
- **Coût** : ~0.006$/min (~9 centimes pour 15 min)
- **Compte** : Organisation "lina" sur platform.openai.com, clé `whisper-transcription`
- **Limite** : 25 MB par fichier (compression automatique via ffmpeg)
- **Sortie** : fichiers .txt dans `./transcripts/`
- **Formats acceptés** : mp3, mp4, m4a, wav, webm, mpeg, mpga, oga, ogg, flac

## Pré-requis sur la machine

- Python 3 + package `openai` dans l'environnement virtuel `~/transcribe-env`
- ffmpeg (`brew install ffmpeg`)
- Variable d'environnement `OPENAI_API_KEY` définie
- Le repo scribus cloné dans `~/scribus`

## Clé API

La clé OpenAI est stockée dans l'ancien script `~/Downloads/transcribe.py` (hardcodée dans le code, ligne `api_key=`).

Pour la retrouver :
```
grep "api_key" ~/Downloads/transcribe.py
```

Alternative : aller sur platform.openai.com → organisation "lina" → projet "Default project" → clé `whisper-transcription`.

À terme, migrer vers un fichier `~/scribus/.env` pour éviter de la chercher à chaque fois.

## Processus

1. **Identifier les fichiers** — Demander ou déduire les noms exacts et le chemin des fichiers audio/vidéo à transcrire
2. **Vérifier le chemin** — Si le chemin est ambigu, demander. Chemins fréquents : `~/Downloads/`, `~/Formations/[nom]/audios/`
3. **Vérifier les pré-requis** — Scribus cloné ? Env Python activé ? Clé API accessible ?
4. **Construire la commande** — Avec les bons chemins de fichiers et la syntaxe batch si plusieurs fichiers
5. **Générer le prompt** — Via claudus si c'est un prompt Cowork, directement si c'est Claude Code
6. **Indiquer la sortie** — Préciser que les .txt seront dans `~/scribus/transcripts/` et proposer de les copier au bon endroit si besoin

## Prompt type — Cowork

```
Ouvre le Terminal sur le Mac et exécute ces commandes une par une.

1. source ~/transcribe-env/bin/activate
2. cd ~/scribus
3. export OPENAI_API_KEY="[CLÉ EXTRAITE DE ~/Downloads/transcribe.py]"
4. python3 scribus.py [CHEMINS COMPLETS DES FICHIERS]

Attends que chaque transcription soit terminée (✅ pour chaque fichier).
Les fichiers .txt seront dans ~/scribus/transcripts/

5. [OPTIONNEL] cp ~/scribus/transcripts/*.txt [DOSSIER CIBLE]
```

## Prompt type — Claude Code

```
source ~/transcribe-env/bin/activate
cd ~/scribus
export OPENAI_API_KEY="$(grep -oP 'api_key="[^"]+' ~/Downloads/transcribe.py | cut -d'"' -f2)"
python3 scribus.py [CHEMINS COMPLETS DES FICHIERS]
```

## Edge cases

| Situation | Action |
|-----------|--------|
| Scribus pas cloné | `git clone https://github.com/djamel-lab/scribus.git ~/scribus` |
| Env Python pas activé | `source ~/transcribe-env/bin/activate` |
| Env Python inexistant | `python3 -m venv ~/transcribe-env && source ~/transcribe-env/bin/activate && pip install openai` |
| Clé API introuvable | `grep "api_key" ~/Downloads/transcribe.py` ou aller sur platform.openai.com (orga "lina") |
| Fichier > 25 MB | Compression automatique par scribus — rien à faire |
| Fichier > 23 min | Splitter avant : `ffmpeg -i fichier.m4a -f segment -segment_time 1380 -c copy part_%02d.m4a` |
| Crédits épuisés | Recharger sur platform.openai.com ou prévenir Djamel. Budget initial $10, auto-recharge désactivée |
| ffmpeg pas installé | `brew install ffmpeg` |
| Nom de fichier avec espaces | Entourer de guillemets : `python3 scribus.py "mon fichier.m4a"` |
| Transcripts mal placés | Les .txt sortent dans `~/scribus/transcripts/`. Copier au bon endroit après |

## Intégration avec les autres skills

- **claudus** — Si la sortie est un prompt Cowork, utiliser le format claudus pour le bloc prêt à coller
- **speed-learner** — Scribus est l'outil de transcription du pipeline de formation. Speed-learner appelle scribus après la génération audio NotebookLM
- **Ne PAS confondre avec** la génération d'audio (NotebookLM) ni l'analyse de transcripts (Claude directement)

## Règles

- Toujours utiliser le script du repo `~/scribus/scribus.py`, jamais un curl brut vers l'API
- Toujours activer l'environnement Python (`source ~/transcribe-env/bin/activate`) avant d'exécuter
- Ne jamais afficher la clé API en clair dans la conversation — utiliser la commande grep pour l'extraire
- Si plusieurs fichiers, utiliser la syntaxe batch : `python3 scribus.py fichier1.m4a fichier2.m4a`
- Toujours indiquer où les transcripts atterrissent et proposer de les copier au bon endroit
