Name:           linux-sgx
Version:        2.5
Release:        1%{?dist}
Summary:        Intel SGX for Linux

License:  BSD or GPLv2+
URL:      https://github.com/intel/linux-sgx
Source0:  https://github.com/intel/linux-sgx/archive/sgx_%{version}.tar.gz
Source1:  sgx_packer.py

%global debug_package %{nil}

# SGX exists only for x86_64
ExclusiveArch: x86_64

# General tools
BuildRequires: gcc-c++ autoconf automake libtool systemd git
# For the SDK
BuildRequires: ocaml ocaml-ocamlbuild redhat-rpm-config openssl-devel wget python
# For the Platform SoftWare (PSW, includes AESMD)
BuildRequires: openssl-devel libcurl-devel protobuf-devel cmake

Requires(pre): shadow-utils

%global warnings_ignore "-Wno-error=implicit -Wno-error=conversion -Wno-error=shadow -Wno-error=float-equal -Wno-error=redundant-decls"
%if %{fedora} >= 30
%global warnings_ignore "%{warnings_ignore} -Wno-error=deprecated-copy"
%endif


%description
Intel(R) Software Guard Extensions (Intel(R) SGX) is an Intel technology for application developers seeking to protect select code and data from disclosure or modification.

The Linux* Intel(R) SGX software stack is comprised of the Intel(R) SGX driver, the Intel(R) SGX SDK, and the Intel(R) SGX Platform Software (PSW). The Intel(R) SGX SDK and Intel(R) SGX PSW are hosted in the linux-sgx project.

The linux-sgx-driver project hosts the out-of-tree driver for the Linux* Intel(R) SGX software stack, which will be used until the driver upstreaming process is complete.

The repository provides a reference implementation of a Launch Enclave for 'Flexible Launch Control' under psw/ae/ref_le. The reference LE implemenation can be used as a basis for enforcing different launch control policy by the platform developer or owner. To build and try it by yourself, please refer to the ref_le.md for details.


%prep
echo "foo%{warnings_ignore}bar"
exit 1
%autosetup -n linux-sgx-sgx_%{version}


%build
git init
git add .
git -c user.name=Builder -c user.email=builder@puiterwijk.org commit -sm init
git clone https://github.com/intel/SGXDataCenterAttestationPrimitives.git external/dcap_source

./download_prebuilt.sh

CXXFLAGS="%{warnings_ignore}" make psw_install_pkg DEBUG=1


%install
rm -rf %{_builddir}/out
mkdir %{_builddir}/out
python3 %{SOURCE1} %{_builddir}/out linux/installer/common/{libsgx-enclave-common,psw}/BOMs/*_{base,x64}.txt

mkdir -p %{buildroot}/usr/lib64
cp %{_builddir}/out/package/lib64/*.so %{buildroot}/usr/lib64/

mkdir -p %{buildroot}/var/opt/aesmd %{buildroot}/etc
cp -rf %{_builddir}/out/package/aesm/data %{buildroot}/var/opt/aesmd/
cp -rf %{_builddir}/out/package/aesm/conf/aesmd.conf %{buildroot}/etc/aesmd.conf
rm -rf %{_builddir}/out/package/aesm/{data,conf}

mkdir -p %{buildroot}/var/run/aesmd

mkdir -p %{buildroot}%{_unitdir}
sed -e "s:@aesm_folder@:/opt/intel/sgxpsw/aesm:" %{_builddir}/out/package/aesm/aesmd.service >%{buildroot}%{_unitdir}/aesmd.service

mkdir -p %{buildroot}/opt/intel/sgxpsw
cp -r %{_builddir}/out/package/aesm %{buildroot}/opt/intel/sgxpsw


%files
/usr/lib64/libsgx_enclave_common.so.1
/usr/lib64/libsgx_enclave_common.so
/usr/lib64/libsgx_uae_service.so
/usr/lib64/libsgx_urts.so
/etc/aesmd.conf
/var/opt/aesmd
/var/run/aesmd
%{_unitdir}/aesmd.service
/opt/intel/sgxpsw


%pre
getent group aesmd  >/dev/null || groupadd -r aesmd
getent passwd aesmd >/dev/null || \
    useradd -r -g aesmd -d /var/opt/aesmd -s /sbin/nologin \
    -c "User for aesmd" aesmd
exit 0


%changelog
* Fri Apr  5 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.5-1
- Initial packaging
