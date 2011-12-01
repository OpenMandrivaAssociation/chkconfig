%define git_url git://git.fedorahosted.org/chkconfig.git

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		chkconfig
Version:	1.3.51
Release:	3
License:	GPL
Group:		System/Configuration/Boot and Init
Url:		http://git.fedorahosted.org/git/?p=chkconfig.git;a=summary
Source0:	https://fedorahosted.org/releases/c/h/chkconfig/%{name}-%{version}.tar.bz2
Source1:	chkconfig.po
Patch1:		ntsysv-mdkconf.patch
Patch3:		chkconfig-runleveldir.patch
Patch5:		chkconfig-fix.patch
Patch6:		chkconfig-1.3.50-adddelxinetd.patch
Patch7:		chkconfig-1.3.50-list.patch
Patch8:		chkconfig-1.3.50-skip-files-with-dot.patch
Patch10:	chkconfig-1.3.11-fix-errno-xinetddotd.patch
# (blino) fix priority when adding a LSB service required by another LSB service (#22019)
Patch13:	chkconfig-1.3.50-targreq.patch
# (fc) introduce runlevel 7, acting as runlevel S
Patch15:	chkconfig-1.3.50-rc7.patch

# upstream patches

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	popt-devel
BuildRequires:	slang
Conflicts:	rpm-helper < 0.6
# explicit file provides
Provides:	/sbin/chkconfig

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc*.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.

%package -n	ntsysv
Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Group:		System/Configuration/Boot and Init
Requires:	chkconfig

%description -n	ntsysv
ntsysv updates and queries runlevel information for system services.
ntsysv relieves system administrators of having to directly manipulate
the numerous symbolic links in /etc/rc*.d.

%prep
%setup -q
%patch1 -p1 -b .mdkconf
%patch3 -p1 -b .runleveldir
%patch5 -p1 -b .fix
%patch6 -p1 -b .adddelxinetd
%patch7 -p1 -b .list
%patch8 -p1 -b .skip-files-with-dot
%patch10 -p0 -b .fix-errno-xinetddotd
%patch13 -p1 -b .targreq
%patch15 -p1 -b .rc7
perl -pi -e 's/\bmv\b/mv -f/' po/Makefile

%build

%ifarch sparc
LIBMHACK=-lm
%endif

%make RPM_OPT_FLAGS="%{optflags}" LIBMHACK=$LIBMHACK LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}
%makeinstall_std MANDIR=%{_mandir}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
for n in 0 1 2 3 4 5 6 7; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
done

cd %{buildroot}%{_sysconfdir}/
ln -s rc.d/init.d init.d
cd -
ln -s rc7.d %{buildroot}%{_sysconfdir}/rc.d/rcS.d

# corrected indonesian language code (it has changed from 'in' to 'id')
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES
mv %{buildroot}%{_datadir}/locale/{in,in_ID}/LC_MESSAGES/* \
	%{buildroot}%{_datadir}/locale/id/LC_MESSAGES || :
rm -rf %{buildroot}%{_datadir}/locale/{in,in_ID} || :

mkdir -p %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES
msgfmt %SOURCE1 -o %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES/chkconfig.mo

# Geoff 20020623 -- zh is incorrect for locale and there's nothing in it anyway
rm -fr %{buildroot}%_datadir/locale/zh

# we use our own alternative system
rm -f %{buildroot}%{_sbindir}/{alternatives,update-alternatives} %{buildroot}%{_mandir}/man8/alternatives.8*

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/sbin/chkconfig
%{_mandir}/man8/chkconfig.8*
%dir %{_sysconfdir}/rc.d/rc*
%{_sysconfdir}/init.d

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*


