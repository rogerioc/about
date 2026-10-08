#!/usr/bin/env python3
"""Generates a professional PDF from curriculo.md using pandoc + weasyprint."""
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "curriculo.md")
OUTPUT_PDF = os.path.join(SCRIPT_DIR, "RogerioCS_CV.pdf")

# Step 1: Convert MD to HTML body via pandoc
result = subprocess.run(
    ["pandoc", MD_FILE, "--to=html5", "--wrap=none"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"Pandoc error: {result.stderr}")
    exit(1)

body_html = result.stdout

# Step 2: Wrap with professional CSS
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

@page {{
    size: A4;
    margin: 18mm 20mm 18mm 20mm;
    @bottom-center {{
        content: counter(page) " / " counter(pages);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }}
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    font-size: 9.5pt;
    line-height: 1.55;
    color: #1e293b;
}}

h1 {{
    font-family: 'Outfit', sans-serif;
    font-size: 22pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2pt;
    letter-spacing: -0.02em;
    border-bottom: 3px solid #6366f1;
    padding-bottom: 6pt;
}}

h1 + p {{
    font-size: 11pt;
    font-weight: 500;
    color: #475569;
    margin-bottom: 4pt;
}}

h2 {{
    font-family: 'Outfit', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 14pt;
    margin-bottom: 6pt;
    padding-bottom: 3pt;
    border-bottom: 1.5px solid #e2e8f0;
}}

h3 {{
    font-family: 'Outfit', sans-serif;
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 8pt;
    margin-bottom: 2pt;
}}

p {{
    margin-bottom: 4pt;
    color: #334155;
    text-align: justify;
}}

em {{
    font-style: italic;
    color: #64748b;
    font-size: 9pt;
}}

strong {{
    font-weight: 600;
    color: #1e293b;
}}

a {{
    color: #4f46e5;
    text-decoration: none;
}}

ul {{
    padding-left: 16pt;
    margin-bottom: 5pt;
}}

li {{
    margin-bottom: 2pt;
    color: #334155;
}}

ol {{
    padding-left: 16pt;
    margin-bottom: 5pt;
}}

ol li {{
    margin-bottom: 6pt;
}}

blockquote {{
    border-left: 2.5px solid #c7d2fe;
    padding-left: 10pt;
    margin: 4pt 0;
    color: #475569;
    font-size: 8.5pt;
    font-style: italic;
}}

hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 8pt 0;
}}

/* Header contact info list */
h1 + p + ul {{
    list-style: none;
    padding-left: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 4pt;
    margin-bottom: 6pt;
}}

h1 + p + ul li {{
    font-size: 8.5pt;
    color: #64748b;
}}

/* Avoid page breaks inside job entries */
h3 {{
    break-after: avoid;
}}

h3 + p, h3 + ul {{
    break-before: avoid;
}}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

# Step 3: Write temporary HTML
temp_html = os.path.join(SCRIPT_DIR, "_cv_temp.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(full_html)

# Step 4: Generate PDF with weasyprint
from weasyprint import HTML
print("Generating PDF...")
HTML(filename=temp_html).write_pdf(OUTPUT_PDF)

# Cleanup
os.remove(temp_html)
print(f"✅ PDF generated: {OUTPUT_PDF}")
