#!/usr/bin/env python3

import multiprocessing
import os
import signal

import uuid

import hashlib

import time
import json

import sys

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

def dequeu_work(thread_number, work_queue, result_queue) :

    while True :
        if work_queue.empty() == False :
            # Get Work
            this_work = work_queue.get(timeout=3)

            # Process Work
            this_result = process_one_thread(uuidtohash=this_work)

            # Store result
            result_queue.put(this_result)

        else :
            # No More work on the queue breaking loop
            break

    my_pid = multiprocessing.current_process().pid

    # Kill myself as I'm no longer needed
    os.kill(my_pid, signal.SIGKILL)


if __name__ == "__main__" :

    # Constant
    RESULTS_WANTED=16
    THREADS=4


    # A place to store my results
    results_dict = dict()
    results_dict["data"] = list()
    results_dict["starttime"] = int(time.time())


    # Multiprocess Items
    manager = multiprocessing.Manager()

    # Create a Queue for data to Live in
    work_queue = manager.Queue(maxsize=0)

    # Results Queue
    result_queue = manager.Queue()

    for i in range(0,RESULTS_WANTED):
       work_queue.put(str(uuid.uuid4()))

    # Normally this would have some meaning and be something imported into your
    # Code. Possibly from a data file or a SQL query
    # Instead were going to take random strings in UUID form.

    thread_array = dict()

    for thread_count in range(0, THREADS) :
        if work_queue.empty() == False :
            # Queue Isn't Empty Turn this on to debug it's useful. :)
            #print("Provisioning thread ", str(thread_count))

            # Provision Thread
            thread_array[thread_count] = multiprocessing.Process(target=dequeu_work, \
                                        args=(thread_count, work_queue, result_queue) )

            # Daemonize it
            thread_array[thread_count].daemon = True

            # Start my This Thread
            thread_array[thread_count].start()
        else :
            # Work Queue is Prematurely Empty
            print("Queue is empty at ", str(thread_count), " threads prematurely stopping thread allocation.")
            break

    # Now we wait for my threads to endtime
    while True :
        any_thread_alive = False

        for thread in thread_array.keys() :
            if thread_array[thread].is_alive() == True :
                any_thread_alive = True

        if any_thread_alive :
            # Threads still alive sleep 5 seconds and check again
            time.sleep(5)
            pass
        else :
            # Threads Done End While Loop
            break

    # Record  End Time
    results_dict["endtime"] = int(time.time())

    # Grab Results
    for i in range(0, result_queue.qsize()) :
        this_result = result_queue.get(timeout=5)
        # Place on Results Queue
        results_dict["data"].append(this_result)

    # Calculate Run Time
    results_dict["totaltime_in_s"] = results_dict["endtime"] - results_dict["starttime"]

    # What happened
    print(json.dumps(results_dict))


