import httpGet
import psycopg2

#the use of this script is to crawl relevant information for the vessels detected by AIS receiver, system arguments are the account and password for the grosstonnage.com website
def main(account, password):
	#Connect to the database with dbname and user password as it is on the computer where the original database is. Users would need to replace the database name and password with their own.
	conn2 = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=admin")
	cur = conn2.cursor()
	#get the mmsi list of the vessels already stored in the ship information table
	cur.execute("SELECT mmsi from ship_info;")
	mmsiList = cur.fetchall()
	existingMMSI = ' '.join(map(str,mmsiList))
	
	#get the list of mmsi from all the vessels whose static AIS messages have been recorded by AIS receiver
	cur.execute("SELECT mmsi from static_msg;")
	
	list = cur.fetchall()
	for i in range(len(list)):
		mmsi = ''.join(map(str,list[i]))
		
		#skip if the mmsi is already stored in the ship information database
		if mmsi in existingMMSI:
			print "mmsi "+mmsi+" already exists in ship_info"
		#if not, use the httpGet script to parse and store relevant information in the ship information database
		else:
			httpGet.main(account,password,mmsi)
	
	#get the list of mmsi from all the vessels whose positional AIS messages have been recorded by AIS receiver
	cur.execute("SELECT mmsi from position_msg;")
	
	list = cur.fetchall()
	for i in range(len(list)):
		mmsi = ''.join(map(str,list[i]))
		
		#skip if the mmsi is already stored in the ship information database
		if mmsi in existingMMSI:
			print "mmsi "+mmsi+" already exists in ship_info"
		#if not, use the httpGet script to parse and store relevant information in the ship information database
		else:
			httpGet.main(account,password,mmsi)
	
	conn2.commit()
	cur.close()
	conn2.close()
	
if __name__ == '__main__':
    main()