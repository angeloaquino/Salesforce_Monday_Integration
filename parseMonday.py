import json
from monday import MondayClient
from datetime import date

with open('config.json') as config_json:
    config = json.load(config_json)
    monday_access_token = config['monday.com']['mondayAccessToken']


monday = MondayClient(monday_access_token)
today = date.today()
today = today.strftime("%b %d, %Y")


class getItemsFromMonday:
    def __init__(self, check_info):
        self.check_info = check_info
        self.information = []
        self.board_id = 2451130033
        self.group_id = "topics"
        self.monday_items = monday.boards.fetch_items_by_board_id([self.board_id])
        self.boards = self.monday_items.get('data').get('boards')[0]
        self.data = self.boards.get('items')
        self.monday_dict = []
        last_updated = 'text57'
        for x in range(len(self.data)):
            monday_name = self.data[x]['name']
            monday_id = self.data[x]['id']
            for i in range(len(self.check_info)):
                self.asm_name = self.check_info[i]['name']
                self.asm_check_type = self.check_info[i]['check type']
                asm_last_value = self.check_info[i]['value']
                self.asm_last_value = str(asm_last_value)
                if monday_name == self.asm_name:
                    if self.asm_check_type == 'Enabled Standard':
                        column_id = 'numbers7'
                        print(self.asm_name, self.board_id, monday_id, column_id, self.asm_last_value)
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                        mutate_monday(self.board_id, monday_id, last_updated, today)
                    elif self.asm_check_type == 'Disabled Standard':
                        column_id = 'numbers44'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Total Standard':
                        column_id = 'numbers3'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Enabled Advanced':
                        column_id = 'numbers24'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Disabled Advanced':
                        column_id = 'numbers56'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Total Advanced':
                        column_id = 'numbers74'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Enabled DAC':
                        column_id = 'numbers55'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Disabled DAC':
                        column_id = 'numbers8'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Total DAC':
                        column_id = 'numbers92'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Total Amount':
                        column_id = 'numbers65'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Private Agent Check':
                        column_id = 'numbers238'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                    elif self.asm_check_type == 'Last ALT Job':
                        column_id = 'numbers41'
                        mutate_monday(self.board_id, monday_id, column_id, self.asm_last_value)
                        mutate_monday(self.board_id, monday_id, last_updated, today)
                    else:
                        pass
                else:
                    pass
                    # create a new item with board id
                    # company_name = self.check_info[i]['name']
                    # create_item(self.board_id, self.group_id, company_name)


print("Today's date:", today)


def mutate_monday(board_id, monday_id, column_id, last_value):
    update_monday = monday.items.change_multiple_column_values(board_id, monday_id, {column_id: last_value})
    return update_monday


def create_item(board_id, group_id, item_name):
    update_item = monday.items.create_item(board_id, group_id, item_name, create_labels_if_missing=True)
    return update_item
