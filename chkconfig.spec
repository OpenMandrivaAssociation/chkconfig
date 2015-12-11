%define git_url git://git.fedorahosted.org/chkconfig.git

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		chkconfig
Version:	1.7
Release:	1
License:	GPL
Group:		System/Configuration/Boot and Init
Url:		http://git.fedorahosted.org/git/?p=chkconfig.git;a=summary
Source0:	https://fedorahosted.org/releases/c/h/chkconfig/%{name}-%{version}.tar.bz2
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
Requires:	initscripts

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

# we use our own alternative system
rm -f %{buildroot}%{_sbindir}/{alternatives,update-alternatives} %{buildroot}%{_mandir}/man8/alternatives.8*

%find_lang %{name}

%files -f %{name}.lang
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc*
/sbin/chkconfig
%{_mandir}/man8/chkconfig.8*
%{_sysconfdir}/init.d

%files -n ntsysv
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*
