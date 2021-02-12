Name         : bzero-ssm-agent
Version      : %rpmversion
Release      : 1
Summary      : Modified Amazon SSM Agent for use with bastionzero.com

License      : Apache License, Version 2.0

Packager     : Commonwealth Crypto, Inc.
Vendor       : Commonwealth Crypto, Inc.

%description
This package provides a modified Amazon SSM Agent for use with bastionzero.com

%files
%defattr(-,root,root,-)
/etc/bzero/ssm/amazon-ssm-agent.json.template
/etc/bzero/ssm/seelog.xml.template
/usr/bin/bzero-ssm-agent
/usr/bin/bzero-ssm-agent-worker
/usr/bin/bzero-ssm-cli
/usr/bin/bzero-ssm-document-worker
/usr/bin/bzero-ssm-session-worker
/usr/bin/bzero-ssm-session-logger
/var/lib/bzero/ssm/
%doc /etc/bzero/ssm/RELEASENOTES.md
%doc /etc/bzero/ssm/README.md
%doc /etc/bzero/ssm/NOTICE.md

%config(noreplace) /etc/init/bzero-ssm-agent.conf
%config(noreplace) /etc/systemd/system/bzero-ssm-agent.service

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
        /sbin/stop bzero-ssm-agent
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl stop bzero-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%preun
# Stop the agent after uninstall
if [ $1 -eq 0 ] ; then
    /sbin/init --version &> stdout.txt
    if [[ `cat stdout.txt` =~ upstart ]]; then
        /sbin/stop bzero-ssm-agent
        sleep 1
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl stop bzero-ssm-agent
        systemctl disable bzero-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%posttrans
# Start the agent after initial install or upgrade
if [[ $1 -ge 0 ]]; then
    /sbin/init --version &> stdout.txt
    if [[ `cat stdout.txt` =~ upstart ]]; then
        /sbin/start bzero-ssm-agent
    elif [[ `systemctl` =~ -\.mount ]]; then
        systemctl enable bzero-ssm-agent
        systemctl start bzero-ssm-agent
        systemctl daemon-reload
    fi
    rm stdout.txt
fi

%clean
# rpmbuild deletes $buildroot after building, specifying clean section to make sure it is not deleted


