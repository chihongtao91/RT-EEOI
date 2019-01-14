Prior to using the three packages, a local database needs to be constructed. Python and PostgreSQL are used together in the three packages. In order to access the database using PostgreSQL, you will need to install the psycopg2 module.

The local database would have three tables, namely ship_info, position_msg, static_msg respectively. The ship_info table is for storing vessel information such as mmsi, design speed, draught information, tpc, engine information, net tonnage and so on. The primary key is the mmsi. (The detailed schema can be found in the paper in this directory)

The other two tables store positional and static AIS messages obtained through the ASSIST API. These tables will be first populated by running the AIS.py in the AIS Package.

Next, vessel information of ships registered by the AIS receivers will be furnished from the grosstonnage.com using the Grosstonnage Package and stored in the ship_info table. This step requires an account for the grosstonnage.com website (deprecated). The ship_info table will then be further updated using the Vesselfinder Package. 

In this repo, you can also find a paper published in the Energy journal as well as the slides used in presentation to IEEE Industrial Engineering & Engineering Management Conference (Big Data & Analytics session). 

Thanks for reading! 
