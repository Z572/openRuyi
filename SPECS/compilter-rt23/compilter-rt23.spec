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
# clang patches

BuildRequires:  llvm%{maj_ver} = %{version}
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
The compiler-rt project is a part of the LLVM project. It provides
implementation of the low-level target-specific hooks required by
code generation, sanitizer runtimes and profiling library for code
instrumentation, and Blocks C language extension.

%prep
%autosetup -p1 -T -b 0 -n %{src_tarball_dir}

%py3_shebang_fix \
    llvm/test/BugPoint/compile-custom.ll.py \
    llvm/tools/opt-viewer/*.py \
    llvm/utils/update_cc_test_checks.py
%py3_shebang_fix \
    clang-tools-extra/clang-tidy/tool/ \
    clang-tools-extra/clang-include-fixer/find-all-symbols/tool/run-find-all-symbols.py
%py3_shebang_fix \
    clang/tools/clang-format/ \
    clang/tools/clang-format/git-clang-format \
    clang/utils/hmaptool/hmaptool \
    clang/tools/scan-view/bin/scan-view \
    clang/tools/scan-view/share/Reporter.py \
    clang/tools/scan-view/share/startfile.py \
    clang/tools/scan-build-py/bin/* \
    clang/tools/scan-build-py/libexec/*
%py3_shebang_fix compiler-rt/lib/hwasan/scripts/hwasan_symbolize
%py3_shebang_fix libcxx/utils/

%conf
export ASMFLAGS="%{build_cflags}"
export FFLAGS=`echo %{build_fflags} | sed -e "s/-pipe//g" -e "s/-funwind-tables//g" -e "s/-fasynchronous-unwind-tables//g" -e "s/-fstack-protector-strong//g" -e "s/-fstack-clash-protection//g" -e "s/-Wformat//g" -e "s/-Werror=format-security//g"`
export FCFLAGS=${FFLAGS}

cd llvm
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
    -DCLANG_LINK_CLANG_DYLIB=ON \\\
    -DLLVM_ENABLE_FFI:BOOL=ON \\\
    -DLLVM_BINUTILS_INCDIR=/usr/include
%global cmake_common_args %{cmake_common_args} \\\
    -DLLVM_ENABLE_EH=OFF

# compiler-rt options
%global cmake_config_args %{cmake_config_args} \\\
    -DCOMPILER_RT_INCLUDE_TESTS:BOOL=OFF

# docs options
%global cmake_config_args %{cmake_config_args} \\\
    -DLLVM_ENABLE_DOXYGEN:BOOL=OFF \\\
    -DLLVM_ENABLE_SPHINX:BOOL=OFF \\\
    -DLLVM_BUILD_DOCS:BOOL=OFF

# lldb options
%global cmake_config_args %{cmake_config_args} \\\
    -DLLDB_ENFORCE_STRICT_TEST_REQUIREMENTS:BOOL=ON \\\
    -DLLDB_PYTHON_RELATIVE_PATH=lib/python%{python3_version}/site-packages

# libcxx options
%global cmake_config_args %{cmake_config_args}  \\\
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \\\
    -DLIBCXX_INCLUDE_BENCHMARKS=OFF \\\
    -DLIBCXX_STATICALLY_LINK_ABI_IN_STATIC_LIBRARY=ON \\\
    -DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=ON \\\
    -DLIBCXXABI_USE_LLVM_UNWINDER=OFF

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
    -DLLVM_ENABLE_PROJECTS="%{projects}" \\\
    -DLLVM_ENABLE_RUNTIMES="%{runtimes}" \\\
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

# mlir options
%global cmake_config_args %{cmake_config_args} \\\
    -DMLIR_INCLUDE_DOCS:BOOL=ON \\\
    -DMLIR_INCLUDE_TESTS:BOOL=ON \\\
    -DMLIR_INCLUDE_INTEGRATION_TESTS:BOOL=OFF \\\
    -DMLIR_INSTALL_AGGREGATE_OBJECTS=OFF \\\
    -DMLIR_BUILD_MLIR_C_DYLIB=ON \\\
    -DMLIR_ENABLE_BINDINGS_PYTHON:BOOL=ON

# openmp options
%global cmake_config_args %{cmake_config_args} \\\
    -DLIBOMP_INSTALL_ALIASES=OFF

# polly options
%global cmake_config_args %{cmake_config_args} \\\
    -DLLVM_POLLY_LINK_INTO_TOOLS=OFF

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

# Now let's build
%cmake -G Ninja %{cmake_config_args} %{extra_cmake_opts} $extra_cmake_args

%build
%cmake_build

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

%end

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

%files -n compiler-rt%{maj_ver}
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
