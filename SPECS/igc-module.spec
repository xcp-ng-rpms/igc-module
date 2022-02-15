%define uname  %{kernel_version}
%define module_dir updates

Summary: Driver for igc-module
Name: igc-module
Version: 4.20.17
Release: %{?release}%{!?release:1}
License: GPL
Source: %{name}-%{version}.tar.gz

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
igc-module Linux Device Driver source.

%prep
%setup -q -n %{name}-%{version}

%build
%{make_build} -C /lib/modules/%{uname}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{uname}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{uname}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{uname} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{uname}/*/*.ko

%changelog
* Tue Feb 15 2022 Rushikesh Jadhav <rushikesh7@gmail.com> - 4.20.17
- Added driver igc from kernel 4.20.17

