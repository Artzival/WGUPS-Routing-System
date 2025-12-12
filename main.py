#Author: Andrew Wilson
#Student ID: 012302297

import csv

#importing the distance table and address list CSV files

with open("CSVdata/distance_table_CSV.csv") as distCSV:
    DistanceCSV = csv.reader(distCSV)
    DistanceCSV = list(DistanceCSV)
with open("Csvdata/address_list_CSV.csv") as addrCSV:
    AddressCSV = csv.reader(addrCSV)
    AddressCSV = list(AddressCSV)

#TODO: Create hash table

#TODO: Create package class

#TODO: parse package CSV and load it into package class

#TODO: create truck class
