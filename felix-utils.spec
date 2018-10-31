%{?_javapackages_macros:%_javapackages_macros}
%global bundle org.apache.felix.utils

Name:             felix-utils
Version:          1.2.0
Release:          3.3
Summary:          Utility classes for OSGi
License:          ASL 2.0

URL:              http://felix.apache.org
Source0:          http://archive.apache.org/dist/felix/%{bundle}-%{version}-source-release.tar.gz

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    jpackage-utils
BuildRequires:    felix-osgi-compendium
BuildRequires:    felix-osgi-core
BuildRequires:    mvn(org.apache.felix:felix-parent:pom:)
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    mockito

Requires:         java

%description
Utility classes for OSGi

%package javadoc

Summary:          API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}

# Remove compiler plugin so default target of 1.5 is used
%pom_remove_plugin :maven-compiler-plugin
# Remove rat plugin that is not in Fedora
%pom_remove_plugin org.codehaus.mojo:rat-maven-plugin

%mvn_file :%{bundle} "felix/%{bundle}"

%build
# one of the tests fails in mock (local build is ok)
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Aug 05 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2.0-3
- Update for latest guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2.0-1
- Update to latest upstream version rhbz #892553.
- Drop patch, use preferred %%pom_* macros instead.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.0-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.1.0-7
- Changing target from jsr14 to 1.5 (#842593)

* Tue Sep  4 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.0-6
- Install NOTICE with javadoc pakcage

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Jaromir Capik <jcapik@redhat.com> - 1.1.0-3
- osgi.org groupId patch removed (fixed in felix-osgi-* packages)

* Thu Sep 08 2011 Jaromir Capik <jcapik@redhat.com> - 1.1.0-2
- Moved to felix subdir
- Minor spec file changes

* Wed Jul 13 2011 Jaromir Capik <jcapik@redhat.com> - 1.1.0-1
- Initial version
