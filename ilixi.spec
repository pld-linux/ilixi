# TODO:
# - reflex
# - baresip_dale.h for SIP?
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	fusiondale	# FusionDale support
%bcond_without	fusionsound	# FusionSound support
%bcond_with	reflex		# Reflex support [experimantal, BR: libReflex]
%bcond_without	sawman		# (SaWMan based) compositor and application manager features
%bcond_with	wnn		# Wnn support [experimental]
#
Summary:	Lightweight C++ user interface toolkit for embedded Linux systems
Summary(pl.UTF-8):	Lekki toolkit C++ interfejsu użytkownika dla linuksowych systemów wbudowanych
Name:		ilixi
Version:	1.0.0
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.directfb.org/downloads/Libs/%{name}-%{version}.tar.gz
# Source0-md5:	c1cf8c2b0e31870df2970ff2f4a42de2
Patch0:		%{name}-link.patch
URL:		http://www.ilixi.org/
BuildRequires:	DirectFB-devel >= 1:1.6.3
%{?with_wnn:BuildRequires:	FreeWnn-devel}
%{?with_fusiondale:BuildRequires:	FusionDale-devel >= 0.8.2}
%{?with_fusionsound:BuildRequires:	FusionSound-devel >= 1.6.0}
%{?with_sawman:BuildRequires:	SaWMan-devel >= 1.6.0}
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	fontconfig-devel >= 1:2.6.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libsigc++-devel >= 2.2.4.2
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.7.7
BuildRequires:	pkgconfig
Requires:	DirectFB >= 1:1.6.3
%{?with_fusiondale:Requires:	FusionDale >= 0.8.2}
%{?with_fusionsound:Requires:	FusionSound >= 1.6.0}
%{?with_sawman:Requires:	SaWMan >= 1.6.0}
Requires:	fontconfig-libs >= 1:2.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ilixi is an open-source lightweight GUI framework and it is designed
with Linux based embedded devices in mind. ilixi uses DirectFB at its
core in order to render all graphics content to a Linux framebuffer
device. This eliminates the need for X server.

%description -l pl.UTF-8
ilixi to mający otwarte źródła lekki szkielet GUI, zaprojektowany z
myślą o urządzeniach z wbudowanym Linuksem. ilixi wykorzystuje
DirectFB w celu rysowania grafiki na linuksowym framebufferze, co
eliminuje potrzebę serwera X.

%package devel
Summary:	Header files for ilixi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ilixi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	DirectFB-devel >= 1:1.6.3
%{?with_wnn:Requires:	FreeWnn-devel}
%{?with_fusiondale:Requires:	FusionDale-devel >= 0.8.2}
%{?with_fusionsound:Requires:	FusionSound-devel >= 1.6.0}
%{?with_sawman:Requires:	SaWMan-devel >= 1.6.0}
Requires:	fontconfig-devel >= 1:2.6.0
Requires:	libsigc++-devel >= 2.2.4.2
Requires:	libstdc++-devel
Requires:	libxml2-devel >= 1:2.7.7

%description devel
Header files for ilixi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ilixi.

%package static
Summary:	Static ilixi library
Summary(pl.UTF-8):	Statyczna biblioteka ilixi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ilixi library.

%description static -l pl.UTF-8
Statyczna biblioteka ilixi.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I config/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_fusiondale:--enable-fusiondale} \
	%{?with_fusionsound:--enable-fusionsound} \
	--enable-nls \
	%{?with_reflex:--enable-reflex} \
	%{?with_sawman:--enable-sawman} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{?with_wnn:--enable-wnn}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/*.cpp $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ilixi_*
%attr(755,root,root) %{_libdir}/libilixi-1.0.0-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libilixi-1.0.0-1.0.so.0
%{_datadir}/ilixi-1.0.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libilixi-1.0.0.so
%{_libdir}/libilixi-1.0.0.la
%{_includedir}/ilixi-1.0.0
%{_pkgconfigdir}/ilixi.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libilixi-1.0.0.a
%endif
