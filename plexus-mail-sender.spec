%{?_javapackages_macros:%_javapackages_macros}
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
Release:        0.a2.28.0.1
Epoch:          0
Summary:        Plexus Mail Sender
Group:          Development/Java
License:        MIT and ASL 1.1

URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/tags/PLEXUS_MAIL_SENDER_1_0_ALPHA_2/
# Note: Exported revision 8188.
# mv PLEXUS_MAIL_SENDER_1_0_ALPHA_2/ plexus-mail-sender-1.0-a2
# tar czf plexus-mail-sender-1.0-a2-src.tar.gz plexus-mail-sender-1.0-a2
Source0:        plexus-mail-sender-%{version}-a2-src.tar.gz

# http://jira.codehaus.org/browse/PLX-417
# http://fisheye.codehaus.org/rdiff/plexus?csid=8336&u&N
Patch0:         %{name}-clarifylicense.patch

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  saxon
BuildRequires:  saxon-scripts
BuildRequires:  java-devel >= 1:1.6.0


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


%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{name}-%{version}-a2
%patch0 -p3

mv release-pom.xml pom.xml

pushd plexus-mail-senders
mv release-pom.xml pom.xml
%pom_disable_module plexus-mail-sender-test
for mod in javamail simple test;do
    pushd %{name}-$mod
    mv release-pom.xml pom.xml
    popd
done
popd

mv %{name}-api/release-pom.xml %{name}-api/pom.xml
find . -iname 'pom.xml' -exec sed -i \
       's:<groupId>plexus</groupId>:<groupId>org.codehaus.plexus</groupId>:g' \{\} \;


%build
%mvn_package ":*senders" __noinstall
%mvn_build -f

%install
%mvn_install
%if 0%{?fedora}
%else
sed -i "s|1.0-alpha-2-SNAPSHOT|1.0.alpha.2.SNAPSHOT|" %{buildroot}%{_datadir}/maven-metadata/*
%endif

%files -f .mfiles

%files javadoc -f .mfiles-javadoc


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.24.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.a2.24
- Fix release tag

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-0.a2.24
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 24 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.a2.23
- Build with xmvn
- Fixed pom_ macro

* Thu Oct 11 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.22
- Do not build test submodule to simplify dependencies

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.21.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar  2 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 0:1.0-0.a2.21
- Fix build and install proper pom files

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.20
- Fix up according to latest guidelines

* Sun Jun 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.19
- Build with maven 3.x

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.18.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.18
- Add update_maven_depmap execution to post/postun (#669495)

* Thu Dec 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.17
- Add maven metadata

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.16
- Fix FTBFS.
- Adapt to current guidelines.

* Wed Sep  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.15
- Add maven-site-plugin to BR
- Update maven-plugin BR names

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.14
- Remove dummy things from the depmap.
- Remove workaround for old javadoc plugin.

* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.13
- BR maven-doxia-sitetools.

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.12
- Force OpenJDK

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.11
- Add BRs on maven2-plugin-{compiler,surefire,jar,install.javadoc}

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.10
- Add BR on maven2-plugin-resources

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.9
- Remove gcj support
- Remove javadoc post scriplet
- Add patch to clarify license (http://jira.codehaus.org/browse/PLX-417)
- Fix license
- Use tarball with versioned directory

* Sun May 17 2009 Fernando Nasser <fnasser@redhat.com> - 0:1.0-0.a2.8
- Fix license

* Tue Apr 30 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.7
- Don't run the tests as they reqyuire access to the net
- Add BRs maven-doxia*
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Tue Mar 17 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.6
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Thu Feb 05 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.5
- Fix release tag

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.4jpp
- Import from dbhole's maven packages, initial building

* Tue May 15 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.3jpp
- Make Vendor, Distribution based on macro

* Thu Mar 15 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.2jpp
- Add dumbster BR

* Wed Sep 13 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.1jpp
- First JPP-1.7 release
- Add post/postun Requires for javadoc
- Add gcj_support option
