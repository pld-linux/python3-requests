#
# Conditional build:
%bcond_with	tests	# pytest tests (one test fails with pytest-httpbin 1.0.0)

%define		urllib3_ver	1.21.1
%define		module		requests
%define		egg_name	requests
Summary:	HTTP library for Python
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona
Name:		python3-%{module}
Version:	2.31.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/requests/
Source0:	https://files.pythonhosted.org/packages/source/r/requests/%{module}-%{version}.tar.gz
# Source0-md5:	941e175c276cd7d39d098092c56679a4
Patch0:		system-cert.patch
Patch1:	        python-requests-reqs.patch
Patch2:		python-requests-disable-xdist.patch
URL:		https://docs.python-requests.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.5.8
BuildRequires:	python3-certifi >= 2017.4.17
BuildRequires:	python3-charset_normalizer >= 2
BuildRequires:	python3-charset_normalizer < 2.1
BuildRequires:	python3-idna >= 2.5
BuildRequires:	python3-idna < 4
BuildRequires:	python3-pytest >= 3
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-httpbin >= 0.0.7
BuildRequires:	python3-pytest-mock >= 2.0.0
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-urllib3 >= %{urllib3_ver}
BuildRequires:	python3-urllib3 < 1.27
%endif
Requires:	python3-modules >= 1:3.6
Requires:	python3-charset_normalizer >= 2
# for https
Requires:	python3-cryptography >= 1.3.4
Requires:	python3-idna >= 2.5
Requires:	python3-pyOpenSSL >= 0.14
Requires:	python3-urllib3 >= 1.22-2
Suggests:	ca-certificates
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Requests is a HTTP library, written in Python, for human beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most
of the HTTP capabilities you should need, but the API is thoroughly
broken. It requires an enormous amount of work (even method overrides)
to perform the simplest of tasks. Things shouldn't be this way. Not in
Python.

This package contains Python 3.x module.

%description -l pl.UTF-8
Requests to napisana w Pythonie biblioteka HTTP dla ludzi.

Większość istniejących modułów Pythona do wysyłania żądań HTTP jest
zbyt gadatliwa i nieporęczna. Wbudowany w Pythona moduł urllib2
zapewnia większość wymaganych możliwości HTTP, ale API jest kiepskie -
wymaga dużych nakładów pracy (nawet nadpisań metod) do wykonania
najprostszych zadań. Nie powinno tak być. Nie w Pythonie.

Ten pakiet zawiera moduł dla Pythona 3.x.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_httpbin.plugin,pytest_mock" \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY.md README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
