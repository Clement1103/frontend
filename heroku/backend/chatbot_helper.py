import re

from starlette.responses import JSONResponse


def check_if_presentation_product(intent: str):
    if re.match(r'^presentation\.(\w+)\s+-\s+context:\s+(.+)$', intent):
        return True
    else:
        return False

def get_product_name(intent: str):
    match = re.search(r'^presentation\.(\w+)\s+-\s+context:\s+(.+)$', intent)
    return match.group(1) if match else None

def check_interest(intent: str):
    match = re.match(r'^capture.of\.(\w+)\s+-\s+context:\s+(.+)$', intent)
    if match:
        if match.group(1)=='interest':
            return True
        elif match.group(1)=='disinterest':
            return False
    else:
        return -1

def check_coordinates(parameters):
    phone_nb = parameters['phone-number']
    email_address = parameters['email']
    if email_address == '' and phone_nb =='':
        fulfillmentText = 'Please, enter correct pieces of information.'
    elif email_address =='':
        fulfillmentText = (f'Is the following phone number correct: \n'
                           f'{phone_nb}')
    elif phone_nb =='':
        fulfillmentText = (f'Is the following e-mail address correct: \n'
                           f'{email_address}')
    else:
        fulfillmentText = (f'Are the following information correct: \n'
                           f'Email address: {email_address}\n'
                           f'Phone number: {phone_nb}')

    return fulfillmentText, email_address, phone_nb

def coordinates_correct():
    pass

def get_session_id(context: str):
    match = re.search(r'sessions/(.*?)/contexts', context)
    return match.group(1) if match else None

# if __name__ == '__main__':
#     context = 'projects/chatbot-health-wmdg/agent/sessions/cbb0e726-3d6e-26fe-8f98-7e3fd513eb5a/contexts/ongoing-presentation'
#     intent = 'presentation.SyntheMedix - context: ongoing-presentation'
#     # intent_bis = 'coordinates.incorrect'
#     # intent_ter = 'presentation.ForecastMed - context: interest-capture'
#     # product_name = get_product_name(intent)
#     # print(product_name)
#     # print('================')
#     # print(check_if_presentation_product(intent))
#     # print(check_if_presentation_product(intent_ter))
#     # print(check_if_presentation_product(intent_bis))
#     intent_interest = 'capture.of.interest - context: ongoing presentation'
#     intent_disinterest = 'capture.of.disinterest - context: ongoing presentation'
#     print('Expected: -1 === got: ', check_interest(intent))
#     print('Expected: True === got: ', check_interest(intent_interest))
#     print('Expected: False === got: ', check_interest(intent_disinterest))
#     # print(get_session_id(context))