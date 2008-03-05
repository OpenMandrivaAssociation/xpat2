Summary:	A set of Solitaire type games for the X Window System
Name:		xpat2
Version:	1.07
Release:    	%mkrel 23
License:	GPL
Group:		Games/Cards
Source:		ftp://sunsite.unc.edu/pub/Linux/games/solitaires/%{name}-%{version}-src.tar.bz2	
Patch:		xpat2-fixes.patch.bz2
Patch1:		xpat2-1.07-lib64.patch.bz2
Patch2:		xpat2-1.07-gcc41.patch.bz2
BuildRequires:	imake
BuildRequires:	qt3-devel
BuildRequires:	perl
BuildRequires:	libxpm-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):		rpm-helper

%description
Xpat2 is a generic patience or Solitaire game for the X Window System.

Xpat2 can be used with different rules sets, so it can be used to play
Spider, Klondike, and other card games.

%prep
%setup -q
%patch -p1 -b kk1
%patch1 -p1 -b .lib64
%patch2 -p0 -b .gcc41

%build
make clean
%__rm -f src/moc*
%__rm -f src/mqmaskedit.cpp
%__rm -f src/mqhelpwin.cpp

export PATH=%{_bindir}/X11:$PATH

find -type f | xargs perl -pi -e "s|/var/games/|/var/lib/games/|g" 
perl -p -i -e "s|xmkmf &&||" Makefile
cd src
xmkmf
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
# 1.0.7-1
perl -p -i -e "s|chown.*||" Makefile
perl -p -i -e "s|-lqt|-lqt-mt|" Makefile
perl -p -i -e "s|LN = ln -s|LN = echo|" Makefile
make CDEBUGFLAGS="$RPM_OPT_FLAGS" CXXDEBUGFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf %buildroot
%makeinstall DESTDIR=%buildroot \
	XPATROOT=%buildroot/usr/games/lib/xpat \
	XPATMANDIR=%buildroot/usr/share/man/man6 \
	APPDEFSDIR=%buildroot/usr/lib
install -m 755 -d %buildroot%{_menudir}
mkdir -p %buildroot/var/lib/games/
touch %buildroot/var/lib/games/xpat.log
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=A set of Solitaire type games for the X Window System
Exec=%{_bindir}/%{name} 
Icon=cards_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;Game;CardGame;X-MandrivaLinux-MoreApplications-Games-Cards;
EOF

%post
%update_menus
%create_ghostfile /var/lib/games/xpat.log root games 664

%postun
%clean_menus

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
#%config(noreplace) %{_sysconfdir}/X11/app-defaults/XPat
%dir %{_prefix}/games/lib/xpat
%{_prefix}/games/lib/xpat/*
%{_mandir}/man6/xpat2.6*
%attr(2755, root, games) %{_prefix}/bin/xpat2
%{_prefix}/lib/*/app-defaults/XPat
%{_datadir}/applications/mandriva-%{name}.desktop
%attr(664, root, games) %ghost /var/lib/games/xpat.log
