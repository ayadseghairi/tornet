#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# tornet - Automate IP address changes using Tor
# Author: Fidal
# Copyright (c) 2024 Fidal. All rights reserved.

import os
import sys
import time
import argparse
import requests
import subprocess
import signal
import shutil
import random
import platform

TOOL_NAME = "tornet"
VERSION = "2.2.1"

green = "\033[92m"
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"

def print_banner():
    """Print tool banner"""
    banner = f"""
{green}
████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗
╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝
   ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   
   ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   
   ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
{white}                    Version: {VERSION}
{reset}"""
    print(banner)

def log(msg: str):
    """Print info message"""
    print(f"{white} [{green}+{white}]{green} {msg}{reset}")

def error(msg: str, exit_code: int = 1):
    """Print error message and optionally exit"""
    print(f"{white} [{red}!{white}] {red}{msg}{reset}")
    if exit_code > 0:
        sys.exit(exit_code)

def warning(msg: str):
    """Print warning message"""
    print(f"{white} [{red}!{white}] {red}{msg}{reset}")

def is_root():
    """Check if running as root"""
    return os.geteuid() == 0

def has_sudo():
    """Check if sudo is available"""
    return shutil.which("sudo") is not None

def run_cmd(cmd, use_sudo=False, check=True):
    """Run command safely with optional sudo"""
    if use_sudo and not is_root():
        if not has_sudo():
            error("Root privileges required but sudo not available. Run as root or install sudo.", 2)
        cmd = ["sudo"] + cmd
    
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        if check:
            error(f"Command failed: {' '.join(cmd)}\nError: {e.stderr.strip()}")
        return e

def detect_service_manager():
    """Detect if systemd or sysv init is used"""
    if shutil.which("systemctl") and os.path.exists("/run/systemd/system"):
        return "systemctl"
    elif shutil.which("service"):
        return "service"
    return None

def service_action(action):
    """Perform service action (start/stop/reload) on tor"""
    current_os = platform.system().lower()
    if current_os == "windows":
        warning(f"Windows detected - manual service management required for '{action}'")
        log(f"On Windows, please {action} Tor service manually")
        return
    
    service_mgr = detect_service_manager()
    
    if service_mgr == "systemctl":
        cmd = ["systemctl", action, "tor"]
    elif service_mgr == "service":
        cmd = ["service", "tor", action]
    else:
        error("No supported service manager found (systemctl or service)", 3)
    
    result = run_cmd(cmd, use_sudo=True, check=False)
    if result.returncode != 0:
        warning(f"Failed to {action} tor service: {result.stderr.strip()}")

def detect_package_manager():
    """Detect available package manager"""
    current_os = platform.system().lower()
    if current_os == "windows":
        return "windows"
    
    managers = [
        ("apt", ["apt-get"]),
        ("dnf", ["dnf"]),
        ("yum", ["yum"]), 
        ("pacman", ["pacman"]),
        ("apk", ["apk"]),
        ("zypper", ["zypper"])
    ]
    
    for pm, binaries in managers:
        if any(shutil.which(binary) for binary in binaries):
            return pm
    return None

def install_package(package_name):
    """Install system package using detected package manager"""
    pm = detect_package_manager()
    if not pm:
        error("No supported package manager found. Please install packages manually.", 4)
    
    if pm == "windows":
        error(f"On Windows, please install {package_name} manually.", 4)
    
    if pm == "apt":
        run_cmd(["apt-get", "update"], use_sudo=True)
        run_cmd(["apt-get", "install", "-y", package_name], use_sudo=True)
    elif pm == "dnf":
        run_cmd(["dnf", "install", "-y", package_name], use_sudo=True)
    elif pm == "yum":
        run_cmd(["yum", "install", "-y", package_name], use_sudo=True)
    elif pm == "pacman":
        run_cmd(["pacman", "-Sy", "--noconfirm", package_name], use_sudo=True)
    elif pm == "apk":
        run_cmd(["apk", "add", package_name], use_sudo=True)
    elif pm == "zypper":
        run_cmd(["zypper", "--non-interactive", "install", package_name], use_sudo=True)

