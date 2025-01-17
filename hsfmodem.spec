# I love OpenSource :-(
#
# Copyright (c) 2003 Linuxant inc.
# Copyright (c) 2001-2003 Conexant Systems, Inc.
#
# NOTE: The use and distribution of this software is governed by the terms in
# the file LICENSE, which is included in the package. You must read this and
# agree to these terms before using or distributing this software.
# 

%define version 7.80.02.05
%define release 6
%define hxftarget hsf
%define hxftargetdir %{_prefix}/lib/%{hxftarget}modem
%define arch_packname() %{name}-%{version}%{1}full
%define packname32 %{arch_packname %{nil}}
%define packname64 %{arch_packname x86_64}
%ifarch x86_64
%define packname %{packname64}
%define packsrc 1
%else
%define packname %{packname32}
%define packsrc 0
%endif

Summary:	Conexant HSF controllerless modem driver for Linux
Name:		%{hxftarget}modem
Version:	%version
Release:	%release
License:	Copyright (c) 2003 Linuxant inc. All rights reserved.
Group:		System/Kernel and hardware
Source0:	http://www.linuxant.com/drivers/hsf/full/archive/%{name}-%{version}/%{packname32}.tar.gz
Source1:	http://www.linuxant.com/drivers/hsf/full/archive/%{name}-%{version}/%{packname64}.tar.gz
Source2:	100498D_RM_HxF_Released.pdf
Source3:	hsfbuild.sh
Source4:	hsfclean.sh
Source5:	hsfmodem-7.80.02.05-kernel-2.6.33.patch
Patch0:		hsfmodem-7.80.02.03full-disable_cfgkernel.patch
Patch1:		hsfmodem-7.80.02.03full-initscripts.patch
# (blino) gcc -v does not match pattern in some locales (at least french)
Patch2:		hsfmodem-7.60.00.09full-locale.patch
Patch3:		hsfmodem-7.80.02.05full-cmpxchg64.patch
URL:		https://www.linuxant.com/drivers/hcf
Requires:	pciutils
Requires:	drakxtools >= 9.2-7mdk
Requires:	kmod(hsfengine)
Conflicts:	hsflinmodem
ExclusiveArch:	%{ix86} x86_64

%description
Conexant HSF controllerless modem driver for Linux

Copyright (c) 2003 Linuxant inc.
Copyright (c) 2001-2003 Conexant Systems, Inc.

1.   Permitted use. Redistribution and use in source and binary forms,
without modification, are permitted under the terms set forth herein.

2.   Disclaimer of Warranties. LINUXANT, ITS SUPPLIERS, AND OTHER CONTRIBUTORS
MAKE NO REPRESENTATION ABOUT THE SUITABILITY OF THIS SOFTWARE FOR ANY PURPOSE.
IT IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTIES OF ANY KIND.
LINUXANT AND OTHER CONTRIBUTORS DISCLAIMS ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, GOOD TITLE AND AGAINST INFRINGEMENT.

This software has not been formally tested, and there is no guarantee that
it is free of errors including, but not limited to, bugs, defects,
interrupted operation, or unexpected results. Any use of this software is
at user's own risk.

3.   No Liability.

(a) Linuxant, its suppliers, or contributors shall not be responsible for
any loss or damage to users, customers, or any third parties for any reason
whatsoever, and LINUXANT, ITS SUPPLIERS OR CONTRIBUTORS SHALL NOT BE LIABLE
FOR ANY ACTUAL, DIRECT, INDIRECT, SPECIAL, PUNITIVE, INCIDENTAL, OR
CONSEQUENTIAL (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED, WHETHER IN CONTRACT, STRICT OR OTHER LEGAL THEORY OF
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
OF SUCH DAMAGE.

(b) User agrees to hold Linuxant, its suppliers, and contributors harmless
from any liability, loss, cost, damage or expense, including attorney's fees,
as a result of any claims which may be made by any person, including
but not limited to User, its agents and employees, its customers, or
any third parties that arise out of or result from the manufacture,
delivery, actual or alleged ownership, performance, use, operation
or possession of the software furnished hereunder, whether such claims
are based on negligence, breach of contract, absolute liability or any
other legal theory.

4.   Notices. User hereby agrees not to remove, alter or destroy any
copyright, trademark, credits, other proprietary notices or confidential
legends placed upon, contained within or associated with the Software,
and shall include all such unaltered copyright, trademark, credits,
other proprietary notices or confidential legends on or in every copy of
the Software.

5.   Reverse-engineering. User hereby agrees not to reverse engineer,
decompile, or disassemble the portions of this software provided solely
in object form, nor attempt in any manner to obtain their source-code.

6.   Redistribution. Redistribution of this software is permitted only
for non-beta, officially released versions. Redistribution of versions
marked "beta" or "lnxtbeta" requires explicit written approval from
Linuxant.

You must also install the %{name}_kernel module if you want to utilize these
drivers.

%package -n dkms-%{name}
Summary:	Conexant HSF controllerless modem driver for Linux
Group:	System/Kernel and hardware
Requires(preun):	dkms
Requires(post):	dkms

%description -n dkms-%{name}
Conexant HSF controllerless modem driver support for Linux kernel %{kernel_version}.

%package doc
Group:		System/Kernel and hardware
Summary:	Documentation for Conexant HSF controllerless modems

%description doc
This package contains the documentation for Conexant HSF controllerless modems.

%prep
%setup -q -T -b %{packsrc} -n %{packname}
%patch0 -p1 -b .cfg
%patch1 -p1 -b .init
%patch2 -p1
%patch3 -p1

%build
make all 
make -C nvm
make -C diag IMPORTED_BLAM_SUPPORT=yes
cp %{SOURCE2} .

%install
make -C scripts ROOT=%{buildroot} install
make -C diag ROOT=%{buildroot} IMPORTED_BLAM_SUPPORT=yes install
make -C nvm ROOT=%{buildroot} install

# driver source
mkdir -p %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/patches
cp -r %{_sourcedir}/hsfbuild.sh %{_sourcedir}/hsfclean.sh config.mak modules \
	%{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}
install -m 0755 -d \
	%{buildroot}/%{_usr}/src/%{name}-%{version}-%{release}/built_modules
cat > %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}

