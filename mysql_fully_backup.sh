#!/bin/bash
# Program
# use mysqldump to Fully backup mysql data per week!
# History
# Path
BakDir=/data/mysqlbackup/
LogFile=/var/log/mysqlbackup/bak.log
Date=`date +%Y%m%d`
Begin=`date +"%Y年%m月%d日 %H:%M:%S"`
cd $BakDir/fully
DumpFile=$Date.sql
GZDumpFile=$Date.sql.tgz
/usr/bin/mysqldump --quick --events --all-databases --flush-logs --delete-master-logs --single-transaction > $DumpFile
/bin/tar -zvcf $GZDumpFile $DumpFile
/bin/rm $DumpFile
Last=`date +"%Y年%m月%d日 %H:%M:%S"`
echo 开始:$Begin 结束:$Last $GZDumpFile success >> $LogFile
cd $BakDir/daily
/bin/rm -f *