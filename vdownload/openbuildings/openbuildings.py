import csv
import requests
import sys
from tqdm import tqdm
from io import StringIO

def get_url(tile_id):
    """Construct the URL for the given tile_id."""
    return f"https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/{tile_id}_buildings.csv.gz"

def download_tile(tile_id, country_name):
    """Download the tile in chunks and save it to disk."""
    tile_url = get_url(tile_id)
    
    # Stream the request so it doesn't download the whole file at once
    response = requests.get(tile_url, stream=True)
    
    if response.status_code == 200:
        # Get the total file size from the Content-Length header for the progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Create a filename based on the country name and tile_id
        filename = f"{country_name}_{tile_id}.csv.gz"
        
        # Open the file in write-binary mode and download in chunks
        with open(filename, "wb") as tile_file, tqdm(
            desc=f"Downloading {filename}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    tile_file.write(chunk)
                    progress_bar.update(len(chunk))
                    
        return True  # Successfully downloaded
    else:
        print(f"Failed to download tile: {tile_id}, Status Code: {response.status_code}")
        return False  # Failed to download

def download_tiles_for_country(country_identifier):
    """Download tiles for a country based on its name or ISO code."""
    tiles_to_download = []
    country_name = ""
    csv_url = "https://raw.githubusercontent.com/thangqd/vdownload/refs/heads/main/vdownload/openbuildings/s2countries.csv"
    
    # Fetch the CSV from the online source
    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Failed to retrieve s2countries.csv, Status Code: {response.status_code}")
        return
    
    # Parse the CSV data from the response content
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(StringIO(csv_content))

    # Find tiles for the given country identifier (name or iso)
    for row in csv_reader:
        if row['name'].lower() == country_identifier.lower() or row['iso'].lower() == country_identifier.lower():
            country_name = row['name']  # Get the country name for naming files
            tiles_to_download.append(row['tile_id'])

    if not tiles_to_download:
        print(f"No tiles found for country: {country_identifier}")
        return

    # Download each tile for the country, displaying a progress bar for each tile
    print(f"Downloading {len(tiles_to_download)} tiles for {country_name}...")
    for tile_id in tqdm(tiles_to_download, desc=f"Downloading tiles for {country_name}", unit="tile"):
        download_tile(tile_id, country_name)

def main():
    """Main function to handle input and trigger tile downloads."""
    if len(sys.argv) != 2:
        print("Usage: openbuildings <country_name_or_iso>")
        sys.exit(1)

    country_identifier = sys.argv[1]
    download_tiles_for_country(country_identifier)

if __name__ == "__main__":
    main()
