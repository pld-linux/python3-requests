#
# Conditional build:
%bcond_without	tests	# pytest tests

%define		module		requests
Summary:	HTTP library for Python
Summary(pl.UTF-8):	Biblioteka HTTP dla Pythona
Name:		python3-%{module}
Version:	2.33.1
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/requests/
Source0:	https://files.pythonhosted.org/packages/source/r/requests/%{module}-%{version}.tar.gz
# Source0-md5:	ebc3b42b51c6245524345d170e5d4c50
Patch0:		system-cert.patch
Patch1:	        python-requests-reqs.patch
Patch2:		python-requests-disable-xdist.patch
URL:		https://docs.python-requests.org/
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:61.0
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.5.8
BuildRequires:	python3-certifi >= 2023.6.7
BuildRequires:	python3-charset_normalizer >= 2
BuildRequires:	python3-charset_normalizer < 4
BuildRequires:	python3-httpbin >= 0.10.0
BuildRequires:	python3-httpbin < 0.11
BuildRequires:	python3-idna >= 2.5
BuildRequires:	python3-idna < 4
BuildRequires:	python3-pytest >= 3
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-httpbin >= 2.1.0
BuildRequires:	python3-pytest-mock >= 2.0.0
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-trustme
BuildRequires:	python3-urllib3 >= 1.26
BuildRequires:	python3-urllib3 < 3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
Requires:	python3-modules >= 1:3.10
# for https
Requires:	python3-cryptography >= 1.3.4
Requires:	python3-pyOpenSSL >= 0.14
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
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%py3_build

%if %{with tests}
# timeout tests fail with network disabled
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_httpbin.plugin,pytest_mock" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_connect_timeout and not test_total_timeout_connect'
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
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
