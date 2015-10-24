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



def rest_request ( query ,wsUser,wsPass):
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

    print json.dumps(results, indent=4, sort_keys=True)

    ts = str(int(time.time()))
    filename = './jsons/' + ts + '.json'

    with open(filename, 'w') as outfile:
    	json.dump(results, outfile, indent=4, sort_keys=True)

    return;

def perform_query( query, wsUser, wsPass ):
    rest_request(query, wsUser, wsPass)
    
    return;

wsUser = 'hack_user02'
wsPass = 'tdhackathon'

# DEFINE ALL POSSIBLE QUERIES
dbases =   [['cdc', 'national_divorce_trends', 'national_marriage_trends'],
			
			['crime_data', 'murders_by_weapon_type',
			'police_military_purchases', 'portland_crime', 'san_diego_crime',
			'us_crime_rates'],
			
			['health', 'country_death_rates',
			'life_expectancy_hivaids_countries', 'life_expectancy_russia',
			'life_expectancy_us', 'life_expectancy_world_projection_2100',
			'world_population_projection_2100'],
			
			['housing_data', 'san_francisco_rental_listings',
			'freddie_mae_house_price_index'],

			['homeland_security', 'refugee_arrivals_by_country', 
			'refugee_arrivals_by_region'],

			['national_fire_protection', 'fire_problem_overview', 
			'number_fires_by_type'],

			['transportation', 'aircraft_accident_rates', 
			'alcohol_related_crashes',
			'monthly_number_of_airline_passengers_all_carriers',
			'retail_deisel_prices', 'unruly_airline_passengers',
			'us_airline_fuel_cost_consumption'],

			['treasury', 'us_debt]',

			['weather', 'tornado_counts', 'tornado_deaths'],

			['world_health_organization', 'hepb_immunizations_oneyearolds',
			'infants_exclusivley_bresatfed_first6mos']
			]

# Define query template
queryText = 'select * from '

# Scrape down every table
for i in range (dbases.length)
	for x in range (dbases[i].length)
		if (x != 0):
			perform_query (queryText + dbases[i][0] + '.' + dbases[i][x], wsUser, wsPass)
			time.sleep(.1)



