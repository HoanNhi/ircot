import chardet
import re

def fully_clean_file(input_path, output_path):
    # Step 1: Read as raw bytes
    with open(input_path, 'rb') as f:
        raw = f.read()

    # Step 2: Detect original encoding (likely Windows-1252 or Latin-1 if corrupted)
    detected = chardet.detect(raw)
    encoding = detected['encoding'] or 'utf-8'

    # Step 3: Decode from detected encoding
    try:
        text = raw.decode(encoding, errors='replace')
    except Exception as e:
        print(f"Decode failed: {e}")
        return

    # Step 4: Try to reverse double encoding (common case: utf-8 read as latin1)
    try:
        text = text.encode('latin1', errors='replace').decode('utf-8', errors='replace')
    except Exception as e:
        print("Double encoding recovery failed (safe to skip)")

    # Step 5: Replace all non-ASCII smart punctuation (quotes, dashes, etc.) with plain text
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201C': '"', '\u201D': '"',
        '\u2014': '-', '\u2013': '-', '\u2026': '...',
        '\u00a0': ' ',  # non-breaking space
        '\u200b': '',   # zero-width space
        '\ufffd': ''    # replacement character
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Step 6: Strip invalid control characters except newline and tab
    text = re.sub(r'[\x00-\x08\x0B-\x1F\x7F]', '', text)

    # Step 7: Write UTF-8 safe file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"✅ Cleaned and saved to {output_path}")

# Example usage
fully_clean_file('multihop_old.jsonnet', 'multihop_strict_cleaned.jsonnet')
