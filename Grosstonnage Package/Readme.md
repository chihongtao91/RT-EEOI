# Details
- To use this package, you will need to install selenium following the instruction in the selenium-2.33.0 folder. 
- Copy and paste the installed folders: 'selenium','selenium-2.33.0-py2.7.egg-info','setuptools-0.7.5-py2.7.egg-info' from ...Python27/Lib/site-packages to the same directory where the scripts are. 
- In the command window, call the ship_info script using the following command:
```
python ship_info.py chtnus 709qyv38
```
- In above statement, the sequence of arguments after the script name are: the username of a grosstonnage.com account and its password.
- The account name and password above are temporary and would have expired now.
- Next, run the grosstonnage script with
```
python grosstonnage.py
```
- The command would search the grosstonnage.com site for relevant ship information such as IMO number, engine specification, fuel type, nominal draught, tpc for those vessels whose positional or static messages have been registered by the AIS receiver. These ship information will be parsed and stored in the local ship information database.
- In order to access the database using PostgreSQL, user will have to replace the *database name (dbname)* and *password* with their own in the script. 
 In our database design, the positional and static messages are stored on the local machine with the table name ***position_msg*** and ***static_msg***. The name of the ship information table is ***ship_info***.  
