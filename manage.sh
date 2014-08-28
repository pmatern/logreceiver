#!/bin/sh -e

basedir=`dirname $0`
logdir=${basedir}/var/log
pidfile=${basedir}/var/run/logreceiver.pid

start() {
  [ -d $logdir ] || mkdir -p $logdir
  [ -d `dirname $pidfile` ] || mkdir -p `dirname $pidfile`
  $basedir/venv/bin/python $basedir/web_server.py >> $logdir/service.log 2>> $logdir/error.log &
  echo $! > $pidfile
  disown
}

stop() {
  [ -f $pidfile ] && kill `cat $pidfile`
  rm $pidfile
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  status)

    if [ -f $pidfile ] && kill -0 `cat $pidfile`; then
      echo "Log receiver is running as process `cat $pidfile`"
    else
      echo "Log receiver is stopped."
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
esac
