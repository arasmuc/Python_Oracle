WHENEVER SQLERROR EXIT SQL.SQLCODE;
WHENEVER OSERROR EXIT;
ALTER TABLESPACE XMLSTOREGG ADD DATAFILE '+DATA/ALMA/DATAFILE/xmlstoregg63.dbf' SIZE 32767M AUTOEXTEND ON NEXT 256M MAXSIZE 32767M;