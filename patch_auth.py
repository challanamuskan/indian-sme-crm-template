"""
patch_auth.py — Run once from repo root to inject auth guard into all pages.
Usage: python patch_auth.py
"""
import os
from pathlib import Path

GUARD = '''import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\\U0001f512 Please login first.")
    st.stop()

'''

pages_dir = Path("pages")
patched = []
skipped = []

for f in sorted(pages_dir.glob("*.py")):
    content = f.read_text()
    if 'st.session_state.get("authenticated"' in content:
        skipped.append(f.name)
        continue
    # Insert guard after first docstring or at top
    if content.startswith('"""'):
        end = content.find('"""', 3) + 3
        new_content = content[:end] + "\n\n" + GUARD + content[end:].lstrip("\n")
    else:
        new_content = GUARD + content
    f.write_text(new_content)
    patched.append(f.name)

print(f"✅ Patched {len(patched)} files: {patched}")
print(f"⏭️  Skipped {len(skipped)} (already had guard): {skipped}")
