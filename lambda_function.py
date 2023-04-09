import json

def validate(slots):

    valid_cities = ['tunis','ariana','sfax',]
    
    if not slots['city']:
        print("Inside Empty city")
        return {
        'isValid': False,
        'violatedSlot': 'city'
        }        
        
    if slots['city']['value']['originalValue'].lower() not in  valid_cities:
        
        print("Not Valid city")
        
        return {
        'isValid': False,
        'violatedSlot': 'city',
        'message': 'We currently  support only {} as a valid destination.?'.format(", ".join(valid_cities))
        }
        
    if not slots['checkindate']:
        
        return {
        'isValid': False,
        'violatedSlot': 'checkindate',
    }
        
    if not slots['days']:
        return {
        'isValid': False,
        'violatedSlot': 'days'
    }
        
    if not slots['roomtype']:
        return {
        'isValid': False,
        'violatedSlot': 'roomtype'
    }

    return {'isValid': True}

def lambda_handler(event, context):
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
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
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
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
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
            return response
            

    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        # Add order in Database
        
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
                "content": "Thanks, I have placed your reservation"
            }
        ]
    }
            
        return response
        
          