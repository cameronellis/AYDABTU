#!/usr/bin/python
import json
import urllib2
import base64
import zlib
import time

# Overall WS Access Variables
dbsAlias = 'xTD150'
wsHost = 'dragon.teradata.ws'
wsPort =  '1080'
path = '/tdrest/systems/' + dbsAlias + '/queries'
wsUser = 'hack_user02'
wsPass = 'tdhackathon'

def rest_request (query ,wsUser,wsPass):
    url = 'http://' + wsHost + ':' + wsPort + path
   
    headers={}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.com.teradata.rest-v1.0+json'
    headers['Authorization'] = "Basic %s" % base64.encodestring('%s:%s' % (wsUser, wsPass)).replace('\n', '');

    # Set query bands
    queryBands = {}
    queryBands['applicationName'] = 'MyApp'
    queryBands['version'] = '1.0'

    # Set request fields. including SQL
    data = {}
    data['query'] = query
    data['queryBands'] = queryBands
    data['format'] = 'array'

    # Build request.
    request = urllib2.Request(url, json.dumps(data), headers)

    #Submit request
    try:
        response = urllib2.urlopen(request);
        # Check if result have been compressed.
        if response.info().get('Content-Encoding') == 'gzip':
            response = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
        else:
            response = response.read();
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        response = e.read();
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
        response = e.read();

    # Parse response to confirm value JSON.
    results = json.loads(response);

    return results

def getJsonFromQuery(query):
    return rest_request(query,"hack_user02","tdhackathon")
# Prompt user for the SQL query
#query = raw_input("Enter desired SQL query:\nEXAMPLE: select * from crime_data.murders_by_weapon_type\nQuery: ")

#perform_query (query, wsUser, wsPass)



