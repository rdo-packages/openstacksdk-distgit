%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

# Disable docs while openstackdocstheme is packaged
%global with_doc 0

%global pypi_name openstacksdk

%global common_desc \
A collection of libraries for building applications to work with OpenStack

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        An SDK for building applications to work with OpenStack

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch


%description
%{common_desc}
clouds.

%package -n python2-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-requests
BuildRequires:  python-keystoneauth1
BuildRequires:  python-os-client-config
# Test requirements
BuildRequires:  python-deprecation
BuildRequires:  python-iso8601 >= 0.1.11
BuildRequires:  python-jsonpatch >= 1.1
BuildRequires:  python-subunit
BuildRequires:  python-os-testr
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools

Requires:       python-deprecation
Requires:       python-jsonpatch >= 1.1
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-os-client-config >= 1.28.0
Requires:       python-six
Requires:       python-stevedore
Requires:       python-pbr >= 2.0.0

%description -n python2-%{pypi_name}
%{common_desc}
clouds.

%package -n python2-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc}
clouds - test files


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-requests
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-os-client-config
# Test requirements
BuildRequires:  python3-deprecation
BuildRequires:  python3-iso8601 >= 0.1.11
BuildRequires:  python3-jsonpatch >= 1.1
BuildRequires:  python3-subunit
BuildRequires:  python3-os-testr
BuildRequires:  python3-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:       python3-deprecation
Requires:       python3-jsonpatch >= 1.1
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-os-client-config >= 1.28.0
Requires:       python3-six
Requires:       python3-stevedore
Requires:       python3-pbr >= 2.0.0

%description -n python3-%{pypi_name}
%{common_desc}
clouds.

%package -n python3-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}
clouds - test files

%endif


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation

%description -n python-%{pypi_name}-doc
%{common_desc}
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version}

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
%{__python2} setup.py test

%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-openstacksdk/commit/?id=c8f5194fdcecc913b4ee83d97654fb233dc617da
