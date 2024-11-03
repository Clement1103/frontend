from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db_helper import *
from chatbot_helper import *

app = FastAPI()

# uvicorn main:app --reload
# ngrok http 8000


sessions = {}

@app.post('/')
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts'][0]['name']

    session_id = get_session_id(output_contexts)

    print('===', intent, '===')

    if session_id not in sessions:
        sessions[session_id] = {
            'product_tmp': None,
            'list_interests': []
        }

    user_session = sessions[session_id]

    if check_if_presentation_product(intent):
        user_session['product_tmp'] = get_product_name(intent)
        # print('Produit capté :', user_session['product_tmp'])

    is_interested = check_interest(intent)
    # print('IS INTERESTED: ', is_interested)
    # print('PRODUCT TMP: ', user_session['product_tmp'])

    if is_interested is True and user_session['product_tmp']:
        user_session['list_interests'].append(user_session['product_tmp'])
        user_session['product_tmp'] = ''

    if intent == 'check.coordinates' or intent == 'coordinates.incorrect':
        (fulfillmentText, email, phone_nb) = check_coordinates(parameters)
        user_session['email_tmp']=email
        user_session['phone_tmp'] = phone_nb
        return JSONResponse(content={
            'fulfillmentText': fulfillmentText
        })

    if intent == 'coordinates.correct':
        user_session['email'] = user_session['email_tmp']
        user_session['phone'] = user_session['phone_tmp']
        user_session['email_tmp'] = ''
        user_session['phone_tmp'] = ''
        save_to_db(user_session)
        user_session['list_interests'] = []

    # print('====', user_session['list_interests'], '====')
    # print('==========', user_session, '==========')
