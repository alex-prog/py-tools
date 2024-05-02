#!/usr/bin/env python3

import random
import time
import json
import argparse

# Function to generate a random log entry
def generate_log_entry():
    log_types = ['Error', 'Warning', 'Information']
    sources = ['Application', 'Security', 'System']
    messages = [
        'Failed to start service.',
        'Disk space running low.',
        'User logged in successfully.',
        'Critical error encountered.',
        'Network connection lost.'
    ]
    return {
        'Type': random.choice(log_types),
        'Source': random.choice(sources),
        'Message': random.choice(messages),
        'EventID': random.randint(1000, 9999),
        'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }

# Function to write logs to a file in .evtx format
def write_evtx_logs(num_logs, filename='windows_logs.evtx'):
    with open(filename, 'a') as file:
        for _ in range(num_logs):
            log_entry = generate_log_entry()
            log_str = f"<Event xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\">\n"
            log_str += f"  <System>\n"
            log_str += f"    <Provider Name=\"{log_entry['Source']}\"/>\n"
            log_str += f"    <EventID>{log_entry['EventID']}</EventID>\n"
            log_str += f"    <Level>{log_entry['Type']}</Level>\n"
            log_str += f"    <TimeCreated SystemTime=\"{log_entry['Timestamp']}\"/>\n"
            log_str += f"  </System>\n"
            log_str += f"  <EventData>\n"
            log_str += f"    <Data>{log_entry['Message']}</Data>\n"
            log_str += f"  </EventData>\n"
            log_str += f"</Event>\n"
            file.write(log_str)

# Function to write logs to a file in .json format
def write_json_logs(num_logs, filename='windows_logs.json'):
    logs = []
    for _ in range(num_logs):
        log_entry = generate_log_entry()
        logs.append(log_entry)
    with open(filename, 'w') as file:
        json.dump(logs, file, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate fake Windows logs.')
    parser.add_argument('format', choices=['evtx', 'json'], help='Choose the log format (evtx or json)')
    parser.add_argument('--num-logs', type=int, default=10, help='Number of logs to generate (default: 10)')
    args = parser.parse_args()

    if args.format == 'evtx':
        write_evtx_logs(args.num_logs)
        print(f"{args.num_logs} logs generated successfully in .evtx format.")
    elif args.format == 'json':
        write_json_logs(args.num_logs)
        print(f"{args.num_logs} logs generated successfully in .json format.")
