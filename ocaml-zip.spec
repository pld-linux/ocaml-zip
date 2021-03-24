#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Zlib binding for OCaml
Summary(pl.UTF-8):	Wiązania Zlib dla OCamla
Name:		ocaml-zip
Version:	1.07
%define	gitver	rel107
Release:	2
License:	LGPL
Group:		Libraries
URL:		http://pauillac.inria.fr/~xleroy/software.html
Source0:	https://github.com/xavierleroy/camlzip/archive/%{gitver}/camlzip-%{version}.tar.gz
# Source0-md5:	8babccb584dfd4eb7b98901122e818a9
BuildRequires:	ocaml >= 1:3.09.2
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
%setup -q -n camlzip-%{gitver}

%build
%{__cc} %{rpmcflags} -fPIC -c zlibstubs.c
%{__make} all %{?with_ocaml_opt:allopt} \
	OCAMLC=ocamlc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

%{__make} install %{?with_ocaml_opt:installopt} \
	INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/zip \
	OCAMLC="echo $RPM_BUILD_ROOT; true"

install zlib.cm[ixa]* $RPM_BUILD_ROOT%{_libdir}/ocaml/zip

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
%if %{with ocaml_opt}
%{_libdir}/ocaml/zip/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc README *.mli
%dir %{_libdir}/ocaml/zip
%{_libdir}/ocaml/zip/*.cma
%{_libdir}/ocaml/zip/*.cm[ix]
%{_libdir}/ocaml/zip/*.mli
%{_libdir}/ocaml/zip/libcamlzip.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/zip/*.cmxa
%{_libdir}/ocaml/zip/zip.a
%endif
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/zip
