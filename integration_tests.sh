#!/bin/sh

# try 120 times == ~2 minute
x=1
while [ $x -le 60 ]
do
  STATUS=$(curl -X PUT -d query=* -s -o /dev/null -w '%{http_code}' https://meetup-search.de)
  if [ $STATUS -eq 200 ]; then
    echo "Got 200! All done!"
    exit 0
  else
    echo "Got $STATUS :( Not done yet..."
    x=$(( $x + 1 ))
  fi
  sleep 1
done

exit 1