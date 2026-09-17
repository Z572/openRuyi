# SPDX-FileCopyrightText: (C) 2025, 2026 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025, 2026 openRuyi Project Contributors
# SPDX-FileContributor: jchzhou <zhoujiacheng@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

# Originally extracted from Fedora Project
# Authors: The Fedora Project Contributors

%global _vpath_srcdir llvm

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
%global build_libdir llvm/%{_vpath_builddir}/%{_lib}
%global unprefixed_libdir %{_lib}
%global targets_to_build "X86;AMDGPU;NVPTX;BPF;WebAssembly;RISCV;AArch64"
%global experimental_targets_to_build ""
%global build_install_prefix %{buildroot}%{install_prefix}
%global llvm_triple %{_target_platform}

Name:           llvm%{maj_ver}
Version:        %{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:~%{rc_ver}}
Release:        %{autorelease}
Summary:        The Low Level Virtual Machine (%{maj_ver})
License:        Apache-2.0 WITH LLVM-exception OR NCSA
URL:            http://llvm.org
VCS:            git:https://github.com/llvm/llvm-project.git
#!RemoteAsset:  sha256:ebe9be46fe8756d58c5b198ffad0fa2a766257add81a4dc52179bfacc7888ee6
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{maj_ver}.%{min_ver}.%{patch_ver}%{?rc_ver:-%{rc_ver}}/%{src_tarball_dir}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(ncurses)
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

Requires:       llvm%{maj_ver}-libs%{?_isa} = %{version}-%{release}
Provides:       llvm(major) = %{maj_ver}

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

%package     -n llvm%{maj_ver}-devel
Summary:        Libraries and header files for LLVM (%{maj_ver})
Requires:       llvm%{maj_ver}%{?_isa} = %{version}-%{release}
Requires:       llvm%{maj_ver}-libs%{?_isa} = %{version}-%{release}
# The installed LLVM cmake files will add -ledit to the linker flags for any
# app that requires the libLLVMLineEditor, so we need to make sure
# libedit-devel is available.
Requires:       pkgconfig(libedit)
Requires:       pkgconfig(libzstd)
Provides:       llvm-devel(major) = %{maj_ver}

%description -n llvm%{maj_ver}-devel
This package contains library and header files needed to develop new native
programs that use the LLVM infrastructure.

%package     -n llvm%{maj_ver}-libs
Summary:        LLVM shared libraries (%{maj_ver})

%description -n llvm%{maj_ver}-libs
Shared libraries for the LLVM compiler infrastructure.

%package     -n llvm%{maj_ver}-static
Summary:        LLVM static libraries (%{maj_ver})
Requires:       llvm%{maj_ver}-devel%{?_isa} = %{version}-%{release}
Provides:       llvm-static(major) = %{maj_ver}

%description -n llvm%{maj_ver}-static
Static libraries for the LLVM compiler infrastructure.

%package     -n llvm%{maj_ver}-cmake-utils
Summary:        CMake utilities shared across LLVM subprojects (%{maj_ver})

%description -n llvm%{maj_ver}-cmake-utils
CMake utilities shared across LLVM subprojects.
This is for internal use by LLVM packages only.


%prep
%autosetup -p1 -T -b 0 -n %{src_tarball_dir}

