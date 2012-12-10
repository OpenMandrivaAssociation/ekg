%define prel rc1

Summary:	A client compatible with Gadu-Gadu
Name:		ekg
Version:	1.8
Release:	0.rc2.3
License:	GPLv2+
Group:		Networking/Instant messaging
URL:		http://ekg.chmurka.net/
Source0:	http://ekg.chmurka.net/%{name}-%{version}%{prel}.tar.bz2
Source1:	%{name}.conf
Patch0:		%{name}-makefile-ioctld-makedir.patch
Patch1:		ekg-1.8_rc1-gtk.patch
BuildRequires:	pkgconfig(python)
BuildRequires:	libgsm-devel
BuildRequires:	aspell-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libgadu)

%description
EKG ("Eksperymentalny Klient Gadu-Gadu") is an open source gadu-gadu
client for UNIX systems. Gadu-Gadu is an instant messaging program,
very popular in Poland.

EKG features include:
  - irssi-like ncurses interface
  - sending and receiving files
  - voice conversations
  - launching shell commands on certain events
  - reading input from pipe
  - python scripting support
  - speech synthesis (using an external program)
  - encryption support

Please note that the program is not internationalized and all messages
are in Polish (although the commands are in English). 

%prep
%setup -qn %{name}-%{version}%{prel}
%patch0 -p1 -b .ioctld
%patch1 -p1 -b .gtk

%build
./autogen.sh
%configure2_5x \
	--enable-aspell \
	--disable-static \
	--enable-shared \
	--enable-ioctld \
	--with-python \
	--with-libgsm

%make

%install
%makeinstall_std

install contrib/ekl2.pl %{buildroot}%{_bindir}
install contrib/ekl2.sh %{buildroot}%{_bindir}
install docs/ekl2.man.pl %{buildroot}%{_mandir}/pl/man1/ekl2.1
install docs/ekl2.man.en %{buildroot}%{_mandir}/man1/ekl2.1
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/ekg.conf
rm -f examples/Makefile examples/Makefile.in examples/.cvsignore

#fix wrong-script-end-of-line-encoding /usr/bin/ekl2.pl
perl -pi -e 's/\015$//' %{buildroot}/%{_bindir}/ekl2.pl

#Remove bad requires from libgadu.pc
perl -pi -e 's/@[^@]*@//' %{buildroot}%{_libdir}/pkgconfig/libgadu.pc

%files
%defattr(644,root,root,755)
%doc docs/{dcc,files,gdb,python,sim,themes,ui-ncurses,vars,voip}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.{ansi,sample}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/e*
%attr(755,root,root) %{_bindir}/ioctld
%{_datadir}/ekg
%{_mandir}/man1/*
%{_mandir}/pl/man1/*

