#Student ID: 012302297
#Author: Andrew Wilson

import csv

#importing the distance table and address list CSV files

with open("CSVdata/distance_table_CSV.csv") as distCSV:
    DistanceCSV = csv.reader(distCSV)
    DistanceCSV = list(DistanceCSV)
with open("CSVdata/address_list_CSV.csv") as addrCSV:
    addressDict = []
    AddressCSV = csv.DictReader(addrCSV)
    for row in AddressCSV:
        addressDict.append(row)


#creating the class for the packages in the hash table
class Package:
    def __init__(self, ID, address, city, zip, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status

        #creating the __str__ method to provide output for package status
    def __str__(self):
        return f"Package ID {self.ID}'s status is {self.status}. {self.address}, {self.city}, {self.zip}, {self.deadline}, {self.weight}"

#creating class for each node of hash table
class HashTableNode:
    def __init__(self, node_key, node_value):
        self.node_key = node_key
        self.node_value = node_value
        self.next = None

#creating the class for the chaining hash table
class HashTable:
    def __init__(self, size):
        self.size = 40
        self.table = []
        for i in range(size):
            self.table.append([])

#ensure non-negative hash code
    def hash(self, key):
        return abs(hash(key))

#insert method
    def insert(self, key, value):
        #hash key to compute bucket
        bucket = self.hash(key) % len(self.table)
        #search linked list for value. if value exists, update it, if not, append to end of linked list
        current_item = self.table[bucket]
        previous_item = None
        #search for key in bucket and update
        for itemkey in current_item:
            if itemkey == key:
                itemkey[1] = value
                return True
        #add to end of chain if not in bucket
        keyvalue = [key, value]
        current_item.append(keyvalue)
        return True



#remove method
    def remove(self, key):
        #hash the key to compute bucket
        bucket = self.hash(key) % len(self.table)
        #search linked list within bucket for key
        current_item = self.table[bucket]
        previous_item = None
        for key in current_item:
            current_item.remove(key)

    #get method - searches for a key and returns associated value, or None if no value found
    def get(self, key):
        #hashes key to compute bucket
        bucket = self.hash(key) % len(self.table)
        #search linked list for key
        current_item = self.table[bucket]
        #search for key in bucket
        for itemkey in current_item:
            if itemkey[0] == key:
                return itemkey[1]
        return "Package not found!"


#creating a hashtable object for the packages
packageTable = HashTable(40)

#parses package CSV file and loads it into Package Class
def parsePackages(packageFile):
    with open(packageFile) as packCSV:
        packageInfo = csv.reader(packCSV)
        next (packageInfo, None)
        for package in packageInfo:
            packID = int(package[0])
            packAddress = package[1]
            packCity = package[2]
            packZip = package[4]
            packDeadline = package[5]
            packWeight = package[6]
            packStatus = "At WGU shipment facility"

            #puts csv packages into Package class and then into packageTable
            pack = Package(packID, packAddress, packCity, packZip,packDeadline, packWeight, packStatus)
            packageTable.insert(packID, pack)



#TODO: create truck class
class Truck:
    def __init__(self, locationID, departure_time, packages):
        self.speedMPH = 18
        self.locationID = locationID
        self.departure_time = departure_time
        self.packages = packages
        self.distance_travelled = 0

    def load(self, packages):
        self.packages = packages

    #TODO: algorithm to find closest address and begin travel
    def nextAddress(self):
        #take current location, then iterate through address of each package in truck, then find whichever is shortest and choose that one

        return True


#TODO: call trucks to begin delivering

truck1 = Truck("At WGU facility", "8:00 AM", [1,2,4,5,7,8,10,11,12,17,21,22,23,24,26,27])
truck2 = Truck("At WGU facility", "8:00 AM", [3,13,14,15,16,18,19,20,29,30,31,33,34,35,36,38])
truck3 = Truck("At WGU facility", "10:00 AM", [6,9,25,28,32,37,39,40])

#TODO: create output for user interface

#loads package csv data:
parsePackages("CSVdata/packages_CSV.csv")

print(packageTable.get(1))