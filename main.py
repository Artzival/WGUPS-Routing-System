#Student ID: 012302297
#Author: Andrew Wilson

import csv

#importing the distance table and address list CSV files
with open("CSVdata/distance_table_CSV.csv") as distCSV:
    DistanceCSV = csv.reader(distCSV)
    DistanceCSV = list(DistanceCSV)
with open("CSVdata/address_list_CSV.csv",mode='r',newline='') as addrCSV:
    AddressCSV = csv.reader(addrCSV)
    address_list = []
    for row in AddressCSV:
        address_list.append(row[1])

#TODO: Find out if this class is even needed
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
            if itemkey[0] == key:
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

    #algorithm to find distance between 2 addresses
    def distanceBetween(self, row_value, column_value):
        #take current location, then iterate through address of each package in truck, then find whichever is shortest and choose that one
        distance = DistanceCSV[row_value][column_value]
        if distance == '':
            distance = DistanceCSV[row_value][column_value]
        print(float(distance))

    #class method that returns the delivery address of a package given its unique ID
    @classmethod
    def addressGetter(cls, ID):
        packaddress = packageTable.get(ID)
        location = address_list.index(packageTable.get(ID).address)
        return location



#creating a hashtable object for the packages
packageTable = HashTable(40)

#parses package CSV file and loads it into Package Class
def parsePackages(package_file):
    with open(package_file) as packCSV:
        packageInfo = csv.reader(packCSV)
        next (packageInfo, None)
        for package in packageInfo:
            packID = int(package[0])
            pack_address = package[1]
            pack_city = package[2]
            pack_zip = package[4]
            pack_deadline = package[5]
            pack_weight = package[6]
            pack_status = "At WGU shipment facility"

            #puts csv packages into Package class and then into packageTable
            pack = Package(packID, pack_address, pack_city, pack_zip,pack_deadline, pack_weight, pack_status)
            packageTable.insert(packID, pack)

#truck class
class Truck:
    def __init__(self, locationID, departure_time, packages):
        self.speedMPH = 18
        self.locationID = int(locationID)
        self.departure_time = departure_time
        self.packages = packages
        self.distance_travelled = 0

    def load(self, packages):
        self.packages = packages

    def listPackages(self):
        return self.packages

    def nextAddress(self):
        lowest_dist = 100.0
        shortestPackage = None
        distance = None
        for item in self.packages:
            #call distanceBetween for locationID and Package.addressGetter(ID)
            distance = DistanceCSV[Package.addressGetter(item)][self.locationID]
            #if distance == '':
                #distance = DistanceCSV[Package.addressGetter(item)][self.locationID]
            distance = float(distance)
            if distance < lowest_dist:
                lowest_dist = distance
                shortestPackage = item
        self.distance_travelled += lowest_dist
        self.packages.remove(shortestPackage)
        print(shortestPackage)
        print(distance)
        print(lowest_dist)
#lowest_distance = 100
#distance = 2.2
#if 2.2 is less than 100, which it is, then lowest distance is now 2.2 and the shortest package is package 1
#then why is it showest the shortest package to be 21 with a distance of 7.2
        #TODO: add passage of time

        #take as input the current location id
        # run the distanceBetween for each package in the list
        #need to convert packages in list to their address




#creates trucks and loads them with packages
truck1 = Truck(0, "8:00 AM", [1,2,4,5,7,8,10,11,12,17,21,22,23,24,26,27])
truck2 = Truck(0, "8:00 AM", [3,13,14,15,16,18,19,20,29,30,31,33,34,35,36,38])
truck3 = Truck(0, "10:00 AM", [6,9,25,28,32,37,39,40])

#TODO: call trucks to begin delivering
#TODO: create output for user interface

#loads package csv data:
parsePackages("CSVdata/packages_CSV.csv")


#updates package #9 address to 410 S. State St., Salt Lake City, UT 84111
package9 = Package(9, "410 S State St", "Salt Lake City", 84111, "EOD", 2, "At WGU shipment facility")
packageTable.insert(9, package9)

print(packageTable.get(1))
print(Package.addressGetter(1))
print(truck1.locationID)
truck1.nextAddress()
print(packageTable.get(9))