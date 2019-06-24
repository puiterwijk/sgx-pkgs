%include config

Name:           linux-sgx-driver
Version:        2.5
Release:        1%{?dist}
Summary:        Intel SGX Linux* Driver

%global commit f7dc97c021b46878910958b285a12e8787593fd8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

License:  BSD or GPLv2+
URL:      https://github.com/intel/linux-sgx-driver
Source0:  https://github.com/intel/linux-sgx-driver/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# SGX exists only for x86_64
ExclusiveArch: x86_64

%global kernelrel %(rpm -q --qf '%%{VERSION}-%%{RELEASE}\\n' kernel | head -1)
%include kernelrel_override
%global kernelrela %{kernelrel}.x86_64

BuildRequires:  kernel-devel
Requires:	kernel%{?_isa} == %{kernelrel}

%description
Intel(R) Software Guard Extensions (Intel(R) SGX) is an Intel technology for application developers seeking to protect select code and data from disclosure or modification.

The Linux SGX software stack is comprised of the Intel(R) SGX driver, the Intel(R) SGX SDK, and the Intel(R) SGX Platform Software. The Intel(R) SGX SDK and Intel(R) SGX PSW are hosted in the linux-sgx project.

The linux-sgx-driver project hosts the out-of-tree driver for the Linux Intel(R) SGX software stack, which will be used until the driver upstreaming process is complete.


%prep
%autosetup -n linux-sgx-driver-%{commit}


%build
make -C /lib/modules/%{kernelrela}/build SUBDIRS=`pwd` modules
%if 0%{?sign_key}
/lib/modules/%{kernelrela}/build/scripts/sign-file sha256 %{sign_key} %{sign_cert} isgx.ko
%endif


%install
mkdir -p %{buildroot}/lib/modules/%{kernelrela}/kernel/drivers/intel/sgx
install isgx.ko %{buildroot}/lib/modules/%{kernelrela}/kernel/drivers/intel/sgx


%files
%license License.txt
%doc README.md
/lib/modules/%{kernelrela}/kernel/drivers/intel


%post
depmod


%postun
depmod


%changelog
* Fri Apr  5 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.5-1
- Initial packaging
