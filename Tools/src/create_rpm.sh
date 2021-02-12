#!/usr/bin/env bash
echo "*************************************************"
echo "Creating rpm file for Amazon Linux and RHEL amd64"
echo "*************************************************"

rm -rf ${BGO_SPACE}/bin/linux_amd64/linux

echo "Creating rpmbuild workspace"

mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/SPECS
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/COORD_SOURCES
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/DATA_SOURCES
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/BUILD
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/RPMS
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/SRPMS
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/etc/init/
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/etc/systemd/system/
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/
mkdir -p ${BGO_SPACE}/bin/linux_amd64/linux/var/lib/bzero/ssm/

echo "Copying application files"

cp ${BGO_SPACE}/bin/linux_amd64/amazon-ssm-agent ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-agent
cp ${BGO_SPACE}/bin/linux_amd64/ssm-agent-worker ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-agent-worker
cp ${BGO_SPACE}/bin/linux_amd64/ssm-document-worker ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-document-worker
cp ${BGO_SPACE}/bin/linux_amd64/ssm-session-worker ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-session-worker
cp ${BGO_SPACE}/bin/linux_amd64/ssm-session-logger ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-session-logger
cp ${BGO_SPACE}/bin/linux_amd64/ssm-cli ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/bzero-ssm-cli
cp ${BGO_SPACE}/seelog_unix.xml ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/seelog.xml.template
cp ${BGO_SPACE}/amazon-ssm-agent.json.template ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/
cp ${BGO_SPACE}/RELEASENOTES.md ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/
cp ${BGO_SPACE}/README.md ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/
cp ${BGO_SPACE}/NOTICE.md ${BGO_SPACE}/bin/linux_amd64/linux/etc/bzero/ssm/
cp ${BGO_SPACE}/packaging/linux/amazon-ssm-agent.conf ${BGO_SPACE}/bin/linux_amd64/linux/etc/init/bzero-ssm-agent.conf
cp ${BGO_SPACE}/packaging/linux/amazon-ssm-agent.service ${BGO_SPACE}/bin/linux_amd64/linux/etc/systemd/system/bzero-ssm-agent.service
cd ${BGO_SPACE}/bin/linux_amd64/linux/usr/bin/; strip --strip-unneeded bzero-ssm-agent; strip --strip-unneeded bzero-ssm-agent-worker; strip --strip-unneeded bzero-ssm-cli; strip --strip-unneeded bzero-ssm-document-worker; strip --strip-unneeded bzero-ssm-session-worker; strip --strip-unneeded bzero-ssm-session-logger; cd ~-

echo "Creating the rpm package"

SPEC_FILE="${BGO_SPACE}/packaging/linux/amazon-ssm-agent.spec"
BUILD_ROOT="${BGO_SPACE}/bin/linux_amd64/linux"

setarch x86_64 rpmbuild -bb --define "rpmversion `cat ${BGO_SPACE}/VERSION`" --define "_topdir bin/linux_amd64/linux/rpmbuild" --buildroot ${BUILD_ROOT} ${SPEC_FILE}

echo "Copying rpm files to bin"

cp ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/RPMS/x86_64/*.rpm ${BGO_SPACE}/bin/
cp ${BGO_SPACE}/bin/linux_amd64/linux/rpmbuild/RPMS/x86_64/*.rpm ${BGO_SPACE}/bin/linux_amd64/bzero-ssm-agent.rpm
