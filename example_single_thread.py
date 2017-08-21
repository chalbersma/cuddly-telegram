#!/usr/bin/env python3

import multiprocessing

import uuid

import hashlib

import time
import json

def process_one_thread(uuidtohash="nostring?", num=1000000) :
    # This will be our stand in process for doing a cpu intensive task
    # It generates a randomish string and hashes it 1000000 times.
    # This is done to simulate a single threaded load on my workstation
    # this takes about 25 seconds (for all 16) you may need to lower it or raise it
    # to make the example work.

    current_hash = uuidtohash.encode()

    for i in range(0,num) :
        # Hash it
        hashobject = hashlib.sha512(current_hash).hexdigest().encode()
        current_hash = hashobject

    return_dict = { uuidtohash : hashobject.decode() }
    return return_dict

if __name__ == "__main__" :

    # Constant
    RESULTS_WANTED=16

    # Normally this would have some meaning and be something imported into your
    # Code. Possibly from a data file or a SQL query
    # Instead were going to take random strings in UUID form.
    input_list = list()
    for i in range(0,RESULTS_WANTED):
        input_list.append(str(uuid.uuid4()))


    # A place to store my results
    results_dict = dict()
    results_dict["data"] = list()
    results_dict["starttime"] = int(time.time())

    # Do the Work
    for i in range(0,RESULTS_WANTED) :
        this_result = process_one_thread(uuidtohash=input_list[i])
        results_dict["data"].append(this_result)

    # Record  End Time
    results_dict["endtime"] = int(time.time())

    # Calculate Run Time
    results_dict["totaltime_in_s"] = results_dict["endtime"] - results_dict["starttime"]

    # What happened
    print(json.dumps(results_dict))


