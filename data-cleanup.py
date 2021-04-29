import csv
import json

# Helper function for retrieving the year from the dataset
def get_year( item ):
    return item["Year"]

# Convert CSV files to a dictionary

data = {}

with open( "MPVDatasetDownload.csv", encoding = "utf-8" ) as csvf:
    csvReader = csv.DictReader(csvf)
    key = 0
    for rows in csvReader:
        key += 1
        data[key] = rows

stats = []
statuses_charges = []

for index in data:
    year = "20" + data[index]["Date of Incident (month/day/year)"][-2:]

    # Skip data for 2021 that's still in progress

    if year != "2021":
        years_processed = map( get_year, stats )

        if year not in years_processed:
            stats.append ( {
                "Year": year,
                "Killings": 0,
                "Charges": 0,
                "Convictions": 0
            } )

            current_index = len( stats ) - 1
        else:
            for i, item in enumerate( stats ):
                if stats[i]["Year"] == year:
                    current_index = i

        if stats[current_index]["Charges"] not in statuses_charges:
            statuses_charges.append( stats[current_index]["Charges"] )

        stats[current_index]["Killings"] += 1

        if "Charged" in data[index]["Criminal Charges?"]:
            stats[current_index]["Charges"] += 1

        if "Charged, Convicted" in data[index]["Criminal Charges?"]:
            stats[current_index]["Convictions"] += 1

stats.reverse()

print( json.dumps( stats, indent = 4, sort_keys=True ) )

# Save the dataset to a CSV file
    
data_file = open( "data-summary.csv", "w" )
csv_writer = csv.writer( data_file )
count = 0

for item in stats:
    if count == 0:
        header = item.keys()
        csv_writer.writerow( header )
        count += 1
  
    csv_writer.writerow( item.values() )
  
data_file.close()
