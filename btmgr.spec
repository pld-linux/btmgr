# TODO
# - x86_64 is broken, use ix86 version
#
# Conditional build:
%bcond_without	doc		# build documentation

Summary:	Smart Boot Manager is an OS independent boot manager
Name:		btmgr
Version:	3.7
Release:	0.2
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/btmgr/%{name}-%{version}-1.tar.gz
# Source0-md5:	7bfe432821c3cef48df8b3d6be800009
Patch0:		nasm.patch
Patch1:		major-macro.patch
URL:		http://sourceforge.net/projects/btmgr/
BuildRequires:	nasm
BuildRequires:	sed >= 4.0
BuildRequires:	ucl-devel
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-metafont
BuildRequires:	tetex-tex-babel
%endif
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
%patch0 -p1
%patch1 -p1

# allow passing defaults
%{__sed} -i -e '/^CC=/ s/gcc/$(HOSTCC)/' Makefile
%{__sed} -i -e '/^COMMON_FLAGS=/ s/-g/$(CFLAGS)/' Makefile
%{__sed} -i -e '/^ASM=/ s/$/ $(AFLAGS)/' Makefile

# we run docs in bcond
%{__sed} -i -e '/^SUBDIRS=/ s/docs//' Makefile
# pipe breaks error handling
%{__sed} -i -e '/(MAKE)/ s/|tee -a errors.log//' Makefile

%build
%{__make} \
	HOSTCC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	AFLAGS="-w-orphan-labels"

%{?with_doc:%{__make} -C docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CREDITS INSTALL README TODO
%doc %lang(zh) README-ZH
%attr(755,root,root) %{_sbindir}/sbminst
%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT
