import json
import requests

BOARD_ID = '2451130033'
GROUP_ID = 'topics'


def getBoardItems(accessToken):
    instanceURL = 'https://api.monday.com/v2/'
    authHeader = {'Authorization': accessToken}
    query = r'query{boards(ids:' + BOARD_ID + '){items{id name column_values{id title text}}}}'
    data = {'query': query}
    response = requests.post(instanceURL, headers=authHeader, json=data)
    json_response = json.loads(response.text)
    with open('monday_input.json', 'w') as f:
        f.write(json.dumps(json_response, indent=4, sort_keys=False))
    return json_response


# Could be more abstract by looking for the keywords in the Title value
def parseBoardData(data):
    items = data['data']['boards'][0]['items']
    company_info = {}

    for company in items:
        company_name = company['name']
        company_id = company['column_values'][0]['text']
        acv = company['column_values'][1]['text']
        tcv = company['column_values'][2]['text']
        market = company['column_values'][3]['text']
        industry = company['column_values'][4]['text']
        close_date = company['column_values'][5]['text']
        item_id = company['id']

        company_data = {'Company Name': company_name, 'ACV': acv, 'TCV': tcv, 'CompanyID': company_id,
                        'Industry': industry, 'Close Date': close_date, 'Addressable Market': market,
                        'Item ID': item_id}
        company_info[company_id] = company_data

    with open('monday.json', 'w') as f:
        f.write(json.dumps(company_info, indent=4, sort_keys=True))
    return company_info


def changeItems(changes, accessToken):
    for c in changes:
        mutation_string = "mutation {change_multiple_column_values (board_id:" + BOARD_ID + ", item_id:" + changes[c][
            'Item ID'] + \
                          ", column_values:\"{\\\"name\\\": \\\"" + changes[c][
                              'Company Name'] + "\\\",\\\"customerid\\\": \\\"" + changes[c]['CompanyID'] + \
                          "\\\",\\\"numbers\\\": \\\"" + changes[c]['ACV'] + "\\\",\\\"numbers4\\\": \\\"" + changes[c][
                              'TCV'] + \
                          "\\\",\\\"dup__of_at_risk___mm_\\\": \\\"" + changes[c][
                              'Addressable Market'] + "\\\",\\\"dropdown_19\\\": \\\"" + \
                          changes[c]['Industry'] + "\\\",\\\"date24\\\": \\\"" + changes[c][
                              'Close Date'] + "\\\"}\") {name}}"
        query = {'query': mutation_string}
        instanceURL = 'https://api.monday.com/v2/'
        authHeader = {'Authorization': accessToken}
        response = requests.post(instanceURL, headers=authHeader, json=query)

    return


def addItems(adds, accessToken):
    for a in adds:
        mutation_string = "mutation {create_item (board_id:" + BOARD_ID + ", group_id:" + GROUP_ID + ", item_name:\"" + \
                          adds[a]['Company Name'] + "\", column_values:\"{\\\"customerid\\\": \\\"" + adds[a][
                              'CompanyID'] + \
                          "\\\",\\\"numbers\\\": \\\"" + adds[a]['ACV'] + "\\\",\\\"numbers4\\\": \\\"" + adds[a][
                              'TCV'] + \
                          "\\\",\\\"dup__of_at_risk___mm_\\\": \\\"" + adds[a][
                              'Addressable Market'] + "\\\",\\\"dropdown_19\\\": \\\"" + \
                          adds[a]['Industry'] + "\\\",\\\"date24\\\": \\\"" + adds[a]['Close Date'] + "\\\"}\") {id}}"
        query = {'query': mutation_string}
        # print(json.dumps(query, indent=4))
        instanceURL = 'https://api.monday.com/v2/'
        authHeader = {'Authorization': accessToken}
        response = requests.post(instanceURL, headers=authHeader, json=query)
        # json_response = json.loads(response.text)
        # print(json.dumps(json_response, indent=4))

    return


def removeItems(removes, accessToken):
    for r in removes:
        mutation_string = "mutation {delete_item (item_id: " + removes[r]['Item ID'] + ") { id } }"
        query = {'query': mutation_string}
        instanceURL = 'https://api.monday.com/v2/'
        authHeader = {'Authorization': accessToken}
        response = requests.post(instanceURL, headers=authHeader, json=query)
        # json_response = json.loads(response.text)
        # print(json.dumps(json_response, indent=4))

    return