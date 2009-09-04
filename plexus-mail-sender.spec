# Copyright (c) 2000-2008, JPackage Project
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

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section     free
%define repo_dir    m2_repo/repository
%define namedversion 1.0-alpha-2
%define parent plexus
%define subname mail-sender

Name:           plexus-mail-sender
Version:        1.0
Release:        %mkrel 0.a2.4.0.2
Epoch:          0
Summary:        Plexus Mail Sender Component
License:        Apache Software License
Group:          Development/Java
URL:            http://plexus.codehaus.org/
Source0:        plexus-mail-sender.tar.gz
# svn export http://svn.codehaus.org/plexus/tags/PLEXUS_MAIL_SENDER_1_0_ALPHA_2/

Source1:        %{name}-autogenerated-files.tar.gz
Source2:        %{name}-jpp-depmap.xml
Source3:        maven2-settings.xml

BuildRequires:  java-rpmbuild >= 0:1.6
%if %{with_maven}
BuildRequires:  maven2 >= 0:2.0.4
BuildRequires:  maven2-plugin-ant
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-plugin-resources
%endif
BuildRequires:  ant
BuildRequires:  saxon
BuildRequires:  saxon-scripts
BuildRequires:  dumbster
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  plexus-container-default 
BuildRequires:  plexus-utils 
Requires:  classworlds >= 0:1.1
Requires:  plexus-container-default 
Requires:  plexus-utils 
%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n plexus-mail-sender
gzip -dc %{SOURCE1} | tar xf -
cp %{SOURCE3} maven2-settings.xml
sed -i -e "s|haltonerror=\"true\"|haltonerror=\"false\"|g" plexus-mail-senders/plexus-mail-sender-javamail/build.xml
sed -i -e "s|haltonfailure=\"true\"|haltonfailure=\"false\"|g" plexus-mail-senders/plexus-mail-sender-javamail/build.xml

%build
export JAVA_HOME=%{_jvmdir}/java-rpmbuild
%if %{with_maven}
sed -i -e "s|<url>__INTERNAL_REPO_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" maven2-settings.xml
sed -i -e "s|<url>__EXTERNAL_REPO_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" maven2-settings.xml

export MAVEN_REPO_LOCAL=`pwd`/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
    -e \
    -s $(pwd)/maven2-settings.xml \
    -Dmaven2.jpp.depmap.file=%{SOURCE2} \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    -Dmaven.test.skip=true \
    ant:ant install javadoc:javadoc

%else
export CLASSPATH=$(build-classpath \
classworlds \
dumbster \
jaf \
javamail \
plexus/container-default \
plexus/utils \
)
CLASSPATH=$CLASSPATH:$(pwd)/plexus-mail-sender-api/target/plexus-mail-sender-api-1.0-alpha-2-SNAPSHOT.jar 
CLASSPATH=$CLASSPATH:$(pwd)/plexus-mail-senders/plexus-mail-sender-test/target/plexus-mail-sender-test-1.0-alpha-2-SNAPSHOT.jar 
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd plexus-mail-sender-api
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-mail-senders/plexus-mail-sender-test
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-mail-senders/plexus-mail-sender-simple
%ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-mail-senders/plexus-mail-sender-javamail
%ant -Dbuild.sysclasspath=only jar javadoc
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 plexus-mail-senders/plexus-mail-sender-javamail/target/%{name}-javamail-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-javamail-%{version}.jar
install -pm 644 plexus-mail-senders/plexus-mail-sender-simple/target/%{name}-simple-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-simple-%{version}.jar
install -pm 644 plexus-mail-senders/plexus-mail-sender-test/target/%{name}-test-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-test-%{version}.jar
install -pm 644 plexus-mail-sender-api/target/%{name}-api-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-api-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/plexus && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# poms and depmap frags
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}
%add_to_maven_depmap plexus %{name} %{version} JPP/%{parent} %{subname}
install -pm 644 plexus-mail-sender-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-api.pom
%add_to_maven_depmap org.codehaus.plexus %{name}-api %{version} JPP/%{parent} %{subname}-api
%add_to_maven_depmap plexus %{name}-api %{version} JPP/%{parent} %{subname}-api
install -pm 644 plexus-mail-senders/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}s.pom
%add_to_maven_depmap org.codehaus.plexus %{name}s %{version} JPP/%{parent} %{subname}s
%add_to_maven_depmap plexus %{name}s %{version} JPP/%{parent} %{subname}s
install -pm 644 plexus-mail-senders/plexus-mail-sender-javamail/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-javamail.pom
%add_to_maven_depmap org.codehaus.plexus %{name}-javamail %{version} JPP/%{parent} %{subname}-javamail
%add_to_maven_depmap plexus %{name}-javamail %{version} JPP/%{parent} %{subname}-javamail
install -pm 644 plexus-mail-senders/plexus-mail-sender-simple/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-simple.pom
%add_to_maven_depmap org.codehaus.plexus %{name}-simple %{version} JPP/%{parent} %{subname}-simple
%add_to_maven_depmap plexus %{name}-simple %{version} JPP/%{parent} %{subname}-simple
install -pm 644 plexus-mail-senders/plexus-mail-sender-test/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}-test.pom
%add_to_maven_depmap org.codehaus.plexus %{name}-test %{version} JPP/%{parent} %{subname}-test
%add_to_maven_depmap plexus %{name}-test %{version} JPP/%{parent} %{subname}-test

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
cp -pr plexus-mail-sender-api/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
cp -pr plexus-mail-senders/plexus-mail-sender-test/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/simple
cp -pr plexus-mail-senders/plexus-mail-sender-simple/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/simple
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/javamail
cp -pr plexus-mail-senders/plexus-mail-sender-javamail/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/javamail
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
