import requests
import re
import json
import psycopg2
import sys
from datetime import datetime, date, time

#connect the ASSIST server
url = 'http://ais-receiver.d2.comp.nus.edu.sg:8443'
s = requests.Session()
s.auth = ('sTi008LAtria','xIAYleR5A9oa')
#start the session
r1 = s.post(url+'/start')
sessionId = r1.json()['session_id']
id = {'session_id':sessionId}

#connect to the database with dbname and user password as it is on the computer where the original database is. Users would need to replace the database name and password with their own.
conn = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=admin")
cur = conn.cursor()
while True:
	#retrieve the next chunk of AIS messages received
	r2 = s.post(url+'/next',id)
	if r2.json()['status'] == 'ok':
		jsonobj = r2.json()['messages']
	jsonstr = json.dumps(jsonobj)
	jsonstr = jsonstr[1:-1]
	p = re.compile('},\s*{')
	jsonstr = p.sub('}\n{',jsonstr)
	
	print jsonstr
	#get the array of AIS messages
	jsonarr = jsonstr.split('\n')
	#load each AIS message
	for jsonstr in jsonarr:
		jsonobj = json.loads(jsonstr)
		#according to the type of message (1, 2, 3, 18 for position messages; 5, 19 for static messages), parse the relevant data field and store in the position_msg or static_msg table
		if 'message_type' in jsonobj:
			if jsonobj['message_type'] == 1 or jsonobj['message_type'] == 2 or jsonobj['message_type'] == 3 or jsonobj['message_type'] == 18:
				message_type = jsonobj['message_type']
				repeat_indicator = jsonobj['repeat_indicator']
				mmsi = jsonobj['mmsi']
				channel = jsonobj['channel']
				if 'navigation_status' in jsonobj:
					navigation_status = jsonobj['navigation_status']
				else: navigation_status = 'null'
				if 'rate_of_turn' in jsonobj:
					rate_of_turn = jsonobj['rate_of_turn']
				else: rate_of_turn = 'null'
				speed_over_ground = jsonobj['speed_over_ground']
				position_accuracy = jsonobj['position_accuracy']
				longitude = jsonobj['longitude']
				latitude = jsonobj['latitude']
				course_over_ground = jsonobj['course_over_ground']
				true_heading = jsonobj['true_heading']
				
				if 'manoeuvre_indicator' in jsonobj:
					manoeuvre_indicator = jsonobj['manoeuvre_indicator']
				else: manoeuvre_indicator = 'null'
				raim = jsonobj['raim']
				sync_state = jsonobj['sync_state']
				#if timestamp is already recorded, update the second of the timestamp with that reported in the AIS positional message; else take the current timestamp with the time zone '+08'
				try:
					timestamp
					if jsonobj['message_type']==1 or jsonobj['message_type']==2 or jsonobj['message_type']==3 or jsonobj['message_type']==18:
						second_of_timestamp = jsonobj['second_of_timestamp']
						if second_of_timestamp >= 60:
							second_of_timestamp = second_of_timestamp%60
						elif second_of_timestamp<10:
							second_of_timestamp = '0'+str(second_of_timestamp)
						print 'Second of timestamp: '+str(second_of_timestamp)
						timeStamp = str(timestamp)[:17]+str(second_of_timestamp)+str(timestamp)[19:]
						
				except NameError:
					timestamp = str(datetime.now())[:19]+'+08'
					timeStamp = timestamp	
				#insert the data fields into the positional message table
				try: 
					cur.execute("INSERT INTO position_msg(message_type, repeat_indicator, mmsi, channel, navigation_status, rate_of_turn, speed_over_ground, position_accuracy, longitude, latitude, course_over_ground, true_heading, manoeuvre_indicator, raim, sync_state, timestamp) VALUES(%s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s');"%(message_type, repeat_indicator, mmsi, channel, navigation_status, rate_of_turn, speed_over_ground, position_accuracy, longitude, latitude, course_over_ground, true_heading, manoeuvre_indicator, raim, sync_state, timeStamp))
					print "mmsi %s inserted at time %s"%(mmsi, timeStamp)
				except psycopg2.IntegrityError:
					print "Duplicate values found for mmsi %s. Insertion of position message was not successful."%(mmsi)
				conn.commit()
				
			#this is for insertion of static messages
			elif jsonobj['message_type'] == 5 or jsonobj['message_type'] == 19:
				message_type = jsonobj['message_type']
				repeat_indicator = jsonobj['repeat_indicator']
				mmsi = jsonobj['mmsi']
				channel = jsonobj['channel']
				if 'ais_version' in jsonobj:
					ais_version = jsonobj['ais_version']
				else: ais_version = 'null'
				if 'imo' in jsonobj:
					imo = jsonobj['imo']
				else: imo = 'null'
				if 'call_sign' in jsonobj:
					call_sign = jsonobj['callsign']
				else:
					call_sign = 'null'
				ship_name = jsonobj['ship_name']
				ship_type = jsonobj['ship_type']
				to_bow = jsonobj['to_bow']
				to_stern = jsonobj['to_stern']
				to_port = jsonobj['to_port']
				to_starboard = jsonobj['to_starboard']
				epfd = jsonobj['epfd']
				if 'eta_month' in jsonobj:
					eta_month = jsonobj['eta_month']
				else:
					eta_month = 'null'
				if 'eta_day' in jsonobj:
					eta_day = jsonobj['eta_day']
				else:
					eta_day = 'null'
				if 'eta_hour' in jsonobj:
					eta_hour = jsonobj['eta_hour']
				else:
					eta_hour = 'null'
				if 'eta_minute' in jsonobj:
					eta_minute = jsonobj['eta_minute']
				else:
					eta_minute = 'null'
				if 'draught' in jsonobj:
					draught = jsonobj['draught']
				else: draught = 'null'
				if 'destination' in jsonobj:
					destination = str(jsonobj['destination']).replace("'","")
				else:
					destination = 'null'
					
				if 'dte' in jsonobj:
					dte = jsonobj['dte']
				else:
					dte = 'null'
				try:
					timestamp
				except NameError:
					timestamp = str(datetime.now())[:19]+'+08'
				
				try:
					cur.execute("INSERT INTO static_msg(message_type, repeat_indicator, mmsi, channel, ais_version, imo, callsign, ship_name, ship_type, to_bow, to_stern, to_port, to_starboard, epfd, eta_month, eta_day, eta_hour, eta_minute, draught, destination, dte, timestamp) VALUES(%s, %s, %s, '%s', %s, %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s');"%(message_type, repeat_indicator, mmsi, channel, ais_version, imo, call_sign, ship_name, ship_type, to_bow, to_stern, to_port, to_starboard, epfd, eta_month, eta_day, eta_hour, eta_minute, draught, destination, dte, timestamp))
				except psycopg2.IntegrityError:
					print "Duplicate values found for mmsi %s. Insertion of static message was not successful."%(mmsi)
				conn.commit()
		#this is for when no message is detected, the timestamp will still be reported and updated
		elif 'timestamp' in jsonobj:
			timestamp = jsonobj['timestamp']
			if 'T01' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+01')
			elif 'T02' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+02')
			elif 'T03' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+03')
			elif 'T04' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+04')
			elif 'T05' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+05')
			elif 'T06' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+06')
			elif 'T07' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+07')
			elif 'T08' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+08')
			elif 'T09' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+09')
			elif 'T10' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+10')
			elif 'T11' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+11')
			elif 'T12' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+12')
			elif 'T13' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+13')
			elif 'T14' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+14')
			elif 'T15' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+15')
			elif 'T16' in timestamp:
				timestamp = timestamp.replace('T',' ').replace('+00:00','+16')
			#print timestamp
	
cur.close()
conn.close()