#!/usr/bin/env python3
import requests, json, time, sys
from config import *

# Get key values required to access Enterprise API from config file; build complete header to accompany API request
if SESSION_ID:
	myHeader = {'Authorization': 'Bearer ' + SESSION_ID,
				'User-Agent': 'KBH Python Script to test API Limits',
				'Host': HOST,
				'Content-Type' : 'application/json'
				}
else:
	print("Session ID or Auth token not found - cannot proceed")
	sys.exit(2)

############################################ FUNCTION DEFINITIONS #############################################

# Function that makes Product Catalog API request until successful response obtained, returns that response for processing
def apiRequest(url):

	try:
		apiResponse = requests.get(url, headers=myHeader, timeout=120)
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

objectsResponse = apiRequest(getObjectsUrl)
limitsResponse = apiRequest(getLimitUrl)
requestsMade = 2

remainingLimit = limitsResponse.json()['DailyApiRequests']['Remaining']

print("Per sObjects request: {0}".format(objectsResponse.headers['Sforce-Limit-Info']))
print("Per Limits request: {0}".format(limitsResponse.headers['Sforce-Limit-Info']))
print(remainingLimit)

while remainingLimit > 0:

	requestsMade += 1
	print("Requests attempted: {0}".format(requestsMade))
	objectsResponse = apiRequest(getObjectsUrl)
	limitsResponse = apiRequest(getLimitUrl)
	remainingLimit = limitsResponse.json()['DailyApiRequests']['Remaining']

	print(objectsResponse.headers['Sforce-Limit-Info'])
	print(remainingLimit)

print("End: ", time.asctime( time.localtime(time.time()) ))	# Log script completion ending time to console
print(objectsResponse.headers['Sforce-Limit-Info'])
print(remainingLimit)
print("Requests submitted: {0}".format(requestsMade))