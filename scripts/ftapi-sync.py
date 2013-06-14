#!python
#Fusion Table Insert/Update Utility

#from FTSync.MysqlFTSync import MysqlFTSync
from FTSync.PostgresFTSync import PostgresFTSync

# modify path for FTAPI_v1
import sys, os
import FTSync
v1_path = os.path.join(os.path.dirname(os.path.dirname(FTSync.__file__)),
                                       'FTAPI_v1')
sys.path.append(v1_path)
print "Add to sys.path:", v1_path

from FTClient import FTClient
#from FTClient.authorization.clientlogin import ClientLogin
import psycopg2
import logging
from optparse import OptionParser
#import contextlib
#import sys
#import os.path
import time

import settings

USE_API_KEY = False

def get_args():
    desc = ("Syncs a Postgres table with a Fusion Table, using a sequential "
            "ID field as the key.  The tables must have the same schema, "
            "and must contain a single field that uniquely identifies each "
            "record and is also updated sequentially so every new record "
            "gets a larger value that all previous records")

    usage = """%prog [options] COMMAND FT_ID DB_TABLE

  COMMAND
    DB2FT    Sync records from the Postgres Table into the Fusion Table
    FT2DB    Sync records from the Fusion Table into the Postgres table

  FT_ID
    ID of the fusion table - to find the id, open the table and
    select File/About.
    This can also be a reference in the form @TABLE_NAME for
    tables in the table_id map in settings.py.
  DB_TABLE
    Postgres Table.  Column names must
    match columns in the fusion table
"""
    parser = OptionParser(description=desc, usage=usage)

    parser.set_defaults(loglevel=logging.INFO)
    parser.add_option("-q", "--quiet",
            action="store_const", dest="loglevel", const=logging.ERROR,
            help="Only output error messages")
    parser.add_option("-v", "--verbose",
            action="store_const", dest="loglevel", const=logging.DEBUG,
            help="Output debugging information")
    parser.add_option("--ft_id_field",
            action="store",  default='ft_id', type='string', dest='ft_id_field',
            help="Name of the column in the Postgres table that stores the "
                  "Fusion Table ROWID.  Default is 'ft_id'",
            metavar="FT_ID_FIELD")
    parser.add_option("--seq_field",
            action="store",  default='seqid', type='string', dest='seq_field',
            help="Name of the column in the Postgres table that stores the "
                 "unique key - always called 'seqid' in the Fusion Table.  "
                 "Default is 'seqid'.",
            metavar="SEQ_FIELD")
    parser.add_option("--max_recs",
            action="store",  default=1000, type='int', dest='max_recs',
            help="Maximum number of records to transfer",
            metavar="MAX_RECS")
    parser.add_option("--batch_size",
            action="store",  default=100, type='string', dest='batch_size',
            help="Number of records to sync in each batch",
            metavar="BATCH_SIZE")
    parser.add_option("--id_logfile",
            action="store", type='string', dest='id_logfile',
            help="File to write ids of synced records to for debug",
            metavar="ID_LOGFILE")

    (options, args) = parser.parse_args()

    if len(args) < 3:
        parser.error("Not enough arguments.")
    elif len(args) > 3:
        parser.error("Too many arguments.")
    if args[0] not in ('DB2FT', 'FT2DB'):
        parser.error("unknown command: %s" % args[0])

    return options, args

def get_ft():
#    ft_username = settings.FT_USERNAME
#    ft_password = settings.FT_PASSWORD
    if USE_API_KEY:
        logging.info ("Connecting to Fusion Tables with api key")
        ft_client = FTClient.APIKeyFTClient(settings.FTAPI_KEY)
    else:  # USE SERVICE ACCOUNT
        logging.info ("Connecting to Fusion Tables with service account")
        keyfile = open(settings.FTAPI_PRIVATE, "rb")
        key = keyfile.read()
        keyfile.close()
        ft_client = FTClient.ServiceAccountFTClient(
                client_id=settings.FTAPI_CLIENT_EMAIL, key=key, alt='csv')
    return ft_client

def get_db():
    db_host = settings.DB_HOST
    db_user = settings.DB_USER
    db_passwd = settings.DB_PASSWORD
    db_name = settings.DB_NAME
    logging.info ("Connecting to Postgres with host: %s  user: %s  db: %s "
                  %(db_host, db_user, db_name) )
    postgres_db = psycopg2.connect (
        host = db_host,
        user = db_user,
        password = db_passwd,
        database = db_name)
        #charset = 'utf8')
    postgres_db.autocommit = True
    return postgres_db

def get_ft_id(ft_table_nm):
    if ft_table_nm[0] == '@':
        if ft_table_nm[1:] in settings.table_ids:
            ft_table_id = settings.table_ids[ft_table_nm[1:]]
        else:
            logging.error ("Fusion table name '%s' not in settings.table_ids."
                           % ft_table_nm)
            return
    else:
        ft_table_id = ft_table_nm
    return ft_table_id

def get_ft_count(ft_client, table_id):
    sql = u'select count() from %s' % table_id
    result = ft_client.query(sql)
    if True:  # using json
        count = int(result['rows'][0][0])
    else: # using csv
        csv = ft_client.query(sql)
        try:
        	count = int( csv.split('\n')[1])
        except ValueError:
        	count = csv.split('\n')[1]
        except IndexError:
            count = csv
    return count

