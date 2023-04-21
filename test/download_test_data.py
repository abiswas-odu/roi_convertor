import zipfile

https://drive.google.com/file/d/14lYZ3SlK0aDMgjkT2xsMaowdz1pztAnA?export=download
if __name__ == '__main__':
    with zipfile.ZipFile('roi_convertor_test_v1.zip', 'r') as zip_ref:
        zip_ref.extractall('.')