%define module_dir extra

Summary: Driver for igc-module
Name: igc-module
Version: 5.10.150
Release: 1%{?dist}
License: GPL
# Sources extracted from the Linux kernel %{version}
Source: %{name}-%{version}.tar.gz

Patch0: 0001-makefile.patch
Patch1: 0002-backport.patch
Patch2: 0003-fallthrough.patch
Patch3: 0004-showversion.patch
Patch4: 0005-i226.patch

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
* Thu Oct 27 2022 Andrew Lindh <andrew@netplex.net> - 5.10.150-1
- Use kernel source 5.10.150 and patches for XCP driver support

