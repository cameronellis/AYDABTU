import os
import vizQuery as vq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import json
from sklearn import preprocessing, datasets, linear_model
from sklearn.cross_validation import train_test_split
import itertools as it
from scipy.stats import linregress
import warnings

#Read Query File
query_file = open(sys.argv[1], "r")

#Get query fields based on file and store into a data structure
queryCmdTpl = json.loads(query_file.read())

#Perform Querys and store them into an array of pandas data frames
dfList = {}
le = preprocessing.LabelEncoder() #Used to encode categorical data

for table in queryCmdTpl:
	# Query the JSON file for the desired fields
	tbl_name = table
	field_names  = queryCmdTpl[table]['names']
	for i in range(len(field_names)):
		field_names[i] = str(field_names[i])

	# Compose SQL query from desired fields
	queryString = "select "
	for name in field_names:
		queryString += " \""+name+"\", "
	queryString = queryString[:len(queryString)-2]
	queryString += " from " + table

	# Delegate to vizQuery to grab data from TD REST API
	jsonData = vq.getJsonFromQuery(queryString)["results"][0]["data"]

	#Convert jsonData to a pandas dataframe
	pdData = pd.DataFrame(jsonData, columns=field_names)
	dfList[tbl_name] = pdData


# Generate n Choose 2 combinations
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

# Track coefficients of determination
rsv = {}

# Plot and calculate error
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

		# Handle cases of non-numerical data
		if(not(isinstance(featOneData[0], (int, long, float, complex)))):
	 		le.fit(featOneData)
	 		featOneData = le.transform(featOneData)

	 	if(not(isinstance(featTwoData[0], (int, long, float, complex)))):
	 		le.fit(featTwoData)
	 		featTwoData = le.transform(featTwoData)

	 	# Set up the new figure
	 	plt.figure(figNum)


	 	# Eliminate outliers
	 	tolerable = (np.std(featTwoData))**1.068
		model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression(), residual_threshold=tolerable, max_trials=1000)
		featOne = [[x] for x in featOneData]
		model_ransac.fit(featOne, featTwoData)
		inlier_mask = model_ransac.inlier_mask_
		outlier_mask = np.logical_not(inlier_mask)

		# Split into test and train sets
		featOneDataTrain, featOneDataTest, featTwoDataTrain, featTwoDataTest = train_test_split(featOneData[inlier_mask], featTwoData[inlier_mask], test_size = .2)

		# MACHINE LEARNING
		# NEW linear regression
		slope, intercept, r_value, p_value, std_err = linregress(featOneDataTrain, featTwoDataTrain)
		m = slope
		b = intercept
		polynomial = np.poly1d([m,b])
		ys = polynomial(featOneDataTrain)
		# Track r^2 of all plots
		rsv[featOneName + " --AND-- " + featTwoName] = (r_value**2) 

		# Plot the data points
		plt.scatter(featOneDataTrain, featTwoDataTrain, color="blue")
		plt.scatter(featOneDataTest, featTwoDataTest, color="yellow")
		plt.scatter(featOneData[outlier_mask], featTwoData[outlier_mask], color="red")
		plt.plot(featOneDataTrain, ys)

		#Finally, Make the Prediction for every point in the test set and calculate 
		#Hamming Loss and MSE 
		MSE = 0
		for i in range(len(featOneDataTest)):
		 	prediction = m*featOneDataTest[i]+b
		 	actual = featTwoDataTest[i]
		 	MSE += (prediction - actual)**2
		MSE = float(MSE)/len(featOneDataTest)

		plt.xlabel(featOneNdxName + "." + featOneNameSplit[2])
		plt.ylabel(featTwoNdxName + "." + featTwoNameSplit[2])
		plt.title("THE MSE: " + str(MSE))

# Compare all coefficients of determination to identify best fits
os.system('clear')
sortedR = sorted(rsv.items(), key=lambda rsv: rsv[1])
print "*\nPossible strong correlation between (Top 10%)"
for x in range (len(sortedR)/10):
	print "\n#" + (x+1) + ": " + sortedR[len(sortedR)-(x+1)][0] + ": with r^2 = " + sortedR[len(sortedR)-(x+1)][1] + "\n"
# If none were printed, print the best one
if (len(sortedR)/10) < 1:
	print "\n#1: " + sortedR[len(sortedR)-1][0] + "\n"


# Filter pandas future warning
warnings.simplefilter(action = "ignore", category = FutureWarning)

# Show all the plots
plt.show()

