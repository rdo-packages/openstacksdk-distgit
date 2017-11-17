%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

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

BuildRequires:  git

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-keystoneauth1
BuildRequires:  python-appdirs
BuildRequires:  python-requestsexceptions
BuildRequires:  python-dogpile-cache
BuildRequires:  python-munch
BuildRequires:  python-decorator
BuildRequires:  python-jmespath
BuildRequires:  python-ipaddress
BuildRequires:  python-futures
BuildRequires:  python-netifaces
BuildRequires:  python-jsonschema
BuildRequires:  python-os-service-types
# Test requirements
BuildRequires:  python-deprecation
BuildRequires:  python-iso8601 >= 0.1.11
BuildRequires:  python-jsonpatch >= 1.6
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-stestr
BuildRequires:  python-mock
BuildRequires:  python-requests-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-glanceclient

Requires:       python-deprecation
Requires:       python-jsonpatch >= 1.6
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-six
Requires:       python-pbr >= 2.0.0
Requires:       PyYAML
Requires:       python-appdirs
Requires:       python-requestsexceptions
Requires:       python-dogpile-cache
Requires:       python-munch
Requires:       python-decorator
Requires:       python-jmespath
Requires:       python-ipaddress
Requires:       python-futures
Requires:       python-netifaces
Requires:       python-iso8601
Requires:       python-os-service-types

%description -n python2-%{pypi_name}
%{common_desc}

%package -n python2-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc_tests}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-dogpile-cache
BuildRequires:  python3-appdirs
BuildRequires:  python3-requestsexceptions
BuildRequires:  python3-munch
BuildRequires:  python3-decorator
BuildRequires:  python3-jmespath
BuildRequires:  python3-futures
BuildRequires:  python3-netifaces
BuildRequires:  python3-jsonschema
BuildRequires:  python3-os-service-types
# Test requirements
BuildRequires:  python3-deprecation
BuildRequires:  python3-iso8601 >= 0.1.11
BuildRequires:  python3-jsonpatch >= 1.6
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-mock
BuildRequires:  python3-requests-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-glanceclient

Requires:       python3-deprecation
Requires:       python3-jsonpatch >= 1.6
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-six
Requires:       python3-pbr >= 2.0.0
Requires:       python3-PyYAML
Requires:       python3-appdirs
Requires:       python3-requestsexceptions
Requires:       python3-dogpile-cache
Requires:       python3-munch
Requires:       python3-decorator
Requires:       python3-jmespath
Requires:       python3-futures
Requires:       python3-netifaces
Requires:       python3-jsonschema
Requires:       python3-iso8601
Requires:       python3-os-service-types

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc_tests}

%endif


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation

%description -n python-%{pypi_name}-doc
A collection of libraries for building applications to work with OpenStack
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the requirements
rm -rf {,test-}requirements.txt

%build
%py2_build

%if 0%{?with_python3}
%{py3_build}
%endif

%if 0%{?with_doc}
# generate html docs 
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py2_install

%if 0%{?with_python3}
%{py3_install}
%endif


%check
stestr --test-path ./openstack/tests/unit run

%if 0%{?with_python3}
rm -rf .testrepository
stestr-3 --test-path ./openstack/tests/unit run
%endif


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/openstack-inventory
%{python2_sitelib}/openstack
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/openstack/tests

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/openstack/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/openstack
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/openstack/tests

%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/openstack/tests
%endif

%changelog
