"""
$MONDAY Image Generator — Imagen 4.0
Generates mascot, logo, and meme templates
"""
import os, json, base64, requests
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL   = "imagen-4.0-generate-001"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={API_KEY}"
OUT     = Path(__file__).parent

PROMPTS = {
    "mascot_default": {
        "prompt": (
            "A cute cartoon raccoon mascot with extreme dark circles under eyes, "
            "permanent tired frown, messy bedhead fur, chubby round body, holding "
            "a tiny coffee cup. The raccoon mask is dark navy blue #1A1F3C. "
            "Body fur is dark grey. Small crescent moon birthmark on left cheek. "
            "Expression: deeply unenthusiastic, Monday morning energy. "
            "Style: flat vector illustration, thick outlines, Pepe the frog level "
            "simplicity meets Pudgy Penguins cuteness. White background. "
            "Suitable as a crypto token mascot pfp."
        ),
        "aspect": "1:1"
    },
    "mascot_coffee": {
        "prompt": (
            "Same cute cartoon raccoon mascot: dark circles, navy mask #1A1F3C, "
            "messy bedhead, frown. Now holding oversized steaming coffee mug "
            "with '$MON' printed on it. Steam rising. Eyes half-open. "
            "One hand gripping mug desperately. Background: dark #0a0a0a with "
            "subtle yellow glow behind. Flat vector style, thick outlines. "
            "Crypto meme coin mascot energy."
        ),
        "aspect": "1:1"
    },
    "mascot_moon": {
        "prompt": (
            "Same cute cartoon raccoon mascot: dark circles, navy mask, messy fur. "
            "Now floating in space, riding a yellow crescent moon. Tiny smile "
            "for the first time — just slightly less miserable. Holding a flag "
            "that says '$MONDAY'. Stars in background. Yellow #FFD60A accent color. "
            "Flat vector illustration, crypto meme coin style. White background."
        ),
        "aspect": "1:1"
    },
    "token_logo": {
        "prompt": (
            "Cryptocurrency token logo for $MONDAY. Circular badge design. "
            "Dark navy background #1A1F3C inside circle. Center: stylized letter M "
            "where the two inner peaks droop down like heavy tired eyelids, "
            "bright yellow #FFD60A color. Small crescent moon hanging off "
            "the right leg of the M. The overall M looks like a sleepy face. "
            "Clean, minimal, professional. Suitable for CoinGecko listing. "
            "White outer background. Thick circular border in yellow."
        ),
        "aspect": "1:1"
    },
    "twitter_banner": {
        "prompt": (
            "Twitter/X banner image 1500x500 for $MONDAY Solana meme coin. "
            "Dark background #0a0a0a. Left side: grumpy raccoon mascot with "
            "dark circles and navy mask, holding coffee. Center: large bold text "
            "'$MONDAY' in yellow #FFD60A Bebas Neue style font. Below: smaller "
            "text 'YOU HATE IT. YOU NEED IT.' in white. Right side: Solana "
            "purple glow effect. Scattered coffee cup and moon emojis. "
            "Professional crypto project banner energy."
        ),
        "aspect": "16:9"
    },
    "meme_template_drake": {
        "prompt": (
            "Drake meme format with the $MONDAY raccoon mascot replacing Drake. "
            "Two panels stacked vertically. Top panel: raccoon looking away "
            "disgusted, pointing away. Label: 'Having a good Monday'. "
            "Bottom panel: raccoon pointing approvingly, smiling slightly. "
            "Label: '$MONDAY in my portfolio'. "
            "Clean meme format, white background with panels. "
            "Crypto Twitter meme style."
        ),
        "aspect": "1:1"
    },
}

def generate(name, prompt, aspect="1:1"):
    print(f"  Generating {name}...")
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": aspect}
    }
    r = requests.post(URL, json=body, timeout=60)
    if r.status_code != 200:
        print(f"  ❌ {name}: {r.status_code} — {r.text[:200]}")
        return False
    data = r.json()
    img_b64 = data["predictions"][0]["bytesBase64Encoded"]
    out_path = OUT / f"{name}.png"
    out_path.write_bytes(base64.b64decode(img_b64))
    print(f"  ✅ {name} → {out_path}")
    return True

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"🎨 Generating $MONDAY assets with Imagen 4.0...\n")
    for name, cfg in PROMPTS.items():
        generate(name, cfg["prompt"], cfg.get("aspect", "1:1"))
    print("\n✅ Done! Check monday-coin/assets/")
