from global_functions.LoggingGenerator import Logger
from global_functions.new_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('new_process_init', __name__, description="A new job process")


@blueprint.route('/new_process_start', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process.
    It listens for a POST request at the '/new_process_start' endpoint open for the MS RnD team
        """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='direct')
        
        return new_process_dict['id'], 201


@blueprint.route('/new_process_typeform', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='typeform')
        
        return new_process_dict['id'], 201


if __name__ == '__main__':
    import json
    
    test = """
    	{
      "event_id": "01HZ01NC88Z10SGXE447QR3AX8",
      "event_type": "form_response",
      "form_response": {
        "form_id": "Apf5GNSZ",
        "token": "hxpuh90rm1zsnbxajikhxpun5hqp4ucm",
        "landed_at": "2024-05-28T16:41:08Z",
        "submitted_at": "2024-05-28T16:48:45Z",
        "definition": {
          "id": "Apf5GNSZ",
          "title": "Interview_notification",
          "fields": [
            {
              "id": "uGidsoDwfCES",
              "ref": "1872f227-7c08-4651-b5aa-0c16fe0a4b68",
              "type": "dropdown",
              "title": "What is your domain?",
              "properties": {}
            },
            {
              "id": "FBYMmvdFNhfw",
              "ref": "cac2e68b-c202-49d4-82ed-342fdac8bb0b",
              "type": "email",
              "title": "First off, what's your email address?",
              "properties": {}
            },
            {
              "id": "Kys4EcJ4WViT",
              "ref": "29311df9-c5ea-4e4c-99ae-ff5c08bfdf43",
              "type": "short_text",
              "title": "What's your full name?",
              "properties": {}
            },
            {
              "id": "nORcuBtbnzBZ",
              "ref": "e2b500df-7800-4719-9d46-e461523fe917",
              "type": "short_text",
              "title": "Where is the job located?",
              "properties": {}
            },
            {
              "id": "hhV0z2H3bFbC",
              "ref": "3214f31d-6cf6-450f-ad24-c96fc3ceac4f",
              "type": "short_text",
              "title": "What's the company name?",
              "properties": {}
            },
            {
              "id": "dQbDwUKSTl7G",
              "ref": "7133f736-f8a6-4402-963e-4ae73659381c",
              "type": "short_text",
              "title": "What's the job title?",
              "properties": {}
            },
            {
              "id": "xeaPZrcMGmR4",
              "ref": "3188cfb5-5052-4560-b51a-de40bdd46c02",
              "type": "date",
              "title": "What is the date of the interview?",
              "properties": {}
            },
            {
              "id": "yFyfpcjPDaal",
              "ref": "d420f7cf-3ba4-4c05-9ba6-65b4b28d610b",
              "type": "multiple_choice",
              "title": "At what stage of the interview process are you?",
              "properties": {},
              "allow_other_choice": true,
              "choices": [
                {
                  "id": "9t696Z9y3nut",
                  "ref": "d535511c-9673-4eed-bda6-a0a6bddbfb62",
                  "label": "1st Interview"
                },
                {
                  "id": "nWtTrKwFuRFJ",
                  "ref": "ad5a3a3a-ab2f-46c6-ae2d-83886b89675e",
                  "label": "2nd Interview"
                },
                {
                  "id": "i3QvsZc7QWsD",
                  "ref": "e0623676-917f-4e06-b6f2-2a7ec4eb7613",
                  "label": "3rd Interview"
                },
                {
                  "id": "BEdzETAKeo3X",
                  "ref": "3a796874-9a79-46d1-ac1e-351157e7dd85",
                  "label": "4th Interview"
                },
                {
                  "id": "SUsLNaO5oQeO",
                  "ref": "9e03dbda-b485-4fb3-af87-742d2f399bbb",
                  "label": "5th Interview"
                }
              ]
            },
            {
              "id": "BVIHyvpqVsNS",
              "ref": "63e73707-bd3e-43a1-93fb-58c8b0b46804",
              "type": "multiple_choice",
              "title": "What is the nature of this interview?",
              "properties": {},
              "allow_other_choice": true,
              "choices": [
                {
                  "id": "4qVioivfiAgz",
                  "ref": "95564391-262d-454a-a1ab-a03ad29e02de",
                  "label": "HR Interview"
                },
                {
                  "id": "t03pSZv6pRqa",
                  "ref": "e5982a75-d9b2-48da-986f-fcdc2d7b1549",
                  "label": "Technical Interview"
                },
                {
                  "id": "1zNdjKQi0I9z",
                  "ref": "49000ec4-6db0-49f1-9404-cca080026272",
                  "label": "Time limited test"
                },
                {
                  "id": "SAYvmvWrYSvv",
                  "ref": "80bcaace-76f1-4b55-af38-de64f5c66972",
                  "label": "Home assignment"
                },
                {
                  "id": "llQxtTnckiH1",
                  "ref": "120cdd04-6ca5-4741-ba11-dbe47c1ef167",
                  "label": "Phone Screening"
                },
                {
                  "id": "edMkNQltv1Rw",
                  "ref": "b2942204-2103-4c75-af00-c3cdc8ae2369",
                  "label": "Final Interview"
                },
                {
                  "id": "TgwI7sq1a6jx",
                  "ref": "2d499596-632e-48af-a2a8-37c0f1daf604",
                  "label": "General (HR + Tech)"
                }
              ]
            },
            {
              "id": "qgbW21oTd1mO",
              "ref": "e23f96eb-55e0-40d5-97fd-d78f8ba43513",
              "type": "file_upload",
              "title": "Please upload the home assignment",
              "properties": {}
            },
            {
              "id": "YIXeDQWMVqLr",
              "ref": "37260b31-5b25-4ca7-b9d4-2bd4ae57d1fd",
              "type": "file_upload",
              "title": "Please upload the resume you sent for this {{field:7133f736-f8a6-4402-963e-4ae73659381c}} role ",
              "properties": {}
            },
            {
              "id": "06oyTS92IyDZ",
              "ref": "5c7d3104-6a5a-49a0-8d38-b749e3227847",
              "type": "file_upload",
              "title": "Please upload a .pdf file of the {{field:7133f736-f8a6-4402-963e-4ae73659381c}} description`",
              "properties": {}
            },
            {
              "id": "n6j9MkBtbqcF",
              "ref": "9ec5d4d0-1f7a-4552-9e7a-455a89918995",
              "type": "multiple_choice",
              "title": "Where did you find the job opportunity?",
              "properties": {},
              "allow_other_choice": true,
              "choices": [
                {
                  "id": "Pp6PvPP3o9Ab",
                  "ref": "d1be6a3f-25bc-44e1-9a4b-ab359d29bd25",
                  "label": "Smart Matching"
                },
                {
                  "id": "Zt94rGdIBP62",
                  "ref": "5dfa8c84-1e38-4cb2-8b59-816892d1d21a",
                  "label": "Online"
                },
                {
                  "id": "CyRsNU627xj7",
                  "ref": "8974ee1a-fe8b-492d-9bea-dc4e231dba74",
                  "label": "Offline"
                }
              ]
            },
            {
              "id": "ysVEuC3W9lKV",
              "ref": "bdd70691-5ac8-477c-91d4-e9cadfda6381",
              "type": "multiple_choice",
              "title": "Where did you find that opportunity?",
              "properties": {},
              "allow_other_choice": true,
              "choices": [
                {
                  "id": "BrmEPlFJ2VXh",
                  "ref": "32247479-3fd5-4dbc-a88e-0dff67a3943e",
                  "label": "Facebook Groups"
                },
                {
                  "id": "Sny3kRr9V4tJ",
                  "ref": "566ecf5e-b9ca-49a0-ac37-1f6006423d0f",
                  "label": "Facebook ads"
                },
                {
                  "id": "aiLri8HvR8yH",
                  "ref": "4e95f673-3119-4d78-b2c0-b41cc4335b5c",
                  "label": "Facebook share"
                },
                {
                  "id": "1q94Tiwa38KW",
                  "ref": "14d4b707-7e1e-464f-9f1e-c6ee59cfe236",
                  "label": "Indeed"
                },
                {
                  "id": "3WhD2yi1gBG7",
                  "ref": "b447179b-e057-42a3-903b-21ebbc9b2733",
                  "label": "LinkedIn group"
                },
                {
                  "id": "ykK1xtUmEebq",
                  "ref": "2198c462-5531-4c4d-a1a9-46f7ff20b729",
                  "label": "LinkedIn connection"
                },
                {
                  "id": "ZsCHx4ARWJ6z",
                  "ref": "85f4fe2e-8d5a-44d1-93c3-c1911ce0373e",
                  "label": "Company website"
                }
              ]
            }
          ],
          "endings": [
            {
              "id": "QrQ8owCb2KCZ",
              "ref": "d8189f1c-473c-4580-a456-8f2bbb0ab42f",
              "title": "Data Mock Interview",
              "type": "url_redirect",
              "properties": {
                "redirect_url": "https://calendly.com/d/ckfb-5w9-htp/mock-interview?utm_source={{field:29311df9-c5ea-4e4c-99ae-ff5c08bfdf43}}&utm_medium={{field:3214f31d-6cf6-450f-ad24-c96fc3ceac4f}}&utm_content={{field:d420f7cf-3ba4-4c05-9ba6-65b4b28d610b}}"
              }
            }
          ]
        },
        "answers": [
          {
            "type": "choice",
            "choice": {
              "id": "8vj2WzjQUVfT",
              "label": "Data",
              "ref": "4f7641d6-2ccb-4141-817c-d024f6d29be5"
            },
            "field": {
              "id": "uGidsoDwfCES",
              "type": "dropdown",
              "ref": "1872f227-7c08-4651-b5aa-0c16fe0a4b68"
            }
          },
          {
            "type": "email",
            "email": "ronrevensari@gmail.com",
            "field": {
              "id": "FBYMmvdFNhfw",
              "type": "email",
              "ref": "cac2e68b-c202-49d4-82ed-342fdac8bb0b"
            }
          },
          {
            "type": "text",
            "text": "Ron Revensari",
            "field": {
              "id": "Kys4EcJ4WViT",
              "type": "short_text",
              "ref": "29311df9-c5ea-4e4c-99ae-ff5c08bfdf43"
            }
          },
          {
            "type": "text",
            "text": "Israel - IL",
            "field": {
              "id": "nORcuBtbnzBZ",
              "type": "short_text",
              "ref": "e2b500df-7800-4719-9d46-e461523fe917"
            }
          },
          {
            "type": "text",
            "text": "Assured Allies",
            "field": {
              "id": "hhV0z2H3bFbC",
              "type": "short_text",
              "ref": "3214f31d-6cf6-450f-ad24-c96fc3ceac4f"
            }
          },
          {
            "type": "text",
            "text": "Junior Quantitative Researcher",
            "field": {
              "id": "dQbDwUKSTl7G",
              "type": "short_text",
              "ref": "7133f736-f8a6-4402-963e-4ae73659381c"
            }
          },
          {
            "type": "date",
            "date": "2024-06-02",
            "field": {
              "id": "xeaPZrcMGmR4",
              "type": "date",
              "ref": "3188cfb5-5052-4560-b51a-de40bdd46c02"
            }
          },
          {
            "type": "choice",
            "choice": {
              "id": "9t696Z9y3nut",
              "label": "1st Interview",
              "ref": "d535511c-9673-4eed-bda6-a0a6bddbfb62"
            },
            "field": {
              "id": "yFyfpcjPDaal",
              "type": "multiple_choice",
              "ref": "d420f7cf-3ba4-4c05-9ba6-65b4b28d610b"
            }
          },
          {
            "type": "choice",
            "choice": {
              "id": "SAYvmvWrYSvv",
              "label": "Home assignment",
              "ref": "80bcaace-76f1-4b55-af38-de64f5c66972"
            },
            "field": {
              "id": "BVIHyvpqVsNS",
              "type": "multiple_choice",
              "ref": "63e73707-bd3e-43a1-93fb-58c8b0b46804"
            }
          },
          {
            "type": "file_url",
            "file_url": "https://api.typeform.com/responses/files/1a5003b6804731cfaaf96ddeca73f5b6c9224a2658530b0c39db9cd72a98f279/Junior_Quantitative_Researcher___Interview_Exercise_4.pdf",
            "field": {
              "id": "qgbW21oTd1mO",
              "type": "file_upload",
              "ref": "e23f96eb-55e0-40d5-97fd-d78f8ba43513"
            }
          },
          {
            "type": "file_url",
            "file_url": "https://api.typeform.com/responses/files/1c52a986ef071e0a8ec510cb6b4d9d926d5de924db49420b7205102b5f485e82/Ron_Revensari___C.V..pdf",
            "field": {
              "id": "YIXeDQWMVqLr",
              "type": "file_upload",
              "ref": "37260b31-5b25-4ca7-b9d4-2bd4ae57d1fd"
            }
          },
          {
            "type": "file_url",
            "file_url": "https://api.typeform.com/responses/files/1436acd74431032f2677840615fdbeeb71d82206c8ca44a444561a6b3c69d12d/Junior_Quantitative_Researcher.pdf",
            "field": {
              "id": "06oyTS92IyDZ",
              "type": "file_upload",
              "ref": "5c7d3104-6a5a-49a0-8d38-b749e3227847"
            }
          },
          {
            "type": "choice",
            "choice": {
              "id": "Zt94rGdIBP62",
              "label": "Online",
              "ref": "5dfa8c84-1e38-4cb2-8b59-816892d1d21a"
            },
            "field": {
              "id": "n6j9MkBtbqcF",
              "type": "multiple_choice",
              "ref": "9ec5d4d0-1f7a-4552-9e7a-455a89918995"
            }
          },
          {
            "type": "choice",
            "choice": {
              "other": "Linkedin job search"
            },
            "field": {
              "id": "ysVEuC3W9lKV",
              "type": "multiple_choice",
              "ref": "bdd70691-5ac8-477c-91d4-e9cadfda6381"
            }
          }
        ],
        "ending": {
          "id": "QrQ8owCb2KCZ",
          "ref": "d8189f1c-473c-4580-a456-8f2bbb0ab42f"
        }
      }
    }
    """
    payload = json.loads(test)
    
    final_ = parse_and_write_to_db_new_processes(payload, 'typeform')
    print(final_)