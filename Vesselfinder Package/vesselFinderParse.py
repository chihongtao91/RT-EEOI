import psycopg2
import urllib
import sys

#This function extracts the desired information by providing the original mainStr and the string before and after the desired information
def find(mainStr, front, back):
    startIdx = mainStr.find(front) + len(front)
    offset = mainStr[startIdx:].find(back)
    endIdx = startIdx + offset
    return mainStr[startIdx:endIdx]

#This script is used to crawl relevant information such as gross tonnage, net tonnage, deadweight, current draught, nominal draught, design speed, ship type and store it in the ship information table on local machine
def main(mmsi):
	#open the url of the search result page for the specified mmsi on vesselfinder.com
	source = urllib.urlopen("http://www.vesselfinder.com/vessels?name="+mmsi)
	s=source.read()
	
	url=find(s,'<a href="/vessels/','" class="th" role="button">')
	print url
	
	#open the vessel information page and crawl the required data fields 
	pageSource = urllib.urlopen("http://www.vesselfinder.com/vessels/"+url)
	s=pageSource.read()

	name = find(s, '<div class="ship-description" itemprop="description"><p>Vessel named "', '", registered with IMO number')


	call_sign = find(s, '<span class="small-7 columns value" itemprop="callsign">', '</span>')


	current_draught = find(s,'''<span class="small-5 columns name">Current draught:</span>
						<span class="small-7 columns value">
							''',''' m						</span>''')

	design_speed = find(s,'<td>Speed recorded (Max / Average)</td>','</td>')
	design_speed = find(design_speed.strip(),'<td>',' / ')
	
	draught = find(s,'<span class="small-7 columns value" itemprop="Draught">',' m</span>')
	
	grossTonnage = find(s,'<span class="small-7 columns value" itemprop="GT">',' t</span>')
	
	netTonnage = find(s,'<span class="small-7 columns value" itemprop="NT">',' t</span>')
	
	deadWeight = find(s,'<span class="small-7 columns value" itemprop="DWT">',' t</span>')
	
	ship_type = find(s,'''<span class="small-5 columns name">Ship type:</span>
						<span class="small-7 columns value" itemprop="type">''','</span>')

	conn = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=admin")

	cur = conn.cursor()

	if len(name)>50:
		name = ''
	print "name: "+name

	if len(design_speed)>50:
		design_speed=''
	else:
		design_speed.strip()
	print "Design speed: "+design_speed

	if len(current_draught)>50:
		current_draught=''
	else: 
		current_draught.strip()
	print "Current draught: "+current_draught
	
	if len(draught)>50:
		draught=''
	else:
		draught.strip()
	print "Draught: "+draught
		
	if len(call_sign)>50:
		call_sign = ''
	print "call sign: "+call_sign

	if len(grossTonnage)>50:
		grossTonnage = ''
	else:
		grossTonnage.strip()
	print "Gross tonnage: "+grossTonnage

	if len(netTonnage)>50:
		netTonnage = ''
	else:
		netTonnage.strip()
	print "Net tonnage: "+netTonnage

	if len(deadWeight)>50:
		deadWeight = ''
	else:
		deadWeight.strip()
	print "Deadweight: "+deadWeight
	
	if len(ship_type)>50:
		ship_type = ''
	else:
		ship_type.strip()
	print ship_type
	
	#perform insertion into the ship information table for the given mmsi
	try:
		cur.execute("UPDATE ship_info SET call_sign='%s', name='%s', current_draught=%s, design_speed=%s, draught=%s, gross_tonnage=%s, net_tonnage=%s, dead_weight=%s, ship_type=%s WHERE mmsi=%s;"%(call_sign, name, current_draught, design_speed, draught, grossTonnage, netTonnage, deadWeight, mmsi, ship_type))
		print "Relevant information inserted for mmsi: "+mmsi
		conn.commit()
	except ValueError:
		cur.close()
		conn.close
	except psycopg2.IntegrityError:
		print "mmsi "+mmsi+" already exists"
		cur.close()
		conn.close()
	except psycopg2.ProgrammingError:
		print "Missing fields for mmsi "+mmsi
		cur.close()
		conn.close()
	except NameError:
		cur.close()
		conn.close()
	finally:
		cur.close()
		conn.close()

if __name__ == '__main__':
    main()