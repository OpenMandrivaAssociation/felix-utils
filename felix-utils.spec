Name:		felix-utils
Version:	1.11.10
Release:	1
Summary:	Utility classes for OSGi
Group:		Development/Java
License:	ASL 2.0
URL:		https://felix.apache.org/
Source0:	https://repo1.maven.org/maven2/org/apache/felix/org.apache.felix.utils/%{version}/org.apache.felix.utils-%{version}-sources.jar
Patch0:		felix-utils-repository-1.1.patch

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.osgi:osgi.core)
BuildRequires:	mvn(org.osgi:org.osgi.service.repository)
BuildRequires:	mvn(org.osgi:org.osgi.util.promise)
BuildRequires:	mvn(org.osgi:org.osgi.service.cm)
BuildRequires:	mvn(org.osgi:org.osgi.namespace.service)
BuildRequires:	mvn(org.osgi:org.osgi.service.log)
BuildSystem:	maven
BuildOption(install):	--file-name org.apache.felix.utils --link %{name}
Obsoletes:	%{name}-javadoc < %{version}-%{release}

%description
Apache Felix Utils 1.11.10. The jar contains collection, manifest,
property, resource, and repository helpers, plus the configuration-admin
base class. Framework types come from OSGi Core 6. BaseRepository and
AggregateRepository implement the Repository 1.1 expression, combiner,
and requirement-builder methods on the existing capability index.
Configuration Admin and the service namespace are required. The Log
Service is optional and is used only when it is present. This build
targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
cp -p META-INF/LICENSE LICENSE
cp -p META-INF/NOTICE NOTICE
rm -rf META-INF
patch -p1 < %{PATCH0}
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path

java_files = list(Path("src/main/java").rglob("*.java"))
if len(java_files) != 38:
    raise SystemExit("java files " + str(len(java_files)))
base = Path("src/main/java/org/apache/felix/utils/repository/BaseRepository.java")
aggregate = Path("src/main/java/org/apache/felix/utils/repository/AggregateRepository.java")
support = Path("src/main/java/org/apache/felix/utils/repository/RepositorySupport.java")
for path in (base, aggregate, support):
    if not path.is_file():
        raise SystemExit("missing " + str(path))
for path in (base, aggregate):
    if "newRequirementBuilder" not in path.read_text(encoding="utf-8"):
        raise SystemExit("missing Repository 1.1 methods in " + path.name)
if "Apache License" not in Path("LICENSE").read_text(encoding="utf-8"):
    raise SystemExit("LICENSE is not the Apache license")
if "Apache Felix Utils" not in Path("NOTICE").read_text(encoding="utf-8"):
    raise SystemExit("NOTICE is not the Felix utils notice")
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.class")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.felix</groupId>
  <artifactId>org.apache.felix.utils</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>Apache Felix Utils</name>
  <description>Utility classes for OSGi.</description>
  <url>https://felix.apache.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>6.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.service.repository</artifactId>
      <version>1.1.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.util.promise</artifactId>
      <version>1.3.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.service.cm</artifactId>
      <version>1.6.1</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.namespace.service</artifactId>
      <version>1.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.service.log</artifactId>
      <version>1.5.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
poms = sorted(str(path) for path in Path(".").rglob("pom.xml"))
if poms != ["pom.xml"]:
    raise SystemExit("poms " + str(poms))
for needle in (
    "<artifactId>org.apache.felix.utils</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<version>6.0.0</version>",
    "<artifactId>org.osgi.service.repository</artifactId>",
    "<version>1.1.0</version>",
    "<artifactId>org.osgi.util.promise</artifactId>",
    "<version>1.3.0</version>",
    "<artifactId>org.osgi.service.cm</artifactId>",
    "<version>1.6.1</version>",
    "<artifactId>org.osgi.namespace.service</artifactId>",
    "<version>1.0.0</version>",
    "<artifactId>org.osgi.service.log</artifactId>",
    "<version>1.5.0</version>",
    "<scope>provided</scope>",
    "<version>%{version}</version>",
    "<release>8</release>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "SNAPSHOT", "<source>", "<target>", "<parent>", "maven-bundle-plugin", "mockito", "osgi.cmpn"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.apache.felix.utils-%{version}.jar --describe-module org.apache.felix.utils > module-describe.txt
grep -q '^org.apache.felix.utils' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }

%files -f .mfiles
%doc LICENSE NOTICE
