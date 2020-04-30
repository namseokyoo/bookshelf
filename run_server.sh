#!/bin/bash
PORT=80

function start_server(){
    echo "Start server on port ${PORT}"
    nohup authbind --deep python3 app.py & 2> /dev/null
}

function stop_server(){
    echo "Stop server.."
    kill -9 $(lsof -i:${PORT} -t) 2> /dev/null
}

function status_server(){
    echo "PID:[" $(lsof -i:${PORT} -t) "]"
}

function print_success(){
    echo "Success $1!"
}

if [ "$1" == "-q" ];then
    status_server
    stop_server
    sleep 2
    print_success 'to stop server'
else
    status_server
    stop_server
    start_server
    sleep 2
    status_server
fi
