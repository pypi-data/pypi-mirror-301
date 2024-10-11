chmod -R 777 /kcwebplus
pkill kcwebpl
sleep 3
nohup kcwebplus --app app --host 0.0.0.0 --port 39001 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &
sleep 1
nohup kcwebplus --app app --host 0.0.0.0 --port 39002 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &
sleep 1
nohup kcwebplus --app app --host 0.0.0.0 --port 39003 --processcount 2 --timeout 600 server -start > app/runtime/log/server.log 2>&1 &