import sys
import psycopg2
import urllib
import convertHex

#This function extracts the desired information by providing the original mainStr and the string before and after the desired information
def find(mainStr, front, back):
    startIdx = mainStr.find(front) + len(front)
    offset = mainStr[startIdx:].find(back)
    endIdx = startIdx + offset
    return mainStr[startIdx:endIdx]

def main(s):
	#open the html page for parsing
	f = urllib.urlopen(s)
	#need to convert the hexadecimal representation to normal html code
	s = convertHex.main(f.read())
	
	#get IMO number on the page
	IMO = find(s, 'IMO&nbsp;NUMBER</p></td><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px"><p class="t10" style="margin-top:4;margin-bottom:4;margin-left:10;margin-right:0"><b>', '</b></p></td></tr><tr><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px" width="130px"><p class="t10" style="margin-top:4;margin-bottom:4;margin-left:0;margin-right:0">MMSI&nbsp;CODE')
	if len(IMO)>50:
		IMO=""
	
	#get MMSI number on the page
	mmsi = find(s, 'MMSI&nbsp;CODE</p></td><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px"><p class="t10" style="margin-top:4;margin-bottom:4;margin-left:10;margin-right:0"><b>', '</b></p></td></tr><tr><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px" width="130px">').replace(" ","")
	if len(mmsi)>50:
		mmsi=""
		
	#breadth = find(s,"BREADTH&nbsp;EXTREME</small></td><td style='border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px'><p class='t10' style='margin-top:4;margin-bottom:4;margin-left:10;margin-right:0'><b><b>","</b>&nbsp;m</td></tr>").replace(",",".")
	#if len(breadth)>50:
	#	breadth=""

	#length = find(s, "LENGTH&nbsp;OVERALL</small></td><td style='border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px'><p class='t10' style='margin-top:4;margin-bottom:4;margin-left:10;margin-right:0'><b><b>", "</b>&nbsp;m</td></tr>").replace(",",".")
	#if len(length)>50:
	#	length=""

	#_call_sign = find(s,"CALL%26nbsp%3BSIGN%3C%2Ftd%3E%3Ctd%20style%3D%27border-bottom-color%3A1861D3%3Bborder-bottom-style%3Asolid%3Bborder-bottom-width%3A1px%3Bborder-left-width%3A0px%3Bborder-right-width%3A0px%3Bborder-top-width%3A0px%27%3E%3Cp%20class%3D%27t10%27%20style%3D%27margin-top%3A4%3Bmargin-bottom%3A4%3Bmargin-left%3A10%3Bmargin-right%3A0%27%3E%3Cb%3E","%3C%2Fa%3E%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%20")
	#print _call_sign

	#_name = find(s,"style%3D%27margin-top%3A0%3Bmargin-bottom%3A0%3Bmargin-left%3A40%3Bmargin-right%3A0%27%3E%3Ctr%3E%3Ctd%20valign%3D%27top%27%3E%3Cp%20class%3D%27t16%27%20style%3D%27margin-top%3A0%3Bmargin-bottom%3A0%3Bmargin-left%3A0%3Bmargin-right%3A0%27%3E%3Cb%3E", "%3C%2Fb%3E%3C%2Fa%3E%3C%2Ftd%3E%3Ctd%20align%3D%27right").replace("%20"," ")
	#print _name
	
	#get engine information on the page
	engine_cylinders = find(s,'ENGINE&nbsp;CYLINDERS</p></td><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px"><p class="t10" style="margin-top:4;margin-bottom:4;margin-left:10;margin-right:0"><b><b>','</b>&nbsp;</b></p></td></tr><tr>')
	if len(engine_cylinders)>50:
		engine_cylinders=""

	engine_power = find(s,'ENGINE&nbsp;POWER</p></td><td style="border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px"><p class="t10" style="margin-top:4;margin-bottom:4;margin-left:10;margin-right:0"><b><b>','</b>&nbsp;KW</b></p></td></tr>')
	if len(engine_power)>50:
		engine_power=""

	engine_stroke = find(s,"ENGINE&nbsp;STROKE</small></td><td style='border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px'><p class='t10' style='margin-top:4;margin-bottom:4;margin-left:10;margin-right:0'><b><b>","</b>&nbsp;mm</td></tr>")
	if len(engine_stroke)>50:
		engine_stroke=""
	
	#get fuel type on the page
	fuel_type = find(s,"FUEL&nbsp;TYPE</small></td><td style='border-bottom-color:1861D3;border-bottom-style:solid;border-bottom-width:1px;border-left-width:0px;border-right-width:0px;border-top-width:0px'><p class='t10' style='margin-top:4;margin-bottom:4;margin-left:10;margin-right:0'><b><b>","</b>&nbsp;</b></p></td></tr><tr>").replace("&nbsp;"," ")
	if len(fuel_type)>50:
		fuel_type=""
		
	#get tpc data on the page if any
	tpc = urllib.unquote(find(s,"TPC%26nbsp%3BIMMERSION%26nbsp%3B%3Csmall%3E%28SUMMER%26nbsp%3BDRAFT%29%3C%2Fsmall%3E%3C%2Ftd%3E%3Ctd%20style%3D%27border-bottom-color%3A1861D3%3Bborder-bottom-style%3Asolid%3Bborder-bottom-width%3A1px%3Bborder-left-width%3A0px%3Bborder-right-width%3A0px%3Bborder-top-width%3A0px%27%3E%3Cp%20class%3D%27t10%27%20style%3D%27margin-top%3A4%3Bmargin-bottom%3A4%3Bmargin-left%3A10%3Bmargin-right%3A0%27%3E%3Cb%3E%3Cb%3E","%3C%2F"))
	if len(tpc)>50:
		tpc = ""
	else:
		tpc = tpc.replace(",",".")
	
	#get nominal draught of the vessel on the page	
	draught =urllib.unquote(find(s,"DRAUGHT%3C%2Fsmall%3E%3C%2Ftd%3E%3Ctd%20style%3D%27border-bottom-color%3A1861D3%3Bborder-bottom-style%3Asolid%3Bborder-bottom-width%3A1px%3Bborder-left-width%3A0px%3Bborder-right-width%3A0px%3Bborder-top-width%3A0px%27%3E%3Cp%20class%3D%27t10%27%20style%3D%27margin-top%3A4%3Bmargin-bottom%3A4%3Bmargin-left%3A10%3Bmargin-right%3A0%27%3E%3Cb%3E%3Cb%3E","%3C%2Fb%3E%26nbsp%3Bm%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%20style"))
	
	if len(draught)>50:
		draught = ""
	else: 
		draught = draught.replace(",",".")
				
	#Connect to the database with dbname and user password as it is on the computer where the original database is. Users would need to replace the database name and password with their own.
	conn = psycopg2.connect("host=localhost port=5433 dbname=postgres user=postgres password=admin")

	cur = conn.cursor()

	#insert the relevant data fields into the local database
	try:
		cur.execute("INSERT INTO ship_info (mmsi, source, timestamp, imo, engine_cylinder, engine_stroke, engine_power, fuel_type, draught, tpc) VALUES(%s, 'www.grosstonnage.com', current_timestamp, %s, %s, %s, %s, '%s', %s, %s);"%mmsi, IMO, length, breadth, engine_cylinders, engine_stroke, engine_power, fuel_type, draught, tpc)

		conn.commit()
		print "Successfully inserted mmsi "+mmsi+" into ship_info"
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
		f.close()

if __name__ == '__main__':
    main()
