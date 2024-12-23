# Matomo Utilities Scripts

This repository contains three Python scripts designed to interact with a Matomo analytics instance. These scripts help automate tasks such as managing segments, deleting users, and retrieving custom reports. Below is an overview of each script and how to use them.

---

## 1. `segment.py`

### Purpose
The `segment.py` script fetches segment data for specified `idSite` values from a Matomo instance and saves it as a CSV file.

### Features
- Retrieves all segments for specified sites.
- Processes segment data and checks for important fields like `idsegment`, `name`, and `enable_only_idsite`.
- Outputs the data into a `segment_data.csv` file for further analysis.

### How to Use
1. Run the script using Python.
2. Provide the following inputs:
   - Matomo instance URL (e.g., `https://your-matomo-instance/index.php`).
   - Matomo `token_auth` (authentication token).
   - A comma-separated list of `idSite` values (e.g., `1,2,3`).
3. The script will fetch and save the segment data as `segment_data.csv`.

---

## 2. `delete.py`

### Purpose
The `delete.py` script deletes specified users from a Matomo instance.

### Features
- Deletes users based on their usernames.
- Optionally supports password confirmation if required by your Matomo instance.

### How to Use
1. Run the script using Python.
2. Provide the following inputs:
   - Matomo instance URL (e.g., `https://your-matomo-instance/index.php`).
   - Matomo `token_auth` (authentication token).
   - A comma-separated list of usernames to delete (e.g., `user1,user2,user3`).
   - (Optional) Password confirmation.
3. The script will attempt to delete each specified user and print the result.

---

## 3. `customreports.py`

### Purpose
The `customreports.py` script retrieves custom report configurations for specified `idSite` values and saves them to a CSV file.

### Features
- Fetches custom reports as XML data and parses it.
- Extracts details such as `idcustomreport` and `name`.
- Outputs the data into a `custom_reports_data.csv` file.

### How to Use
1. Run the script using Python.
2. Provide the following inputs:
   - Matomo instance URL (e.g., `https://your-matomo-instance/index.php`).
   - Matomo `token_auth` (authentication token).
   - A comma-separated list of `idSite` values (e.g., `1,2,3`).
3. The script will fetch and save the custom report data as `custom_reports_data.csv`.

---

## Prerequisites

- Python 3.x
- Libraries: `requests`, `pandas`, `xml.etree.ElementTree`
  - Install the required libraries using pip: `pip install requests pandas`

---

## Notes

- Ensure your `token_auth` has sufficient permissions to perform the desired actions (e.g., admin privileges may be required).
- Carefully validate inputs like `idSite` or usernames to avoid unintended data modifications.

---

If you have any questions or need support, feel free to reach out.
