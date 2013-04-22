
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @PA_Spud PA_Spud
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @PA_DrillingPermit PA_DrillingPermit
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @PA_Violation PA_Violation
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=seqid --max_recs=1000 @FracFocusReport FracFocusReport
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @CogisInspection CogisInspection
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @CogisSpill CogisSpill
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=1000 @WV_DrillingPermit WV_DrillingPermit
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=reportnum --max_recs=5000 @NrcScrapedReport NrcScrapedReport
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=reportnum --max_recs=5000 @NrcParsedReport NrcParsedReport
/srv/scraper/bin/python /srv/scraper/FTutils/scripts/ft-sync DB2FT --seq_field=st_id --max_recs=5000 @NrcScrapedMaterial NrcScrapedMaterial

