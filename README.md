# TorNet

Automates IP address rotation via the Tor network.  
Published on [PyPI](https://pypi.org/project/python-tornet/) · 252 ⭐

[![Made in Algeria](https://www.madeinalgeria.dev/badge/tornet.svg)](https://www.madeinalgeria.dev/projects/tornet)

## Installation
```bash
pip install python-tornet
```
```bash
yay -S python-tornet  # Arch Linux
```

## Usage
```bash
tornet --interval 60 --count 10   # Change IP every 60s, 10 times
tornet --interval 60 --count 0    # Change IP indefinitely
tornet --ip                        # Show current IP
tornet --stop                      # Stop all processes
tornet --auto-fix                  # Fix missing dependencies
```

## Verify Your IP
```bash
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

## Python API
```python
from tornet import ma_ip, change_ip, initialize_environment, change_ip_repeatedly

initialize_environment()
print("Current IP:", ma_ip())
print("New IP:", change_ip())
change_ip_repeatedly(60, 10)
```

## Browser Configuration (Firefox)

`Preferences` → `Network Settings` → `Manual proxy`  
SOCKS Host: `127.0.0.1` · Port: `9050` · Enable: `Proxy DNS when using SOCKS v5`

## License

MIT · Based on [ByteBreach/tornet](https://github.com/ByteBreach/tornet)
