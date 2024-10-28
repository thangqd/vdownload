import os
import sys
import subprocess
import platform
import json
from datetime import datetime, timedelta

def load_country_bbox(country_code):
    # Path to the JSON file containing bounding boxes
    bbox_file = os.path.join(os.path.dirname(__file__), 'countries_bbox.json')
    with open(bbox_file, 'r') as f:
        countries_bbox = json.load(f)
    
    # Look up the bounding box by country code
    bbox = countries_bbox.get(country_code.upper())
    if not bbox:
        print(f"Error: Country code {country_code} not found in countries_bbox.json.")
        sys.exit(1)
    
    # Format the bounding box as expected by the pmtiles command
    sw = bbox["sw"]
    ne = bbox["ne"]
    return f"{sw['lon']},{sw['lat']},{ne['lon']},{ne['lat']}"

def get_default_input_url():
    # Get the current date and subtract one day
    previous_date = datetime.now() - timedelta(days=1)
    return f"https://build.protomaps.com/{previous_date.strftime('%Y%m%d')}.pmtiles"

def run_pmtiles():
    # Determine the appropriate binary based on the operating system
    if platform.system() == 'Windows':
        binary = os.path.join(os.path.dirname(__file__), 'pmtiles.exe')
    else:
        binary = os.path.join(os.path.dirname(__file__), 'pmtiles')

    # Check for existing arguments
    args = sys.argv[1:]

    # Ensure that at least one command is provided
    if not args:
        print("Error: You must specify a command (e.g., convert, show, tile, extract, verify, serve, upload, version).")
        sys.exit(1)

    # Handle the 'extract' command specifically
    if args[0] == 'extract':
        # Ensure there's an output file argument present
        if len(args) < 3:
            print("Error: You must specify an input file and an output file.")
            sys.exit(1)

        # Set the default input URL if not provided
        input_url = get_default_input_url()
        if not any(arg.startswith("https://") for arg in args):
            # Insert the URL after the extract command
            args.insert(1, input_url)

        # Check if '--country' is in the arguments and convert it to a bounding box
        if '--country' in args:
            country_index = args.index('--country') + 1
            if country_index < len(args):
                country_code = args[country_index]
                bbox = load_country_bbox(country_code)
                # Replace '--country <code>' with '--bbox=<bbox>'
                args[country_index - 1:country_index + 1] = [f'--bbox={bbox}']
                print(f'Bounding box for {country_code} is: {bbox}')
                print(f'Default URL to extract: {input_url}. Download in progress...')
            else:
                print("Error: Please provide a country code after '--country'.")
                sys.exit(1)

    # Run the binary with modified arguments
    subprocess.run([binary] + args)

# Uncomment the following line to allow the script to run directly
# if __name__ == '__main__':
#     run_pmtiles()
