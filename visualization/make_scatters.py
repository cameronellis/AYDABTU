import vizQuery as vq
import pandas as pd
import numpy
import matplotlib
import sys
import json

### TOP DOWN DESIGN:
# 1. Read in query JSON
# 2. Perform query to get structure of tables in the JSON 
# 3. Perform query for table objects and store an array of JSON for each table object
# 4. Compare fields of each object to the fields of each other object

#Read Query File
query_file = open(sys.argv[1], "r")

#Get Data based on Query files instructions and store into a data structure
queryCmdTpl = json.loads(query_file.read())

#Perform SQL querys for all fields in each table and store corresponding JSON objects to a file
#print vq.getJsonFromQuery("select \"Total Murders\", \"Shotguns\" from crime_data.murders_by_weapon_type")

#Perform Querys and store them into an array of pandas data frames
dfList = []
for table in queryCmdTpl:
	#Query the JSON Data
	tbl_name = table
	field_names  = queryCmdTpl[table]['names']

	for i in range(len(field_names)):
		field_names[i] = str(field_names[i])

	queryString = "select "
	for name in field_names:
		queryString += " \""+name+"\", "
	queryString = queryString[:len(queryString)-2]
	queryString += " from " + table
	jsonData = vq.getJsonFromQuery(queryString)["results"][0]["data"]

	#Convert jsonData to a pandas dataframe
	pdData = pd.DataFrame(jsonData, columns=field_names)
	dfList.append(pdData)

print dfList


