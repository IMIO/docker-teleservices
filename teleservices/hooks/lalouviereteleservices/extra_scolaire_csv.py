import logging
import os
from logging.handlers import SysLogHandler

import requests

# Setup logging
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

# File handler for logging to a file
file_handler = logging.FileHandler("download_log.txt")
file_handler.setFormatter(log_formatter)

# Syslog handler for logging to /var/log/syslog
syslog_handler = SysLogHandler(address="/dev/log")
syslog_handler.setFormatter(log_formatter)

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(syslog_handler)

# URLs to download the .ods files from
urls = [
    "https://lalouviere-formulaires.guichet-citoyen.be/api/forms/commande-de-tickets-repas/csv-pour-david/ods",
    "https://lalouviere-formulaires.guichet-citoyen.be/api/forms/commande-de-cartes-de-garderie/csv-pour-export/ods",
]


def download_and_save_ods(url, filename):
    """Download the .ods file from the given URL and save it to /var/tmp/"""
    try:
        ts_api_key = os.environ.get("TS_API_KEY")
        ts_api_identifier = os.environ.get("TS_API_IDENTIFIER")

        response = requests.get(url, auth=(ts_api_identifier, ts_api_key))

        if response.status_code == 200:
            save_path = f"/var/tmp/{filename}"
            with open(save_path, "wb") as file:
                file.write(response.content)
            logging.info(f"Successfully downloaded and saved {save_path}")
        else:
            logging.error(f"Failed to download {save_path}. Status code: {response.status_code}")
            print(f"Failed to download {save_path}. Status code: {response.status_code}")

    except Exception as e:
        logging.error(f"An error occurred while downloading {save_path}: {e}")
        print(f"An error occurred while downloading {save_path}: {e}")


# Main execution
if __name__ == "__main__":
    filenames = ["commande_de_tickets_repas_nightly_export.ods", "commande_de_cartes_de_garderie_nightly_export.ods"]

    for url, filename in zip(urls, filenames):
        download_and_save_ods(url, filename)
