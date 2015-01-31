#!/usr/bin/python

# We need python's URL getting functionality
import urllib

# Set a sane default timeout (for all socket connections unfortunately...)
import socket
socket.setdefaulttimeout(3)

# for CSV support
import csv

# We ned sys in order to grab the argument to the script (which is the IP to connect to)
import sys

# We need os to delete files
import os

# random for the temporary file created
import random

# The web server IP to query
WebServer = sys.argv[1]

# Web server Port is the second argument
Port = sys.argv[2]

# Metric the user is asking for
RequestedMetric = sys.argv[3]

# URL is hard coded to /status?auto but could be different in the future if needed
URL = "/status?auto"

############### Function to fire off an HTTP request to the web server, throw an exception gracefully
############### and print FAIL if a connection can't be made
def getURL(WebServer,Port,URL):
    try:
        # Setup connection string
        ConnectionString = ("http://%s:%s%s") % (WebServer, Port, URL)

        conn = urllib.urlopen(ConnectionString)
        URLresponse = conn.read()

        # Clean up the connection
        conn.close()

        # The response to the function is the output of the URL called
        return URLresponse

    # Catch all exceptions
    except:
        print "Error getting URL"

########################################################################
### This function deals with "ordinary" metrics, such as CPULoad etc ###
########################################################################
def GetMetric(RequestedMetric):
    if RequestedMetric == "TotalAccesses":
        return ServerStatusOutput[0][1]

    if RequestedMetric == "TotalkBytes":
        return ServerStatusOutput[1][1]

    if RequestedMetric == "CPULoad":
        return ServerStatusOutput[2][1]

    if RequestedMetric == "ReqPerSec":
        return ServerStatusOutput[4][1]

    if RequestedMetric == "BytesPerSec":
        return ServerStatusOutput[5][1]

    if RequestedMetric == "BytesPerReq":
        return ServerStatusOutput[6][1]

    if RequestedMetric == "BusyWorkers":
        return ServerStatusOutput[7][1]

    if RequestedMetric == "IdleWorkers":
        return ServerStatusOutput[8][1]

###################################################################
### This function deals with specifically the Apache scoreboard ###
###################################################################

# function to count the metric requested... used in every if statement
def GetScoreboardMetric(RequestedMetric):
    # initialize counter variable
    RequestedMetricCount = 0

    # iterate over the ScoreBoard part and count the number of the requested metric
    for CountMetric in ServerStatusOutput[8][1]:
        if CountMetric == RequestedMetric:
            RequestedMetricCount = RequestedMetricCount + 1
    return RequestedMetricCount

    # Scoreboard Key:
    # "_" Waiting for Connection,
    # "S" Starting up,
    # "R" Reading Request,
    # "W" Sending Reply,
    # "K" Keepalive (read),
    # "D" DNS Lookup,
    # "C" Closing connection,
    # "L" Logging,
    # "G" Gracefully finishing,
    # "I" Idle cleanup of worker,
    # "." Open slot with no current process

#######################  End of function definitions ############################

#### Main body of script - Apache status is parsed and split into a list ####
RandomInt = random.randint(1, 1000)
TemporaryFileName = ("/tmp/%s.txt") % RandomInt
TemporaryFile = open(TemporaryFileName, 'a')
TemporaryFile.write(getURL(WebServer,Port,URL))

# Parse the CSV file we just wrote
CSVReader = csv.reader(open(TemporaryFileName, "rb"), delimiter = ":", skipinitialspace=True)

# Close the file handle and delete the file, to clean up because we're done with it at this point
TemporaryFile.close()
os.remove(TemporaryFileName)

# Turn the split CSV into a two dimensional list
ServerStatusOutput = []
for Metric in CSVReader:
    ServerStatusOutput.append(Metric)

# if the last argument to the script is more than two characters, this means an "ordinary" metric was asked for
if len(RequestedMetric) > 2:
    print GetMetric(RequestedMetric)

# Otherwise print the Scoreboard specific metric
else:
    print GetScoreboardMetric(RequestedMetric)