DEST_MODULE_LOCATION[0]=/kernel/drivers/char
DEST_MODULE_LOCATION[1]=/kernel/drivers/char
DEST_MODULE_LOCATION[2]=/kernel/drivers/char
DEST_MODULE_LOCATION[3]=/kernel/drivers/char
DEST_MODULE_LOCATION[4]=/kernel/drivers/char
DEST_MODULE_LOCATION[5]=/kernel/drivers/char
DEST_MODULE_LOCATION[6]=/kernel/drivers/char
DEST_MODULE_LOCATION[7]=/kernel/drivers/char
DEST_MODULE_LOCATION[8]=/kernel/drivers/char
DEST_MODULE_LOCATION[9]=/kernel/drivers/char
DEST_MODULE_LOCATION[10]=/kernel/drivers/char
DEST_MODULE_LOCATION[11]=/kernel/drivers/char
DEST_MODULE_LOCATION[12]=/kernel/drivers/char
DEST_MODULE_LOCATION[13]=/kernel/drivers/char
BUILT_MODULE_NAME[0]=%{hxftarget}engine
BUILT_MODULE_LOCATION[0]=built_modules
BUILT_MODULE_NAME[1]=%{hxftarget}mc97ali
BUILT_MODULE_LOCATION[1]=built_modules
BUILT_MODULE_NAME[2]=%{hxftarget}mc97ich
BUILT_MODULE_LOCATION[2]=built_modules
BUILT_MODULE_NAME[3]=%{hxftarget}mc97via
BUILT_MODULE_LOCATION[3]=built_modules
BUILT_MODULE_NAME[4]=%{hxftarget}osspec
BUILT_MODULE_LOCATION[4]=built_modules
BUILT_MODULE_NAME[5]=%{hxftarget}pcibasic2
BUILT_MODULE_LOCATION[5]=built_modules
BUILT_MODULE_NAME[6]=%{hxftarget}pcibasic3
BUILT_MODULE_LOCATION[6]=built_modules
BUILT_MODULE_NAME[7]=%{hxftarget}serial
BUILT_MODULE_LOCATION[7]=built_modules
BUILT_MODULE_NAME[8]=%{hxftarget}soar
BUILT_MODULE_LOCATION[8]=built_modules
BUILT_MODULE_NAME[9]=%{hxftarget}usbcd2
BUILT_MODULE_LOCATION[9]=built_modules
BUILT_MODULE_NAME[10]=%{hxftarget}hda
BUILT_MODULE_LOCATION[10]=built_modules
BUILT_MODULE_NAME[11]=%{hxftarget}mc97ati
BUILT_MODULE_LOCATION[11]=built_modules
BUILT_MODULE_NAME[12]=%{hxftarget}mc97sis
BUILT_MODULE_LOCATION[12]=built_modules
BUILT_MODULE_NAME[13]=%{hxftarget}mc97via
BUILT_MODULE_LOCATION[13]=built_modules
MAKE[0]="sh hsfbuild.sh \${kernel_source_dir}"
CLEAN="sh hsfclean.sh"

AUTOINSTALL=yes
PATCH[0]="hsfmodem-7.80.02.05-kernel-2.6.33.patch"
PATCH_MATCH[0]="^2\.6\.(3[3-9])|([4-9][0-9]+)|([1-9][0-9][0-9]+)"
EOF

cp %{_sourcedir}/hsfmodem-7.80.02.05-kernel-2.6.33.patch \
   %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/patches/

%post
%{_sbindir}/%{hxftarget}config --auto
echo "Relaunch drakconnect to configure your Conexant HSF modem"

%preun
%{_sbindir}/%{hxftarget}stop

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{name} -v %{version}-%{release}
:

%preun -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{name} -v %{version}-%{release} --all
:

%files
%defattr(0555, root, root, 755)
%{_sbindir}/%{hxftarget}config
%{_sbindir}/%{hxftarget}diag
%{_sbindir}/%{hxftarget}dcpd
%{_sbindir}/%{hxftarget}modconflicts
%{_sbindir}/%{hxftarget}stop
%{hxftargetdir}/rc%{hxftarget}
%defattr(0444, root, root, 755)
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/*
%doc BUGS CHANGES CREDITS FAQ INSTALL LICENSE README

%files -n dkms-%{name}
%doc README
%doc LICENSE
%dir %{_usr}/src/%{name}-%{version}-%{release}
%{_usr}/src/%{name}-%{version}-%{release}/*

%files doc
%doc *.pdf

