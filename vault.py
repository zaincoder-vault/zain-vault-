#!/usr/bin/env python3
import os
import json
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_FILE = os.path.expanduser("~/.zain_vault.enc")
KEY_FILE = os.path.expanduser("~/.zain_key.key")

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def init_vault():
    print("\n[-] First time setup: Let's create your Secure Vault!")
    pwd = getpass("Set Master Password: ")
    confirm_pwd = getpass("Confirm Master Password: ")
    
    if pwd != confirm_pwd:
        print("[-] Passwords do not match! Restart the script.")
        exit(1)
        
    salt = os.urandom(16)
    with open(KEY_FILE, "wb") as kf:
        kf.write(salt)
        
    key = generate_key(pwd, salt)
    initial_data = {"passwords": {}, "notes": {}, "files": {}}
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(initial_data).encode())
    
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)
    print("[+] Vault created and securely encrypted successfully!\n")

def get_vault_data():
    if not os.path.exists(VAULT_FILE) or not os.path.exists(KEY_FILE):
        init_vault()
        
    pwd = getpass("🔐 Enter Master Password to unlock vault: ")
    try:
        with open(KEY_FILE, "rb") as kf:
            salt = kf.read()
        key = generate_key(pwd, salt)
        fernet = Fernet(key)
        
        with open(VAULT_FILE, "rb") as f:
            decrypted_data = fernet.decrypt(f.read())
        return fernet, json.loads(decrypted_data.decode())
    except Exception:
        print("[-] Wrong Master Password! Access Denied.")
        return None, None

def save_vault_data(fernet, vault_data):
    encrypted_data = fernet.encrypt(json.dumps(vault_data).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)

def print_banner():
    R = "\033[91m"
    G = "\033[92m"
    Y = "\033[93m"
    B = "\033[94m"
    C = "\033[96m"
    RESET = "\033[0m"

    banner = f"""
{C}╔═════════════════════════════════════════╗
║ {B} ███████╗ █████╗ ██╗███╗   ██╗{C}          ║
║ {B} ╚══███╔╝██╔══██╗██║████╗  ██║{C}          ║
║ {B}   ███╔╝ ███████║██║██╔██╗ ██║{C}          ║
║ {B}  ███╔╝  ██╔══██║██║██║╚██╗██║{C}          ║
║ {B} ███████╗██║  ██║██║██║ ╚████║{C}          ║
╚═════════════════════════════════════════╝{RESET}
{Y}[+] Developer : ZAIN OFFICIAL         v2.0{RESET}
{G}[+] Status    : AES-256 Secure Storage{RESET}
{R}-------------------------------------------{RESET}
"""
    print(banner)

