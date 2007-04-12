%define	prel 20070305
%define	major 3
%define	libname	%mklibname gadu %{major}

Summary:	A client compatible with Gadu-Gadu
Name:		ekg
Version:	1.7
Release:	%mkrel 0.%{prel}.2
License:	GPL
Group:		Networking/Instant messaging
Source0:	http://ekg.chmurka.net/ekg-%{prel}.tar.bz2
Source1:	%{name}.conf
URL:		http://ekg.chmurka.net/
Patch0:		%{name}-makefile-ioctld-makedir.patch
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	libgsm-devel		>= 1.0.10
BuildRequires:	libaspell-devel		>= 0.60.4
BuildRequires:	libncurses-devel	>= 5.5
BuildRequires:	libjpeg-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
A client compatible with Gadu-Gadu.

Build options:
- Use pthread in resolver
- Compile shared version of libgadu
- Compile with aspell
- Compile with OpenSSL
- Compile with Python bindings
- Compile with zlib (compressed logs)
- Compile with libjpeg (token support)
- Compile with ioctld (voip)

%package -n %{libname}
Summary:	Libgadu shared library
Group:		System/Libraries

%description -n %{libname}
libgadu is intended to make it easy to add Gadu-Gadu
communication support to your software.

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.%{major}*

%package -n %{libname}-devel
Summary:	Libgadu development library
Group:		Development/C
Provides:	gadu-devel = %{version}-%{release}
Provides:	libgadu-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-devel
The libgadu-devel package contains the header files and some
documentation needed to develop application with libgadu.

%files -n %{libname}-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,api,ui,devel-hints,przenosny-kod}.txt docs/protocol.html docs/api/{functions,index,types,style}.*
%doc ChangeLog docs/{README,TODO} examples
%{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_includedir}/libgadu-config.h
%{_libdir}/pkgconfig/*.pc

%package -n %{libname}-static-devel
Summary:	Libgadu static library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
Libgadu static library.

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
%{_libdir}/libgadu.a

%prep
%setup -qn %{name}-%{prel}
%patch0 -p1 -b .%{name}-makefile-ioctld-makedir
rm -fr examples/CVS
./autogen.sh

%build

%configure2_5x \
	--disable-libgadu-openssl \
	--enable-dynamic \
	--enable-static \
	--enable-aspell \
	--enable-shared \
	--enable-ioctld \
	--with-pthread \
	--with-python \
	--with-libgsm

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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

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
%lang(pl) %{_mandir}/pl/man1/*


