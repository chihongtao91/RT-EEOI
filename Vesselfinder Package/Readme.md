# Details 
- This package is for crawling and updating vessel information such as *gross tonnage*, *net tonnage*, *deadweight*, *current draught*, *nominal draught*, *design speed*, *ship type* in the ship information table on the local database. 
- Run the loop.py using below command
```
python loop.py
```
- Insertion will be performed for each vessel in the existing vessel information database. Insertion for individual vessel with a given mmsi could also be performed from the command line as follow:
```
python vesselFinderParse.py 220417000
```
,where the mmsi has to be used as an argument. 

- Alternatively, the loop.py script can be used to select all vessels MMSIs in the database, and crawl their ship information vessel by vessel.
