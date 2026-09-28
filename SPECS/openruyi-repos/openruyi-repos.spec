# SPDX-FileCopyrightText: (C) 2025 Institute of Software, Chinese Academy of Sciences (ISCAS)
# SPDX-FileCopyrightText: (C) 2025 openRuyi Project Contributors
# SPDX-FileContributor: Zheng Junjie <zhengjunjie@iscas.ac.cn>
# SPDX-FileContributor: misaka00251 <liuxin@iscas.ac.cn>
#
# SPDX-License-Identifier: MulanPSL-2.0

%if %{undefined _vendor_repo_url}
%global _vendor_repo_url https://repo.build.openruyi.cn/openruyi/\\$basearch/
%endif

Name:           openruyi-repos
Version:        4
Release:        %autorelease
Summary:        openRuyi repository files
License:        MulanPSL-2.0
URL:            https://www.openruyi.cn

Source0:        RPM-GPG-KEY-openruyi-obs
Source1:        RPM-GPG-KEY-openruyi
Provides:       system-repos
Provides:       openRuyi-repos

%description
This package contains the repository files for %{_vendor}.

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d/

cat >> %{_vendor}.repo <<EOF
[Base]
name=%{_vendor} Base
baseurl=%{_vendor_repo_url}
enabled=1
gpgcheck=1
gpgkey=file://%{_datadir}/pki/rpm-gpg/RPM-GPG-KEY-openruyi-obs file://%{_datadir}/pki/rpm-gpg/RPM-GPG-KEY-openruyi
EOF

cat %{_vendor}.repo

install -c -m 644 %{_vendor}.repo %{buildroot}%{_sysconfdir}/yum.repos.d/%{_vendor}.repo
mkdir -p %{buildroot}%{_datadir}/pki/rpm-gpg/
cp %{SOURCE0} %{SOURCE1} %{buildroot}%{_datadir}/pki/rpm-gpg/
%files
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/yum.repos.d/%{_vendor}.repo
%dir %{_datadir}/pki/rpm-gpg/
%{_datadir}/pki/rpm-gpg/RPM-GPG-KEY-openruyi*
%changelog
%autochangelog
