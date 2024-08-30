# TorNet

TorNet is a Python package that automates IP address changes using Tor. It is a top tool for securing your networks by frequently changing your IP address, making it difficult for trackers to pinpoint your location.

## Benefits

- **Enhanced Privacy**: By regularly changing your IP address, TorNet makes it much harder for websites and trackers to monitor your online activity.
- **Increased Security**: Frequent IP changes can help protect you from targeted attacks and make it more difficult for malicious actors to track your online presence.
- **Anonymity**: Using Tor, TorNet helps you maintain a high level of anonymity while browsing the internet.
- **Ease of Use**: TorNet is designed to be simple and easy to use, whether you prefer command-line tools or integrating it directly into your Python scripts.
- **Protection from Tracking**: With your IP address changing frequently, tracking services and advertisers will find it more challenging to build a profile on you.
- **Peace of Mind**: Knowing that your IP address is regularly changed can give you confidence in your online privacy and security.

## Installation

To install TorNet, use pip:

```bash
pip install -i https://test.pypi.org/simple/ tornet
```

To install TorNet, use yay (Arch Linux):

```bash
yay -S python-tornet
```

## Usage

TorNet provides a command-line interface for easy use. Here are the available options:

```bash
tornet --interval <seconds> --count <number>
```

- `--interval` (optional): Time in seconds between IP changes (default is 60 seconds).
- `--count` (optional): Number of times to change the IP (default is 10 times). If set to 0, the IP will be changed indefinitely.
- `--stop` (optional): Stop all Tor services and TorNet processes and exit.
- `--ip` (optional): Display the current IP address and exit.
- `--auto-fix` (optional): Automatically fix issues (install/upgrade packages).
- `--help`: Show the help message and exit.
- `--version`: Show the version number and exit.

## How It Works

TorNet uses the Tor network to route your internet traffic through multiple nodes, effectively masking your IP address. By periodically changing the IP address, TorNet ensures that your online activity remains anonymous and secure. This can be particularly useful for:

- **Privacy enthusiasts** who want to minimize their digital footprint.
- **Security professionals** who need to conduct penetration testing or other security assessments without revealing their true IP address.
- **Journalists and activists** operating in regions with internet censorship or surveillance.

### Examples

Change the IP address every 30 seconds, for a total of 5 times:

```bash
tornet --interval 30 --count 5
```

Change the IP address every 60 seconds indefinitely:

```bash
tornet --interval 60 --count 0
```

Stop all Tor services and TorNet processes:

```bash
tornet --stop
```

Display the current IP address:

```bash
tornet --ip
```

Automatically fix issues (install/upgrade packages):

```bash
tornet --auto-fix
```

## Configuring Your Browser to Use TorNet

To ensure your browser uses the Tor network for anonymity, you need to configure it to use TorNet's proxy settings:

1. **Firefox**:
    - Go to `Preferences` > `General` > `Network Settings`.
    - Select `Manual proxy configuration`.
    - Enter `127.0.0.1` for `SOCKS Host` and `9050` for the `Port` (or your specified values if different).
    - Ensure the checkbox `Proxy DNS when using SOCKS v5` is checked.
    - Click `OK`.
<img src="https://ayadseghairi.github.io/assets/img/port.png" alt="Firefox Configuration Example" />


## In Your Python Code

You can also use TorNet within your Python scripts if needed.

```python
from tornet import ma_ip, change_ip, initialize_environment, change_ip_repeatedly

# Initialize the environment (install dependencies and start Tor)
initialize_environment()

# Get the current IP
current_ip = ma_ip()
print("Current IP:", current_ip)

# Change the IP once
new_ip = change_ip()
print("New IP:", new_ip)

# Change the IP repeatedly
change_ip_repeatedly(60, 10)
```

## Troubleshooting

If you encounter any issues while using TorNet, here are a few steps you can take:

- Ensure that Tor is installed and running on your system.
- Make sure your internet connection is stable.
- Use the `--auto-fix` option to automatically install or upgrade required packages.
- Check the Tor logs for any error messages that might indicate connectivity problems.

## Contributing

We welcome contributions from the community! If you have an idea for a new feature or have found a bug, please open an issue on our [GitHub repository](https://github.com/ayadseghairi/tornet).

## License

TorNet is released under the MIT License. See the LICENSE file for more details.

## Acknowledgements

We would like to thank the developers of the Tor project for their work in creating a robust and secure anonymity network.

## Thanks

Thank you for using TorNet! We hope this tool helps you secure your network and maintain your privacy. If you have any feedback or suggestions, please feel free to reach out to us.

Many thanks also to the original developer [ByteBreach](https://github.com/ByteBreach/tornet) 
This project is an improvement to his own project

---

By following this guide, you should be able to effectively use TorNet to enhance your online privacy and security. Happy browsing!
