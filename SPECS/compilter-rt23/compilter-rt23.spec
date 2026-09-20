# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: jchzhou <zhoujiacheng@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# Originally extracted from Fedora Project
# Authors: The Fedora Project Contributors

%global _vpath_srcdir compiler-rt
%global maj_ver 23
%global min_ver 1
%global patch_ver 1
#global rc_ver rc3

%bcond check 0

# Make sure that we are not building with a newer compiler than the targeted
# version. For example, if we build LLVM 19 with Clang 20, then we'd build
# LLVM libraries with Clang 20, and then the runtimes build would use the
# just-built Clang 19. Runtimes that link against LLVM libraries would then
# try to make Clang 19 perform LTO involving LLVM 20 bitcode.
%if %{defined host_clang_maj_ver}
%global __cc /usr/bin/clang-%{host_clang_maj_ver}
%global __cxx /usr/bin/clang++-%{host_clang_maj_ver}
%endif

# Suffixless tarball name (essentially: basename -s .tar.xz llvm-project-17.0.6.src.tar.xz)
%global src_tarball_dir llvm-project-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-%{rc_ver}}.src

%global build_ldflags %{?build_ldflags} -Wl,--build-id=sha1
%global build_cflags %{?build_cflags} -fno-lto
%global build_cxxflags %{?build_cxxflags} -fno-lto
%global build_fflags %{?build_fflags} -fno-lto

# llvm
# Apart from compiler-rt and libcxx, everything is installed into a
# version-specific prefix. Non-compat packages add symlinks to this prefix.
%global install_prefix %{_libdir}/llvm%{maj_ver}
%global install_bindir %{install_prefix}/bin
%global install_includedir %{install_prefix}/include
%global install_libdir %{install_prefix}/lib
%global install_datadir %{install_prefix}/share
%global install_mandir %{install_prefix}/share/man
%global install_libexecdir %{install_prefix}/libexec
%global install_python3mod %{install_libdir}/python%{python3_version}/site-packages
%global build_libdir llvm/%{_vpath_builddir}/%{_lib}
%global unprefixed_libdir %{_lib}
%global targets_to_build "X86;AMDGPU;NVPTX;BPF;WebAssembly;RISCV;AArch64"
%global experimental_targets_to_build ""
%global build_install_prefix %{buildroot}%{install_prefix}
%global llvm_triple %{_target_platform}

# enabled projects and runtimes
%global projects clang
%global runtimes compiler-rt;openmp

# clang

# compiler-rt
# pkg_name removed - using hardcoded names like clang

# openmp
%global so_suffix %{maj_ver}.%{min_ver}
%global libomp_arch %{_arch}

Name:           compilter-rt%{maj_ver}
Version:        %{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:~%{rc_ver}}
Release:        %{autorelease}
Summary:        LLVM "compiler-rt" runtime libraries (%{maj_ver})
License:        Apache-2.0 WITH LLVM-exception OR NCSA OR MIT
URL:            http://llvm.org
VCS:            git:https://github.com/llvm/llvm-project.git
#!RemoteAsset:  sha256:ebe9be46fe8756d58c5b198ffad0fa2a766257add81a4dc52179bfacc7888ee6
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-%{rc_ver}}/%{src_tarball_dir}.tar.xz

Provides:       compiler-rt(major) = %{maj_ver}
BuildSystem:    cmake

BuildOption(conf):  -G Ninja
BuildOption(conf):  -DLLVM_CMAKE_DIR=%{install_libdir}/cmake/llvm
BuildOption(conf):  -DCMAKE_BUILD_TYPE=RelWithDebInfo
BuildOption(conf):  -DLLVM_USE_PERF=ON
BuildOption(conf):  -DLLVM_TARGETS_TO_BUILD=%{targets_to_build}
BuildOption(conf):  -DBUILD_SHARED_LIBS=OFF
BuildOption(conf):  -DCLANG_LINK_CLANG_DYLIB=ON
BuildOption(conf):  -DCOMPILER_RT_INCLUDE_TESTS:BOOL=OFF
BuildOption(conf):  -DLLVM_DEFAULT_TARGET_TRIPLE=%{llvm_triple}
BuildOption(conf):  -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON
BuildOption(conf):  -DLLVM_UNREACHABLE_OPTIMIZE:BOOL=OFF
BuildOption(conf):  -DLLVM_UTILS_INSTALL_DIR:PATH=bin
BuildOption(conf):  -DLLVM_LIT_ARGS="-vv"
BuildOption(conf):  -DCMAKE_INSTALL_PREFIX=%{install_prefix}
BuildOption(conf):  -DENABLE_LINKER_BUILD_ID:BOOL=ON
BuildOption(conf):  -DPython3_EXECUTABLE=%{__python3}
BuildOption(conf):  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON
BuildOption(conf):  -DCLANG_CONFIG_FILE_SYSTEM_DIR=%{_sysconfdir}/clang%{maj_ver}/
BuildOption(conf):  -DCLANG_DEFAULT_PIE_ON_LINUX=OFF
BuildOption(conf):  -DCLANG_DEFAULT_UNWINDLIB=libgcc
BuildOption(conf):  -DCLANG_ENABLE_STATIC_ANALYZER:BOOL=ON
BuildOption(conf):  -DCLANG_INCLUDE_DOCS:BOOL=ON
BuildOption(conf):  -DCLANG_INCLUDE_TESTS:BOOL=ON
BuildOption(conf):  -DCLANG_PLUGIN_SUPPORT:BOOL=ON
BuildOption(conf):  -DCLANG_REPOSITORY_STRING="%{?_vendor_name} %{version}-%{release}"


