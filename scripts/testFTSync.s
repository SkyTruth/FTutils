#!bash

# THIS SHOULD NOT BE RUN ON THE SERVER. 
# IT WILL CORRUPT THE SYNC BETWEEN THE DATABASE AN THE TABLE.
# EXECUTE ON A MACHINE WITH A SCRATCH DATABASE.

#/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @PA_Spud PA_Spud

~/Dev/SkyTruth1/Scripts/python.exe ./ftapi-sync.py DB2FT --seq_field=st_id --max_recs=150 @TestFTSync_CogisSpill CogisSpill

