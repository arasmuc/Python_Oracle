#!/usr/local/bin/python2.7

import sys
import re
import argparse
import logging
import string
import datetime
from subprocess import Popen, PIPE, check_output

__version__ = "1.0"
__author__="Arkadiusz Borucki"

connectString = 'dp/dp'


def check_arg(args):
        parser = argparse.ArgumentParser(description='Oracle database add datafiles')
        parser.add_argument('-p', '--percent',
                        help='percent free',
                        required='True',
                        type=int)
        parser.add_argument('-a', '--all',
                        help='list all tablespaces')

        results = parser.parse_args(args)
        return results.percent,results.all


def getDate():
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return date


def createLog():
        logging.basicConfig(filename='OracleAlert.log',filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
        log = logging.getLogger("Oracle")
        return log


def runSqlQuery(sqlCommand, connectString):
        session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        session.stdin.write(sqlCommand)
        out,err= session.communicate()
        returncod= session.returncode
        return out,err,returncod


def findFileNum():
        tab=''
        com='select * from (select file_name from dba_data_files where tablespace_name=\'XMLSTOREGG\' order by file_name desc) where rownum=1;'
        tab=str(runSqlQuery(com, connectString))
        file=re.findall('\d+',tab)
        file=int(file[0])
        return file - 2

def selectTablespace():
        sql=''
        command='select (sum(nvl(fs.bytes,0))/1024/1024/b.tablespace_size_mb *100) free_percent\
        FROM dba_free_space fs, (SELECT tablespace_name, sum(bytes)/1024/1024 tablespace_size_mb FROM dba_data_files\
        GROUP BY tablespace_name) b where fs.tablespace_name=\'XMLSTOREGG\' and fs.tablespace_name = b.tablespace_name \
        group by b.tablespace_name, b.tablespace_size_mb;'
        sql=str(runSqlQuery(command, connectString))
        file=re.findall('\d+',sql)
        file=int(file[0])
        return file

def generateCommand():
        num=findFileNum()
        with open('sql.sql', 'w') as the_sql:
                the_sql.write('WHENEVER SQLERROR EXIT SQL.SQLCODE;\n')
                the_sql.write('WHENEVER OSERROR EXIT;\n')
                the_sql.write('ALTER TABLESPACE XMLSTOREGG ADD DATAFILE')
                the_sql.write(' \'+DATA/ALMA/DATAFILE/xmlstoregg'+str(num)+'.dbf\'')
                the_sql.write(' SIZE 32767M AUTOEXTEND ON NEXT 256M MAXSIZE 32767M;')
        sqlCommand ='@sql.sql'
        return sqlCommand

def checkAllTablespaces():
        table=None
        command='select tablespace_name from dba_tablespaces;'
        sql=str(runSqlQuery(command, connectString))
        with open('tablespaces.sql', 'w') as the_sql:
                the_sql.write(sql)

        with open('tablespaces.sql', 'rw') as the_sql:
                for line in the_sql:
                        table=re.findall('[A-Z]+\w+[A-Z]+',line)

        return table
