import json
import requests
from datetime import datetime



def getAccessToken(config):
    accessToken = ''
    authURL = 'https://apica.my.salesforce.com/services/oauth2/token?grant_type=password&client_id={clientId}' \
            '&client_secret={clientSecret}&username={username}&password={password}'.format(clientId=config['salesforceClientID'], \
            clientSecret=config['salesforceClientSecret'], username=config['salesforceUsername'], password=config['salesforcePassword'])
    response = requests.post(authURL)
    json_response = json.loads(response.text)
    accessToken = json_response['access_token']
    return accessToken


def getInstanceId(accessToken):
    instanceId = ''
    instanceURL = 'https://apica.my.salesforce.com/services/data/v53.0/analytics/reports/00O1n000008JcPqEAK/instances'
    authHeader = {'Authorization': 'Bearer ' + accessToken}
    response = requests.post(instanceURL, headers=authHeader)
    json_response = json.loads(response.text)
    instanceId = json_response['id']
    return instanceId


def getReportData(accessToken, instanceId):
    reportResponse = ''
    reportURL = 'https://apica.my.salesforce.com/services/data/v53.0/analytics/reports/00O1n000008JcPqEAK/instances/{instanceId}'.format(instanceId=instanceId)
    authHeader = {'Authorization': 'Bearer ' + accessToken}
    response = requests.get(reportURL, headers=authHeader)
    reportResponse = json.loads(response.text)
    # print(json.dumps(reportResponse, indent=4, sort_keys=False))
    with open('salesforce_raw.json', 'w') as f:
        f.write(json.dumps(reportResponse, indent=4, sort_keys=True))
    return reportResponse



# addressable market is total market TCV for all companies in that industry
# leave out TBD and null's entirely
# use earliest close date
def iterateReportResponse(reportResponse):
    company_info = {}
    industries = {}
    factMap = reportResponse['factMap']['T!T']['rows']

    for company in factMap:
        if company['dataCells'][0]['label'] == '' or company['dataCells'][0]['label'] == 'TBD':
            continue
        else:
            company_number = company['dataCells'][0]['label']
            company_name = company['dataCells'][1]['label']
            acv_total = getDollar(company['dataCells'][2]['label'])
            tcv_total = getDollar(company['dataCells'][3]['label'])
            industry = company['dataCells'][4]['label']
            close_date = convertDate(company['dataCells'][5]['label'])

            # Find a dupe company -> add the ACV and TCV values
            if company_number in company_info.keys():
                company_info[company_number]['ACV'] = format(round(float(acv_total) + float(company_info[company_number]['ACV']), 2), '.2f')
                company_info[company_number]['TCV'] = format(round(float(tcv_total) + float(company_info[company_number]['TCV']), 2), '.2f')
                if getDate(close_date) < getDate(company_info[company_number]['Close Date']):
                    company_info[company_number]['Close Date'] = close_date
            else:
                aggregates = {'Company Name': company_name, 'ACV': acv_total, 'TCV': tcv_total, 'CompanyID': company_number, 'Industry': industry, 'Close Date': close_date}
                company_info[company_number] = aggregates

    # Gather Addressable Market per Industry
    for company in company_info:
        industry = company_info[company]['Industry']
        tcv = company_info[company]['TCV']
        if industry in industries.keys():
            industries[industry] = format(round(float(tcv) + float(industries[industry]), 2), '.2f')
        else:
            industries[industry] = tcv

    for company in company_info:
        industry = company_info[company]['Industry']
        company_info[company]['Addressable Market'] = industries[industry]


    # print(json.dumps(factMap, indent=4, sort_keys=True))
    with open('salesforce.json', 'w') as f:
        f.write(json.dumps(company_info, indent=4, sort_keys=True))
    return company_info


def getDollar(string):
    stripped_string = ''
    for c in range(len(string)):
        if string[c] in '0123456789.':
            stripped_string += string[c]
    if stripped_string == '':
        return '0.00'
    else:
        return stripped_string


def getDate(date):
    s_tuple = date.split('-')
    return datetime(int(s_tuple[0]), int(s_tuple[1]), int(s_tuple[2]))


def convertDate(date):
    s_tuple = date.split('/')
    if len(s_tuple[0]) == 1:
        s_tuple[0] = '0' + s_tuple[0]
    if len(s_tuple[1]) == 1:
        s_tuple[1] = '0' + s_tuple[1]

    return s_tuple[2] + '-' + s_tuple[0] + '-' + s_tuple[1]
