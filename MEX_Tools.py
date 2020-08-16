import requests
import time
from datetime import datetime
import logging
import threading

URL = "https://www.bitmex.com/api/v1/orderBook/L2?symbol=XBT&depth=50"


now = datetime.now()
current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

logfile = "info_"+current_time+".log"

logging.basicConfig(filename=logfile, level=logging.INFO)
starttime = time.time()
DetectedSpoofers = list()

spoofer_minimum_size = 2500000

while(True):
    r = requests.get(url = URL)
    data = r.json()
    
    for order in data:
        if(order["size"] > spoofer_minimum_size):
            spoofDict = {"price" : order["price"], "size" : order["size"], "side": order["side"]}
            alreadyDetected = False
            
            #Reset the vector to detect new spoofers at same price 
            if(DetectedSpoofers.count == 200):
                logging.info("Cleared vector. ")
                DetectedSpoofers.clear()

            #Start condition 
            if(DetectedSpoofers.count == 0):
                DetectedSpoofers.append(spoofDict)
                continue
            
            #Check if the spoofer was already detected at the same price
            for detectedSpoof in DetectedSpoofers:
                if(spoofDict["price"] == detectedSpoof["price"]):
                    alreadyDetected = True

            #If the spoofer is new add to DetectedSpoofers list and log to file
            if(alreadyDetected == False):
                DetectedSpoofers.append(spoofDict)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time + " Potential " + str(spoofDict["size"]) +  " spoofer appended on the list " + spoofDict["side"] + " side at price : " +  str(order["price"]))
                logging.info(current_time + " Potential " + str(spoofDict["size"]) +  " spoofer appended on the list " + spoofDict["side"] + " side at price : " +  str(order["price"]))
    
    time.sleep(3)
    

