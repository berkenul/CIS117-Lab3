# CIS-117 Lab3
# Reads country_full.csv and writes a CSV file for each region.
# Alex Sett and Berk Enul
# Group: 1
# Alex worked on reading and grouping the data.
# Berk worked on writing the output files.

import csv
import os


def read_countries_by_region(filename="country_full.csv"):
    """Read the CSV and group the countries by region."""
    countries_by_region = {}

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            fields = reader.fieldnames or []

            # check that the file has name and region columns
            if "name" not in fields or "region" not in fields:
                print("Error: The file must have 'name' and 'region' columns.")
                return {}

            for row in reader:
                name = (row["name"] or "").strip()
                region = (row["region"] or "").strip()

                # skip rows with no region (Antarctica)
                if not name or not region:
                    continue

                # add the country to its region
                if region not in countries_by_region:
                    countries_by_region[region] = []

                countries_by_region[region].append({"name": name, "region": region})

        return countries_by_region

    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
    except PermissionError:
        print(f"Error: No permission to read {filename}.")
    except csv.Error as error:
        print(f"Error: Could not read the CSV data: {error}")
    except UnicodeError as error:
        print(f"Error: Could not decode the file: {error}")
    except OSError as error:  # OSError covers IOError too in python 3
        print(f"Error: Could not open/read the file: {error}")

    return {}


def write_region_files(countries_by_region):
    """Write the country names and regions to separate CSV files."""
    try:
        os.makedirs("output", exist_ok=True)

        # make a file for each region
        for region, countries in countries_by_region.items():
            filename = os.path.join("output", region + ".CSV")
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "region"])
                writer.writeheader()
                writer.writerows(countries)

            print(f"Created {filename}")

    except PermissionError as error:
        print(f"Error: No permission to write {error.filename}.")
    except OSError as error:
        print(f"Error: Could not write the output files: {error}")
    except csv.Error as error:
        print(f"Error: Could not write the CSV data: {error}")


if __name__ == "__main__":
    regions = read_countries_by_region()
    if regions:
        write_region_files(regions)
