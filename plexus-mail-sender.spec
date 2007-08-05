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

%define _with_gcj_support 1
%define gcj_support  %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section     free
%define repo_dir    m2_repo/repository
%define namedversion 1.0-alpha-2

Name:           plexus-mail-sender
Version:        1.0
Release:        %mkrel 0.a2.3.0.2
Epoch:          0
Summary:        Plexus Archiver Component
License:        Apache Software License
Group:          Development/Java
URL:            http://plexus.codehaus.org/
Source0:        plexus-mail-sender.tar.gz
# svn export http://svn.codehaus.org/plexus/tags/PLEXUS_MAIL_SENDER_1_0_ALPHA_2/

Source1:        %{name}-mapdeps.xsl
Source2:        %{name}-jpp-depmap.xml
Source3:        maven2-settings.xml

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  maven2 >= 0:2.0.4
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
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
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
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
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n plexus-mail-sender
%{__perl} -pi -e 's|Security\.addProvider|//Security\.addProvider|' plexus-mail-senders/plexus-mail-sender-javamail/src/main/java/org/codehaus/plexus/mailsender/javamail/JavamailMailSender.java

%build
cp %{SOURCE3} maven2-settings.xml

sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/m2_repo/repository</url>|g" maven2-settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" maven2-settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/m2_repo/repository</url>|g" maven2-settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" maven2-settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" maven2-settings.xml

for p in $(find . -name "*.pom"); do
    pushd $(dirname $p)
    bp=`basename $p`
    cp $bp $bp.orig
    /usr/bin/saxon -o $bp $bp.orig %{SOURCE1} map=%{SOURCE2}
    popd
done

for p in $(find . -name "*pom.xml"); do
    pushd $(dirname $p)
    bp=`basename $p`
    cp $bp $bp.orig
    /usr/bin/saxon -o $bp $bp.orig %{SOURCE1} map=%{SOURCE2}
    popd
done

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

MVN=/usr/bin/mvn
export M2SETTINGS=$(pwd)/maven2-settings.xml
export MAVEN_REPO_LOCAL=`pwd`/%{repo_dir}
export MAVEN_OPTS="-Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven2.jpp.mode=true -Dmaven.test.failure.ignore=true"
${MVN} -s ${M2SETTINGS} ${MAVEN_OPTS} install javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 plexus-mail-senders/plexus-mail-sender-javamail/target/%{name}-javamail-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-javamail-%{version}.jar
install -pm 644 plexus-mail-senders/plexus-mail-sender-simple/target/%{name}-simple-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-simple-%{version}.jar
install -pm 644 plexus-mail-senders/plexus-mail-sender-test/target/%{name}-test-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-test-%{version}.jar
install -pm 644 plexus-mail-sender-api/target/%{name}-api-%{namedversion}-SNAPSHOT.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/mail-sender-api-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/plexus && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
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
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/mail-sender-*-%{version}.jar.*
%endif


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
