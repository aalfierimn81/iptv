#!/bin/bash
CMD_PATH="/usr/bin/"
ROOT="https://github.com/Free-TV/IPTV/"
GIT_PATH="archive/refs/heads/"
FILE="master.zip"

FULL="${ROOT}${GIT_PATH}${FILE}"
echo $FULL
#CMD="${CMD_PATH}curl ${FULL} -L --output ${FILE}"
CMD="curl ${FULL} -L --output ${FILE}"
echo $CMD
$CMD

DIGEST_NEW=$(sum ${FILE})
echo $DIGEST_NEW
DIGEST_OLD=$(sum old/${FILE})
echo $DIGEST_OLD

if [ "$DIGEST_NEW" == "$DIGEST_OLD" ]; then
    echo "no file changes"
else
    rm -rf "IPTV-master"
    UNZIP="unzip ${FILE}"
    $UNZIP
    mv ${FILE} old/
    python3 update_channel_list.py
fi    

