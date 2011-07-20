#
# Conditional build:
%bcond_without	doc		# build documentation

Summary:	Smart Boot Manager is an OS independent boot manager
Name:		btmgr
Version:	3.7
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/btmgr/%{name}-%{version}-1.tar.gz
# Source0-md5:	7bfe432821c3cef48df8b3d6be800009
URL:		http://sourceforge.net/projects/btmgr/
BuildRequires:	nasm
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	sgml-tools}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The main goals of SBM are to be absolutely OS independent, flexible
and full-featured. It has all of the features needed to boot a variety
of OSes from several kinds of media, while keeping its size no more
than 30K bytes. In another words, SBM does NOT touch any of your
partitions, it totally fits into the first track (the hidden track) of
your hard disk! SBM now supports booting from floppy, hard disk and
CD-ROM. There are plans to support ZIP and LS-120 in the near future.

%prep
%setup -q -n %{name}-%{version}-1

%{__sed} -i -e '/^CC=/ s/gcc/%{__cc}/' Makefile
%{__sed} -i -e '/^SUBDIRS=/ s/docs//' Makefile

%build
%{__make}

%{?with_doc:%{__make} -C docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CREDITS INSTALL README TODO
%doc(zh) README-ZH
%attr(755,root,root) %{_sbindir}/sbminst
%{_datadir}/btmgr

%clean
rm -rf $RPM_BUILD_ROOT
