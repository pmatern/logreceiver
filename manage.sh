#!/bin/sh -e

basedir=`dirname $0`
logdir=${basedir}/var/log
pidfile=${basedir}/var/run/logreceiver.pid

start() {
  if is_running; then
    echo "Process is already running as pid `cat $pidfile`! Stop it first."
    exit 2
  fi
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

is_running() {
  [ -f $pidfile ] && kill -0 `cat $pidfile` >/dev/null 2>&1
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
    if is_running; then
      echo "Log receiver is running as process `cat $pidfile`"
    else
      echo "Log receiver is stopped."
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
esac
