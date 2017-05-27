import vesselFinderParse
import addShipType
import psycopg2

#this script loops all the vessel within the ship_info table to perform insertion of relevant data
def main():
	conn2 = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=admin")
	cur = conn2.cursor()
	cur.execute("SELECT mmsi from ship_info;")
	list = cur.fetchall()

	for i in range(len(list)):
		mmsi = ''.join(map(str,list[i]))
		#perform crawling and insertion of relevant data for the given mmsi
		vesselFinderParse.main(mmsi)
	conn2.commit()
	cur.close()
	conn2.close()

if __name__ == '__main__':
    main()