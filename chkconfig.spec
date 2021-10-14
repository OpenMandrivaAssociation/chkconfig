%define git_url git://git.fedorahosted.org/chkconfig.git

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		chkconfig
Version:	1.15
Release:	2
License:	GPL
Group:		System/Configuration/Boot and Init
Url:		https://github.com/fedora-sysv/chkconfig
Source0:	https://github.com/fedora-sysv/chkconfig/archive/%{name}-%{version}.tar.gz
Source1:	chkconfig.po
# (tpg) taken from initscripts as it got obsoleted
Source2:	service
Patch0:		chkconfig-1.11-drop-selinux.patch
BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(slang)
BuildRequires:	pkgconfig(libsystemd)
# explicit file provides
Provides:	/sbin/chkconfig
Provides:	%{_sbindir}/chkconfig
Provides:	%{_sbindir}/alternatives
Provides:	%{_sbindir}/update-alternatives
Provides:	update-alternatives = 1.18.4-2
Obsoletes:	update-alternatives < 1.18.4-2
Provides:	/sbin/service
Provides:	%{_sbindir}/service
Conflicts:	initscripts < 11.0-1
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

%description -n ntsysv
ntsysv updates and queries runlevel information for system services.
ntsysv relieves system administrators of having to directly manipulate
the numerous symbolic links in /etc/rc*.d.

%prep
%autosetup -p1

%build
%make_build CC=%{__cc} RPM_OPT_FLAGS="%{optflags}" LIBMHACK=$LIBMHACK LDFLAGS="%{ldflags}"

%install
%make_install MANDIR=%{_mandir} BINDIR=%{_sbindir}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
ln -s rc.d/init.d %{buildroot}%{_sysconfdir}/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
    ln -s rc.d/rc${n}.d %{buildroot}%{_sysconfdir}/rc${n}.d
done

mkdir -p %{buildroot}%{_sysconfdir}/chkconfig.d

# corrected indonesian language code (it has changed from 'in' to 'id')
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES
mv %{buildroot}%{_datadir}/locale/{in,in_ID}/LC_MESSAGES/* \
    %{buildroot}%{_datadir}/locale/id/LC_MESSAGES || :
rm -rf %{buildroot}%{_datadir}/locale/{in,in_ID} || :

mkdir -p %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES/chkconfig.mo

# Geoff 20020623 -- zh is incorrect for locale and there's nothing in it anyway
rm -fr %{buildroot}%{_datadir}/locale/zh

# Create alternatives directories
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
touch %{buildroot}%{_localstatedir}/log/update-alternatives.log

# (tpg) compat symlink
mkdir -p %{buildroot}/sbin
ln -sf %{_sbindir}/chkconfig %{buildroot}/sbin/chkconfig

# (tpg) ship service executable for backward compatability
install -m755 %{SOURCE2} %{buildroot}%{_sbindir}/service
ln -sf %{_sbindir}/service %{buildroot}/sbin/service

%find_lang %{name}

%pretrans -p <lua>
path = "%{_localstatedir}/lib/alternatives"
path2 = "%{_localstatedir}/lib/rpm/alternatives"
st = posix.stat(path)
st2 = posix.stat(path2)
if st and st.type == "link" and st2 and st2.type == "directory" then
  os.remove(path)
  os.rename(path2, path)
  posix.symlink(path, path2)
end

%files -f %{name}.lang
/sbin/chkconfig
%{_sbindir}/chkconfig
/sbin/service
%{_sbindir}/service
/lib/systemd/systemd-sysv-install
%{_mandir}/man8/chkconfig.8*
%dir %{_sysconfdir}/chkconfig.d
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%{_sysconfdir}/init.d
%{_sysconfdir}/rc[0-6].d
%{_sysconfdir}/rc.d/rc[0-6].d
%{_sbindir}/alternatives
%{_sbindir}/update-alternatives
%doc %{_mandir}/man8/alternatives.8*
%doc %{_mandir}/man8/update-alternatives.8*
%dir %{_localstatedir}/lib/alternatives
%dir %{_sysconfdir}/alternatives
%ghost %{_localstatedir}/log/update-alternatives.log

%files -n ntsysv
%{_sbindir}/ntsysv
%doc %{_mandir}/man8/ntsysv.8*
