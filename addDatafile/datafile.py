#!/usr/local/bin/python2.7

import sys
import re
import functions
import subprocess
import argparse
import logging
import datetime


__version__ = "1.0"
__author__="Arkadiusz Borucki"

per,all= functions.check_arg(sys.argv[1:])
print per

table=functions.selectTablespace()
log=functions.createLog()

if table < per:
        try:

                functions.findFileNum()
                sqlCommand=functions.generateCommand()
                (out,err,returncode)=functions.runSqlQuery(sqlCommand,functions.connectString)
                if returncode !=0:
                        print returncode
                        log.error(out.strip())
                        raise RuntimeError, 'Datafile Error creation\n'
                else:
                        print "Add datafile complited\n"
                        print out
                        log.info(out)

        except RuntimeError, error:
                        print "Check ALert.log: ", error
                        print out.strip()
else:
        print "Free space more than  %:", per
        print "Free space is %:",table
        log.info("Free space is OK, %:")
        log.info(table)



if all:
        print functions.checkAllTablespaces()
        log.info("Check all tablespaces in Database")


else:
        print "ssss"
        log.info(functions.getDate())

