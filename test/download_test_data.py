import zipfile
import gdown
import os
# Show URL: https://drive.google.com/file/d/14lYZ3SlK0aDMgjkT2xsMaowdz1pztAnA

if __name__ == '__main__':
    test_data_url = "https://drive.google.com/uc?id=1hmjpBgEZCow3JbJTSot1k1S-vUFQV4-9"
    output_zip = 'roi_convertor_test_v1.7.zip'
    gdown.download(test_data_url, output_zip, quiet=False)
    with zipfile.ZipFile(output_zip, 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove(output_zip)