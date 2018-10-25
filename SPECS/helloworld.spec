# -----------------------------------------------------------------------------
# Overview of a spec
# -----------------------------------------------------------------------------
# This file provides the instructions for:
#
#   1) How to build an .rpm file.
#   2) What happens when the RPM is installed or uninstalled.
#
# To deferentiate between the two events, we use 'build time' and 'installation
# time' in the comments. The result of a build is a .rpm file. The result of an
# installation is the software existing on a machine, usually after a 'yum
# install ...' command has been ran.
#
# For more information see:
# - https://confluence.dev.bbc.co.uk/display/platform/Packaging+your+software
# - https://access.redhat.com/articles/216643
# -----------------------------------------------------------------------------

Name: helloworld
Version: 0.1.1%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: A helloworld application
Source0: src.tar.gz

# -----------------------------------------------------------------------------
# CentOS packages
# -----------------------------------------------------------------------------
# Because we are using a CentOS 7 base image, at 'installation time', all
# packages CentOS 7 provide are made available for us without us having to
# specify the repository url in the Cosmos component.

# See: http://mirror.centos.org/centos/7/os/x86_64/Packages/
# -----------------------------------------------------------------------------
Requires: nodejs

# -----------------------------------------------------------------------------
# Apache TLS - Access control
# -----------------------------------------------------------------------------
# Restrict the application to 'services' and 'developers' with valid BBC issued
# certificates (https://github.com/bbc/cloud-httpd-conf/).
#
# As this package is not available in the base CentOS 7 repositories, we have
# to configure the component to make another repository available at
# 'installation time'. If we forgot this step, the installation process will be
# unable to locate this package and will fail.
#
# To see where this repository is defined, search 'cloud-httpd-conf-el7' at
# https://admin.live.bbc.co.uk/cosmos/component/sample-app-python/repositories.
# -----------------------------------------------------------------------------
Requires: cloud-httpd24-ssl-services-devs-staff
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: x86_64

# -----------------------------------------------------------------------------
# Requirements for 'build time'
# -----------------------------------------------------------------------------
# As with most node projects, we require npm to build code. The npm packages 
# which are installed in the node_modules folder in src/ are also added to the
# final package by our build process.
# -----------------------------------------------------------------------------
BuildRequires: npm
BuildRequires: systemd
BuildRequires: cosmos-release

%description
A hello world application

# https://fedoraproject.org/wiki/How_to_create_an_RPM_package#.25prep_section
# http://rpm.org/max-rpm-snapshot/s1-rpm-inside-macros.html
%prep
%setup -q -n src/

# https://fedoraproject.org/wiki/How_to_create_an_RPM_package#.25build_section
%build
npm rebuild

# https://fedoraproject.org/wiki/How_to_create_an_RPM_package#.25install_section
%install
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}%{_sysconfdir}/bake-scripts/helloworld
mkdir -p %{buildroot}/usr/lib/helloworld
cp %{_builddir}/src/index.js %{buildroot}/usr/lib/helloworld
cp -R %{_builddir}/src/helloworld/ %{buildroot}/usr/lib/helloworld/
cp -R %{_builddir}/src/node_modules %{buildroot}/usr/lib/helloworld
cp -R %{_builddir}/src/usr/lib/systemd/system/helloworld.service %{buildroot}/usr/lib/systemd/system/
cp -R %{_builddir}/src/bake-scripts %{buildroot}%{_sysconfdir}/bake-scripts/helloworld

%pre
getent group helloworld >/dev/null || groupadd -r helloworld
getent passwd helloworld >/dev/null || \
        useradd -r -g helloworld -G helloworld -d / -s /sbin/nologin \
        -c "helloworld node.js service" helloworld

# https://fedoraproject.org/wiki/How_to_create_an_RPM_package#.25files_section
%files
%defattr(644, root, root, 755)
/usr/lib/helloworld
/usr/lib/systemd/system/helloworld.service
%defattr(-, root, root, 755)
/etc/bake-scripts/helloworld
