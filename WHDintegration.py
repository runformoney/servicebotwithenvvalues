from dbhelper import DBHelper
import json
import requests
db = DBHelper()

class APIintegration:

    def create_ticket_in_whd(self,ticket_id,owner_id,date_today):
        data = db.get_case_subject(ticket_id, owner_id, date_today)
        print(data)
        js = {
            "type": "problem",
            "subject" : "Help, my printer is on fire!",
            "description": "The fire is very colorful.",
            "priority": "high",
            "status": "open",
            "custom_fields": [
                {
                    "id": 360001465651,
                    "value": "TC1234"
                },
                {
                    "id": 360001465671,
                    "value": "OW12346"
                },
                {
                    "id": 3600014689511,
                    "value": "Facilities"
                },
                {
                    "id": 360001424032,
                    "value": "Rukhshan"
                },
                {
                    "id": 360001465691,
                    "value": "Rahman"
                },
                {
                    "id": 360001424192,
                    "value": "8884300686"
                },
                {
                    "id": 360001467331,
                    "value": "Hyderabad"
                }
            ]
        }
        #js = json.load(js)
        print(data)
        if len(data) > 0:
            js["subject"] = data[3]
            js["description"] = data[4]
            js["priority"] = 'low'
            js["status"]= "open"
            js["custom_fields"] = []
            custom_field_ids = [360001465651, 360001465671, 360001468951, 360001424032, 360001465691, 360001424192,
                                360001467331]
            data_custom_fields = [data[0], data[2], data[6], data[7], data[8], data[9], data[11]]
            for i in range(0, 7):
                entity = {}
                entity["id"] = custom_field_ids[i]
                entity["value"] = data_custom_fields[i]
                js["custom_fields"].append(entity)

            data =  {"ticket": js}
            payload = json.dumps(data)

            print(data)

            url = 'https://servicebot.zendesk.com/api/v2/tickets.json'
            user = 'rukshan4u4ever@gmail.com'
            pwd = 'Rukhshan@1'
            headers = {'content-type': 'application/json'}

            response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)
            response = response.text

            print(response)

            if type(response) is not dict:
                json_acceptable_string = response.replace("'", "\"")
                d = json.loads(json_acceptable_string)
                id = d['ticket']['id']
                db.update_whd_ticket_id(id,owner_id,date_today,ticket_id)

    def escalate_ticket(self, ticket_id,owner_id,date_today):
        data = db.get_case_subject(ticket_id, owner_id, date_today)
        whd_ticket_id = data[-1]
        priority = int(data[-2])
        priorityDict = {1: "low", 2: "high", 3: "urgent"}
        js = {"ticket": {"priority": str(priorityDict[priority])}}
        print(whd_ticket_id)
        url = 'https://servicebot.zendesk.com/api/v2/tickets/' + str(whd_ticket_id)+ '.json'
        user = 'rukshan4u4ever@gmail.com'
        pwd = 'Rukhshan@1'
        headers = {'content-type': 'application/json'}
        payload = json.dumps(js)

        # Do the HTTP post request
        response = requests.put(url, data=payload, auth=(user, pwd), headers=headers)
        print(response.text, response)

    def delete_ticket(self,whd_ticket_id):
        #data = db.get_case_subject(ticket_id, owner_id, date_today)[0]

        print(whd_ticket_id)
        url = 'https://servicebot.zendesk.com/api/v2/tickets/' + str(whd_ticket_id) + '.json'
        user = 'rukshan4u4ever@gmail.com'
        pwd = 'Rukhshan@1'
        headers = {'content-type': 'application/json'}

        # Do the HTTP post request
        response = requests.delete(url, auth=(user, pwd), headers=headers)

        print(response.text, response)

