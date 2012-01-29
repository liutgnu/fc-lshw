Summary:       Hardware lister
Name:          lshw
Version:       B.02.16
Release:       1%{?dist}
License:       GPLv2
Group:         Applications/System
URL:           http://ezix.org/project/wiki/HardwareLiSter
Source0:       http://www.ezix.org/software/files/lshw-%{version}.tar.gz
Source1:       lshw.desktop
Source2:       lshw.consolehelper
Source3:       lshw.pam
BuildRequires: sqlite-devel
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      hwdata

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
Requires: hwdata
Requires: %{name} = %{version}-%{release}
BuildRequires: gtk2-devel >= 2.4
BuildRequires: desktop-file-utils

%description gui
Graphical frontend for the hardware lister (lshw) tool.
If desired, hardware information can be saved to file in
plain, XML or HTML format.

%prep
%setup -q -n %{name}-%{version}

%build
%{__make} %{?_smp_mflags} SBINDIR="%{_sbindir}" RPM_OPT_FLAGS="%{optflags}" SQLITE=1 gui 

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
        SQLITE=1               \
        STRIP="/bin/true"      \
        INSTALL="%{__install} -p"

%{__make} install-gui          \
        DESTDIR="%{buildroot}" \
        PREFIX="%{_prefix}"    \
        SBINDIR="%{_sbindir}"  \
        MANDIR="%{_mandir}"    \
        SQLITE=1               \
        STRIP="/bin/true"      \
        INSTALL="%{__install} -p"

%{__ln_s} -f gtk-lshw %{buildroot}%{_sbindir}/lshw-gui

# don't package these copies, use the ones from hwdata instead
rm -f %{buildroot}%{_datadir}/%{name}/pci.ids
rm -f %{buildroot}%{_datadir}/%{name}/usb.ids
# don't package these copies, they're not actually used by the app,
# and even if they were, should use the hwdata versions
rm -f %{buildroot}%{_datadir}/%{name}/oui.txt
rm -f %{buildroot}%{_datadir}/%{name}/manuf.txt

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

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc COPYING README docs/*
%doc %{_mandir}/man1/lshw.1*
%{_sbindir}/%{name}

%files gui
%defattr(-, root, root, -)
%doc COPYING
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-gui
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}-gui
%{_bindir}/%{name}-gui
%{_sbindir}/gtk-%{name}
%{_sbindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}-logo.svg
%{_datadir}/applications/fedora-%{name}.desktop

%changelog
* Sun Jan 29 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-1
- B.02.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-3
- Own all dirs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-1
- B.02.15
- Remove patches now upstream
- Build with sqlite support

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-5
- Add patch to fix build with gcc-4.5

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-4
- Add patch to fix ext4 issue

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Adam Jackson <ajax@redhat.com> - B.02.14-2
- Requires: hwdata
- Drop redundant copies of pci.ids and friends, since we'll pick up the
  copies in hwdata at runtime

* Sun Mar  1 2009 Terje Rosten <terjeros@phys.ntnu.no> - B.02.14-1
- B.02.14
- Drop gcc43 patch now upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.13-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-3
- rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-2
- proper patch macro

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-1
- B.02.13
- remove patches now upstream
- add new gcc43 patch

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-5
- rebuild

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-4
- add patch to fix bz #442501

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

