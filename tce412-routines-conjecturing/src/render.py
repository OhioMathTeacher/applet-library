import sys,os
from playwright.sync_api import sync_playwright
src,out=sys.argv[1],sys.argv[2]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/chromium-browser'); pg=b.new_page()
    pg.goto('file://'+os.path.abspath(src)); pg.wait_for_load_state('networkidle')
    pg.pdf(path=out, format='Letter', print_background=True, prefer_css_page_size=True)
    b.close()
