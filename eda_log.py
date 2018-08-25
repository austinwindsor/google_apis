#exploratory data analysis
#"201501-hubwya-tripdata"  is the excel that shows the trip history
#"export.csv" is the full or empty notices for each station
#Google Maps Distance Matrix API Key:
#AIzaSyAgqyb4m9ECjevhXWoY65S86MbmOfSL08c

import pandas as pd
import numpy as np 
import json
import csv
import urllib
from bs4 import BeautifulSoup
import google_maps_services_python.googlemaps as googlemaps
from googlemaps import geocoding
import time 
import argparse
import requests

# from distance_matrix import distance_matrix
pd.set_option('display.multi_sparse', False)

# tripHistory = pd.read_csv("201712-hubway-tripdata.csv")
# statusHistory = pd.read_csv("export.csv")


# print("DATA ANALYSIS")
# print("\n\n")
# print(statusHistory.columns)
# print("\n\n")
# print("COUNT OF STATION OUTAGE\n"+str(len(statusHistory)))
# print("\n\n")
# print("COUNT OF TRIPS\n"+str(len(tripHistory)))
# print("\n\n")
# # print("FREQUENCY OF OUTAGE BY STATION\n"+str(statusHistory.groupby(["Station Name"])["Duration"].sum()))
# print("\n\n")


# the count for each kind of path taken
# routes = tripHistory.groupby(["start station latitude", "start station longitude", "end station latitude", "end station longitude"], sort=True).size()

# routes.sort_values(axis=0, ascending = False, inplace=True)
# print("FREQUENCY OF TRIPS BY START AND END STATION\n"+str(routes))
# print(tripHistory.shape)
# # print(tripHistory.groupby(['start station name', 'end station name']).size().reset_index().rename(columns={0:'count'}))
# routes = tripHistory.groupby(['start station name', 'end station name']).size().reset_index().rename(columns={0:'count'})
# routes.sort_values('count', ascending = False, inplace = True)
# print(routes.head())


# routes_geo = tripHistory.groupby(['start station latitude', 'start station longitude','end station latitude','end station longitude']).size().reset_index().rename(columns={0:'count'})
# # print(routes_geo)
# tog = pd.merge(statusHistory,routes, left_on='Row Labels', right_on= 'start station name')
# tog.groupby(['Row Labels'])['start station latitude', 'start station longitude','end station latitude','end station longitude', 'empty']
# # .sort_values('empty', ascending=False, inplace=True)
# print(tog.head())


# routes_geo.sort_values('count', ascending = False, inplace = True)
# print(routes_geo.iloc[0:9])
# print(routes_geo.iloc[1:9][['start station latitude', 'start station longitude','end station latitude','end station longitude']].nunique())
# print(len(routes_geo))

# print("NUMBER OF START STATIONS\n")
# start_geo= tripHistory.groupby(['start station latitude', 'start station longitude']).size().reset_index().rename(columns={0:'count'})
# eng_geo= tripHistory.groupby(['end station latitude', 'end station longitude']).size().reset_index().rename(columns={0:'count'})
# print("NUMBER OF END STATIONS\n" + str(len(np.unique(tripHistory[['end station latitude','end station longitude']]))))
# print(str(len(np.unique(tripHistory[['end station longitude','end station latitude']]))) == str(len(np.unique(tripHistory[['start station latitude', 'start station longitude']]))))

# print(tripHistory.groupby(['end station name'])['end station latitude', 'end station longitude'].nunique().max())

