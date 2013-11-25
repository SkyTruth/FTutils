
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @PA_Spud PA_Spud
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @PA_DrillingPermit PA_DrillingPermit
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @PA_Violation PA_Violation
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=seqid --max_recs=1000 @FracFocusReport FracFocusReport
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @CogisInspection CogisInspection
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @CogisSpill CogisSpill
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=1000 @WV_DrillingPermit WV_DrillingPermit
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=reportnum --max_recs=5000 @NrcScrapedReport NrcScrapedReport
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=reportnum --max_recs=5000 @NrcParsedReport NrcParsedReport
/srv/scrapy/bin/python /srv/scrapy/FTutils/scripts/ftapi-sync.py DB2FT --seq_field=st_id --max_recs=5000 @NrcScrapedMaterial NrcScrapedMaterial
