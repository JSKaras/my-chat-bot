#!/bin/sh

if [ $# -ne 1 ]
then
	echo "usage : $0 <file-name>"
	exit 1
fi

BODY="-d @./$1"

#curl -k -X POST https://localhost:8000/message/ $BODY

curl -X POST http://localhost:8000/message/ $BODY
