Summary:       Hardware lister
Name:          lshw
Version:       B.02.18
Release:       12%{?dist}
License:       GPLv2
Group:         Applications/System
URL:           http://ezix.org/project/wiki/HardwareLiSter
Source0:       http://www.ezix.org/software/files/lshw-%{version}.tar.gz
Source1:       lshw-gui.desktop
Source2:       org.ezix.lshw.gui.policy
Source3:       lshw-gui
Source4:       lshw-gui.appdata.xml
Patch1:        lshw-B.02.18-scandir.patch
Patch2:        lshw-B.02.18-d05baa7.patch
BuildRequires: gtk2-devel >= 2.4
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
Requires:      hwdata
%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory
configuration, firmware version, mainboard configuration, CPU version
and speed, cache configuration, bus speed, etc. on DMI-capable x86
systems and on some PowerPC machines (PowerMac G4 is known to work).

Information can be output in plain text, XML or HTML.

%package       gui
Summary:       Graphical hardware lister
Group:         Applications/System
Requires:      polkit
Requires:      %{name} = %{version}-%{release}
%description   gui
Graphical frontend for the hardware lister (lshw) tool. If desired,
hardware information can be saved to file in plain, XML or HTML
format.

%prep
%setup -q
%patch01 -p1
%patch02 -p1

%build
make %{?_smp_mflags} SBINDIR="%{_sbindir}" RPM_OPT_FLAGS="%{optflags}" gui

# Replace copyrighted icons
pushd src
make nologo

%install
make install                   \
        DESTDIR="%{buildroot}" \
        PREFIX="%{_prefix}"    \
        SBINDIR="%{_sbindir}"  \
        MANDIR="%{_mandir}"    \
        STRIP="/bin/true"      \
        INSTALL="install -p"

make install-gui               \
        DESTDIR="%{buildroot}" \
        PREFIX="%{_prefix}"    \
        SBINDIR="%{_sbindir}"  \
        MANDIR="%{_mandir}"    \
        STRIP="/bin/true"      \
        INSTALL="install -p"

mv %{buildroot}%{_sbindir}/gtk-lshw %{buildroot}%{_sbindir}/lshw-gui
ln -s -f lshw-gui %{buildroot}%{_sbindir}/gtk-lshw

# don't package these copies, use the ones from hwdata instead
rm -f %{buildroot}%{_datadir}/%{name}/pci.ids
rm -f %{buildroot}%{_datadir}/%{name}/usb.ids
# don't package these copies, they're not actually used by the app,
# and even if they were, should use the hwdata versions
rm -f %{buildroot}%{_datadir}/%{name}/oui.txt
rm -f %{buildroot}%{_datadir}/%{name}/manuf.txt

# desktop icon
install -D -m 0644 -p ./src/gui/artwork/logo.svg \
     %{buildroot}%{_datadir}/pixmaps/%{name}-gui.svg
install -D -m 0644 -p ./src/gui/artwork/logo.svg \
     %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-gui.svg
desktop-file-install %{?vendortag:--vendor fedora} \
  --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

# PolicyKit
install -D -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/polkit-1/actions/org.ezix.lshw.gui.policy
install -D -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/lshw-gui

# AppData
install -D -m 0644 %{SOURCE4} \
    %{buildroot}%{_datadir}/appdata/lshw-gui.appdata.xml

# translations seems borken, remove for now
#find_lang %{name}
rm -rf %{buildroot}%{_datadir}/locale/fr/

%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

#files -f %{name}.lang
%files
%license COPYING
%doc README.md
%{_mandir}/man1/lshw.1*
%{_sbindir}/%{name}

%files gui
%license COPYING
%{_bindir}/%{name}-gui
%{_sbindir}/gtk-%{name}
%{_sbindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}-gui.svg
%{_datadir}/icons/hicolor/scalable/apps/%{name}-gui.svg
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/appdata/%{name}-gui.appdata.xml
%{_datadir}/polkit-1/actions/org.ezix.lshw.gui.policy

%changelog
* Fri Jan 26 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-12
- Update to commit d05baa7

* Mon Aug 28 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-11
- Prefer lshw-gui in lshw-gui context

* Sun Aug 13 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-10
- Add AppData bz#1476498

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 24 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-5
- Modify lshw gui wrapper to fix bz#1368404

* Thu Aug 11 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-4
- Add patches to fix sysconf/long_bit issue and crash (bz#1342792)

* Wed May 18 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-3
- Add patch to fix crash (bz#1332486)

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-2
- Date fix

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-1
- B.02.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - B.02.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - B.02.17-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-2
- Add patch to fix segfault in scan fat code

* Thu Sep 26 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-1
- B.02.17

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-8
- Rename macro

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-7
- Fix desktop file (bz #953684)
- Remove broken translations (bz #905896)
- Add vendor macro
 
* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - B.02.16-6
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-3
- Switch from consolehelper to PolicyKit (bz #502730)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-2
- Rebuilt for c++ ABI breakage

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

* Sat Feb 09 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-2
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

