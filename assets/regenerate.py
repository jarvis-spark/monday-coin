import os
import requests, base64
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL   = "imagen-4.0-generate-001"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={API_KEY}"
OUT     = Path(__file__).parent

def gen(name, prompt, aspect="1:1"):
    print(f"Generating {name}...")
    r = requests.post(URL, json={
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": aspect}
    }, timeout=60)
    if r.status_code != 200:
        print(f"❌ {r.status_code}: {r.text[:200]}")
        return
    img = r.json()["predictions"][0]["bytesBase64Encoded"]
    (OUT / f"{name}.png").write_bytes(base64.b64decode(img))
    print(f"✅ {name}.png saved")

gen("mascot_default",
    "Cartoon raccoon mascot character for a crypto meme coin. "
    "The raccoon has very pronounced dark circles under its eyes, a permanent frown, "
    "messy bedhead fur sticking up, chubby round cute body, short stubby arms. "
    "The raccoon eye mask area is dark navy blue. Body fur is dark grey. "
    "Small crescent moon shape on left cheek. Standing pose, arms slightly out. "
    "Pure white background. Flat 2D vector cartoon illustration style. "
    "Thick black outlines. Simple, clean, meme-ready. No text. No props.",
    "1:1"
)

gen("twitter_banner",
    "Wide horizontal banner for a crypto meme coin called MONDAY on Solana. "
    "Pure dark background #0a0a0a. Left third: grumpy raccoon cartoon with dark circles "
    "holding a coffee cup. Center: giant bold text MONDAY in bright yellow. "
    "Below that: smaller white text YOU HATE IT. YOU NEED IT. "
    "Right side: yellow glow effect, scattered small coffee cup icons and moon icons. "
    "Professional clean crypto project banner. No hex codes visible. No raw color values. "
    "Finished polished design ready to use.",
    "16:9"
)

gen("mascot_rage",
    "Same cartoon raccoon mascot character: dark circles, navy eye mask, messy fur, frown. "
    "Now in RAGE pose: fists clenched, steam coming from ears, face slightly red, "
    "eyes wide open for once. Monday morning anger energy. "
    "Pure white background. Flat 2D vector cartoon style. Thick outlines. No text.",
    "1:1"
)
