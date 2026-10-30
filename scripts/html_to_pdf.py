"""Print an HTML page (the style guide) to PDF with headless Chrome.

    python3 html_to_pdf.py brand/style-guide.html brand/style-guide.pdf

Size the pages in the HTML with @page { size: 1080px 1350px; margin: 0 }.
"""
import os, pathlib, shutil, subprocess, sys

src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
chrome = next((c for c in [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    shutil.which('google-chrome') or '', shutil.which('chromium') or '', shutil.which('chrome') or '',
    *[os.path.join(os.environ.get(v, ''), 'Google', 'Chrome', 'Application', 'chrome.exe')
      for v in ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'LOCALAPPDATA') if os.environ.get(v)],
    # Edge is Chromium and comes with every Windows install
    *[os.path.join(os.environ.get(v, ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe')
      for v in ('PROGRAMFILES(X86)', 'PROGRAMFILES') if os.environ.get(v)],
] if c and os.path.exists(c)), None)
if not chrome:
    sys.exit('Google Chrome or Microsoft Edge not found. Install Chrome, or open the HTML and print it to PDF.')
subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=5000',
                f'--print-to-pdf={out}', pathlib.Path(src).as_uri()], check=True, capture_output=True)
print('wrote', out)
