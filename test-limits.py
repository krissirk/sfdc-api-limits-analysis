#!/usr/bin/env python3
import requests, json, time, sys
from config import *

#Suppress InsecureRequestWarning message in console when verify certificate option is set to false in API request 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get key values required to access Enterprise API from config file; build complete header to accompany API request
if SESSION_ID:
	myHeader = {'Authorization': 'Bearer ' + SESSION_ID,
				'User-Agent': 'KBH Python Script to test API Limits',
				'Host': HOST,
				'Content-Type': 'application/json',
				'Accept': 'application/json',
				'Accept-Charset': 'UTF-8'
				}
else:
	print("Session ID or Auth token not found - cannot proceed")
	sys.exit(2)

############################################ FUNCTION DEFINITIONS #############################################

# Function that makes GET request
def apiGetRequest(url, certCheck):

	try:
		apiResponse = requests.get(url, headers=myHeader, timeout=120, verify=certCheck)

	except:
		print(apiResponse.status_code)
		print(apiResponse.content)

	apiResponse.close()

	if apiResponse:
		return apiResponse
	else:
		print(apiResponse.status_code)
		print(apiResponse.content)
		sys.exit(2)

######################################### END OF FUNCTION DEFINITIONS #########################################

print("Start: ", time.asctime( time.localtime(time.time()) ))	#Log script start time to console

remainingLimit = 0
getObjectsUrl = "https://{0}/services/data/v{1}/sobjects/".format(HOST, VERSION)
getLimitUrl = "https://{0}/services/data/v{1}/limits/".format(HOST, VERSION)

limitsResponse = apiGetRequest(getLimitUrl, False)
requestsMade = 1

remainingLimit = limitsResponse.json()['DailyApiRequests']['Remaining']

print("Per Limits request: {0}".format(limitsResponse.headers['Sforce-Limit-Info']))
print(remainingLimit)

while remainingLimit > 0:

	requestsMade += 1
	print("Requests attempted: {0}".format(requestsMade))
	objectsResponse = apiGetRequest(getObjectsUrl, False)
	print(objectsResponse.headers['Sforce-Limit-Info'])

	requestsMade += 1
	print("Requests attempted: {0}".format(requestsMade))
	limitsResponse = apiGetRequest(getLimitUrl, False)
	remainingLimit = limitsResponse.json()['DailyApiRequests']['Remaining']

	print(limitsResponse.headers['Sforce-Limit-Info'])
	print(remainingLimit)

print("End: ", time.asctime( time.localtime(time.time()) ))	# Log script completion ending time to console
print(objectsResponse.headers['Sforce-Limit-Info'])
print(remainingLimit)
print("Requests submitted: {0}".format(requestsMade))