# clang patches

BuildRequires:  llvm%{maj_ver}-devel = %{version}
BuildRequires:  llvm%{maj_ver}-static = %{version}
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  binutils-devel

%ifarch %{valgrind_arches}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  pkgconfig(libedit)
# For %%py3_shebang_fix
BuildRequires:  pkgconfig(python3)
BuildRequires:  swig
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  doxygen
BuildRequires:  perl
BuildRequires:  pkgconfig(libffi)
BuildRequires:  libatomic
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(pybind11)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(nanobind)
# for python buildrequires
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(pexpect)
BuildRequires:  pyproject-rpm-macros
# for tests
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(lib)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  procps-ng

%description
The compiler-rt project is a part of the LLVM project. It provides
implementation of the low-level target-specific hooks required by
code generation, sanitizer runtimes and profiling library for code
instrumentation, and Blocks C language extension.

%prep
%autosetup -p1 -T -b 0 -n %{src_tarball_dir}

%py3_shebang_fix \
    llvm/tools/opt-viewer/*.py \
    llvm/utils/update_cc_test_checks.py

%conf -p
export ASMFLAGS="%{build_cflags}"

%install -a
mkdir -p %{buildroot}/%{_bindir}
pushd %{buildroot}/%{_bindir}
for e in `ls %{buildroot}/%{install_bindir}`;do
  e_src=`realpath --relative-to=. %{buildroot}/%{install_bindir}/$e`
  ln -sf ${e_src} ${e}-%{maj_ver}
done
rm -f *-%{maj_ver}-%{maj_ver}
popd

mkdir -p %{buildroot}/%{_libdir}
pushd %{buildroot}/%{_libdir}
relpath=`realpath --relative-to=. %{buildroot}/%{install_libdir}`
for e in `ls %{buildroot}/%{install_libdir} | grep -e '-%{maj_ver}.so' -e '.so.%{maj_ver}'`;do
  ln -sf $relpath/${e} .
done
popd

%check
# it takes days to complete the testing. Let's just disable it for now.
%end

%define expand_bins() %{lua:
  local bindir = rpm.expand("%{_bindir}")
  local install_bindir = rpm.expand("%{install_bindir}")
  local maj_ver = rpm.expand("%{maj_ver}")
  for arg in rpm.expand("%*"):gmatch("%S+") do
    print(install_bindir .. "/" .. arg .. "\\n")
    print(bindir .. "/" .. arg .. "-" .. maj_ver .. "\\n")
  end
}
%define expand_generic(d:i:) %{lua:
  local dir = rpm.expand("%{-d*}")
  local install_dir = rpm.expand("%{-i*}")
  for arg in rpm.expand("%*"):gmatch("%S+") do
    print(install_dir .. "/" .. arg .. "\\n")
    print(dir .. "/" .. arg .. "\\n")
  end
}
%define expand_libs() %{expand_generic -d %{_libdir} -i %{install_libdir}  %*}

%files
%license compiler-rt/LICENSE.TXT
%ifarch x86_64 riscv64
%{install_libdir}/clang/%{maj_ver}/bin/hwasan_symbolize
%endif
%{install_libdir}/clang/%{maj_ver}/include/fuzzer
%{install_libdir}/clang/%{maj_ver}/include/orc
%{install_libdir}/clang/%{maj_ver}/include/profile
%{install_libdir}/clang/%{maj_ver}/include/sanitizer
%{install_libdir}/clang/%{maj_ver}/include/xray
%{install_libdir}/clang/%{maj_ver}/share/*.txt
# Files that appear on all targets
%{install_libdir}/clang/%{maj_ver}/lib/%{llvm_triple}/libclang_rt.*
%{install_libdir}/clang/%{maj_ver}/lib/%{llvm_triple}/clang_rt.crtbegin.o
%{install_libdir}/clang/%{maj_ver}/lib/%{llvm_triple}/clang_rt.crtend.o
%ifnarch riscv64
%{install_libdir}/clang/%{maj_ver}/lib/%{llvm_triple}/liborc_rt.a
%endif

%changelog
%autochangelog
