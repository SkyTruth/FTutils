#bash

# THIS SHOULD NOT BE RUN ON THE SERVER. 
# IT WILL CORRUPT THE SYNC BETWEEN THE DATABASE AN THE TABLE.
# EXECUTE ON A MACHINE WITH A SCRATCH DATABASE.
if [ `uname -n` = 'ewn3' ] ; then echo THIS TEST DOES NOT OPERATE ON ewn3; exit; fi

# for ewn4
#/srv/scraper/bin/python ./ftapi-sync.py DB2FT --seq_field=st_id --max_recs=150 @TestFTSync_CogisSpill CogisSpill
/srv/scrapy/bin/python ./ftapi-sync.py DB2FT --seq_field=st_id --max_recs=150 @TestFTSync_CogisSpill CogisSpill

# for windows machines
#~/Dev/SkyTruth1/Scripts/python.exe ./ftapi-sync.py DB2FT --seq_field=st_id --max_recs=150 @TestFTSync_CogisSpill CogisSpill

