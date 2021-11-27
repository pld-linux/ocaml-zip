#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Zlib binding for OCaml
Summary(pl.UTF-8):	Wiązania Zlib dla OCamla
Name:		ocaml-zip
Version:	1.11
%define	gitver	rel111
Release:	1
License:	LGPL v2.1 with OCaml linking exception
Group:		Libraries
#Source0Download: https://github.com/xavierleroy/camlzip/tags
Source0:	https://github.com/xavierleroy/camlzip/archive/%{gitver}.tar.gz?/camlzip-%{gitver}.tar.gz
# Source0-md5:	ee7a2ecf4801226003ba2cd1b1f11d4d
URL:		https://xavierleroy.org/software.html
BuildRequires:	ocaml >= 1:4.07
BuildRequires:	ocaml-findlib
BuildRequires:	zlib-devel >= 1.1.3
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
%{__cc} %{rpmcflags} %{rpmcppflags} -fPIC -c zlibstubs.c

%{__make} allbyt %{?with_ocaml_opt:allopt}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

# useless in rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so.owner

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr test/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcamlzip.so
%if %{with ocaml_opt}
%{_libdir}/ocaml/zip/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/camlzip
%{_libdir}/ocaml/camlzip/META
%dir %{_libdir}/ocaml/zip
%{_libdir}/ocaml/zip/META
%{_libdir}/ocaml/zip/*.cma
%{_libdir}/ocaml/zip/*.cmi
%{_libdir}/ocaml/zip/*.cmt
%{_libdir}/ocaml/zip/*.cmti
%{_libdir}/ocaml/zip/*.mli
%{_libdir}/ocaml/zip/libcamlzip.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/zip/*.cmx
%{_libdir}/ocaml/zip/*.cmxa
%{_libdir}/ocaml/zip/zip.a
%endif
%{_examplesdir}/%{name}-%{version}
