%define lib   lib010
Summary:      ZZipLib - libZ-based ZIP-access Library
Name:         zziplib
Version:      0.13.49
Release:      1
License:      LGPL
Group:        Development/Libraries
URL:          http://zziplib.sf.net
Vendor:       Guido Draheim <guidod@gmx.de>
Source0:      http://prdownloads.sf.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:    /var/tmp/%{name}-%{version}-%{release}

Distribution: Original
Packager:     Guido Draheim <guidod@gmx.de>
Requires:      zlib
BuildRequires: zlib-devel
BuildRequires: SDL-devel

#Begin3
# Author1:        too@iki.fi (Tomi Ollila)
# Author2:        guidod@gmx.de (Guido Draheim)
# Maintained-by:  guidod@gmx.de (Guido Draheim)
# Primary-Site:   zziplib.sf.net
# Keywords:       zip zlib inflate archive gamedata
# Platforms:      zlib posix
# Copying-Policy: Lesser GPL Version 2
#End

%package %lib
Summary:      ZZipLib - Documentation Files
Group:        Development/Libraries
Provides:     zziplib
Provides:     libzzip0
Provides:     libzzip-0.so.10

%package doc
Summary:      ZZipLib - Documentation Files
Group:        Development/Libraries

%package devel
Summary:      ZZipLib - Development Files
Group:        Development/Libraries
Requires:     zziplib-%lib = %version
# Requires: pkgconfig (not yet)

%description
 : zziplib provides read access to zipped files in a zip-archive,
 : using compression based solely on free algorithms provided by zlib.

%description %lib
 : zziplib provides read access to zipped files in a zip-archive,
 : using compression based solely on free algorithms provided by zlib.
 zziplib provides an additional API to transparently access files
 being either real files or zipped files with the same filepath argument.
 This is handy to package many files being shared data into a single
 zip file - as it is sometimes used with gamedata or script repositories.
 The library itself is fully multithreaded, and it is namespace clean
 using the zzip_ prefix for its exports and declarations.
 
%description doc
 : zziplib provides read access to zipped files in a zip-archive,
 : using compression based solely on free algorithms provided by zlib.
 these are the (html) docs, mostly generated actually.

%description devel
 : zziplib provides read access to zipped files in a zip-archive,
 : using compression based solely on free algorithms provided by zlib.
 these are the header files needed to develop programs using zziplib.
 there are test binaries to hint usage of the library in user programs.

%prep
#'
%setup
# fixing relink problems during install too
LDFLAGS="-L%buildroot%_libdir" \
CFLAGS="$RPM_OPT_FLAGS" \
sh configure --prefix=%{_prefix} --with-docdir=%{_docdir} --mandir=%{_mandir} \
             --enable-sdl  TIMEOUT=9
make zzip64-setup

%build
make 
make zzip64-build
make doc

%install
rm -rf %{buildroot}
make zzip64-install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
make zzip32-postinstall DESTDIR=%{buildroot}
make zzip-postinstall
make install-doc DESTDIR=%{buildroot}
make install-mans DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files %lib
      %defattr(-,root,root)
      %{_libdir}/lib*.so.*

%post %lib 
/sbin/ldconfig || true
%postun %lib
/sbin/ldconfig || true

%files doc
      %defattr(-,root,root)
      %{_datadir}/doc/*
%dir  %{_datadir}/omf/%{name}
      %{_datadir}/omf/%{name}/*
%post doc
test ! -f %_bindir/scrollkeeper-update || %_bindir/scrollkeeper-update
%postun doc
test ! -f %_bindir/scrollkeeper-update || %_bindir/scrollkeeper-update

%files devel
      %defattr(-,root,root)
      %{_bindir}/*
%dir  %{_includedir}/zzip
      %{_includedir}/zzip/*
      %{_includedir}/*.h
      %{_libdir}/lib*.so
      %{_libdir}/lib*.a
      %{_libdir}/lib*.la
      %{_libdir}/pkgconfig/*
%dir  %{_datadir}/%{name}
      %{_datadir}/%{name}/*
      %{_datadir}/aclocal/%{name}*.m4
      %{_mandir}/man3/*	
