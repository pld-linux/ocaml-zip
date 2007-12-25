%define		ocaml_ver	1:3.09.2
Summary:	Zlib binding for OCaml
Summary(pl.UTF-8):	Wiązania Zlib dla OCamla
Name:		ocaml-zip
Version:	1.03
Release:	1
License:	LGPL
Group:		Libraries
URL:		http://pauillac.inria.fr/~xleroy/software.html
Source0:	http://caml.inria.fr/distrib/bazar-ocaml/camlzip-%{version}.tar.gz
# Source0-md5:	65cee9abf1df6544cae554b94128d441
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	zlib-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Objective Caml library provides easy access to compressed files
in ZIP and GZIP format, as well as to Java JAR files. It provides
functions for reading from and writing to compressed files in these
formats.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Biblioteka ta pozwala na dostęp do plików w formacie ZIP i GZIP jak
również dla plików JAR Javy z poziomy OCamla. Udostępnia ona funkcje
do czytania i pisania do plików w tych formatach.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	Zlib binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania Zlib dla OCamla - cześć programistyczna
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

%description devel -l pl.UTF-8
Biblioteka ta pozwala na dostęp do plików w formacie ZIP i GZIP jak
również dla plików JAR Javy z poziomy OCamla. Udostępnia ona funkcje
do czytania i pisania do plików w tych formatach.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n camlzip-%{version}

%build
%{__cc} %{rpmcflags} -fPIC -c zlibstubs.c
%{__make} all allopt OCAMLC=ocamlc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

%{__make} install installopt \
	INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/zip \
	OCAMLC="echo $RPM_BUILD_ROOT; true"

mv $RPM_BUILD_ROOT%{_libdir}/ocaml/zip/dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc README *.mli
%dir %{_libdir}/ocaml/zip
%{_libdir}/ocaml/zip/*.cm[ixa]*
%{_libdir}/ocaml/zip/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/zip
