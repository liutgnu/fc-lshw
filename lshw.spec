Summary: Hardware lister
Name:    lshw
Version: B.02.12.01
Release: 3%{?dist}
License: GPLv2
Group:   Applications/System
URL:     http://ezix.org/project/wiki/HardwareLiSter
Source0: http://www.ezix.org/software/files/%{name}-%{version}.tar.gz
Source1: lshw.desktop
Source2: lshw.consolehelper
Source3: lshw.pam
Patch0:  lshw-B.02.12.01-gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory configuration,
firmware version, mainboard configuration, CPU version and speed, cache
configuration, bus speed, etc. on DMI-capable x86 systems and on some
PowerPC machines (PowerMac G4 is known to work).

Information can be output in plain text, XML or HTML.

%package gui
Summary:  Graphical hardware lister
Group:    Applications/System
Requires: usermode
Requires: %{name} = %{version}-%{release}
BuildRequires: gtk2-devel >= 2.4
BuildRequires: desktop-file-utils

%description gui
Graphical frontend for the hardware lister (lshw) tool.
If desired, hardware information can be saved to file in
plain, XML or HTML format.

%prep
%setup -q -n %{name}-%{version}
%patch -p1

%{__sed} -i 's|-g -Wall -g|%{optflags}|' src/Makefile
%{__sed} -i 's|-g -Wall -Os|%{optflags}|' src/core/Makefile
%{__sed} -i 's|-g -Wall -Os|%{optflags}|' src/gui/Makefile
%{__sed} -i 's|LDFLAGS= -Os -s|LDFLAGS=|' src/gui/Makefile

%build
%{__make} %{?_smp_mflags} SBINDIR="%{_sbindir}" gui 

# Replace copyrighted icons
pushd src
%{__make} nologo

%install
%{__rm} -rf %{buildroot}
%{__make} install              \
        DESTDIR="%{buildroot}" \
        PREFIX="%{_prefix}"    \
        SBINDIR="%{_sbindir}"  \
        MANDIR="%{_mandir}"    \
        INSTALL="%{__install} -p"

%{__make} install-gui          \
        DESTDIR="%{buildroot}" \
        PREFIX="%{_prefix}"    \
        SBINDIR="%{_sbindir}"  \
        MANDIR="%{_mandir}"    \
        INSTALL="%{__install} -p"

%{__ln_s} -f gtk-lshw %{buildroot}%{_sbindir}/lshw-gui

# desktop icon
%{__install} -D -m 0644 -p ./src/gui/artwork/logo.svg \
     %{buildroot}%{_datadir}/pixmaps/%{name}-logo.svg

desktop-file-install --vendor fedora  \
  --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

# consolehelper
%{__install} -d %{buildroot}%{_bindir}
%{__ln_s} -f consolehelper %{buildroot}%{_bindir}/%{name}-gui
%{__install} -D -m 0644 %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-gui
%{__install} -D -m 0644 %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/pam.d/%{name}-gui

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING README docs/*
%doc %{_mandir}/man1/lshw.1*
%{_sbindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/*.ids

%files gui
%defattr(-, root, root, -)
%doc COPYING
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-gui
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}-gui
%{_bindir}/%{name}-gui
%{_sbindir}/gtk-%{name}
%{_sbindir}/%{name}-gui
%{_datadir}/%{name}/artwork
%{_datadir}/pixmaps/%{name}-logo.svg
%{_datadir}/applications/fedora-%{name}.desktop

%changelog
* Mon Feb 11 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-3
- add patch to build with gcc-4.3

* Mon Feb  9 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-2
- rebuild

* Mon Nov  5 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-1
- B.02.12.01
- Replace trademark icons

* Tue Aug 14 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-3
- Move desktop and pam config to files
- Simplify build

* Tue Aug 07 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-2
- Remove trademarks

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-1
- B.02.11.01

* Sun Aug 05 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-3
- Move artwork to gui subpackage
- Implement consolehelper support

* Sat Aug 04 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-2
- License is GPLv2 (only)
- Fix ui %%description

* Wed Aug 01 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-1
- Follow upstream version scheme

* Wed Jul 25 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.11-1
- 2.11

* Wed Jun 27 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.10-2
- minor fixes
- add patch to avoid stripping
- add desktop file
- strip changelog
- move from sbin to bin
- new url

* Wed Feb 14 2007 Dag Wieers <dag@wieers.com> - 2.10-1 - 4876+/dag
- Updated to release B.02.10.

* Tue Dec 21 2004 Dag Wieers <dag@wieers.com> - 2.0-1
- Initial package. (using DAR)
