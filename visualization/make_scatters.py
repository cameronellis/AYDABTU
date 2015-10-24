import vizQuery as vq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import json
from sklearn import preprocessing
import itertools as it
from scipy.stats import linregress

#Read Query File
query_file = open(sys.argv[1], "r")

#Get Data based on Query files instructions and store into a data structure
queryCmdTpl = json.loads(query_file.read())

#Perform SQL querys for all fields in each table and store corresponding JSON objects to a file
#print vq.getJsonFromQuery("select \"Total Murders\", \"Shotguns\" from crime_data.murders_by_weapon_type")

#Perform Querys and store them into an array of pandas data frames
dfList = {}
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
	dfList[tbl_name] = pdData


#Create triangular matrix of feature pairs, re-label features to associate with tables too
all_features = []
for table in dfList.iteritems():
	table_name = table[0]
	tblFeats = []
	for column_name in table[1].columns.values:
		tblFeats.append(table_name + "." + column_name)
	all_features.append(tblFeats)

# A list of all possible feature pair combinations
tblFeatPairs = []
for tblFeats in all_features:
	tblFeatPairs.append(list(it.combinations(tblFeats, 2)))



figNum = 0
for featPairs in tblFeatPairs:
	for pair in featPairs:
		figNum += 1
		featOneName = pair[0]
		featTwoName = pair[1]
		featOneNameSplit = featOneName.split(".")
		featTwoNameSplit = featTwoName.split(".")

		featOneNdxName = featOneNameSplit[0] + "." + featOneNameSplit[1]
		featTwoNdxName = featTwoNameSplit[0] + "." + featTwoNameSplit[1]

		featOneData = np.array(dfList[featOneNdxName][featOneNameSplit[2]])
		featTwoData = np.array(dfList[featTwoNdxName][featTwoNameSplit[2]])

		if(not(isinstance(featOneData[0], (int, long, float, complex)))):
	 		le.fit(featOneData)
	 		featOneData = le.transform(featOneData)

	 	if(not(isinstance(featTwoData[0], (int, long, float, complex)))):
	 		le.fit(featTwoData)
	 		featTwoData = le.transform(featTwoData)

	 	# Plot that shiznit
	 	plt.figure(figNum)

		#Index to cut data from
		cut_ndx = int(len(featOneData)*0.6)

		#The Training set for the feature pair
		featOneDataTrain = featOneData[:cut_ndx]
		featTwoDataTrain = featTwoData[:cut_ndx]

		#The Testing set for the feature pair
		featOneDataTest = featOneData[cut_ndx:]
		featTwoDataTest = featTwoData[cut_ndx:]



		coefficients = np.polyfit(featOneDataTrain, featTwoDataTrain, 1)

		polynomial = np.poly1d(coefficients)
		ys = polynomial(featOneDataTrain)


		plt.scatter(featOneDataTrain, featTwoDataTrain)
		plt.scatter(featOneDataTest, featTwoDataTest, color="red")
		plt.plot(featOneDataTrain, ys)

		#Finally, Make the Prediction for every point in the test set and calculate 
		#Hamming Loss and MSE 

		#Create Y_HAT array
		m = coefficients[0]
		b = coefficients[1]
		Y_HAT = []

		MSE = 0
		for i in range(len(featOneDataTest)):
		 	prediction = m*featOneDataTest[i]+b
		 	actual = featTwoDataTest[i]
		 	MSE += (prediction - actual)**2
		MSE = float(MSE)/len(featOneDataTest)

		plt.xlabel(featOneNdxName + "." + featOneNameSplit[2])
		plt.ylabel(featTwoNdxName + "." + featTwoNameSplit[2])
		plt.title("THE MSE: " + str(MSE))
plt.show()


#Encode any categorical data into integers using sklearn
# for column in pdData:
# 	if(not(isinstance(pdData[column][0], (int, long, float, complex)))):
# 		npStrList = np.array(pdData[column])
# 		le.fit(npStrList)
# 		strEncodings = le.transform(npStrList)
# 		pdData.append(pd.DataFrame(strEncodings))
# 		#pdData.insert(0,column,npStrList)
# 		dfList.append(pdData)

#Scatter plot when they are both numbers
# feat1 = np.array(dfList[0]["# Divorces & Annulments"])
# feat2 = np.array(dfList[0]["Rate per 1000"])
# plt.xlabel("# Divorces & Annulments")
# plt.ylabel("Rate per 1000")



# #Scatter plot when it is numbers and a string
# feat3 = np.array(dfList[1]["Age Group"])
# if(not(isinstance(feat1, (int, long, float, complex)))):
#  		npStrList = np.array(pdData["Age Group"])
#  		le.fit(npStrList)
#  		feat3 = le.transform(npStrList)

# feat4 = np.array(dfList[1]["Number of Deaths"])
# plt.xlabel("Age Group")
# plt.ylabel("Number of Deaths")

# plt.figure(1)
# plt.scatter(feat1, feat2)
# plt.figure(2)
# plt.scatter(feat3, feat4)
# plt.show()






