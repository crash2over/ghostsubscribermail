#! /bin/sh
### BEGIN INIT INFO
# Provides:          ghostmailsubscriber
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example initscript
# Description:       This file should be used to construct scripts to be
#                    placed in /etc/init.d.
### END INIT INFO

INSTALLPATH="opt"

## Check to see if we are running as root first.
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

checkstatus() {
	local VAR=""
	for param in "$@"
	do
		VAR="$param"
	done
	FINAL=`echo "$@" | sed -e "s/\<$VAR\>//g"`
	local __resultvar=$VAR
	$FINAL
	local status=$?
	if [ $status -eq 0 ]; then
		echo "Ok on... $1 ... command"
	fi
	#echo $status
	eval $__resultvar="'$status'"
}

doinstall()
{
	echo "Copying Scripts..."
	MYDIR=`pwd`
	checkstatus /bin/cp $MYDIR/ghostmailsys /etc/init.d/ STATMAIL
	sleep 1
	checkstatus /bin/cp -R ../../ghostsubscribermail /$INSTALLPATH/ STATCPY
	sleep 2

	if [ $STATMAIL -eq 0 ] && [ $STATCPY -eq 0 ]; then
		echo "Changing Owner..."
		checkstatus /bin/chown root:root /etc/init.d/ghostmailsys STATMAIL
		sleep 2
		if [ $STATMAIL -eq 0 ]; then
			echo "Making it: +x ..."
			checkstatus /bin/chmod +x /etc/init.d/ghostmailsys STATMAIL
			sleep 2
			if [ $STATMAIL -eq 0 ]; then
				echo "update-rc..."
				update-rc.d ghostmailsys defaults 20 80
				echo "All Done..."
			else
				echo "Some error making +x... check route"
			fi
		else
			echo "Some error changing owner... check route"

		fi
	else
		echo "Some error copying files... check route"
	fi
}

douninstall()
{
	echo "Deleting files..."
	checkstatus /bin/rm -R /$INSTALLPATH/ghostsubscribermail STATRMFOLD
	sleep 1
	checkstatus /bin/rm /etc/init.d/ghostmailsys STATRMMAIL
	sleep 2
	if [ $STATRMFOLD -eq 0 ] && [ $STATRMMAIL -eq 0 ]; then
		echo "update-rc removing..."
		update-rc.d -f ghostmailsys remove
	else
		echo "Some error while removing..."
	fi
}

croninstall()
{
	echo "Appending rule to crontab..."
	APPEND=`/bin/sed -i.bak '$ a \0    6  * * *   root    python /opt/ghostsubscribermail/main.py &\' /etc/crontab`
	STAT=$?
	sleep 1
	checkstatus /bin/cp -R ../../ghostsubscribermail /$INSTALLPATH/ STATCPY
	sleep 2
	if [ $STAT -eq 0 ] && [ $STATCPY -eq 0 ]; then
		echo "Restarting cron..."
		service cron restart
	else
		echo "Some error while appending rule"
	fi
}

cronuninstall()
{
	echo "Removing rule from crontab..."
	APPEND=`sudo sed -i.bak '/ghostsubscribermail\/main.py/d' /etc/crontab`
	STAT=$?
	sleep 1
	checkstatus /bin/rm -R /$INSTALLPATH/ghostsubscribermail STATRMFOLD
	sleep 2
	if [ $STAT -eq 0 ] && [ $STATRMFOLD -eq 0 ]; then
		echo "Restarting cron..."
		service cron restart
	else
		echo "Some error while removing rule"
	fi
}

case "$1" in
    install)
        doinstall
        exit 0
    ;;
    uninstall)
	douninstall
	exit 0
    ;;
    croninstall)
	croninstall
	exit 0
    ;;
    cronuninstall)
	cronuninstall
	exit 0
    ;;
    **)
        echo "Usage: $0 {install|uninstall|croninstall|cronuninstall}" 1>&2
        exit 1
    ;;
esac
