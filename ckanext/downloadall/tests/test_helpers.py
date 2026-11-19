from ckanext.downloadall.helpers import is_archive_resource, has_own_archive_resource


def test_generated_zip_is_not_a_user_zip():
    res = {'format': 'ZIP', 'downloadall_metadata_modified': '2020-01-01'}
    assert not is_archive_resource(res)


def test_zip_detected_by_format_url_or_mimetype():
    assert is_archive_resource({'format': 'zip'})
    assert is_archive_resource({'format': '', 'url': 'http://x/data.ZIP?v=1'})
    assert is_archive_resource({'mimetype': 'application/zip'})
    assert is_archive_resource({'format': '7Z'})
    assert is_archive_resource({'url': 'http://x/data.tar.gz'})
    assert is_archive_resource({'mimetype': 'application/x-rar-compressed'})
    assert not is_archive_resource({'format': 'CSV', 'url': 'http://x/data.csv'})
    assert not is_archive_resource({'url': 'http://x/zipper'})


def test_has_own_archive_resource_ignores_generated_zip():
    generated = {'format': 'ZIP', 'downloadall_metadata_modified': 'x'}
    assert not has_own_archive_resource({'resources': [generated, {'format': 'CSV'}]})
    assert has_own_archive_resource({'resources': [generated, {'format': 'ZIP'}]})
