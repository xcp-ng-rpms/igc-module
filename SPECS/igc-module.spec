%define vendor_name Intel
%define vendor_label intel
%define driver_name igc
%define module_dir extra

Summary: Driver for igc-module
Name: igc-module
Version: 5.10.145
Release: 1%{?dist}
License: GPL
# Sources extracted from the Linux kernel %{version}
Source: %{name}-%{version}.tar.gz

Patch0: 0001-makefile.patch
Patch0: 0002-backport.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
Intel igc device drivers for the Linux Kernel version %{kernel_version}.

%prep
%autosetup -n %{name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Sep 23 2022 Andrew Lindh <andrew@netplex.net> - 5.10.145-1
- Update Intel I225 driver from 5.10.145 kernel source

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.20.17-2
- Rebuild for XCP-ng 8.3

* Tue Feb 15 2022 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.20.17-1
- Added driver igc from kernel 4.20.17

