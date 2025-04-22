import os
import wget

# URL of your local Django app
site_url = "http://127.0.0.1:8000"  # Replace with your Django app's URL if different

# Directory to save downloaded files
output_dir = "static_site"
os.makedirs(output_dir, exist_ok=True)

# Download the main page
html_file = wget.download(site_url, out=output_dir)
print(f"\nDownloaded: {html_file}")