def main():
    os.system('clear')
    print_banner()
    
    fernet, vault_data = get_vault_data()
    if not fernet:
        return

    print("\n[+] Vault Unlocked Successfully!")

    while True:
        os.system('clear')
        print_banner()
        print("\n=================== ZAIN MENU ===================")
        print("1. Add Password")
        print("2. View Saved Passwords")
        print("3. Add Secret Text Note")
        print("4. View Secret Notes")
        print("5. Save File / Image Securely")
        print("6. Extract / View Saved File & Image")
        print("7. Change Master Password")
        print("8. Exit Vault")
        
        choice = input("\nSelect an option (1-8): ").strip()
        
        if choice == '1':
            print("\n--- ADD PASSWORD ---")
            site = input("Enter App/Website Name (or type 'back' to return): ").strip()
            if site.lower() == 'back':
                continue
            username = input("Enter Username/Email: ").strip()
            password = getpass("Enter Password: ")
            vault_data["passwords"][site] = {"username": username, "password": password}
            save_vault_data(fernet, vault_data)
            print(f"[+] Password for '{site}' saved securely!")
            input("\nPress Enter to return to menu...")
            
        elif choice == '2':
            print("\n--- SAVED PASSWORDS ---")
            if not vault_data["passwords"]:
                print("No passwords saved yet.")
            for site, info in vault_data["passwords"].items():
                print(f"📌 Site: {site} | User: {info['username']} | Pass: {info['password']}")
            input("\nPress Enter to return to menu...")
                
        elif choice == '3':
            print("\n--- ADD SECRET NOTE ---")
            title = input("Enter Note Title (or type 'back' to return): ").strip()
            if title.lower() == 'back':
                continue
            note_text = input("Enter Secret Text: ").strip()
            vault_data["notes"][title] = note_text
            save_vault_data(fernet, vault_data)
            print(f"[+] Note '{title}' saved securely!")
            input("\nPress Enter to return to menu...")
            
        elif choice == '4':
            print("\n--- SECRET NOTES ---")
            if not vault_data["notes"]:
                print("No notes saved yet.")
            for title, text in vault_data["notes"].items():
                print(f"📝 Title: {title}\nContent: {text}\n------------------")
            input("\nPress Enter to return to menu...")
                
        elif choice == '5':
            print("\n--- SAVE FILE / IMAGE ---")
            file_path = input("Enter full path of file/image to lock (or type 'back' to return): ").strip()
            if file_path.lower() == 'back':
                continue
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as fl:
                    encoded_file = base64.b64encode(fl.read()).decode()
                vault_data["files"][file_name] = encoded_file
                save_vault_data(fernet, vault_data)
                print(f"[+] File '{file_name}' locked inside vault!")
            else:
                print("[-] File not found at given path!")
            input("\nPress Enter to return to menu...")
                
        elif choice == '6':
            print("\n--- SAVED FILES & IMAGES ---")
            if not vault_data["files"]:
                print("No files saved yet.")
                input("\nPress Enter to return to menu...")
                continue
            for fname in vault_data["files"].keys():
                print(f"📁 {fname}")
            
            fname_to_extract = input("\nEnter file name to extract (or type 'back' to return): ").strip()
            if fname_to_extract.lower() == 'back':
                continue
            if fname_to_extract in vault_data["files"]:
                out_path = input("Enter path/folder to save restored file (e.g., /home/zainofficial/aaa/): ").strip()
                
                if os.path.isdir(out_path) or out_path.endswith('/'):
                    out_path = os.path.join(out_path, fname_to_extract)
                elif not out_path:
                    out_path = fname_to_extract

                with open(out_path, "wb") as fl:
                    fl.write(base64.b64decode(vault_data["files"][fname_to_extract]))
                print(f"[+] File successfully restored to '{out_path}'!")
            else:
                print("[-] File not found in vault!")
            input("\nPress Enter to return to menu...")

        elif choice == '7':
            print("\n--- CHANGE MASTER PASSWORD ---")
            old_pwd = getpass("Enter Current Master Password (or press Enter to cancel): ")
            if not old_pwd:
                continue
            
            try:
                with open(KEY_FILE, "rb") as kf:
                    salt = kf.read()
                test_key = generate_key(old_pwd, salt)
                test_fernet = Fernet(test_key)
                with open(VAULT_FILE, "rb") as f:
                    test_fernet.decrypt(f.read())
            except Exception:
                print("[-] Incorrect Current Password! Password change aborted.")
                input("\nPress Enter to return to menu...")
                continue

            new_pwd = getpass("Enter New Master Password: ")
            confirm_new_pwd = getpass("Confirm New Master Password: ")
            
            if new_pwd != confirm_new_pwd:
                print("[-] New passwords do not match! Password change aborted.")
                input("\nPress Enter to return to menu...")
                continue
                
            new_salt = os.urandom(16)
            with open(KEY_FILE, "wb") as kf:
                kf.write(new_salt)
                
            new_key = generate_key(new_pwd, new_salt)
            fernet = Fernet(new_key)
            save_vault_data(fernet, vault_data)
            print("[+] Master Password changed successfully!")
            input("\nPress Enter to return to menu...")
                
        elif choice == '8':
            print("Exiting vault. Stay secure, Zain!")
            break
        else:
            print("[-] Invalid option! Choose between 1-8.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()