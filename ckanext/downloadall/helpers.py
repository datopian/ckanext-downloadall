def pop_zip_resource(pkg):
    '''Finds the zip resource in a package's resources, removes it from the
    package and returns it. NB the package doesn't have the zip resource in it
    any more.
    '''
    zip_res = None
    non_zip_resources = []
    for res in pkg.get('resources', []):
        if res.get('downloadall_metadata_modified'):
            zip_res = res
        else:
            non_zip_resources.append(res)
    # Only write back when the package had resources. On the "new dataset"
    # page the template passes pkg={}; adding a 'resources' key would make
    # that empty dict truthy and CKAN's resources.html would then try to
    # build an "Add new resource" link with no package type.
    if 'resources' in pkg:
        pkg['resources'] = non_zip_resources
    return zip_res


def count_uploaded_resources(pkg):
    '''Counts the number of uploaded resources in a package (excluding linked 
    resources). Uploaded resources have url_type == 'upload'.
    '''
    count = 0
    for res in pkg.get('resources', []):
        # Don't count the downloadall zip itself
        if res.get('downloadall_metadata_modified'):
            continue
        # Only count uploaded resources, not linked ones
        if res.get('url_type') == 'upload':
            count += 1
    return count


def is_zip_up_to_date(pkg, zip_res):
    '''Checks if the download all zip is up to date with the package.
    Returns True if the zip was generated after the package was last modified.
    '''
    if not zip_res:
        return False
    
    # Check if the zip's recorded metadata_modified matches the package's current one
    zip_metadata_modified = zip_res.get('downloadall_metadata_modified')
    pkg_metadata_modified = pkg.get('metadata_modified')
    
    if not zip_metadata_modified or not pkg_metadata_modified:
        return False
    
    return zip_metadata_modified == pkg_metadata_modified


ARCHIVE_EXTENSIONS = (
    'zip', 'zipx', '7z', 'rar', 'tar', 'gz', 'tgz', 'bz2', 'tbz2', 'xz', 'txz')
ARCHIVE_FORMATS = ARCHIVE_EXTENSIONS + ('gzip', 'bzip2')
ARCHIVE_MIMETYPE_PARTS = ('zip', 'x-7z', 'rar', 'x-tar', 'x-xz', 'x-compressed')


def is_archive_resource(res):
    '''True for an archive (zip, 7z, rar, tar, gz...) that someone published
    themselves, not our generated zip. Format is often empty or wrong on
    linked files, so the URL and mimetype are checked too.
    '''
    if res.get('downloadall_metadata_modified'):
        return False
    url = (res.get('url') or '').split('?')[0].split('#')[0].lower()
    mimetype = (res.get('mimetype') or '').lower()
    return ((res.get('format') or '').strip().lower() in ARCHIVE_FORMATS or
            url.endswith(tuple('.' + ext for ext in ARCHIVE_EXTENSIONS)) or
            any(part in mimetype for part in ARCHIVE_MIMETYPE_PARTS))


def has_own_archive_resource(pkg):
    return any(is_archive_resource(res) for res in pkg.get('resources', []))
