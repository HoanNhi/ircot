unicode_replacements = {
    "\u201c": '\\\"',   # “
    "\u201d": '\\\"',   # ”
    "\u2018": "'",   # ‘
    "\u2019": "'",   # ’
    "\u2013": '-',   # –
    "\u2014": '--',  # —
    "\u2026": '...', # …
    "\u00a0": ' ',   # non-breaking space
    "\u00a9": '(c)', # ©
    "\u00ae": '(R)', # ®
    "\u2122": '(TM)',# ™
    "\u00bd": '1/2', # ½
    "\u00bc": '1/4', # ¼
    "\u00be": '3/4', # ¾
    "\u2032": "'",   # ′
    "\u2033": '\\\"',   # ″
    "\u02dc": '~',   # ˜
    "\u200b": '',    # zero-width space
    "\u2009": ' ',   # thin space
}

def replace_smart_chars_by_codepoint(text):
    for unicode_char, replacement in unicode_replacements.items():
        text = text.replace(unicode_char, replacement)
    return text

input_file = 'multihop_old.jsonnet'
output_file = 'multihop_2.jsonnet'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to decode unicode escape sequences if present:
try:
    content = content.encode('utf-8').decode('unicode_escape')
except Exception as e:
    print("No unicode escapes to decode or decoding failed:", e)

cleaned_content = replace_smart_chars_by_codepoint(content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print(f"Cleaned output written to {output_file}")
