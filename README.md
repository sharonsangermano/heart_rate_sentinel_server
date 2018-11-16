# heart_rate_sentinel_server
A simple centralized heart rate sentinel server. Receives POST requests from mock patient heart rate monitors and contains patient heart rate information to be used to determine if a patient is tachycardic.  An email warning is sent to a physician if tachycardia is detected.

## Code
**server.py:** Flask server program that allows physicians to register heart rate monitors with a patient, collect, store, and receive patient heart rate data, determine if a patient is tachycardic based on age and heart rate, and find a patient's average heart rate during specified time intervals

**main.py:** Contains basic POST and GET examples for all of the functions established on the server

**test_server.py:** Unit testing for all server.py functions that are not covered by pymodm or flask

## Testing the server 
The server can be run locally or on a virtual machine using *$ python server.py*.  The server is currently running on a virtual machine (vcm-7307.vm.duke.edu) for testing purposes. 

## 
[![Build Status](https://travis-ci.org/sharonsangermano/heart_rate_sentinel_server.svg?branch=master)](https://travis-ci.org/sharonsangermano/heart_rate_sentinel_server)
