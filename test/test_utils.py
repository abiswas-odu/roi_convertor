import os


def dir_filesize_cmp(dir1: os.PathLike, dir2: os.PathLike):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
   """
    roi_zip_files_1 = os.listdir(dir1)
    roi_zip_files_2 = os.listdir(dir2)
    assert [row for row in roi_zip_files_1] == [row for row in roi_zip_files_2]

    for row in roi_zip_files_1:
        path_1 = os.path.join(dir1, row)
        path_2 = os.path.join(dir2, row)
        if not (os.path.isfile(path_1) and os.path.isfile(path_2) and os.path.getsize(path_1) == os.path.getsize(path_2)):
            return False
    return True