def ensure_pip():
    """Ensure pip is available"""
    try:
        subprocess.run([sys.executable, "-c", "import pip"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        log("pip not found, attempting to install...")
        
        # Try ensurepip first
        try:
            run_cmd([sys.executable, "-m", "ensurepip", "--upgrade"])
            return True
        except:
            pass
        
        # Try system package manager
        try:
            pm = detect_package_manager()
            if pm == "windows":
                error("On Windows, please install pip manually or use Python installer.", 5)
            elif pm == "apt":
                install_package("python3-pip")
            elif pm in ["dnf", "yum"]:
                install_package("python3-pip")
            elif pm == "pacman":
                install_package("python-pip")
            elif pm == "apk":
                install_package("py3-pip")
            elif pm == "zypper":
                install_package("python3-pip")
            return True
        except:
            error("Failed to install pip. Please install pip manually.", 5)

def ensure_requests():
    """Ensure requests package is available"""
    try:
        import requests
        return True
    except ImportError:
        log("requests package not found, installing...")
        ensure_pip()
        try:
            run_cmd([sys.executable, "-m", "pip", "install", "requests", "requests[socks]"])
            return True
        except:
            error("Failed to install requests package.", 6)

def is_tor_installed():
    """Check if tor binary is installed"""
    if shutil.which("tor") is not None:
        return True
    
    current_os = platform.system().lower()
    if current_os == "windows":
        import winreg 
        
        common_paths = [
            os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
            os.path.join(os.environ.get('PROGRAMDATA', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
            os.path.join(os.environ.get('APPDATA', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Tor', 'tor.exe'),
        ]
        
        try:
            registry_keys = [
                (winreg.HKEY_CURRENT_USER, r"Software\Tor Browser"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Tor Browser"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Tor Browser"),
            ]
            
            for hive, key_path in registry_keys:
                try:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
                    install_path, _ = winreg.QueryValueEx(key, "InstallDirectory")
                    winreg.CloseKey(key)
                    
                    tor_path = os.path.join(install_path, "Browser", "TorBrowser", "Tor", "tor.exe")
                    if os.path.exists(tor_path):
                        tor_dir = os.path.dirname(tor_path)
                        os.environ["PATH"] = tor_dir + os.pathsep + os.environ.get("PATH", "")
                        return True
                except WindowsError:
                    continue
        except ImportError:
            pass
        
        for path in common_paths:
            if os.path.exists(path):
                tor_dir = os.path.dirname(path)
                os.environ["PATH"] = tor_dir + os.pathsep + os.environ.get("PATH", "")
                return True
    
    return False

def ensure_tor():
    """Ensure tor is installed"""
    if is_tor_installed():
        return True
    
    current_os = platform.system().lower()
    
    if current_os == "windows":
        error("On Windows, please install Tor Browser manually from: https://www.torproject.org/download/", 7)
    
    log("tor not found, installing...")
    try:
        install_package("tor")
        return True
    except:
        error("Failed to install tor. Please install tor manually.", 7)

def is_tor_running():
    """Check if tor process is running"""
    current_os = platform.system().lower()
    
    if current_os == "windows":
        
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq tor.exe", "/FO", "CSV", "/NH"], 
                capture_output=True, 
                text=True, 
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return "tor.exe" in result.stdout
        except:
            
            try:
                import psutil
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and 'tor.exe' in proc.info['name'].lower():
                        return True
                return False
            except ImportError:
                
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(("127.0.0.1", 9050))
                    sock.close()
                    return result == 0
                except:
                    return False

def get_current_ip():
    """Get current public IP address"""
    if is_tor_running():
        return get_ip_via_tor()
    else:
        return get_ip_direct()

def get_ip_via_tor():
    """Get IP address via Tor proxy"""
    url = 'https://api.ipify.org'
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        warning("Having trouble connecting to the Tor network. Please wait a moment.")
        return None

def get_ip_direct():
    """Get IP address directly (without Tor)"""
    try:
        response = requests.get('https://api.ipify.org', timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        warning("Having trouble fetching IP address. Please check your internet connection.")
        return None

def change_ip():
    """Change IP by reloading Tor service or sending NEWNYM signal"""
    current_os = platform.system().lower()
    
    if current_os == "windows":
        return change_ip_windows()
    else:
        service_action("reload")
        time.sleep(2)  
        return get_current_ip()

def change_ip_windows():
    """Change Tor IP on Windows using control port"""
    import socket
    
    control_port = 9051
    control_password = ""
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("127.0.0.1", control_port))
        
        if control_password:
            sock.send(f"AUTHENTICATE \"{control_password}\"\r\n".encode())
            response = sock.recv(1024).decode()
            if "250" not in response:
                warning(f"Authentication failed: {response}")
                sock.close()
                return None
        
        sock.send(b"SIGNAL NEWNYM\r\n")
        response = sock.recv(1024).decode()
        sock.close()
        
        if "250" in response:
            log("Successfully sent NEWNYM signal to Tor")
            time.sleep(2)
            return get_current_ip()
        else:
            warning(f"Failed to change IP: {response}")
            return None
            
    except ConnectionRefusedError:
        warning("Could not connect to Tor control port (9051). Is Tor running with ControlPort enabled?")
        return None
    except socket.timeout:
        warning("Timeout connecting to Tor control port")
        return None
    except Exception as e:
        warning(f"Error changing IP on Windows: {str(e)}")
        return None

def check_tor_config_windows():
    """Check if Tor is configured with ControlPort for Windows"""
    current_os = platform.system().lower()
    
    if current_os != "windows":
        return True
    
    log("Checking Tor configuration for Windows...")
    
    config_paths = [
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'Tor Browser', 'Browser', 'TorBrowser', 'Data', 'Tor', 'torrc'),
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Data', 'Tor', 'torrc'),
        os.path.join(os.environ.get('APPDATA', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Data', 'Tor', 'torrc'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tor Browser', 'Browser', 'TorBrowser', 'Data', 'Tor', 'torrc'),
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            log(f"Found Tor config at: {config_path}")
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                    if "ControlPort" in content:
                        log("ControlPort is configured in torrc")
                        return True
            except:
                pass
    
    warning("ControlPort not found in Tor configuration.")
    log("To enable IP changing on Windows, add these lines to your torrc file:")
    log("ControlPort 9051")
    log("CookieAuthentication 1")
    log("OR if you want password authentication:")
    log("HashedControlPassword <hashed-password>")
    log("")
    log("Then restart Tor.")
    return False

def start_tor_windows():
    """Start Tor process on Windows"""
    tor_path = find_tor_path()
    
    if not tor_path or not os.path.exists(tor_path):
        warning("Could not find tor.exe")
        return False
    
    try:
        log(f"Starting Tor from: {tor_path}")
        
        
        tor_dir = os.path.dirname(tor_path)
        
        
        subprocess.Popen(
            [tor_path],
            cwd=tor_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        log("Tor process started. Waiting for connection...")
        time.sleep(10)
        
        return True
    except Exception as e:
        warning(f"Failed to start Tor: {str(e)}")
        return False

def print_ip(ip):
    """Print current IP address"""
    log(f"Your IP address is: {white}{ip}")

def change_ip_repeatedly(interval_str, count):
    """Change IP repeatedly with specified interval and count"""
    if count == 0:  # Infinite loop
        while True:
            try:
                sleep_time = parse_interval(interval_str)
                time.sleep(sleep_time)
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)
            except KeyboardInterrupt:
                break
    else:
        for _ in range(count):
            try:
                sleep_time = parse_interval(interval_str)
                time.sleep(sleep_time)
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)
            except KeyboardInterrupt:
                break

def parse_interval(interval_str):
    """Parse interval string (single number or range)"""
    try:
        if "-" in str(interval_str):
            start, end = map(int, str(interval_str).split("-", 1))
            return random.randint(start, end)
        else:
            return int(interval_str)
    except ValueError:
        error("Invalid interval format. Use number or range (e.g., '60' or '30-120')", 8)

def auto_fix():
    """Automatically fix dependencies"""
    log("Running auto-fix...")
    ensure_pip()
    ensure_requests()
    ensure_tor()
    log("Auto-fix complete")

def stop_services():
    """Stop tor service and tornet processes"""
    current_os = platform.system().lower()
    
    if current_os == "windows":
        log("Windows detected - attempting to stop Tor processes...")
        try:
            subprocess.run(["taskkill", "/F", "/IM", "tor.exe"], check=False, capture_output=True)
            log("Tor processes stopped on Windows")
        except:
            warning("Could not stop Tor processes on Windows")
    else:
        service_action("stop")
    
    try:
        subprocess.run(["pkill", "-f", TOOL_NAME], check=False, capture_output=True)
    except:
        pass
    log(f"Tor services and {TOOL_NAME} processes stopped.")

def signal_handler(sig, frame):
    """Handle interrupt signals"""
    signal_name = "Unknown"
    if sig == signal.SIGINT:
        signal_name = "SIGINT (Ctrl+C)"
    elif hasattr(signal, 'SIGQUIT') and sig == signal.SIGQUIT:
        signal_name = "SIGQUIT (Ctrl+\\)"
    elif hasattr(signal, 'SIGBREAK') and sig == signal.SIGBREAK:
        signal_name = "SIGBREAK (Ctrl+Break)"
    elif hasattr(signal, 'SIGHUP') and sig == signal.SIGHUP:
        signal_name = "SIGHUP"
    
    log(f"Received {signal_name}")
    stop_services()
    print(f"\n{white} [{red}!{white}] {red}Program terminated by user.{reset}")
    sys.exit(0)

def setup_signal_handlers():
    """Setup signal handlers based on operating system"""
    current_os = platform.system().lower()
    
    signal.signal(signal.SIGINT, signal_handler)
    log("Registered handler for SIGINT (Ctrl+C)")
    
    if current_os == "windows":
        termination_signals = [signal.SIGBREAK]
        log("Running on Windows - use Ctrl+C to interrupt, Ctrl+Break to terminate")
    else:
        termination_signals = [signal.SIGQUIT, signal.SIGHUP]
        log(f"Running on {current_os} - use Ctrl+C to interrupt, Ctrl+\\ to terminate")
    
    for sig in termination_signals:
        try:
            signal.signal(sig, signal_handler)
            signal_name = "Unknown"
            if hasattr(signal, 'SIGBREAK') and sig == signal.SIGBREAK:
                signal_name = "SIGBREAK"
            elif hasattr(signal, 'SIGQUIT') and sig == signal.SIGQUIT:
                signal_name = "SIGQUIT"
            elif hasattr(signal, 'SIGHUP') and sig == signal.SIGHUP:
                signal_name = "SIGHUP"
            log(f"Registered handler for {signal_name}")
            break
        except (AttributeError, ValueError):
            continue

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        response = requests.get('http://www.google.com', timeout=5)
        return True
    except requests.RequestException:
        error("Internet connection required but not available.", 9)

def initialize_environment():
    """Initialize tor environment"""
    current_os = platform.system().lower()
    
    if current_os == "windows":
        log("Windows detected - checking Tor configuration...")
        if not is_tor_running():
            warning("Tor is not running. Please start Tor Browser or Tor service manually.")
            log("Waiting 10 seconds for Tor to start...")
            time.sleep(10)
        
        
        check_tor_config_windows()
        
        if is_tor_running():
            log("Tor is running. IP changing via control port will be attempted.")
        else:
            warning("Tor is still not running. IP changing may fail.")
        
        log("Configure your browser to use Tor proxy (127.0.0.1:9050) for anonymity.")
    else:
        service_action("start")
        log("Tor service started. Please wait for Tor to establish connection.")
        log("Configure your browser to use Tor proxy (127.0.0.1:9050) for anonymity.")

def main():
    """Main function"""
    setup_signal_handlers()

    parser = argparse.ArgumentParser(description="TorNet - Automate IP address changes using Tor")
    parser.add_argument('--interval', type=str, default='60', help='Time in seconds between IP changes (or range like "30-120")')
    parser.add_argument('--count', type=int, default=10, help='Number of times to change IP. If 0, change IP indefinitely')
    parser.add_argument('--ip', action='store_true', help='Display current IP address and exit')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically install missing dependencies')
    parser.add_argument('--start-tor', action='store_true', help='Start Tor process on Windows')
    parser.add_argument('--stop', action='store_true', help='Stop all Tor services and tornet processes')
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()

    if args.stop:
        stop_services()
        return

    if args.start_tor:
        if platform.system().lower() == "windows":
            start_tor_windows()
        else:
            log("--start-tor is only needed on Windows")
        return

    if args.ip:
        ip = get_current_ip()
        if ip:
            print_ip(ip)
        return

    if args.auto_fix:
        auto_fix()
        return

    # Check dependencies
    if not is_tor_installed():
        error("Tor is not installed. Run with --auto-fix to install automatically.", 10)

    try:
        import requests
    except ImportError:
        error("requests package not found. Run with --auto-fix to install automatically.", 11)

    check_internet_connection()
    print_banner()
    initialize_environment()
    
    # Wait for tor to establish connection
    time.sleep(5)
    
    change_ip_repeatedly(args.interval, args.count)

if __name__ == "__main__":
    main()
