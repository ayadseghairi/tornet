from tornet import ma_ip, change_ip, initialize_environment, change_ip_repeatedly

# Initialize the environment (install dependencies and start Tor)
initialize_environment()

# Get the current IP
current_ip = ma_ip()
print("Current IP:", current_ip)

# Change the IP once
new_ip = change_ip()
print("New IP:", new_ip)
print("hh")
# Change the IP repeatedly
change_ip_repeatedly(5, 0)
