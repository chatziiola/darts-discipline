#!/usr/local/bin/python3
import sys
import argparse
import yaml
import time
import os

# Defaults to 5 min
practiceTime = 300
location = "home"
numberOfDarts = 3
logFolder = "./logs/"
debug = False
verbose = False

def checkFile(logFile):
    # Check if divergence.yaml exists, if not, create it as a blank file
    logPath = os.path.join(logFolder,logFile)
    if not os.path.isfile(logPath):
        with open(logPath, 'a') as file:
            file.write("")

def initial_config():
    global numberOfDarts, logFolder, location
    if debug: print("initial config")
    config_file = "darts.yaml"
    if os.path.isfile(config_file):
        if debug: print(f"Opened {config_file}")
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            if "numberOfDarts" in config:
                # Set numberOfDarts if present in the config file
                numberOfDarts = config["numberOfDarts"]
                if debug: print(f"Setting numberOfDarts to: {numberOfDarts}")
                # You can set the numberOfDarts variable or use it as needed
            if "location" in config:
                # Set location if present in the config file
                location = config["location"]
                if debug: print(f"Setting location to: {location}")
                # You can set the location variable or use it as needed
            if "logFolder" in config:
                # Set location if present in the config file
                logFolder = config["logFolder"]
                logFolder = os.path.expanduser(logFolder)
                if debug: print(f"Setting logFolder to: {logFolder}")
    else:
        print("No darts.yaml file found. Using default settings.")
    os.makedirs(logFolder,exist_ok=True)
    for logFile in {"divergence.yaml", "301.yaml", "501.yaml"}:
        checkFile(logFile)


def div_darts():
    print(f"Starting for {practiceTime/60} min")
    rounds = 0
    min_divergence = float('inf')
    max_divergence = float('-inf')
    total_divergence = 0

    start_time = time.time()
    end_time = start_time + practiceTime

    while time.time() < end_time:
        print(f"{round(end_time- time.time(),3)} seconds left")
        divergence_input = input("Enter divergence (or 'end' to finish): ")
        if divergence_input.lower() == "end":
            end_time = time.time()
            break
        try:
            divergence = int(divergence_input)
            rounds += 1
            total_divergence += divergence
            min_divergence = min(min_divergence, divergence)
            max_divergence = max(max_divergence, divergence)
        except ValueError:
            print("Invalid input. Please enter an integer or 'end'.")

    median_divergence = total_divergence / rounds if rounds > 0 else 0

    # Create a new entry in divergence.yaml
    current_time = time.strftime("%y%m%d%H%M_%A")
    divergence_file = os.path.join(logFolder, "divergence.yaml")
    entry = {
        "Location": location,
        "Number of Darts": numberOfDarts,
        "Duration": "{:.3f}".format(end_time - start_time),
        "Rounds": rounds,
        "Median Divergence": median_divergence,
        "Minimum Divergence": min_divergence,
        "Maximum Divergence": max_divergence
        }
 
    # Print the entry information
    print("Good job! This session's stats:")
    for key, value in entry.items():
        print(f"{key}: {value}")   

    with open(divergence_file, "a") as file:
        yaml.dump({current_time: entry}, file)

    if debug: print("Divergence data saved.")


def too_darts():
    print("Running too-darts()")
    # Add your too-darts logic here

def foo_darts():
    print("Running foo-darts()")
    # Add your foo-darts logic here

def main():

    parser = argparse.ArgumentParser(description="Command line tool for running specific commands")
    parser.add_argument("command", choices=["div", "301", "501"], help="Select a command: div, 301, or 501")
    parser.add_argument("--time", help="Optional time argument")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")


    args = parser.parse_args()

    global debug
    debug = args.debug
    if debug:
        print("Starting in debug mode")

    global verbose
    verbose = args.verbose
    if debug:
        print("Starting in verbose mode")

    initial_config()

    command = args.command

    global practiceTime
    if args.time:
        try:
            # Parse the time argument if provided
            practiceTime = int(args.time[:-3])  # Extracting the numerical part from the time string
            time_unit = args.time[-3:]  # Extracting the unit part from the time string
            if time_unit == "min":
                practiceTime *= 60  
            elif time_unit == "hr":
                practiceTime *= 360
        except ValueError:
            print("Invalid time argument. Please provide time in the format '5min'.")

    if command == "div":
        div_darts()
    elif command == "301":
        too_darts()
    elif command == "501":
        foo_darts()

if __name__ == "__main__":
    main()
