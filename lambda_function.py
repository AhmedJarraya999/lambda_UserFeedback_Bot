import json
import boto3

def validate(slots):

    valid_score = ['1', '2', '3', '4', '5']
    valid_studyfield = ['DS', 'AI', 'ARCTIC', 'TWIN', 'BI', 'SAE', 'GAMIX', 'INFINI', 'NIDS', 'SIM']
    
    if not slots['score']:
        print("Inside Empty score")
        return {
            'isValid': False,
            'violatedSlot': 'score'
        }        
        
    if slots['score']['value']['originalValue'] not in valid_score:
        print("Not Valid score")
        return {
            'isValid': False,
            'violatedSlot': 'score',
            'message': 'We currently support only {} as a valid score.'.format(", ".join(map(str, valid_score)))
        }
        
    if not slots['studyfield']:
        print("Inside Empty studyfield")
        return {
            'isValid': False,
            'violatedSlot': 'studyfield'
        }        
        
    if slots['studyfield']['value']['originalValue'].upper() not in valid_studyfield:
        print("Not Valid studyfield")
        return {
            'isValid': False,
            'violatedSlot': 'studyfield',
            'message': 'We currently support only {} as a valid study field.'.format(", ".join(valid_studyfield))
        }
        
    if not slots['skill1']:
        return {
            'isValid': False,
            'violatedSlot': 'skill1',
        }
        
    if not slots['skill2']:
        return {
            'isValid': False,
            'violatedSlot': 'skill2'
        }
        
    if not slots['skill3']:
        return {
            'isValid': False,
            'violatedSlot': 'skill3'
        }
    
    if not slots['suggestions']:
        return {
            'isValid': False,
            'violatedSlot': 'suggestions'
        }

    return {'isValid': True}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('feedbacks')


def lambda_handler(event, context):
    
  
    
    
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    
    validation_result = validate(slots)
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            'slotToElicit': validation_result['violatedSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            'name': intent,
                            'slots': slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result['message']
                        }
                    ]
                } 
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            'slotToElicit': validation_result['violatedSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            'name': intent,
                            'slots': slots
                        }
                    }
                } 
            return response
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':


        # Add order in Database
        item = {
            'score': slots['score']['value']['originalValue'],
            'studyfield': slots['studyfield']['value']['originalValue'],
            'skill1': slots['skill1']['value']['originalValue'],
            'skill2': slots['skill2']['value']['originalValue'],
            'skill3': slots['skill3']['value']['originalValue'],
            'suggestions': slots['suggestions']['value']['originalValue']
        }

        table.put_item(Item=item)

        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Thanks, I got your feedback"
            }
        ]
    }
            
        return response