Name:           linux-sgx
Version:        2.5
Release:        1%{?dist}
Summary:        Intel SGX for Linux

License:  BSD or GPLv2+
URL:      https://github.com/intel/linux-sgx
Source0:  https://github.com/intel/linux-sgx/archive/sgx_%{version}.tar.gz

# SGX exists only for x86_64
ExclusiveArch: x86_64

# General tools
BuildRequires: gcc-c++ autoconf automake libtool
# For the SDK
BuildRequires: ocaml ocaml-ocamlbuild redhat-rpm-config openssl-devel wget python
# For the Platform SoftWare (PSW, includes AESMD)
BuildRequires: openssl-devel libcurl-devel protobuf-devel cmake


%description
Intel(R) Software Guard Extensions (Intel(R) SGX) is an Intel technology for application developers seeking to protect select code and data from disclosure or modification.

The Linux* Intel(R) SGX software stack is comprised of the Intel(R) SGX driver, the Intel(R) SGX SDK, and the Intel(R) SGX Platform Software (PSW). The Intel(R) SGX SDK and Intel(R) SGX PSW are hosted in the linux-sgx project.

The linux-sgx-driver project hosts the out-of-tree driver for the Linux* Intel(R) SGX software stack, which will be used until the driver upstreaming process is complete.

The repository provides a reference implementation of a Launch Enclave for 'Flexible Launch Control' under psw/ae/ref_le. The reference LE implemenation can be used as a basis for enforcing different launch control policy by the platform developer or owner. To build and try it by yourself, please refer to the ref_le.md for details.


%prep
%autosetup -n linux-sgx-sgx_%{version}


%build
git init
git add .
git -c user.name=Builder -c user.email=builder@puiterwijk.org commit -sm init

./download_prebuilt.sh

#make USE_OPT_LIBS=0 DEBUG=1
make sdk_install_pkg DEBUG=1


%install


%files


%changelog
* Fri Apr  5 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.5-1
- Initial packaging
