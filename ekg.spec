Summary:	A client compatible with Gadu-Gadu
Name:		ekg
Version:	1.7
Release:	%mkrel 3
License:	GPL
Group:		Networking/Instant messaging
Source0:	http://ekg.chmurka.net/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf
URL:		http://ekg.chmurka.net/
Patch0:		%{name}-makefile-ioctld-makedir.patch
Patch1:		%{name}-1.7-external-libgadu.patch
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	libgsm-devel		>= 1.0.10
BuildRequires:	libaspell-devel		>= 0.60.4
BuildRequires:	libncurses-devel	>= 5.5
BuildRequires:	libjpeg-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	libgadu-devel		>= 1.7.1

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
%setup -q
%patch0 -p1 -b .%{name}-makefile-ioctld-makedir
%patch1 -p1

rm -fr examples/CVS

%build
./autogen.sh
%configure2_5x \
	--enable-aspell \
	--disable-static \
	--enable-shared \
	--enable-ioctld \
	--with-python \
	--with-libgsm \
	--without-libgadu

%make
pushd docs/api
./make.pl
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc docs/{7thguard,dcc,files,gdb,python,sim,themes,ui-ncurses,vars,voip}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.{ansi,sample}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/e*
%attr(755,root,root) %{_bindir}/ioctld
%{_datadir}/ekg
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
