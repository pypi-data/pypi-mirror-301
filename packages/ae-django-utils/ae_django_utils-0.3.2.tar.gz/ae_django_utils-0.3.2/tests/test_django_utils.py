""" ae.django_utils unit tests. """
from django.conf import settings
from django.test.utils import override_settings

from ae.django_utils import generic_language, requested_language, set_url_part


settings.configure()


class TestLanguageHelpers:
    def test_generic_language(self):
        assert generic_language('') == ''
        assert generic_language('en') == 'en'
        assert generic_language('de') == 'de'
        assert generic_language('en-uk') == 'en'
        assert generic_language('en-US') == 'en'
        assert generic_language('es-ar') == 'es'

    def test_requested_language_with_default_settings(self):
        assert requested_language() == 'en'

    @override_settings(LANGUAGE_CODE='es')
    def test_requested_language_with_es_setting(self):
        assert requested_language() == 'es'

    @override_settings(LANGUAGE_CODE='de-CH')
    def test_requested_language_with_de_setting(self):
        assert requested_language() == 'de'


class TestUrlHelpers:
    def test_set_url_part_add(self):
        query = "query=value"
        frag = "fragment"
        url = "service://host/path/"
        assert set_url_part(url) == url
        assert set_url_part(url, fragment=frag) == url + "#" + frag
        assert set_url_part(url, query=query) == url + "?" + query
        assert set_url_part(url, fragment=frag, query=query) == url + "?" + query + "#" + frag

    def test_set_url_part_replace(self):
        query = "old_query=old_value"
        frag = "old_fragment"
        url = "service://host/path/" + "?" + query + "#" + frag
        assert set_url_part(url) == url

        new_frag = "new_frag"
        assert frag not in set_url_part(url, fragment=new_frag)
        assert set_url_part(url, fragment=new_frag).endswith("#" + new_frag)

        new_q = "new_query=new_val"
        assert query not in set_url_part(url, query=new_q)
        assert "?" + new_q in set_url_part(url, query=new_q)

        new_url = set_url_part(url, fragment=new_frag, query=new_q)
        assert query not in new_url and frag not in new_url
        assert new_url.endswith("?" + new_q + "#" + new_frag)
