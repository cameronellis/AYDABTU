'''
Purpose:	This Python script will allow extremely easy queries to Teradata
				databases using the TD REST api. Make sure the url and auth
				info match your needs, then run the script and enter a SQL
				query. The results will be stored locally in a json file.

Author:		Chad Atalla
Date:		10/21/2015
'''
import requests
import json
import time

# Prompt user for the SQL query
query = raw_input("Enter desired SQL query:\n")

# Make sure these two variables are set to your specifications:
url = 'http://dragon.teradata.ws:1080/tdrest/systems/MYSYS/queries'
myAuth = 'Basic ZGJjOmRiYw=='

# Leave these as they are
myHeaders = {'Accept': "application/vnd.com.teradata.rest-v1.0+json",
		'Authorization': myAuth}

# Assemble the data argument
myData = {"query": query ,"format":"object"}

# Make the actual request
req = requests.post(url, data=myData, headers=myHeaders,
	auth=myAuth)

# Get time string for name
ts = str(int(time.time()))

# Extract and save json
results = req.json()
with open((ts + '.json'), 'w') as outfile:
    json.dump(results, outfile)
