#TODO:
# - summary, description
# - check python
# - check files 
# - make it work
# - server init scripts
# - user and group for server ?
# - french translation (debian patch)
# - teoretically underware is a library to create games, not necesary
#   poker, but it links to libpoker-eval

Summary:	Multiuser 3D online poker game
Summary(pl):	Sieciowa gra w pokera w 3D
Name:		poker3d
Version:	0.2.12
Release:	0.1
License:	GPL v2
Group:		X11/Applications/Games
Source0:	http://download.gna.org/underware/dists/%{name}-%{version}.tar.gz
# Source0-md5:	e4a16c02f5abb4bf6c5c30a366ab0cf9
Patch0:		%{name}-cal3d.patch
Patch1:		%{name}-namespace.patch
URL:		http://www.mekensleep.org/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenSceneGraph-devel >= 0.9.7
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	cal3d-devel
BuildRequires:	doxygen
BuildRequires:	fontconfig-devel
BuildRequires:	libglade2-devel >= 2.4.0
BuildRequires:	libvorbis-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	osgAL-devel
BuildRequires:	osgcal-devel >= 0.1.23
BuildRequires:	poker-eval-devel >= 123.0
BuildRequires:	python-devel >= 2.3
Requires:	poker3d-common = %{version}-%{release}
Requires:	Xwnc
Requires:	pypoker-eval
Requires:	python-Twisted
Requires:	python-libxml2
Requires:	python-pycurl
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Poker3D is a multiuser online poker game. It connects to server where
thirteen tables can be found (Hold'em, Omaha, Omaha8, 7 Stud, Sit and
Go tournaments) with more than fifty players.

%description -l pl
pl desc

%package common
Summary:	Common files for game and server
Summary(pl):	Wspólne pliki serwera i gry
Group:		Applications/Games
Requires:	underware = %{version}-%{release}

%description common

%description common -l pl

%package server
Summary:	Poker3D server
Summary(pl):	Serwer pokera 3D
Group:		Applications/Games
Requires:	poker3d-common = %{version}-%{release}

%description server

%description server -l pl

%package -n underware
Summary:	underware - 3D game programming libraries
Summary(pl):	underware - biblioteki programistyczne gier 3D
Group:		Libraries

%description -n underware

%description -n underware -l pl

%package -n underware-devel
Summary:	underware header files
Summary(pl):	pliki nag³ówkowe underware
Group:		Libraries/Developement
Requires:	underware = %{version}-%{release}
Requires:	OpenSceneGraph-devel
Requires:	cal3d-devel
Requires:	libstdc++-devel
Requires:	osgAL-devel
Requires:	osgcal-devel

%description -n underware-devel

%description -n underware-devel -l pl


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autopoint}
%{__libtoolize}
%{__aclocal} -I ./config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.py" -and -not -name "jabberaccount.py" \
	-exec rm "{}" ";"
# empty
# %find_lang underware
touch underware.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n underware	-p /sbin/ldconfig
%postun	-n underware	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/poker3d
%attr(755,root,root) %{_bindir}/poker3d-interface
%{_mandir}/man6/poker3d.6.*
%{_mandir}/man6/poker3d-interface.6.*
%{_datadir}/underware/poker/data
%{_datadir}/underware/interface.glade*
%{_sysconfdir}/poker3d/client
%{_sysconfdir}/poker3d/engine
%{_sysconfdir}/poker3d/gaim

%files common
%defattr(644,root,root,755)
%dir %{_sysconfdir}/poker3d
%dir %{_datadir}/underware/poker
%{_datadir}/underware/poker/*.py[co]
%{_datadir}/underware/twibber
%{_datadir}/underware/jabberaccount.py
%attr(755,root,root) %{_libdir}/libpoker.so.*.*.*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/poker3d-server
%{_mandir}/man6/poker3d-server.6.*
%{_sysconfdir}/poker3d/tournament
%{_sysconfdir}/poker3d/server
%{_sysconfdir}/poker3d/bot
%{_datadir}/underware/poker/db

%files -n underware -f underware.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CREDITS LICENSE.OSG LICENSE.twibber NEWS README
%attr(755,root,root) %{_bindir}/underware
%dir %{_datadir}/underware
%attr(755,root,root) %{_libdir}/lib[emu]*.so.*.*.*
%{_mandir}/man6/underware.6.*
%dir %{py_sitedir}/underware
%{py_sitedir}/underware/*.py[co]
%attr(755,root,root) %{py_sitedir}/underware/*.so.*.*.*
%attr(755,root,root) %{_libdir}/osgPlugins/libosgdb_hdr.so.*.*.*

%files -n underware-devel
%defattr(644,root,root,755)
%{_includedir}/underware
%attr(755,root,root) %{_libdir}/lib[emu]*.so
%{_libdir}/lib[emu]*.la
%{_pkgconfigdir}/underware.pc
%attr(755,root,root) %{py_sitedir}/underware/*.so
%{py_sitedir}/underware/*.la
%attr(755,root,root) %{_libdir}/osgPlugins/libosgdb_hdr.so
%{_libdir}/osgPlugins/libosgdb_hdr.la
