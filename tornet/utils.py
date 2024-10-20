import os
import subprocess
import platform

def is_arch_linux():
    try:
        if 'arch' in platform.platform().lower():
            return 'arch' in platform.platform().lower()
        elif 'manjaro' in platform.platform().lower():
            return 'manjaro' in platform.platform().lower()
    except:
        return False

def install_pip():
    if is_arch_linux():
        try:
            subprocess.check_output('pacman -Qi python-pip', shell=True)
            print("pip is already installed.")
        except subprocess.CalledProcessError:
            print("pip not found, installing...")
            subprocess.check_output('sudo pacman -Sy python-pip --noconfirm', shell=True)
            print("pip installed successfully.")
    else:
        try:
            subprocess.check_output('dpkg -s python3-pip', shell=True)
            print("pip is already installed.")
        except subprocess.CalledProcessError:
            print("pip not found, installing...")
            subprocess.check_output('sudo apt update', shell=True)
            subprocess.check_output('sudo apt install python3-pip -y', shell=True)
            print("pip installed successfully.")

def install_requests():
    try:
        import requests
        print("requests is already installed.")
    except ImportError:
        print("requests not found, installing...")
        os.system('pip3 install requests')
        os.system('pip3 install requests[socks]')
        print("requests installed successfully.")

def install_tor():
    if is_arch_linux():
        try:
            subprocess.check_output('which tor', shell=True)
            print("tor is already installed.")
        except subprocess.CalledProcessError:
            print("tor not found, installing...")
            subprocess.check_output('sudo pacman -Sy tor --noconfirm', shell=True)
            print("tor installed successfully.")
    else:
        try:
            subprocess.check_output('which tor', shell=True)
            print("tor is already installed.")
        except subprocess.CalledProcessError:
            print("tor not found, installing...")
            subprocess.check_output('sudo apt update', shell=True)
            subprocess.check_output('sudo apt install tor -y', shell=True)
            print("tor installed successfully.")

if __name__ == "__main__":
    install_pip()
    install_requests()
    install_tor()
