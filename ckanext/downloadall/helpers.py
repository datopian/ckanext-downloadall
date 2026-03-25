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
