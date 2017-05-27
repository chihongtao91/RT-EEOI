{\rtf1\ansi\ansicpg1252\cocoartf1344\cocoasubrtf720
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural

\f0\fs24 \cf0 The AIS.py script uses the ASSIST API developed by Mr Thomas Kister to retrieve AIS messages in real time and store them in the local database. In order to access the database using PostgreSQL, you will need to install the psycopg2 module.\
\
The script, if run under command line, can only stopped manually. As long as it runs, it will stream positional and static AIS messages, which will be stored in the position_msg and static_msg table in the local database. No system arguments are required. }