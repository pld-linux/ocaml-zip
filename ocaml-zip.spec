Summary:	Zlib binding for OCaml
Summary(pl):	Wi�zania Zlib dla OCamla
Name:		ocaml-zip
Version:	1.01
Release:	1
License:	LGPL
Group:		Libraries
Vendor:		Xavier Leroy <Xavier.Leroy@inria.fr>
URL:		http://pauillac.inria.fr/~xleroy/software.html
Source0:	http://caml.inria.fr/distrib/bazar-ocaml/camlzip-%{version}.tar.gz
BuildRequires:	zlib-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Objective Caml library provides easy access to compressed files
in ZIP and GZIP format, as well as to Java JAR files. It provides
functions for reading from and writing to compressed files in these
formats.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
Biblioteka ta pozwala na dost�p do plik�w w formacie ZIP i GZIP jak
r�wnie� dla plik�w JAR Javy z poziomy OCamla. Udost�pnia ona funkcje
do czytania i pisania do plik�w w tych formatach.

Pakiet ten zawiera binaria potrzebne do uruchamiania program�w
u�ywaj�cych tej biblioteki.

%package devel
Summary:	Zlib binding for OCaml - development part
Summary(pl):	Wi�zania Zlib dla OCamla - cze�� programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This Objective Caml library provides easy access to compressed files
in ZIP and GZIP format, as well as to Java JAR files. It provides
functions for reading from and writing to compressed files in these
formats.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Biblioteka ta pozwala na dost�p do plik�w w formacie ZIP i GZIP jak
r�wnie� dla plik�w JAR Javy z poziomy OCamla. Udost�pnia ona funkcje
do czytania i pisania do plik�w w tych formatach.

Pakiet ten zawiera pliki niezb�dne do tworzenia program�w u�ywaj�cych
tej biblioteki.

%prep
%setup -q -n camlzip-%{version}

%build
%{__cc} %{rpmcflags} -fPIC -c zlibstubs.c
%{__make} all allopt OCAMLC=ocamlc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install installopt \
	INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/zip \
	OCAMLC="echo $RPM_BUILD_ROOT; true"

(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s zip/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r test/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/zip
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/zip/META <<EOF
requires = ""
version = "%{version}"
directory = "+zip"
archive(byte) = "zip.cma"
archive(native) = "zip.cmxa"
linkopts = ""
EOF

gzip -9nf README *.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/zip
%attr(755,root,root) %{_libdir}/ocaml/zip/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc *.gz
%{_libdir}/ocaml/zip/*.cm[ixa]*
%{_libdir}/ocaml/zip/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/zip