import json
import requests

import salesforceApi as sf
import mondayApi as md


def compareReports(sf_report, md_report):
    diff = {'adds': {}, 'removes': {}, 'changes': {}}

    for k in sf_report:
        if k in md_report.keys():
            sf_report[k]['Item ID'] = md_report[k]['Item ID']
            diff['changes'][k] = sf_report[k]
        else:
            diff['adds'][k] = sf_report[k]

    for k in md_report:
        if k not in sf_report.keys():
            diff['removes'][k] = md_report[k]

    return diff


if __name__ == '__main__':
    with open('config.json') as config_json:
        config = json.load(config_json)

    at = sf.getAccessToken(config['salesforce'])
    ins_id = sf.getInstanceId(at)
    report_data = sf.getReportData(at, ins_id)
    sf_report = sf.iterateReportResponse(report_data)

    monday_access_token = config['monday.com']['mondayAccessToken']
    board_items = md.getBoardItems(monday_access_token)
    md_report = md.parseBoardData(board_items)

    diff = compareReports(sf_report, md_report)
    with open('monday_output.json', 'w') as f:
        f.write(json.dumps(diff, indent=4, sort_keys=True))

    md.changeItems(diff['changes'], monday_access_token)
    md.addItems(diff['adds'], monday_access_token)

    # Removing items could interfere with ASM metric data collection
    # md.removeItems(diff['removes'], monday_access_token)