%py3_shebang_fix \
    llvm/tools/opt-viewer/*.py \
    llvm/utils/update_cc_test_checks.py

%conf
export ASMFLAGS="%{build_cflags}"
export FFLAGS=`echo %{build_fflags} | sed -e "s/-pipe//g" -e "s/-funwind-tables//g" -e "s/-fasynchronous-unwind-tables//g" -e "s/-fstack-protector-strong//g" -e "s/-fstack-clash-protection//g" -e "s/-Wformat//g" -e "s/-Werror=format-security//g"`
export FCFLAGS=${FFLAGS}

# Remember old values to reset to
OLD_PATH="$PATH"
OLD_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
OLD_CWD="$PWD"

# general cmake options
# Any ABI-affecting flags should be in here
%global cmake_common_args \\\
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \\\
    -DLLVM_ENABLE_RTTI=ON \\\
    -DLLVM_USE_PERF=ON \\\
    -DLLVM_TARGETS_TO_BUILD=%{targets_to_build} \\\
    -DBUILD_SHARED_LIBS=OFF \\\
    -DLLVM_BUILD_LLVM_DYLIB=ON \\\
    -DLLVM_LINK_LLVM_DYLIB=ON \\\
    -DLLVM_ENABLE_FFI:BOOL=ON \\\
    -DLLVM_BINUTILS_INCDIR=/usr/include
%global cmake_common_args %{cmake_common_args} \\\
    -DLLVM_ENABLE_EH=OFF

%ifarch riscv64
%global cmake_common_args %{cmake_common_args} \\\
    -DLLVM_PARALLEL_LINK_JOBS=2 \\\
    -DLLVM_PARALLEL_COMPILE_JOBS=16
%endif

%global cmake_config_args %{cmake_common_args}

# docs options
%global cmake_config_args %{cmake_config_args} \\\
    -DLLVM_ENABLE_DOXYGEN:BOOL=OFF \\\
    -DLLVM_ENABLE_SPHINX:BOOL=OFF \\\
    -DLLVM_BUILD_DOCS:BOOL=OFF

# llvm options
%global cmake_config_args %{cmake_config_args}  \\\
    -DLLVM_APPEND_VC_REV:BOOL=OFF \\\
    -DLLVM_BUILD_EXAMPLES:BOOL=OFF \\\
    -DLLVM_BUILD_EXTERNAL_COMPILER_RT:BOOL=ON \\\
    -DLLVM_BUILD_RUNTIME:BOOL=ON \\\
    -DLLVM_BUILD_TOOLS:BOOL=ON \\\
    -DLLVM_BUILD_UTILS:BOOL=ON \\\
    -DLLVM_DEFAULT_TARGET_TRIPLE=%{llvm_triple} \\\
    -DLLVM_ENABLE_LIBCXX:BOOL=OFF \\\
    -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON \\\
    -DLLVM_ENABLE_ZLIB:BOOL=FORCE_ON \\\
    -DLLVM_ENABLE_ZSTD:BOOL=FORCE_ON \\\
    -DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD=%{experimental_targets_to_build} \\\
    -DLLVM_INCLUDE_BENCHMARKS=OFF \\\
    -DLLVM_INCLUDE_EXAMPLES:BOOL=OFF \\\
    -DLLVM_INCLUDE_TOOLS:BOOL=ON \\\
    -DLLVM_INCLUDE_UTILS:BOOL=ON \\\
    -DLLVM_INSTALL_TOOLCHAIN_ONLY:BOOL=OFF \\\
    -DLLVM_INSTALL_UTILS:BOOL=ON \\\
    -DLLVM_TOOLS_INSTALL_DIR:PATH=bin \\\
    -DLLVM_UNREACHABLE_OPTIMIZE:BOOL=OFF \\\
    -DLLVM_UTILS_INSTALL_DIR:PATH=bin \\\
    -DLLVM_ENABLE_LTO=OFF


# test options
%global cmake_config_args %{cmake_config_args} \\\
    -DLLVM_BUILD_TESTS:BOOL=ON \\\
    -DLLVM_INCLUDE_TESTS:BOOL=ON \\\
    -DLLVM_INSTALL_GTEST:BOOL=ON \\\
    -DLLVM_LIT_ARGS="-vv"

# misc options
%global cmake_config_args %{cmake_config_args} \\\
    -DCMAKE_INSTALL_PREFIX=%{install_prefix} \\\
    -DENABLE_LINKER_BUILD_ID:BOOL=ON \\\
    -DPython3_EXECUTABLE=%{__python3}
# During the build, we use both the system clang and the just-built clang, and
# they need to use the system and just-built shared objects respectively. If
# we use LD_LIBRARY_PATH to point to our build directory, the system clang
# may use the just-built shared objects instead, which may not be compatible
# even if the version matches (e.g. when building compat libs or different rcs).
# Instead, we make use of rpath during the build and only strip it on
# installation using the CMAKE_SKIP_INSTALL_RPATH option.
%global cmake_config_args %{cmake_config_args} -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON
%global cmake_config_args %{cmake_config_args} -DLLVM_VERSION_SUFFIX=''

extra_cmake_args=''
# https://github.com/llvm/llvm-project/issues/111492
if grep 'flags.*la57' /proc/cpuinfo; then
  extra_cmake_args="$extra_cmake_args -DOPENMP_TEST_ENABLE_TSAN=OFF"
fi

# Now reset paths and globals
function reset_paths {
    export PATH="$OLD_PATH"
    export LD_LIBRARY_PATH="$OLD_LD_LIBRARY_PATH"
}
reset_paths
cd $OLD_CWD


%global extra_cmake_opts %{nil}

%cmake -G Ninja %{cmake_config_args} %{extra_cmake_opts} $extra_cmake_args

%build
# Now let's build
%cmake_build
# build the runtimes target here

%install
%cmake_install

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

%files -n llvm%{maj_ver}
%license llvm/LICENSE.TXT
%{expand_bins %{expand:
    FileCheck
    UnicodeNameMappingGenerator
    clang-offload-packager
    count
    dsymutil
    llc
    lli
    lli-child-target
    llubi
    llvm-PerfectShuffle
    llvm-addr2line
    llvm-ar
    llvm-as
    llvm-bcanalyzer
    llvm-bitcode-strip
    llvm-c-test
    llvm-cas
    llvm-cat
    llvm-cfi-verify
    llvm-cgdata
    llvm-cov
    llvm-ctxprof-util
    llvm-cvtres
    llvm-cxxdump
    llvm-cxxfilt
    llvm-cxxmap
    llvm-debuginfo-analyzer
    llvm-debuginfod
    llvm-debuginfod-find
    llvm-diff
    llvm-dis
    llvm-dlltool
    llvm-dwarfdump
    llvm-dwarfutil
    llvm-dwp
    llvm-exegesis
    llvm-extract
    llvm-extract-bundle-entry
    llvm-gpu-loader
    llvm-gsymutil
    llvm-ifs
    llvm-install-name-tool
    llvm-ir2vec
    llvm-jitlink
    llvm-jitlink-executor
    llvm-lib
    llvm-libtool-darwin
    llvm-link
    llvm-lipo
    llvm-lto
    llvm-lto2
    llvm-mc
    llvm-mca
    llvm-ml
    llvm-ml64
    llvm-modextract
    llvm-mt
    llvm-nm
    llvm-objcopy
    llvm-objdump
    llvm-offload-binary
    llvm-offload-wrapper
    llvm-opt-report
    llvm-otool
    llvm-pdbutil
    llvm-profdata
    llvm-profgen
    llvm-ranlib
    llvm-rc
    llvm-readelf
    llvm-readobj
    llvm-readtapi
    llvm-reduce
    llvm-remarkutil
    llvm-rtdyld
    llvm-sim
    llvm-size
    llvm-split
    llvm-stress
    llvm-strings
    llvm-strip
    llvm-symbolizer
    llvm-tblgen
    llvm-test-mustache-spec
    llvm-tli-checker
    llvm-undname
    llvm-windres
    llvm-xray
    not
    obj2yaml
    opt
    reduce-chunk-list
    sancov
    sanstats
    split-file
    verify-uselistorder
    yaml-bench
    yaml2obj
}}
%{install_datadir}/opt-viewer

%files -n llvm%{maj_ver}-libs
%license llvm/LICENSE.TXT
%{install_libdir}/libLLVM*.so*
%{install_libdir}/libLTO*.so*
%{install_libdir}/libRemarks*.so*
%{install_libdir}/LLVMgold.so
%{_libdir}/libLLVM*.so*
%{_libdir}/libLTO*.so*
%{_libdir}/libRemarks*.so*

%files -n llvm%{maj_ver}-devel
%license llvm/LICENSE.TXT
%{install_bindir}/llvm-config
%{_bindir}/llvm-config-%{maj_ver}
%{install_includedir}/llvm
%{install_includedir}/llvm-c
%{install_includedir}/llvm-gmock
%{install_includedir}/llvm-gtest
%{install_libdir}/libLLVM.so
%{install_libdir}/cmake/llvm

%files -n llvm%{maj_ver}-static
%license llvm/LICENSE.TXT
%{install_libdir}/libLLVM*.a
%{install_libdir}/libllvm_gtest*.a

%changelog
%autochangelog
