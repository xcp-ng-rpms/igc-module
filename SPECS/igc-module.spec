%define module_dir extra

Summary: Driver for igc-module
Name: igc-module
Version: 5.10.214
Release: 1%{?dist}
License: GPL
# Sources extracted from the Linux kernel %{version}
Source: %{name}-%{version}.tar.gz

Patch0: 0001-Change-makefile-for-building-igc.patch
Patch1: 0002-Some-backports-from-higher-kernel-version.patch
Patch2: 0003-gettimex64-is-not-supported-until-kernel-v5.0.patch
Patch3: 0004-supported_coalesce_params-is-not-supported-until-ker.patch
Patch4: 0005-TAPRIO-was-not-supported-until-kernel-v5.18.patch

# XCP-ng specific patch
Patch1000: 1000-showversion.patch

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
* Thu Jun 20 2024 Thierry Escande <thierry.escande@vates.tech> - 5.10.214-1
- Import sources and patches from intel-igc-5.10.214-3.xs8.src.rpm
- Rebased showversion patch (And update driver version)
- Drop i226 patch per Andrew feedback

* Wed Nov 8 2023 Andrew Lindh <andrew@netplex.net> - 5.10.200-1
- Use kernel source 5.10.200 and patches for XCP driver support

* Thu Oct 27 2022 Andrew Lindh <andrew@netplex.net> - 5.10.150-1
- Use kernel source 5.10.150 and patches for XCP driver support

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.20.17-2
- Rebuild for XCP-ng 8.3

* Tue Feb 15 2022 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.20.17-1
- Added driver igc from kernel 4.20.17