#write the output of the file such that it fits into the output excel sheet properly
def file_print(output, row, column):
	fd = open('CHOA'+ str(track_across)+'_'+str(track_down)+'.txt','w')
	fd.write(str(output))
	fd.close()
	diction = output
	# diction = { ['300 Vassar St'destination_addresses':, Cambridge, MA 02139, USA', '100 Amherst St, Cambridge, MA 02139, USA', 'Somerville Community Path, Somerville, MA 02144, USA', '33 Vassar St, Cambridge, MA 02142, USA', '100 Amherst St, Cambridge, MA 02139, USA', 'Alewife Linear Park, Cambridge, MA 02140, USA', '300 Vassar St, Cambridge, MA 02139, USA', '34-50 Pacific St, Cambridge, MA 02139, USA', '235-281 Main St, Cambridge, MA 02142, USA'], 'origin_addresses': ['100 Amherst St, Cambridge, MA 02139, USA', '300 Vassar St, Cambridge, MA 02139, USA', 'Alewife Linear Park, Cambridge, MA 02140, USA', '300 Vassar St, Cambridge, MA 02139, USA', '34-50 Pacific St, Cambridge, MA 02139, USA', '299 Elm St, Somerville, MA 02144, USA', '33 Vassar St, Cambridge, MA 02142, USA', '33 Vassar St, Cambridge, MA 02142, USA', '34-50 Pacific St, Cambridge, MA 02139, USA'], 'rows': [{'elements': [{'distance': {'text': '1.0 km', 'value': 1050}, 'duration': {'text': '3 mins', 'value': 184}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '6.6 km', 'value': 6603}, 'duration': {'text': '23 mins', 'value': 1360}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1089}, 'duration': {'text': '5 mins', 'value': 275}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '6.0 km', 'value': 6039}, 'duration': {'text': '21 mins', 'value': 1262}, 'status': 'OK'}, {'distance': {'text': '1.0 km', 'value': 1050}, 'duration': {'text': '3 mins', 'value': 184}, 'status': 'OK'}, {'distance': {'text': '0.9 km', 'value': 911}, 'duration': {'text': '4 mins', 'value': 246}, 'status': 'OK'}, {'distance': {'text': '1.7 km', 'value': 1722}, 'duration': {'text': '7 mins', 'value': 411}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1138}, 'duration': {'text': '4 mins', 'value': 221}, 'status': 'OK'}, {'distance': {'text': '7.2 km', 'value': 7230}, 'duration': {'text': '24 mins', 'value': 1465}, 'status': 'OK'}, {'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 311}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1138}, 'duration': {'text': '4 mins', 'value': 221}, 'status': 'OK'}, {'distance': {'text': '6.7 km', 'value': 6665}, 'duration': {'text': '23 mins', 'value': 1367}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 236}, 'status': 'OK'}, {'distance': {'text': '1.9 km', 'value': 1924}, 'duration': {'text': '7 mins', 'value': 447}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '7.2 km', 'value': 7190}, 'duration': {'text': '27 mins', 'value': 1629}, 'status': 'OK'}, {'distance': {'text': '6.1 km', 'value': 6122}, 'duration': {'text': '21 mins', 'value': 1234}, 'status': 'OK'}, {'distance': {'text': '0.6 km', 'value': 626}, 'duration': {'text': '2 mins', 'value': 139}, 'status': 'OK'}, {'distance': {'text': '6.5 km', 'value': 6497}, 'duration': {'text': '23 mins', 'value': 1373}, 'status': 'OK'}, {'distance': {'text': '6.1 km', 'value': 6122}, 'duration': {'text': '21 mins', 'value': 1234}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '7.2 km', 'value': 7190}, 'duration': {'text': '27 mins', 'value': 1629}, 'status': 'OK'}, {'distance': {'text': '5.9 km', 'value': 5852}, 'duration': {'text': '19 mins', 'value': 1168}, 'status': 'OK'}, {'distance': {'text': '6.1 km', 'value': 6093}, 'duration': {'text': '23 mins', 'value': 1385}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1138}, 'duration': {'text': '4 mins', 'value': 221}, 'status': 'OK'}, {'distance': {'text': '7.2 km', 'value': 7230}, 'duration': {'text': '24 mins', 'value': 1465}, 'status': 'OK'}, {'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 311}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1138}, 'duration': {'text': '4 mins', 'value': 221}, 'status': 'OK'}, {'distance': {'text': '6.7 km', 'value': 6665}, 'duration': {'text': '23 mins', 'value': 1367}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 236}, 'status': 'OK'}, {'distance': {'text': '1.9 km', 'value': 1924}, 'duration': {'text': '7 mins', 'value': 447}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 240}, 'status': 'OK'}, {'distance': {'text': '0.9 km', 'value': 922}, 'duration': {'text': '3 mins', 'value': 195}, 'status': 'OK'}, {'distance': {'text': '6.3 km', 'value': 6300}, 'duration': {'text': '21 mins', 'value': 1289}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1123}, 'duration': {'text': '4 mins', 'value': 261}, 'status': 'OK'}, {'distance': {'text': '0.9 km', 'value': 922}, 'duration': {'text': '3 mins', 'value': 195}, 'status': 'OK'}, {'distance': {'text': '5.7 km', 'value': 5735}, 'duration': {'text': '20 mins', 'value': 1191}, 'status': 'OK'}, {'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 240}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.6 km', 'value': 1609}, 'duration': {'text': '7 mins', 'value': 399}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '6.6 km', 'value': 6556}, 'duration': {'text': '24 mins', 'value': 1462}, 'status': 'OK'}, {'distance': {'text': '5.8 km', 'value': 5750}, 'duration': {'text': '20 mins', 'value': 1211}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '5.9 km', 'value': 5863}, 'duration': {'text': '20 mins', 'value': 1207}, 'status': 'OK'}, {'distance': {'text': '5.8 km', 'value': 5750}, 'duration': {'text': '20 mins', 'value': 1211}, 'status': 'OK'}, {'distance': {'text': '0.6 km', 'value': 626}, 'duration': {'text': '2 mins', 'value': 127}, 'status': 'OK'}, {'distance': {'text': '6.6 km', 'value': 6556}, 'duration': {'text': '24 mins', 'value': 1462}, 'status': 'OK'}, {'distance': {'text': '5.5 km', 'value': 5479}, 'duration': {'text': '19 mins', 'value': 1145}, 'status': 'OK'}, {'distance': {'text': '5.5 km', 'value': 5459}, 'duration': {'text': '20 mins', 'value': 1218}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 316}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1089}, 'duration': {'text': '5 mins', 'value': 277}, 'status': 'OK'}, {'distance': {'text': '6.6 km', 'value': 6610}, 'duration': {'text': '23 mins', 'value': 1397}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1089}, 'duration': {'text': '5 mins', 'value': 277}, 'status': 'OK'}, {'distance': {'text': '6.0 km', 'value': 6046}, 'duration': {'text': '22 mins', 'value': 1300}, 'status': 'OK'}, {'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 316}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1123}, 'duration': {'text': '5 mins', 'value': 290}, 'status': 'OK'}, {'distance': {'text': '0.7 km', 'value': 668}, 'duration': {'text': '3 mins', 'value': 197}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 316}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1089}, 'duration': {'text': '5 mins', 'value': 277}, 'status': 'OK'}, {'distance': {'text': '6.6 km', 'value': 6610}, 'duration': {'text': '23 mins', 'value': 1397}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1089}, 'duration': {'text': '5 mins', 'value': 277}, 'status': 'OK'}, {'distance': {'text': '6.0 km', 'value': 6046}, 'duration': {'text': '22 mins', 'value': 1300}, 'status': 'OK'}, {'distance': {'text': '1.3 km', 'value': 1291}, 'duration': {'text': '5 mins', 'value': 316}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1123}, 'duration': {'text': '5 mins', 'value': 290}, 'status': 'OK'}, {'distance': {'text': '0.7 km', 'value': 668}, 'duration': {'text': '3 mins', 'value': 197}, 'status': 'OK'}]}, {'elements': [{'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 240}, 'status': 'OK'}, {'distance': {'text': '0.9 km', 'value': 922}, 'duration': {'text': '3 mins', 'value': 195}, 'status': 'OK'}, {'distance': {'text': '6.3 km', 'value': 6300}, 'duration': {'text': '21 mins', 'value': 1289}, 'status': 'OK'}, {'distance': {'text': '1.1 km', 'value': 1123}, 'duration': {'text': '4 mins', 'value': 261}, 'status': 'OK'}, {'distance': {'text': '0.9 km', 'value': 922}, 'duration': {'text': '3 mins', 'value': 195}, 'status': 'OK'}, {'distance': {'text': '5.7 km', 'value': 5735}, 'duration': {'text': '20 mins', 'value': 1191}, 'status': 'OK'}, {'distance': {'text': '0.8 km', 'value': 772}, 'duration': {'text': '4 mins', 'value': 240}, 'status': 'OK'}, {'distance': {'text': '1 m', 'value': 0}, 'duration': {'text': '1 min', 'value': 0}, 'status': 'OK'}, {'distance': {'text': '1.6 km', 'value': 1609}, 'duration': {'text': '7 mins', 'value': 399}, 'status': 'OK'}]}], 'status': 'OK'}
	print(diction)
	df = pd.DataFrame(columns = diction['destination_addresses'], index = diction['origin_addresses'])
	print(df)
	list_of_list = []
	for (i,j) in zip(diction['origin_addresses'] ,diction['rows']):
		print(j)
		print(type(j['elements']))
		dt_lst = []
		for z in j['elements']:
			distance = z['distance']['text']
			time = z['duration']['text']
			value = distance,time
			dt_lst.append(value)
		list_of_list.append(dt_lst)
	print(list_of_list)
	df = pd.DataFrame(list_of_list, index=diction['origin_addresses'], columns = diction['destination_addresses'])
	print(df)

	df.to_csv('CHOA_output_'+ str(track_across)+'_'+str(track_down)+'.csv')

