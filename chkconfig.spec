Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		chkconfig
Version:	1.3.34
Release:	%mkrel 2
License:	GPL
Group:		System/Configuration/Boot and Init
Url:		ftp://ftp.redhat.com/pub/redhat/code/chkconfig/
Source0:	ftp://ftp.redhat.com/pub/redhat/code/chkconfig/%{name}-%{version}.tar.bz2
# zh_TW translation -- GEoff
Source1:	chkconfig.po
Patch1:		ntsysv-mdkconf.patch
Patch3:		chkconfig-runleveldir.patch
Patch5:		chkconfig-fix.patch
Patch6:		chkconfig-1.3.25-adddelxinetd.patch
Patch7:		chkconfig-1.3.4-list.patch
Patch8:		chkconfig-1.3.4-skip-files-with-dot.patch
Patch10:	chkconfig-1.3.11-fix-errno-xinetddotd.patch
Patch11:	chkconfig-1.3.34-lsb.patch
Patch12:	chkconfig-1.3.20-fix-fr.patch
# (blino) fix priority when adding a LSB service required by another LSB service (#22019)
Patch13:	chkconfig-1.3.30-targreq.patch
# (blino) handle Should-Start/Should-Stop tags (#28026)
Patch14:	chkconfig-1.3.30-should.patch
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
%patch1 -p0 -b .mdkconf
%patch3 -p1 -b .runleveldir
%patch5 -p0 -b .fix
%patch6 -p1 -b .adddelxinetd
%patch7 -p1 -b .list
%patch8 -p1 -b .skip-files-with-dot
%patch10 -p1 -b .fix-errno-xinetddotd
%patch11 -p1 -b .lsb
%patch12 -p1 -b .fix-fr
%patch13 -p1 -b .targreq
%patch14 -p1 -b .should

%build

%ifarch sparc
LIBMHACK=-lm
%endif

%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" LIBMHACK=$LIBMHACK

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std MANDIR=%{_mandir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc${n}.d
done

cd $RPM_BUILD_ROOT%{_sysconfdir}/
ln -s rc.d/init.d init.d
cd -

# corrected indonesian language code (it has changed from 'in' to 'id')
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/id/LC_MESSAGES
mv $RPM_BUILD_ROOT%{_datadir}/locale/{in,in_ID}/LC_MESSAGES/* \
	$RPM_BUILD_ROOT%{_datadir}/locale/id/LC_MESSAGES || :
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{in,in_ID} || :

mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES
msgfmt %SOURCE1 -o $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES/chkconfig.mo

# Geoff 20020623 -- zh is incorrect for locale and there's nothing in it anyway
rm -fr $RPM_BUILD_ROOT%_datadir/locale/zh

# we use our own alternative system
rm -f $RPM_BUILD_ROOT%{_sbindir}/{alternatives,update-alternatives} $RPM_BUILD_ROOT%{_mandir}/man8/alternatives.8*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
/sbin/chkconfig
%{_mandir}/man8/chkconfig.8*
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc*
%{_sysconfdir}/init.d

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*


