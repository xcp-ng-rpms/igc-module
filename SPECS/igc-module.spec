%global usver 5.10.226
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 5.10.226
%define vendor_name Intel
%define driver_name igc
%define vendor_label module

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{driver_name} %{vendor_name} device drivers
Name: %{driver_name}-%{vendor_label}
Version: 5.10.226
Release: %{?xsrel}%{?dist}
License: GPL
Source0: igc-module.tar.gz
Patch0: 0001-Change-makefile-for-building-igc.patch
Patch1: 0002-Some-backports-from-higher-kernel-version.patch
Patch2: 0003-gettimex64-is-not-supported-until-kernel-v5.0.patch
Patch3: 0004-supported_coalesce_params-is-not-supported-until-ker.patch
Patch4: 0005-TAPRIO-was-not-supported-until-kernel-v5.18.patch

# XCP-ng specific patches
Patch1000: 1000-showversion.patch
Patch1001: 1001-i226.patch

BuildRequires: gcc
BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Provides: %{driver_name}-%{vendor_label}
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{driver_name} %{vendor_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Fri Sep 20 2024 Andrew Lindh <andrew@netplex.net> - 5.10.226-1
- Copy intel-igc code from Xen/XCP 8.3 but use igc-module name
- Update with kernel source 5.10.226 to fix minor lock bug
- Add Provides:igc-module to the package info


* Wed Nov 8 2023 Andrew Lindh <andrew@netplex.net> - 5.10.200-1
- Use kernel source 5.10.200 and patches for XCP driver support

* Thu Oct 27 2022 Andrew Lindh <andrew@netplex.net> - 5.10.150-1
- Use kernel source 5.10.150 and patches for XCP driver support

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 4.20.17-2
- Rebuild for XCP-ng 8.3

* Tue Feb 15 2022 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.20.17-1
- Added driver igc from kernel 4.20.17