def rev_geo(client, file):
	
	data = pd.read_csv(file)
	data.dropna(how='any',inplace=True)
	print(data)
	states = []
	count = -1
	for index, row in data.iterrows():
		count = count + 1
		#to bypass the 50 requests per minute limit
		if count == 0:
			continue
		elif count % 50 == 0:
			time.sleep(1)
		
		location = (float(row['Latitude']),-1*float(row['Longitude']))
		print(location)
		# latitude = 35.1330343
		# longitude = -90.0625056

		output = geocoding.reverse_geocode(client, location, result_type = 'administrative_area_level_1')
		
		# with open('practice_location.json', 'w') as f:
		# 	json.dump(output, f, index= 4)
		print(output)
		print(output[0]['address_components'][0]['short_name'])
		states.append(output[0]['address_components'][0]['short_name'])

		
	# 	print(i['formatted_address'].rsplit(', ', 2)[1].split()[0])
	print(states)
	df['State'] = states
	df.to_csv('update_locations.csv')
	return df



#get the distance and times from the Google API
def main(args):

	gmaps = googlemaps.Client(key=args.api_key)
	#use the google reverse geolocation code and in file'
	#current data is stored in lcoation.csv
	if args.api == 'rev_geo':
		return rev_geo(gmaps, args.in_file)

	# constructing the Google Maps API
	main_string = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
	ending = '&mode=bicycling&key='

	origin='origins='
	dest = '&destinations='

	origin_lst = []
	dest_lst = []

	print('Reading from file: '+ str(args.in_file))
	source = pd.read_excel(args.in_file, sheet_name=0)
	source_end = pd.read_excel(args.in_file,sheet_name=1)

	#get the patient location from the excel sheet
	source.drop_duplicates(subset=['Sibley_ID', 'Patient_Latitude', 'Patient_Longitude'], inplace = True)
	patient = source[['Sibley_ID', 'Patient_Latitude', 'Patient_Longitude']]
	patient['Patient_Longitude'] = -1*source['Patient_Longitude']		#needs to be negative, or else its in China
	print(patient.head())
	print('Number of Unique Sibley Patients: ' + str(len(patient)))

	#get the office location from the excel sheet
	dept = source_end[['Dept_ID', 'Dept_Location_Latitude', 'Dept_Location_Longitude']]
	# dept_id   = source_end['Dept_ID']
	# dept_name = source_end['Dept_Name']
	# dept_lat  = source_end['Dept_Location_Latitude']
	dept['Dept_Location_Longitude'] = -1*source_end['Dept_Location_Longitude']	#needs to be negative, or else its in China
	print('Number of Sibley Departments: '+ str(len(dept)))

	#only iterate across a few of them so as to avoid high pricing
	track_across = 10
	track_down = 10
	iterator = 10
	#sending out the request
	for k in range(int(np.floor(len(patient)/iterator))+1):
		for j in range(track_across - iterator, min(track_across, 177)):
			for i in range(track_down - iterator, min(track_down, 177)):

				start_lat = str(patient['Patient_Latitude'].iloc[i])
				start_long= str(patient['Patient_Longitude'].iloc[i])

				end_lat = str(dept['Dept_Location_Latitude'].iloc[j])
				end_long = str(dept['Dept_Location_Longitude'].iloc[j])

				origin = start_lat , start_long 
				dest =  end_lat , end_long 

				origin_lst.append(origin)
				dest_lst.append(dest)
				
			track_down += iterator
			print('')
			print(origin_lst)
			print(dest_lst)
			print()

			time.sleep(3)

			gmaps = googlemaps.Client(key=api_key)
			output = googlemaps.distance_matrix.distance_matrix(client = gmaps,origins=origin_lst, destinations=dest_lst)
			print(type(output))
			print(output)

			file_print(output)


			print(origin_lst)
			print(dest_lst)
			print()

			origin_lst = []
		track_across += iterator

	print('DONE!!!')





# js = pd.read_json(txt)
# print(js)
# print(js.iloc[0]['rows'])

# distance = []
# time = []
# for i in js['rows']:
# 	distance.append(i['elements'][0])


# # #webscraping
# # page = urllib.request.urlopen(txt)
# # content = page.read()
# # print(content)
# # soup = BeautifulSoup(content,"lxml")
# # print(str(soup))
# # new = json.loads(str(soup))	

# # print(new)
# # name_box = soup.find('pre')

# fd = open('copy.txt','w')
# fd.write(txt)
# fd.close()

# # df = open()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-in_file', type = str, help = 'provide the excel file name including file handle')
	parser.add_argument('-api', help = 'provide google API to use (eg dist_matrix, rev_geo)')
	parser.add_argument('-api_key')
	args = parser.parse_args()

	main(args)