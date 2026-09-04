#!/usr/bin/env python3
"""
Script untuk membuat repository GitHub dan push project secara otomatis
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from getpass import getpass

# Konfigurasi
USERNAME = "jinwofuruda-cloud"
REPO_NAME = "ida-droid"
DESCRIPTION = "IDA Droid - Android Terminal Emulator"
PRIVATE = False

def print_status(message, status="INFO"):
    """Print status dengan warna"""
    colors = {
        "INFO": "\033[94m",    # Biru
        "SUCCESS": "\033[92m",  # Hijau
        "ERROR": "\033[91m",    # Merah
        "WARNING": "\033[93m",  # Kuning
    }
    reset = "\033[0m"
    emoji = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️",
    }
    print(f"{colors.get(status, '')}{emoji.get(status, '')} {message}{reset}")

def run_command(command, show_output=True):
    """Jalankan command shell"""
    try:
        if show_output:
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Command gagal: {command}", "ERROR")
        if e.stderr:
            print(e.stderr.decode())
        return False

def create_repository(token):
    """Buat repository di GitHub menggunakan API"""
    print_status("Membuat repository di GitHub...", "INFO")
    
    url = "https://api.github.com/user/repos"
    data = json.dumps({
        "name": REPO_NAME,
        "description": DESCRIPTION,
        "private": PRIVATE,
        "auto_init": False
    }).encode('utf-8')
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        response = urllib.request.urlopen(request)
        if response.status == 201:
            print_status("Repository berhasil dibuat!", "SUCCESS")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print_status("Repository sudah ada, lanjut ke push...", "WARNING")
            return True
        else:
            error_body = e.read().decode()
            print_status(f"Gagal membuat repository: {e.code}", "ERROR")
            print(error_body)
            return False
    except Exception as e:
        print_status(f"Error: {str(e)}", "ERROR")
        return False
    
    return True

def setup_git(token):
    """Setup git configuration"""
    print_status("Mengkonfigurasi Git...", "INFO")
    
    commands = [
        f'git config --global user.name "{USERNAME}"',
        f'git config --global user.email "{USERNAME}@users.noreply.github.com"',
    ]
    
    for cmd in commands:
        if not run_command(cmd, show_output=False):
            return False
    
    return True

def init_repository():
    """Inisialisasi repository jika belum ada"""
    if not os.path.exists(".git"):
        print_status("Menginisialisasi Git...", "INFO")
        if not run_command("git init", show_output=False):
            return False
    else:
        print_status("Repository Git sudah ada", "INFO")
    
    return True

def add_and_commit():
    """Add dan commit semua file"""
    print_status("Menambahkan file...", "INFO")
    if not run_command("git add .", show_output=False):
        return False
    
    print_status("Commit file...", "INFO")
    if not run_command('git commit -m "Initial commit: IDA Droid project"', show_output=False):
        # Jika tidak ada perubahan, lanjut
        print_status("Tidak ada perubahan untuk di-commit", "WARNING")
    
    return True

def set_remote_and_push(token):
    """Set remote dan push ke GitHub"""
    print_status("Mengatur remote repository...", "INFO")
    
    # Hapus remote lama
    run_command("git remote remove origin 2>/dev/null", show_output=False)
    
    # Set remote baru
    remote_url = f"https://{USERNAME}:{token}@github.com/{USERNAME}/{REPO_NAME}.git"
    if not run_command(f'git remote add origin "{remote_url}"', show_output=False):
        return False
    
    # Set branch main
    run_command("git branch -M main", show_output=False)
    
    # Push
    print_status("Push ke GitHub...", "INFO")
    if not run_command("git push -u origin main"):
        return False
    
    return True

def main():
    """Fungsi utama"""
    print("=" * 50)
    print("🚀 GitHub Repository Creator & Pusher")
    print("=" * 50)
    
    # Minta token
    token = getpass("🔑 Masukkan Personal Access Token: ")
    
    if not token:
        print_status("Token tidak boleh kosong!", "ERROR")
        sys.exit(1)
    
    # Buat repository
    if not create_repository(token):
        sys.exit(1)
    
    # Setup git
    if not setup_git(token):
        sys.exit(1)
    
    # Init repository
    if not init_repository():
        sys.exit(1)
    
    # Add dan commit
    if not add_and_commit():
        sys.exit(1)
    
    # Set remote dan push
    if not set_remote_and_push(token):
        sys.exit(1)
    
    print("")
    print_status("Semua proses selesai!", "SUCCESS")
    print_status(f"Repository: https://github.com/{USERNAME}/{REPO_NAME}", "INFO")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Dibatalkan oleh user")
        sys.exit(1)# Paste semua kode di atas
