from ckanext.downloadall.helpers import is_zip_resource, has_own_zip_resource


def test_generated_zip_is_not_a_user_zip():
    res = {'format': 'ZIP', 'downloadall_metadata_modified': '2020-01-01'}
    assert not is_zip_resource(res)


def test_zip_detected_by_format_url_or_mimetype():
    assert is_zip_resource({'format': 'zip'})
    assert is_zip_resource({'format': '', 'url': 'http://x/data.ZIP?v=1'})
    assert is_zip_resource({'mimetype': 'application/zip'})
    assert not is_zip_resource({'format': 'CSV', 'url': 'http://x/data.csv'})


def test_has_own_zip_resource_ignores_generated_zip():
    generated = {'format': 'ZIP', 'downloadall_metadata_modified': 'x'}
    assert not has_own_zip_resource({'resources': [generated, {'format': 'CSV'}]})
    assert has_own_zip_resource({'resources': [generated, {'format': 'ZIP'}]})
