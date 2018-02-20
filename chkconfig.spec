%define git_url git://git.fedorahosted.org/chkconfig.git

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		chkconfig
Version:	1.10
Release:	3
License:	GPL
Group:		System/Configuration/Boot and Init
Url:		https://github.com/fedora-sysv/chkconfig
Source0:	https://github.com/fedora-sysv/chkconfig/archive/%{name}-%{version}.tar.gz
Source1:	chkconfig.po

# (cg) Revert the selinux stuff for now.
Patch0500:	0500-Revert-leveldb-remove-debug-output.patch
Patch0501:	0501-Revert-leveldb-restore-selinux-context-for-xinetd-co.patch
Patch0502:	0502-Revert-Makefile-fix-wrongly-behaving-LDFLAGS.patch

# Downstream patches
Patch0900:	0900-netsysv-Use-Mandriva-colours.patch
Patch0901:	0901-leveldb-Change-runlevels-dir-to-suit-Mandriva.patch
Patch0902:	0902-chkconfig-Delete-a-service-before-adding-it.patch
Patch0903:	0903-chkconfig-Support-adding-deleting-xinetd-services.patch
Patch0904:	0904-chkconfig-Do-not-show-errors-in-service-lists.patch
Patch0905:	0905-chkconfig-Skip-any-init-script-with-a-dot-comma-or-t.patch
Patch0906:	0906-chkconfig-Fix-xinetd-error-message.patch
Patch0907:	0907-chkconfig-Fix-priority-when-adding-a-LSB-service-req.patch

BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(slang)
# explicit file provides
Provides:	/sbin/chkconfig
Provides:	%{_sbindir}/chkconfig
Provides:	%{_sbindir}/alternatives
Provides:	%{_sbindir}/update-alternatives
Provides:       update-alternatives = 1.18.4-2
Obsoletes:      update-alternatives < 1.18.4-2
Requires:	/bin/sh
Requires:	coreutils
Requires:	util-linux

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc*.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.

%package -n ntsysv
Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Group:		System/Configuration/Boot and Init
Requires:	chkconfig = %{EVRD}

%description -n	ntsysv
ntsysv updates and queries runlevel information for system services.
ntsysv relieves system administrators of having to directly manipulate
the numerous symbolic links in /etc/rc*.d.

%prep
%setup -q
%apply_patches
perl -pi -e 's/\bmv\b/mv -f/' po/Makefile

%build
%make CC=%{__cc} RPM_OPT_FLAGS="%{optflags}" LIBMHACK=$LIBMHACK LDFLAGS="%{ldflags}"

%install
%makeinstall_std MANDIR=%{_mandir} BINDIR=%{_sbindir}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
done

cd %{buildroot}%{_sysconfdir}/
ln -s rc.d/init.d init.d
cd -

# corrected indonesian language code (it has changed from 'in' to 'id')
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES
mv %{buildroot}%{_datadir}/locale/{in,in_ID}/LC_MESSAGES/* \
    %{buildroot}%{_datadir}/locale/id/LC_MESSAGES || :
rm -rf %{buildroot}%{_datadir}/locale/{in,in_ID} || :

mkdir -p %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES/chkconfig.mo

# Geoff 20020623 -- zh is incorrect for locale and there's nothing in it anyway
rm -fr %{buildroot}%{_datadir}/locale/zh

# alternatives were historically stored in /var/lib/rpm/alternatives
mkdir -p %{buildroot}%{_localstatedir}/lib/rpm
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
mv %{buildroot}%{_localstatedir}/lib/alternatives %{buildroot}%{_localstatedir}/lib/rpm/alternatives
ln -s rpm/alternatives %{buildroot}%{_localstatedir}/lib/alternatives
touch %{buildroot}%{_localstatedir}/log/update-alternatives.log

# (tpg) compat symlink
mkdir -p %{buildroot}/sbin
ln -sf %{_sbindir}/chkconfig %{buildroot}/sbin/chkconfig

%find_lang %{name}

%files -f %{name}.lang
/sbin/chkconfig
%{_sbindir}/chkconfig
%{_prefix}/lib/systemd/systemd-sysv-install
%{_mandir}/man8/chkconfig.8*
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc*
%{_sysconfdir}/init.d
%{_sbindir}/alternatives
%attr(0755,root,root) %{_sbindir}/update-alternatives
%{_mandir}/man8/alternatives.8*
%{_mandir}/man8/update-alternatives.8*
%{_localstatedir}/lib/alternatives
%dir %{_localstatedir}/lib/rpm/alternatives
%dir %{_sysconfdir}/alternatives
%ghost %{_localstatedir}/log/update-alternatives.log

%files -n ntsysv
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*
