from flask import Flask, render_template, request, jsonify
from database import *
from utils import *
from tempfile import TemporaryDirectory

application = Flask(__name__)


@application.route('/')
def index():
    return render_template("login.html")


@application.route('/main_page', methods=['POST', "GET"])
def main_page():
    """
    Landing page after user signs in
    :return: render home page template
    """
    customer_details = get_customer_details()
    customers = get_region_customers()
    return render_template("page.html", **locals())


@application.route('/zip_upload', methods=['POST'])
def file_submit():
    """
    Uploads the input zip file and parses through the zip file to run wifi analysis
    @body files: zip file inputted by user
    @body form: form information inputted by user
    :return: render template displaying wi-fi analysis
    """
    region = request.form['region']
    customer_name = request.form['customer_name']
    directory = f'DI_Files/{region}/{customer_name}'
    file = request.files['di_file']
    file_name = file.filename

    with TemporaryDirectory() as tmpdir:
        di_path = "./di.zip"

        file.save(di_path)
    file_path = "./di.zip"

    s3 = S3Storage()
    file_upload_response = s3.upload_file_to_s3(file_path, file_name, directory)
    wifi_check = check_wifi_issue(file)
    if type(wifi_check) is list:
        if len(wifi_check) > 0:
            wifi_result = wifi_check
            wifi_upload_response = ''
            # Wi-Fi analysis upload is dependent on file upload
            if file_upload_response is True:
                wifi_upload_response = s3.upload_wifi_result(wifi_check, file_name, directory)
        else:
            wifi_result = False
    return render_template("wifi-issue.html", **locals())

'''
Route commented out for now until OEX list is received
@application.route('/customers/<region>', methods=['GET'])
def get_customer_names(region: str = None):
    """
    Gets list of customers from metadata database
    @param region: string with name of region
    :return: list of customers from in a given region - default returns all customers
    """
    result = []
    customer_names = get_region_customers(region)
    for customer in customer_names:
        result.append(customer[0])
    return jsonify(result)
'''

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=81, debug=True)
    application.run(debug=True)
