# chmod -R 777 /kcwebplus
# ./server stop
#nohup ./server --h 0.0.0.0 --p 39001 --w 2 start > app/runtime/log/server.log 2>&1 &
#nohup ./server --h 0.0.0.0 --p 39002 --w 2 start > app/runtime/log/server.log 2>&1 &
#nohup ./server --h 0.0.0.0 --p 39003 --w 2 start > app/runtime/log/server.log 2>&1 &
#nohup python3.8kcw_plus server.py intapp/index/pub/clistartplan --cli > app/runtime/log/server.log 2>&1 &
mkdir /kcwebplus/app/runtime/log
chmod -R 777 /kcwebplus
pkill kcwebpl
sleep 3
nohup kcwebplus --app app --host 0.0.0.0 --port 39001 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &
sleep 1
nohup kcwebplus --app app --host 0.0.0.0 --port 39002 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &
sleep 1
nohup kcwebplus --app app --host 0.0.0.0 --port 39003 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &