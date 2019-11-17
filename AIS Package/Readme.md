# Details
- The AIS.py script uses the ASSIST API developed by Mr Thomas Kister to retrieve AIS messages in real time and store them in the local database. (Please note the API endpoints specified in the scripts have been deprecated)
- The script, if run under command line, can only be stopped manually. As long as it runs, it will stream positional and static AIS messages, which will be stored in the position_msg and static_msg table in the local database. No system arguments are required. 
