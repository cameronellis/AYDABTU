import vizQuery as vq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import json
from sklearn import preprocessing

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
le = preprocessing.LabelEncoder() #Used to encode categorical data
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

#Encode any categorical data into integers using sklearn
# for column in pdData:
# 	if(not(isinstance(pdData[column][0], (int, long, float, complex)))):
# 		npStrList = np.array(pdData[column])
# 		le.fit(npStrList)
# 		strEncodings = le.transform(npStrList)
# 		pdData.append(pd.DataFrame(strEncodings))
# 		#pdData.insert(0,column,npStrList)
# 		dfList.append(pdData)

#Make scatterplots of features with every other feature

#Scatter plot when they are both numbers
# feat1 = np.array(dfList[0]["# Divorces & Annulments"])
# feat2 = np.array(dfList[0]["Rate per 1000"])
# plt.xlabel("# Divorces & Annulments")
# plt.ylabel("Rate per 1000")
# plt.scatter(feat1, feat2)
# plt.show()

#Scatter plot when it is numbers and a string
feat1 = np.array(dfList[1]["Age Group"])
if(not(isinstance(feat1, (int, long, float, complex)))):
 		npStrList = np.array(pdData["Age Group"])
 		le.fit(npStrList)
 		feat1 = le.transform(npStrList)

feat2 = np.array(dfList[1]["Number of Deaths"])
plt.xlabel("Age Group")
plt.ylabel("Number of Deaths")
plt.scatter(feat1, feat2)
plt.show()



