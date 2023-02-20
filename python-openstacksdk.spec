
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Disable docs until bs4 package is available
%global with_doc 0

%global pypi_name openstacksdk

%global common_desc \
A collection of libraries for building applications to work with OpenStack \
clouds.

%global common_desc_tests \
A collection of libraries for building applications to work with OpenStack \
clouds - test files

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        An SDK for building applications to work with OpenStack

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git-core

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-appdirs
BuildRequires:  python3-requestsexceptions
BuildRequires:  python3-munch
BuildRequires:  python3-jmespath
BuildRequires:  python3-jsonschema
BuildRequires:  python3-os-service-types

# Test requirements
%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 9)
BuildRequires:  python3-importlib-metadata
%endif
BuildRequires:  python3-iso8601 >= 0.1.11
BuildRequires:  python3-jsonpatch >= 1.16
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-config
BuildRequires:  python3-stestr
BuildRequires:  python3-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-requests-mock
BuildRequires:  python3-dogpile-cache
BuildRequires:  python3-ddt
BuildRequires:  python3-decorator
BuildRequires:  python3-netifaces

Requires:       python3-cryptography >= 2.7
%if (0%{?fedora} && 0%{?fedora} < 32) || (0%{?rhel} && 0%{?rhel} < 9)
Requires:       python3-importlib-metadata >= 1.7.0
%endif
Requires:       python3-jsonpatch >= 1.16
Requires:       python3-keystoneauth1 >= 3.18.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-appdirs
Requires:       python3-requestsexceptions >= 1.2.0
Requires:       python3-jmespath
Requires:       python3-iso8601
Requires:       python3-os-service-types >= 1.7.0
Requires:       python3-dogpile-cache
Requires:       python3-decorator
Requires:       python3-netifaces
Requires:       python3-yaml >= 3.13

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc_tests}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx

%description -n python-%{pypi_name}-doc
A collection of libraries for building applications to work with OpenStack
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the requirements
rm -rf {,test-}requirements.txt
# This unit test requires python-prometheus, which is optional and not needed
rm -f openstack/tests/unit/test_stats.py

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
rm -f ./openstack/tests/unit/test_hacking.py
export OS_STDOUT_CAPTURE=true
export OS_STDERR_CAPTURE=true
export OS_TEST_TIMEOUT=20
# FIXME(jpena) we are skipping some unit tests due to
# https://storyboard.openstack.org/#!/story/2005677
PYTHON=python3 stestr-3 --test-path ./openstack/tests/unit run --exclude-regex '(test_wait_for_task_.*|.*TestOsServiceTypesVersion.*|.*test_timeout_and_failures_not_fail.*)'

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/openstack-inventory
%{python3_sitelib}/openstack
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/openstack/tests

%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/openstack/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%changelog
