Name         : clunk80-ssm-agent
Version      : %rpmversion
Release      : 1
Summary      : Modified Amazon SSM Agent for use with clunk80.com

License      : Apache License, Version 2.0

Packager     : Commonwealth Crypto, Inc.
Vendor       : Commonwealth Crypto, Inc.

%description
This package provides a modified Amazon SSM Agent for use with clunk80.com

%files
%defattr(-,root,root,-)
/etc/clunk80/ssm/amazon-ssm-agent.json.template
/etc/clunk80/ssm/seelog.xml.template
/usr/bin/clunk80-ssm-agent
/usr/bin/clunk80-ssm-agent-worker
/usr/bin/clunk80-ssm-cli
/usr/bin/clunk80-ssm-document-worker
/usr/bin/clunk80-ssm-session-worker
/usr/bin/clunk80-ssm-session-logger
/var/lib/clunk80/ssm/
%doc /etc/clunk80/ssm/RELEASENOTES.md
%doc /etc/clunk80/ssm/README.md
%doc /etc/clunk80/ssm/NOTICE.md

%config(noreplace) /etc/init/clunk80-ssm-agent.conf
%config(noreplace) /etc/systemd/system/clunk80-ssm-agent.service

# The scriptlets in %pre and %post are run before and after a package is installed.
# The scriptlets %preun and %postun are run before and after a package is uninstalled.
# The scriptlets %pretrans and %posttrans are run at start and end of a transaction.

# Examples for the scriptlets are run for clean install, uninstall and upgrade

# Clean install: %posttrans
# Uninstall:     %preun
# Upgrade:       %pre, %posttrans

%pre
# Stop the agent before the upgrade
if [ $1 -ge 2 ]; then
    /sbin/init --version &> stdout.txt
    if [[ `cat stdout.txt` =~ upstart ]]; then
        /sbin/stop clunk80-ssm-agent
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl stop clunk80-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%preun
# Stop the agent after uninstall
if [ $1 -eq 0 ] ; then
    /sbin/init --version &> stdout.txt
    if [[ `cat stdout.txt` =~ upstart ]]; then
        /sbin/stop clunk80-ssm-agent
        sleep 1
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl stop clunk80-ssm-agent
        systemctl disable clunk80-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%posttrans
# Start the agent after initial install or upgrade
if [[ $1 -ge 0 ]]; then
    /sbin/init --version &> stdout.txt
    if [[ `cat stdout.txt` =~ upstart ]]; then
        /sbin/start clunk80-ssm-agent
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl enable clunk80-ssm-agent
        systemctl start clunk80-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%clean
# rpmbuild deletes $buildroot after building, specifying clean section to make sure it is not deleted


