# -*- coding: utf-8 -*-
import subprocess
import ipaddress
from subprocess import DEVNULL
from datetime import datetime
import time
from MrLou_modules.Random_Message.random_message import get_random_message

# ANSI escape codes for red text
RED = '\033[91m'
RESET = '\033[0m'

name = "Louis-Philippe Descamps"
version = "18SEP2024"

# Function to suggest a valid network CIDR
def suggest_valid_cidr(ip_with_cidr):
    try:
        # Create an ip_network object with strict=False to get a valid network address
        network = ipaddress.ip_network(ip_with_cidr, strict=False)
        # Return the network address with a valid CIDR
        return str(network)
    except ValueError:
        # If there's an error, return None
        return None

# Function to prompt user for CIDR values with validation and suggestion
def get_cidr_list():
    while True:
        cidr_input = input(
            "Enter network addresses in CIDR format (separate by commas, e.g., 10.1.1.0/16,10.3.3.0/29): ")
        cidr_list = [cidr.strip() for cidr in cidr_input.split(',')]
        valid = True
        for cidr in cidr_list:
            try:
                # Validate CIDR
                ipaddress.ip_network(cidr, strict=True)
            except ValueError as e:
                # Suggest a valid CIDR and prompt user to try again
                suggested_cidr = suggest_valid_cidr(cidr)
                if suggested_cidr:
                    print(
                        f"{RED}Invalid CIDR format '{cidr}': {e}. Suggested valid CIDR: {suggested_cidr}. Please try again.{RESET}")
                else:
                    print(f"{RED}Invalid CIDR format '{cidr}': {e}. Please try again.{RESET}")
                valid = False
                break
        if valid:
            return cidr_list

# Function to ping an IP address multiple times
def ping_ip(ip):
    result = subprocess.run(['ping', '-n', count, '-w', timeout, str(ip)], stdout=DEVNULL)
    return result.returncode == 0

# Function to handle the main logic for pinging and results
def run_script():
    # Prompt user for CIDR values and timeout settings
    cidr_list_prompt = get_cidr_list()

    # Prompt user for ping settings
    global timeout, count
    timeout_input = input(
        "Enter timeout in milliseconds. "
        "The lower the number, the faster the result, but with less reliability. "
        "(Default: 500): "
    )
    timeout = timeout_input if timeout_input else "500"

    count_input = input(
        "Enter number of pings. "
        "The lower the number, the faster the result, but with less reliability. "
        "(Default: 2): "
    )
    count = count_input if count_input else "2"

    # Initialize lists to track results
    up_ip_list = []
    down_ip_list = []

    # Store results per network for printing at the end
    network_results = {}

    # Loop through each CIDR address provided
    for net_addr in cidr_list_prompt:
        try:
            ip_net = ipaddress.ip_network(net_addr)
            all_hosts = list(ip_net.hosts())

            up_ip_network = []
            down_ip_network = []

            # Ping each IP address in the network
            total_hosts = len(all_hosts)
            for index, ip in enumerate(all_hosts):
                print(f"Pinging {ip} ({index + 1}/{total_hosts})...")
                if ping_ip(ip):
                    print(f"{ip} is up")
                    up_ip_list.append(ip)
                    up_ip_network.append(ip)
                else:
                    print(f"{ip} is down")
                    down_ip_list.append(ip)
                    down_ip_network.append(ip)

                # Print a random joke every time we ping
                print(get_random_message())

                # Sleep a short while to avoid overwhelming the console
                time.sleep(0.1)

            # Store results for this network
            network_results[net_addr.strip()] = {
                "up": up_ip_network,
                "down": down_ip_network
            }

        except ValueError as e:
            print(f"Invalid CIDR format '{net_addr}': {e}")

    # Print the results for each network at the end
    for net_addr, results in network_results.items():
        up_count = len(results["up"])
        down_count = len(results["down"])
        print(f"Network {net_addr}:")
        print(f"Total number of up IP addresses: {up_count}")
        print(f"Total number of down IP addresses: {down_count}")
        if up_count > 0:
            print(f"Up IP addresses: {', '.join(str(ip) for ip in results['up'])}")
        else:
            print("No IP addresses are up.")
        print()

    # Print the total count of up IP addresses across all networks
    print('Total number of up IP addresses across all networks:', len(up_ip_list))

    # Print the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('Current date and time:', current_datetime)

    # Print version and author
    print(f"Author: {name} - Script Version: {version}")

# Main loop to rerun or exit
while True:
    run_script()
    rerun = input("Do you want to rerun the script with new CIDR values? (yes to rerun, any other key to exit): ")
    if rerun.lower() != 'yes':
        print("Exiting the script. Goodbye!")
        break
