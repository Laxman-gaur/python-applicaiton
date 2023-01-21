import tempfile
import zipfile
import io
import boto3
from customers import customer_list


class S3Storage:
    """
    Class that handles S3 functions and credentials
    """
    def __init__(self):
        self.service_name = 's3'
        self.region_name = 'us-east-1'
        self.aws_access_key_id = ''
        self.aws_secret_access_key = ''
        self.bucket = ''

    def upload_file_to_s3(self, file_path: str, filename: str, directory: str):
        """
        Upload file to s3 bucket
        :param file_path: str containing file path to upload
        :param filename: str containing file name
        :param directory: str containing directory to upload file to in s3
        :return: True is successful, exception otherwise
        """
        s3 = boto3.client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)
        upload_path = f'{directory}/{filename}'
        try:
            s3.upload_file(file_path, self.bucket, upload_path)
            return True
        except Exception as exp:
            return f"Error: {exp}"

    def get_s3_file_metadata(self, key: str):
        """
        Get metadata from specific file in s3 bucket
        :param key: str containing key of specific file
        :return: dictionary containing metadata if successful, exception otherwise
        """
        s3 = boto3.client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)
        try:
            metadata = s3.head_object(Bucket=self.bucket, Key=key)
            return metadata
        except Exception as exp:
            return f"Error: {exp}"

    def upload_wifi_result(self, wifi_result: list, file_name: str, file_path: str):
        """
        Convert list of wi-fi issues to temporary file and upload to s3
        :param wifi_result: list of lines (str) that indicate a wi-fi issue
        :param file_name: str containing file name
        :param file_path: str containing file path
        :return: True if upload is successful, exception otherwise
        """
        fp = tempfile.NamedTemporaryFile(delete=False)
        upload_directory = 'wifi-results'
        for line in wifi_result:
            binary_text = bytes(line, 'utf-8')
            fp.write(binary_text)
        try:
            meta_data = self.get_s3_file_metadata(f'{file_path}/{file_name}')
            entity_id = meta_data['ETag'][1:-1]
            self.upload_file_to_s3(fp.name, entity_id, upload_directory)
            fp.close()
            return True
        except Exception as exp:
            return f"Error: {exp}"


def check_wifi_issue(debug_file) -> list:
    """
    Parses through files in zip file to find lines indicating wi-fi issues
    :param debug_file: file storage containing zip file
    :return: list of lines (str) in file
    """
    lines_found = []
    try:
        archive = zipfile.ZipFile(debug_file, 'r')
        for file in archive.namelist():
            if file.endswith('.txt') and 'var/log/dmesg/' in file:
                myfile = archive.open(file)
                for line in io.TextIOWrapper(myfile, errors='ignore'):
                    if 'hardware restart was requested' in line.lower() or 'enqueue_hcmd failed' in line.lower():
                        lines_found.append(line)
                break
        return lines_found
    except Exception as exp:
        return f"Error: {exp}"


'''
Function commented out until list of OEXs is given
def insert_company_json_into_db():
    customers = []
    OEXs = ['OEE', 'ORT', 'OEJ', 'OEK', 'OEP', 'OEZ', 'OEZ-TW', 'OEZ', 'OAA']
    customer_array = customer_list["customers"]["customer"]
    # count = 0
    for customer in customer_array:
        # count += 1
        customer_name = customer["name"]
        region_name = customer["timeZoneId"]
        cust = {
            "Company_Name": customer_name,
            "Region": region_name,
            "OEX": region_name[0:1]
        }
        print(region_name)
    # print(count)
    # return customer_array
'''