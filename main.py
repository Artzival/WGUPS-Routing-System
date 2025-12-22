#Student ID: 012302297
#Author: Andrew Wilson

import csv
from datetime import timedelta, datetime

#importing the distance table and address list CSV files
with open("CSVdata/distance_table_CSV.csv") as distCSV:
    DistanceCSV = csv.reader(distCSV)
    DistanceCSV = list(DistanceCSV)
with open("CSVdata/address_list_CSV.csv",mode='r',newline='') as addrCSV:
    AddressCSV = csv.reader(addrCSV)
    address_list = []
    for row in AddressCSV:
        address_list.append(row[1])

#creating the class for the chaining hash table that will store the package objects
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

    #get method - searches for a key and returns associated value, or a message if no value found
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

#Package class that stores all package info
class Package:
    def __init__(self, ID, address, city, zip, deadline, weight, status, note):
        self.ID = ID
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        #ensuring notes aren't empty for cleaner __str__ output
        if note == "":
            self.note = "N/A"
        else:
            self.note = note
        self.departure_time = None
        self.delivery_time = None

        #Requirement B: lookup function to return data components of package given its ID:
    def __str__(self):
        if self.status =="Delivered!":
            #returns delivery time if package has been delivered already
            return (
                f"Package ID {self.ID}'s status is {self.status}. Delivery address is {self.address}, {self.city}, {self.zip}, by {self.deadline}. Weight is {self.weight} pounds. The package note is: {self.note}. \n"
                f"Package was delivered at {self.delivery_time.strftime("%H:%M")}")
        else:
            return (f"Package ID {self.ID}'s status is {self.status}. Delivery address is {self.address}, {self.city}, {self.zip}, by {self.deadline}. Weight is {self.weight} pounds. The package note is: {self.note}.")

    #method to fing status of package at any given time:
    def statusTime(self, timePassed):
        if self.delivery_time == None:
            self.status = "At WGU shipment facility"
        elif timePassed < self.departure_time:
            self.status = "At WGU shipment facility"
        elif timePassed < self.delivery_time:
            self.status = "In transit"
        else:
            self.status = "Delivered!"

    #class method that returns the delivery address of a package given its unique ID
    @classmethod
    def addressGetter(cls, ID):
        packaddress = packageTable.get(ID)
        location = address_list.index(packageTable.get(ID).address)
        return location

#creates a hashtable object for the packages
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
            pack_note = package[7]
            pack_status = "At WGU shipment facility"

            #puts csv packages into Package class and then into packageTable
            pack = Package(packID, pack_address, pack_city, pack_zip,pack_deadline, pack_weight, pack_status, pack_note)
            packageTable.insert(packID, pack)

#truck class
class Truck:
    def __init__(self, locationID, departure_time, packages):
        self.speedMPH = 18
        self.locationID = int(locationID)
        self.departure_time = departure_time
        self.packages = packages
        self.distance_travelled = 0
        #the time passed is saved as timedelta so we can add it to the datetime value of the current time
        self.time_elapsed = timedelta(hours=0, minutes=0)

    #this is the greedy algorithm that locates the nearest package address and causes the truck to "deliver" it
    def nextAddress(self):
        #updates status of packages in truck to "in transit"
        for item in self.packages:
            packageTable.get(item).status = "In transit"
        lowest_dist = 100.0
        shortestPackage = None
        distance = None
        while len(self.packages) > 0:
            for item in self.packages:
                #using the distance chart CSV file, find distance between current location and the address of each package:
                distance = DistanceCSV[Package.addressGetter(item)][self.locationID]
                distance = float(distance)
                #if the current package needs to be delivered by an early deadline, prioritize it
                if item in [1,6,13,14,15,16,20,25,29,30,31,34,37,40]:
                    lowest_dist = distance
                    shortestPackage = item
                    break
                #if the current package's distance is less than the previous shortest distance, record it as the shortest instead
                if distance < lowest_dist:
                    lowest_dist = distance
                    #keep note of which package is the shortest distance away:
                    shortestPackage = item
            #add the distance of this package to the truck's total distance traveled
            self.distance_travelled += lowest_dist
            #remove package from truck, 'delivering' it
            self.packages.remove(shortestPackage)
            #update package departure time to truck departure time
            packageTable.get(shortestPackage).departure_time = self.departure_time
            #update status to delivered
            packageTable.get(shortestPackage).status = "Delivered"
            #calculates time elapsed while delivering packages and saves it to class variable
            time_passed = timedelta(hours = lowest_dist / self.speedMPH)
            self.time_elapsed += time_passed
            # update package delivery time
            packageTable.get(shortestPackage).delivery_time = self.departure_time + time_passed
            #reset values to run the while loop again until packages list is empty
            shortestPackage = None
            lowest_dist = 100
            distance = None

#creates trucks and loads them with packages
truck1 = Truck(0, datetime(2025,12,21,8,0), [13,14,15,16,19,20,29,30,31,34,37,40]) #12 packages
truck2 = Truck(0, datetime(2025,12,21,9,10), [1,3,6,18,25,28,32,33,35,36,38,39]) #12 packages
truck3 = Truck(0, None, [2,4,5,7,8,9,10,11,12,17,21,22,23,24,26,27]) #16 packages

current_time = datetime(year=2025,month=12,day=21,hour=8, minute=0)

#function to show current time
def printCurrTime():
    now = current_time.strftime("%H:%M")
    print(now)

#loads package csv data:
parsePackages("CSVdata/packages_CSV.csv")

#calls trucks to deliver!
truck1.nextAddress()
truck2.nextAddress()
current_time += max(truck1.time_elapsed, truck2.time_elapsed)
#updates package #9 address to 410 S. State St., Salt Lake City, UT 84111 after 10:20 AM
if current_time >= datetime(year=2025, month=12, day=21, hour=10, minute=20):
    package9 = Package(9, "410 S State St", "Salt Lake City", 84111, "EOD", 2, "At WGU shipment facility", "Address corrected")
    packageTable.insert(9, package9)
truck3.departure_time = current_time + min(truck1.time_elapsed, truck2.time_elapsed)
truck3.nextAddress()
#calculates the end of the day when the last package has been delivered
day_end = truck3.time_elapsed + truck3.departure_time

#user interface:
print(f"The last package was delivered at {day_end.strftime("%H:%M")}.")
print("Enter 'stop' to exit program at any time.")
while True:
    time_check = input("Please enter the time you want to check a package's status (format hh:mm):")
    if time_check == "stop":
        break
    (hr,mn) = time_check.split(":")
    time_check = datetime(2025,12,21,hour=int(hr),minute=int(mn))
    id_input = input("Enter the package ID of the package you'd like to check:")
    if id_input == "stop":
        break
    else:
        id_input = int(id_input)
    package = packageTable.get(id_input)
    package.statusTime(time_check)
    print(time_check)
    print(str(package))
    print()