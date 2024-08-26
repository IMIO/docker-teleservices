import logging
import os
import csv
import requests
import subprocess
from logging.handlers import SysLogHandler

# Setup logging
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

# File handler for logging to a file
file_handler = logging.FileHandler("/var/tmp/download_log.txt")
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
            logger.info(f"Successfully downloaded and saved {save_path}")
            return save_path
        else:
            logger.error(f"Failed to download {filename}. Status code: {response.status_code}")
            print(f"Failed to download {filename}. Status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"An error occurred while downloading {filename}: {e}")
        print(f"An error occurred while downloading {filename}: {e}")
        return None


def ods_to_csv(ods_path, csv_path):
    """Convert an ODS file to CSV using LibreOffice in command line"""
    try:
        # Commande pour convertir ODS en CSV
        command = ["libreoffice", "--headless", "--convert-to", "csv", "--outdir", os.path.dirname(csv_path), ods_path]
        subprocess.run(command, check=True)
        logger.info(f"Successfully converted {ods_path} to CSV")

        # Post-process the CSV to ensure UTF-8 encoding and change delimiter to '|'
        temp_csv_path = csv_path + ".tmp"
        with open(csv_path, mode="r", encoding="ISO-8859-1") as infile, open(
            temp_csv_path, mode="w", encoding="UTF-8", newline=""
        ) as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile, delimiter="|")
            for row in reader:
                writer.writerow(row)

        os.replace(temp_csv_path, csv_path)
        logger.info(f"Successfully re-encoded {csv_path} to UTF-8 with '|' delimiter")

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while converting {ods_path} to CSV: {e}")
        print(f"An error occurred while converting {ods_path} to CSV: {e}")
    except Exception as e:
        logger.error(f"An error occurred during post-processing of {csv_path}: {e}")
        print(f"An error occurred during post-processing of {csv_path}: {e}")


# Main execution
if __name__ == "__main__":
    filenames = ["commande_de_tickets_repas_nightly_export.ods", "commande_de_cartes_de_garderie_nightly_export.ods"]
    csv_filenames = [
        "commande_de_tickets_repas_nightly_export.csv",
        "commande_de_cartes_de_garderie_nightly_export.csv",
    ]

    for url, filename, csv_filename in zip(urls, filenames, csv_filenames):
        ods_path = download_and_save_ods(url, filename)
        if ods_path:
            ods_to_csv(ods_path, f"/var/tmp/{csv_filename}")
