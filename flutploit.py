import requests
import base64
import json

def print_ascii_art():
    ascii_art = """
  _____.__          __         .__         .__  __
_/ ____\\  |  __ ___/  |_______ |  |   ____ |__|/  |_
\\   __\\|  | |  |  \\   __\\____ \\|  |  /  _ \\|  \\   __\\
 |  |  |  |_|  |  /|  | |  |_> >  |_(  <_> )  ||  |
 |__|  |____/____/ |__| |   __/|____/\\____/|__||__|
                        |__|
    Flutter on the web manifest exploiter
    Author : xTuzki (https://github.com/unsa1nted)
"""
    print(ascii_art)

def check_asset_manifest(domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'https://{domain}/',
        'DNT': '1'
    }

    urls = [
        f"http://{domain}/assets/AssetManifest.bin.json",
        f"https://{domain}/assets/AssetManifest.bin.json"
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"[DEBUG] Requesting URL: {url}")
            print(f"[DEBUG] Status Code: {response.status_code}")

            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            continue
    return None

def decode_manifest(manifest_content):
    try:
        # Try parsing as JSON first
        json_data = json.loads(manifest_content)
        return json.dumps(json_data, indent=2)
    except json.JSONDecodeError:
        try:
            # Try base64 decoding
            decoded_bytes = base64.b64decode(manifest_content)
            try:
                # Try decoding as UTF-8
                return decoded_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, try alternative encodings
                try:
                    return decoded_bytes.decode('latin-1')
                except Exception as e:
                    return f"Error decoding: {e}\nRaw bytes: {decoded_bytes}"
        except Exception as e:
            return f"Error decoding base64: {e}"

def main():
    print_ascii_art()
    with open('list.txt', 'r') as file:
        domains = file.read().splitlines()

    for domain in domains:
        if not domain.strip():
            continue
        print(f"[+] {domain} =>")
        asset_manifest = check_asset_manifest(domain.strip())
        if asset_manifest:
            decoded_output = decode_manifest(asset_manifest)
            print(decoded_output)
        else:
            print("AssetManifest.bin.json not found or not accessible.")

if __name__ == "__main__":
    main()
