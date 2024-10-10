from tests import conftest
from geovisio.web.utils import get_api_version
import re


def test_configuration(dburl, tmp_path):
    with (
        conftest.create_test_app(
            {
                "TESTING": True,
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "OAUTH_PROVIDER": None,
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
                "API_PICTURES_LICENSE_SPDX_ID": "etalab-2.0",
                "API_PICTURES_LICENSE_URL": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
                "API_SUMMARY": {"color": "#abcdef", "name": {"en": "My server"}},
            }
        ) as app,
        app.test_client() as client,
    ):
        r = client.get("/api/configuration")
        assert r.status_code == 200
        assert r.json == {
            "color": "#abcdef",
            "description": {"label": "The open source photo mapping solution", "langs": {"en": "The open source photo mapping solution"}},
            "logo": "https://gitlab.com/panoramax/gitlab-profile/-/raw/main/images/logo.svg",
            "name": {"label": "My server", "langs": {"en": "My server"}},
            "auth": {"enabled": False},
            "license": {
                "id": "etalab-2.0",
                "url": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
            },
            "version": get_api_version(),
        }
        assert re.match(r"^\d+\.\d+\.\d+(-\d+-[a-zA-Z0-9]+)?$", r.json["version"])


def test_configuration_i18n(dburl, tmp_path):
    with (
        conftest.create_test_app(
            {
                "TESTING": True,
                "DB_URL": dburl,
                "FS_URL": str(tmp_path),
                "OAUTH_PROVIDER": None,
                "FS_TMP_URL": None,
                "FS_PERMANENT_URL": None,
                "FS_DERIVATES_URL": None,
                "API_PICTURES_LICENSE_SPDX_ID": "etalab-2.0",
                "API_PICTURES_LICENSE_URL": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
                "API_SUMMARY": {"color": "#abcdef", "name": {"en": "My server", "fr": "Mon petit serveur des familles"}},
            }
        ) as app,
        app.test_client() as client,
    ):
        # With user defined language
        r = client.get("/api/configuration", headers={"Accept-Language": "fr_FR,fr,en"})
        assert r.status_code == 200
        assert r.json == {
            "color": "#abcdef",
            "description": {"label": "The open source photo mapping solution", "langs": {"en": "The open source photo mapping solution"}},
            "logo": "https://gitlab.com/panoramax/gitlab-profile/-/raw/main/images/logo.svg",
            "name": {"label": "Mon petit serveur des familles", "langs": {"en": "My server", "fr": "Mon petit serveur des familles"}},
            "auth": {"enabled": False},
            "license": {
                "id": "etalab-2.0",
                "url": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
            },
            "version": get_api_version(),
        }
