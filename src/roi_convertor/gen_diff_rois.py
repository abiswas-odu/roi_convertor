import zipfile

def check_if_diff(zipfile_1, zipfile_2):

    zf_set_1 = set(zipfile.ZipFile(zipfile_1).namelist())
    zf_set_2 = set(zipfile.ZipFile(zipfile_2).namelist())

    if zf_set_1 == zf_set_2:
        return False, [], []
    else:
        zf_only_1 = list(zf_set_1-zf_set_2)
        zf_only_2 = list(zf_set_2-zf_set_1)
        return True,zf_only_1,zf_only_2



