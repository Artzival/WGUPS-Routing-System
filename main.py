#Student ID: 012302297
#Author: Andrew Wilson

import csv
from operator import truediv

#importing the distance table and address list CSV files

with open("CSVdata/distance_table_CSV.csv") as distCSV:
    DistanceCSV = csv.reader(distCSV)
    DistanceCSV = list(DistanceCSV)
with open("Csvdata/address_list_CSV.csv") as addrCSV:
    AddressCSV = csv.reader(addrCSV)
    AddressCSV = list(AddressCSV)

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
            return "Package ID" + self.id + "'s status is " + self.status

#creating class for each node of hash table
class HashTableNode:
    def __init__(self, node_key, node_value):
        self.node_key = node_key
        self.node_value = node_value
        #self.next = None

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
        self.table[bucket] = HashTableNode(key, value)

#remove method
    def remove(self, key):
        #hash the key to compute bucket
        bucket = self.hash(key) % len(self.table)
        #search linked list within bucket for key
        current_item = self.table[bucket]
        previous_item = None
        while current_item != None:
            if current_item.key == key:
                if previous_item == None:
                    #if first item is key, remove first item in list
                    self.table = current_item.next
                else:
                    #directs linked list to skip item, effectively removing it
                    previous_item.next = current_item.next
                return True
            previous_item = current_item
            current_item = current_item.next
        return False

    #get method - searches for a key and returns associated value
    def get(self, key):
        #hashes key to compute bucket
        bucket = self.hash(key) % len(self.table)
        #search linked list for key
        item = self.table[bucket]
        while item != None:
            if key == item.key:
                return item.value
            item = item.next

        return None


#parses package CSV file and loads it into Package Class
def parsePackages(packageFile):
    with open(packageFile) as packCSV:
        packageInfo = csv.reader(packCSV)
        next (packageInfo)
        for package in packageInfo:
            packID = int(package[0])
            packAddress = package[1]
            packCity = package[2]
            packZip = package[4]
            packDeadline = package[5]
            packWeight = package[6]
            packStatus = "At WGU shipment facility"

#TODO: create truck class
class Trucks:
    def __init__(self):
        self.trucks = []

