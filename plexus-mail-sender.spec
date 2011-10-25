# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global namedversion 1.0-alpha-2

Name:           plexus-mail-sender
Version:        1.0
Release:        0.a2.18.1
Summary:        Plexus Mail Sender
License:        MIT and ASL 1.1
Group:          Development/Java
URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/tags/PLEXUS_MAIL_SENDER_1_0_ALPHA_2/
# Note: Exported revision 8188.
# mv PLEXUS_MAIL_SENDER_1_0_ALPHA_2/ plexus-mail-sender-1.0-a2
# tar czf plexus-mail-sender-1.0-a2-src.tar.gz plexus-mail-sender-1.0-a2
Source0:        plexus-mail-sender-%{version}-a2-src.tar.gz

Source1:        %{name}-mapdeps.xsl
Source2:        %{name}-jpp-depmap.xml
Source3:        maven2-settings.xml

# http://jira.codehaus.org/browse/PLX-417
# http://fisheye.codehaus.org/rdiff/plexus?csid=8336&u&N
Patch0:         %{name}-clarifylicense.patch

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  maven2 >= 0:2.0.4
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  dumbster
BuildRequires:  saxon
BuildRequires:  saxon-scripts
BuildRequires:  java-devel >= 0:1.6.0

Requires:       java
Requires:       jpackage-utils
Requires(post): jpackage-utils
Requires(postun):jpackage-utils

BuildArch:      noarch


%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.  This
Plexus component provides SMTP transport.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}-a2

%patch0 -p3
# fix groupIds of plexus to org.codehaus.plexus
# mainly to
find . -name release-pom.xml -exec \
     sed -i 's:<groupId>plexus</groupId>:<groupId>org.codehaus.plexus</groupId>:' \{\} \;

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -Dmaven2.jpp.depmap.file="%{SOURCE2}" \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
pushd plexus-mail-senders
for mod in javamail simple test;do
    pushd %{name}-$mod
    install -pm 644 target/%{name}-$mod-%{namedversion}-SNAPSHOT.jar \
            $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-$mod.jar
    install -pm 644 release-pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.plexus-mail-sender-$mod.pom
    %add_to_maven_depmap org.codehaus.plexus %{name}-$mod %{version} JPP/plexus mail-sender-$mod
    %add_to_maven_depmap plexus %{name}-$mod %{version} JPP/plexus mail-sender-$mod
    popd
done
popd

install -pm 644 \
  %{name}-api/target/%{name}-api-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-api.jar
install -pm 644 %{name}-api/release-pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.plexus-mail-sender-api.pom
%add_to_maven_depmap org.codehaus.plexus %{name}-api %{version} JPP/plexus mail-sender-api
%add_to_maven_depmap plexus %{name}-api %{version} JPP/plexus mail-sender-api


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*pom
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*

