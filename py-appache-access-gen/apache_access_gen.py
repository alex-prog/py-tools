#!/usr/bin/env python3

import sys
import random
import ipaddress
from datetime import datetime, timedelta

# Function to read data from files
def read_file_lines(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()

# Paths to input files
NETWORKS_FILE = "input_files/networks.txt"
SUSPICIOUS_URLS_FILE = "input_files/suspicious_urls.txt"
SUSPICIOUS_USER_AGENTS_FILE = "input_files/suspicious_user_agents.txt"
FEO_TRACKER_ABUSE_CH_FILE = "input_files/feodotracker_abuse_ch.txt"
USER_AGENTS_FILE = "input_files/user_agents.txt"

# List of network ranges in CIDR notation
networks = read_file_lines(NETWORKS_FILE)

# List of suspicious URLs
suspicious_urls = read_file_lines(SUSPICIOUS_URLS_FILE)

# List of suspicious user agents
suspicious_user_agents = read_file_lines(SUSPICIOUS_USER_AGENTS_FILE)

# IP addresses from feodotracker_abuse_ch
feodotracker_abuse_ch = read_file_lines(FEO_TRACKER_ABUSE_CH_FILE)

# List of user agents
user_agents = read_file_lines(USER_AGENTS_FILE)

def generate_random_ip():
    # Include some IP addresses from feodotracker_abuse_ch
    if random.random() < 0.2:
        return random.choice(feodotracker_abuse_ch)
    else:
        network = random.choice(networks)
        ip = ipaddress.IPv4Address(network.split("/")[0])
        subnet = ipaddress.IPv4Network(network, strict=False)
        return str(ipaddress.ip_address(random.randint(int(subnet.network_address), int(subnet.broadcast_address))))

def generate_apache_log_entry(timestamp):
    ip = generate_random_ip()
    url = random.choice(suspicious_urls) if random.random() < 0.2 else random.choice(suspicious_urls)
    status_code = random.choice([200, 404, 500])
    user_agent = random.choice(suspicious_user_agents) if random.random() < 0.2 else random.choice(user_agents)
    referer = "-"  # Not used in this example

    # Generate log entry string
    log_entry = f"{ip} - - [{timestamp}] \"GET {url} HTTP/1.1\" {status_code} - \"{referer}\" \"{user_agent}\""
    return log_entry

def main():
    if len(sys.argv) == 1:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        num_entries = 200  # Default number of entries
    elif len(sys.argv) == 4:
        num_entries = int(sys.argv[1])
        start_time = datetime.fromisoformat(sys.argv[2])
        end_time = datetime.fromisoformat(sys.argv[3])
    else:
        print("Usage:")
        print("   ./generate_logs.py <num_entries> <start_time> <end_time>")
        print("   ./generate_logs.py")
        print("time format: 'YYYY-MM-DDTHH:MM:SS'")
        sys.exit(1)

    if len(sys.argv) != 4 and len(sys.argv) != 1:
        print("Usage:")
        print("   ./generate_logs.py <num_entries> <start_time> <end_time>")
        print("   ./generate_logs.py")
        print("time format: 'YYYY-MM-DDTHH:MM:SS'")
        sys.exit(1)

    time_diff = (end_time - start_time).total_seconds()
    if time_diff <= 0:
        print("End time must be later than start time.")
        sys.exit(1)

    # Generate log entries
    with open("access.log", "w") as log_file:
        for i in range(num_entries):
            # Distribute events evenly within the time frame
            timestamp = start_time + timedelta(seconds=(i / num_entries) * time_diff)
            log_entry = generate_apache_log_entry(timestamp.strftime("%d/%b/%Y:%H:%M:%S %z"))
            log_file.write(log_entry + "\n")
            print(log_entry)

    # Statistics
    with open("access.log", "r") as log_file:
        log_lines = log_file.readlines()

    ip_counts = {}
    for line in log_lines:
        ip = line.split()[0]
        if ip in feodotracker_abuse_ch:
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

    total_entries = len(log_lines)
    stats_output = []
    stats_output.append("Statistics:")
    stats_output.append(f"Total log entries: {total_entries}")
    stats_output.append("Log entries from feodotracker_abuse_ch:")
    for ip, count in ip_counts.items():
        stats_output.append(f"{ip}: {count} ({(count / total_entries) * 100:.2f}%)")

    # Save statistics to file
    with open("access_stats.txt", "w") as stats_file:
        stats_file.write("\n".join(stats_output))

    # Print statistics
    print("\n".join(stats_output))

if __name__ == "__main__":
    main()