def do_DB2FT(ft_nm, db_nm, db_ft_sync, max_records, batch_size, id_logfile):
    success = False
    records_affected = 0
    ft_client = db_ft_sync.ft_client
    ft_id = get_ft_id(ft_nm)
    logging.debug ("Syncing %s to %s for max %s records"
                   % (db_nm, ft_nm, max_records))
    initial_count = get_ft_count(ft_client, ft_id)
    logging.info ("Fusion table %s initial size %s records."
                  % (ft_nm, initial_count))
    try:
        while records_affected < max_records:
            new_records_affected = db_ft_sync.sync_postgres_to_ft (
                    db_nm, ft_id, batch_size, id_logfile)
            if not new_records_affected:
                break
            records_affected += new_records_affected
            logging.info ("Total synced records: %s" % records_affected)
            time.sleep(0.5) # to avoid exceeding 5qps quota errors

        success=True
    except FTClient.FTClientError as e:
        logging.error (e.message)
    except psycopg2.Error as e:
        logging.error (e)

    # Check record count consistency
    final_count = get_ft_count(ft_client, ft_id)
    ft_added = final_count - initial_count
    logging.info (
            "Fusion table %s final size %s records; added %s records."
            % (ft_nm, final_count, ft_added))
    if records_affected != ft_added:
        logging.error (
            "Synced %s records; fusion table %s added %s; missing %s."
            % (records_affected, ft_nm, ft_added, records_affected-ft_added))
    return success, records_affected

def do_FT2DB(ft_nm, db_nm, db_ft_sync, max_records, batch_size, id_logfile):
    success = False
    records_affected = 0
    ft_id = get_ft_id(ft_nm)
    logging.debug ("Syncing %s to %s for max %s records"
                   % (ft_id, db_nm, max_records))
    try:
        while records_affected < max_records:
            new_records_affected = db_ft_sync.sync_ft_to_postgres (
                    db_nm, ft_id, batch_size)
            if not new_records_affected:
                break
            records_affected += new_records_affected

        success=True
    except FTClient.FTClientError as e:
        logging.error (e.message)

    except psycopg2.Error as e:
        logging.error (e)
    return success, records_affected


def main():
    options, args = get_args()

    command = args[0]
    ft_table_nm = args[1]
    db_table_nm = args[2]

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=options.loglevel)

    db_ft_sync = PostgresFTSync (get_ft(),
                                 get_db(),
                                 ft_id_field = options.ft_id_field,
                                 seq_field=options.seq_field)

    id_logfile = open(options.id_logfile, 'w') if options.id_logfile else None

    if command == 'DB2FT':
        success, records_affected = do_DB2FT(ft_table_nm,
                                             db_table_nm,
                                             db_ft_sync,
                                             max_records=options.max_recs,
                                             batch_size=options.batch_size,
                                             id_logfile=id_logfile)

    elif command == 'FT2DB':
        success, records_affected = do_FT2DB(ft_table_nm,
                                             db_table_nm,
                                             db_ft_sync,
                                             max_records=options.max_recs,
                                             batch_size=options.batch_size,
                                             id_logfile=id_logfile)

    if id_logfile:
	id_logfile.close()

    logging.info ("%s records affected" % records_affected)
    if success:
        logging.info ("Done." )
    else:
        logging.info ("Failed." )

    return

if __name__ == "__main__":
    main()

#    if command == 'DB2FT':
#        # reqd: db_table, ft_table_nm, ft_table_id, db_ft_sync
#        #       max_records, batch_size, id_log_file,
#        logging.debug ("Syncing %s to %s for max %s records"
#                       % (db_table, ft_table_nm, max_records))
#        initial_count = get_ft_count(ft_client, ft_table_id)
#        logging.info ("Fusion table %s initial size %s records."
#                      % (ft_table_nm, initial_count))
#        try:
#            while records_affected < max_records:
#                new_records_affected = db_ft_sync.sync_postgres_to_ft (
#                        db_table, ft_table_id, batch_size, id_logfile)
#                if not new_records_affected:
#                    break
#                records_affected += new_records_affected
#                logging.info ("Total synced records: %s" % records_affected)
#                time.sleep(0.5) # to avoid exceeding 5qps quota errors
#
#            success=True
#        except FTClient.FTClientError as e:
#            logging.error (e.message)
#        except psycopg2.Error as e:
#            logging.error (e)
#
#        # Check record count consistency
#        final_count = get_ft_count(ft_client, ft_table_id)
#        ft_added = final_count - initial_count
#        logging.info (
#                "Fusion table %s final size %s records; added %s records."
#                % (ft_table_nm, final_count, ft_added))
#        if records_affected != ft_added:
#            logging.error (
#                "Synced %s records; fusion table %s added %s; missing %s."
#                % (records_affected,
#                   ft_table_nm,
#                   ft_added,
#                   records_affected-ft_added))
#
#    elif command == 'FT2DB':
#        logging.debug ("Syncing %s to %s for max %s records"
#                       % (ft_table_id, db_table, max_records))
#        try:
#            while records_affected < max_records:
#                new_records_affected = db_ft_sync.sync_ft_to_postgres (
#                        db_table, ft_table_id, batch_size)
#                if not new_records_affected:
#                    break
#                records_affected += new_records_affected
#
#            success=True
#        except FTClient.FTClientError as e:
#            logging.error (e.message)
#
#        except psycopg2.Error as e:
#            logging.error (e)
#
#
#
#    if id_logfile:
#	id_logfile.close()
#
#    logging.info ("%s records affected" % records_affected)
#    if success:
#        logging.info ("Done." )
#    else:
#        logging.info ("Failed." )



