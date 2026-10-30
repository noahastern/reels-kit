"""Print an HTML page (the style guide) to PDF with headless Chrome.

    python3 html_to_pdf.py brand/style-guide.html brand/style-guide.pdf

Size the pages in the HTML with @page { size: 1080px 1350px; margin: 0 }.
"""
import os, shutil, subprocess, sys

src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
chrome = next((c for c in [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    shutil.which('google-chrome') or '', shutil.which('chromium') or '', shutil.which('chrome') or '',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
] if c and os.path.exists(c)), None)
if not chrome:
    sys.exit('Google Chrome not found. Install it, or open the HTML and print it to PDF.')
subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=5000',
                f'--print-to-pdf={out}', 'file://' + src], check=True, capture_output=True)
print('wrote', out)
