#
# Author:       Nathaniel Moreno
# Date:         Oct. 23rd, 2015
#
# Purpose:      Function as template file for easily graphing data
#               for exploratory analysis.
#
#
#
##################################################################################

# IMPORTING LIBRARIES

from collections import defaultdict 
import urllib
from operator import itemgetter
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import matplotlib as mpl

##################################################################################

# Functions


# Purpose:      Parses inputted json file 
# Input:        fname   - name of json file
# Output:       yield   - dictionary for every sample in data set
def parseData(fname):
	for l in urllib.urlopen(fname):
		yield eval(l)


# Purpose:      Parses inputted dictionary
# Input:        elem     - the dictionary element to extract features from
#               featList - list of features to extract from dictionary
# Output:       return   - returns list of extracted features
def feature(elem, featList):
	return [elem[f] for f in featList]

# Purpose:      Builds workable list of all samples in json
# Input:        filename        - name of json file
#               features        - list of features to extract
# Output:       return          - returns list of all samples with their designated extracted features
def buildData(filename,features):
	print "Exec buildData\n"
	return [feature(d,features) for d in parseData(filename)]


def aggragateData(inData,s,e):
	print "Exec AggragateData\n"
	timeList = []
	for elem in inData:
                year 	= (elem[0])[0:4]
                month 	= (elem[0])[5:7]
                day 	= (elem[0])[8:10]
                hour 	= (elem[0])[11:13]
                minute	= (elem[0])[14:16]
                second 	= (elem[0])[17:19]
		crime   = elem[1]
		try:	
			longi = float(elem[2])
			lati = float(elem[3])
		except ValueError:
			longi = 0
			lati = 0
		arrest 	= elem[4]
		locat	= elem[5] 
                time = [year,month,day,hour,minute,second,
			crime,
			longi,lati,locat,
			arrest]
                timeList.append(time)

	
	outDict = defaultdict(lambda:defaultdict(int))
	crimeSet = set()
	timeSet = set()
	locList = []
	for time in timeList:
                timeVar = str()
                for i in range(s,e+1): timeVar += time[i]
		outDict[str(int(timeVar))][time[6]] += 1
		locList.append([time[7],time[8],time[9],time[6]])
		crimeSet.add(time[6])
		timeSet.add(int(timeVar))
	
	crimeDict = defaultdict(int)	
	for c in crimeSet:
		crimeDict[c]=sum([outDict[str(t)][c] for t in timeSet])
	tL = sorted(list(timeSet),key=int)
	cL = sorted(	[[c,crimeDict[c]] for c in crimeSet],
			key=itemgetter(1),
			reverse=True)
	cL = [c[0] for c in cL]
	out = [tL,cL,outDict,locList,crimeSet ]
	return out
			 


##########################################################################
# Generate sample data

inFile = ""
featureList = [ "", "" ]
imdata = buildData( inFile, featureList )

data = aggragateData( imdata, 3, 3 )


#locCrime = defaultdict(list)
#X = np.array(data[3]).T

#lon = X[0]
#lat = X[1]
#loc = X[2]
#crime = X[3]




#crimeColor = defaultdict(int)
#i = 0
#for c in data[4]: 
	crimeColor[c] = i
	i += 1

#color = [ float(crimeColor[c])/255 for c in crime ]
#plt.scatter(lon, lat, c=color, s=500, cmap=mpl.cm.gray)

#plt.show()

dataScrub = []
prev = defaultdict(int)
for crime in data[1]:
        sub = [data[2][str(time)][crime] for time in data[0]]
        dataScrub.append(sub)

base = [0]*len(dataScrub[0])
for i in range(0,len(dataScrub)):
	base += dataScrub[len(dataScrub)-i-1]
	plt.plot(base)
	
#X = (np.array(dataScrub[0])).T
#y = np.array(data[0])

#w,v = np.linalg.eig(np.cov(dataScrub))
#print v
#for scrub in dataScrub: plt.plot(scrub)
plt.ylabel('Crime Count')
#plt.legend(data[1], loc='upper left')
#l=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#ax.set_xticklabels(l)
plt.show()
	
def svrRBF(cVar,gamVar):
	print "Exec svrRBF\n"
	svr_rbf = SVR(kernel='rbf', C=cVar, gamma=gamVar)
	y_rbf = svr_rbf.fit(X, y).predict(X)

	plt.scatter(X, y, c='k', label='data')
	plt.hold('on')
	plt.plot(X, y_rbf, c='g', label='RBF model')
	plt.xlabel('data')
	plt.ylabel('target')
	plt.title('Support Vector Regression')
	plt.legend()
	plt.show()

def svrPoly(cVar,degVar):
	print "Exec svrPoly\n"
	svr_poly = SVR(kernel='poly', C=cVar, degree=degVar)
	y_poly = svr_poly.fit(X, y).predict(X)

	plt.scatter(X, y, c='k', label='data')
	plt.hold('on')
	plt.plot(X, y_poly, c='b', label='Polynomial model')
	plt.xlabel('data')
	plt.ylabel('target')
	plt.title('Support Vector Regression')
	plt.legend()
	plt.show()

def svrLin(cVar):
	print "Exec svrLin\n"
	svr_lin = SVR(kernel='linear', C=cVar)
	y_lin = svr_lin.fit(X, y).predict(X)
	
	plt.scatter(X, y, c='k', label='data')
	plt.hold('on')
	plt.plot(X, y_lin, c='r', label='Linear model')
	plt.xlabel('data')
	plt.ylabel('target')
	plt.title('Support Vector Regression')
	plt.legend()
	plt.show()

#svrLin(1e3)
#svrPoly(1e3,2)
svrRBF(1e3,0.1)
