import re
import glob
import pandas as pd
from itertools import count
PROTECTED_PHRASES = [
    "le marabout"
]


# ----------------------------------------
# CONFIG
# ----------------------------------------
INPUT_GLOB = "/Users/jamesgordon/Desktop/James.txt.file.corpus.mini.project_2/*.txt"

CHUNK_SIZE = 25
OVERLAP = 8
def protect_phrases(text, phrases):
    text_lower = text.lower()
    for phrase in phrases:
        protected = phrase.replace(" ", "_")
        text_lower = text_lower.replace(phrase, protected)
    return text_lower


# ----------------------------------------
# NORMALIZATION
# ----------------------------------------
def normalize_text(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"[’']", " ", text)
    text = re.sub(r"[^\w\sàâçéèêëîïôûùüÿñæœ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ----------------------------------------
# STOPWORDS
# ----------------------------------------
FRENCH_STOPWORDS = {
    "a","à","ai","aie","ainsi","alors","après","assez","au","aucun","aucune",
    "aujourd","aujourd'hui","aussi","autre","autres","aux","avant","avec",
    "avoir","ayant","bien","bon","car","ce","cela","celle","celui","ces",
    "cet","cette","ceux","chaque","chez","comme","comment","contre","dans",
    "de","dedans","dehors","depuis","des","donc","du","elle","elles","en",
    "encore","entre","est","et","été","être","eux","fait","faire","fois",
    "font","hors","ici","il","ils","je","jusque","la","le","les","leur",
    "leurs","lors","lui","mais","mes","mon","même","mêmes","ne","ni","non",
    "nos","notre","nous","on","ont","ou","où","par","pas","peu","plus",
    "pour","pourquoi","quand","que","quel","quelle","quelles","quels","qui",
    "quoi","sans","sa","se","ses","si","son","sont","sous","sur","ta","te",
    "tes","toi","ton","tous","tout","toute","toutes","très","tu","un","une",
    "vos","votre","vous","y"
}

# French clitics & particles
FRENCH_CLITICS = {
    "l", "d", "j", "m", "s", "t", "c", "n", "qu"
}

ALL_STOPWORDS = FRENCH_STOPWORDS | FRENCH_CLITICS

# ----------------------------------------
# LEMMA COLLAPSE (lightweight)
# ----------------------------------------
LEMMA_MAP = {
    "etre": "etre",
    "été": "etre",
    "etait": "etre",
    "étais": "etre",
    "etais": "etre",
    "avoir": "avoir",
    "avait": "avoir",
    "avais": "avoir"
}

def lemma_map(token):
    return LEMMA_MAP.get(token, token)

# ----------------------------------------
# TOKENIZATION + FILTERING (CRITICAL STEP)
# ----------------------------------------
def tokenize_filter(text):
    text = protect_phrases(text, PROTECTED_PHRASES)
    tokens = re.findall(r"\b\w+\b", normalize_text(text))
    tokens = [lemma_map(t) for t in tokens]
    tokens = [
        t for t in tokens
        if t not in ALL_STOPWORDS and len(t) > 1
    ]
    return tokens


# ----------------------------------------
# CHUNKING (STRUCTURE ONLY)
# ----------------------------------------
def chunk_tokens(tokens, chunk_size=200, overlap=50):
    step = chunk_size - overlap
    for i in range(0, len(tokens), step):
        chunk = tokens[i:i + chunk_size]
        if len(chunk) >= 20:
            yield chunk

# ----------------------------------------
# BUILD CANONICAL DATAFRAME
# ----------------------------------------
rows = []
chunk_id = count(start=1)

for filepath in glob.glob(INPUT_GLOB):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    tokens = tokenize_filter(raw_text)

    for chunk in chunk_tokens(tokens, CHUNK_SIZE, OVERLAP):
        rows.append({
            "chunk_id": next(chunk_id),
            "source_file": filepath.split("/")[-1],
            "tokens": chunk,
            "text": " ".join(chunk)
        })

df_chunks = pd.DataFrame(rows)

# ----------------------------------------
# SAVE CANONICAL CIV DATASET
# ----------------------------------------
df_chunks.to_csv("chunks_canonical.csv", index=False)

print(f"Saved {len(df_chunks)} chunks to chunks_canonical.csv")
print(df_chunks.head())
