from global_functions.time_functions import last_thursday_getter


def process_form_response(payload):
    # Extract necessary fields from payload
    email = payload['form_response']['hidden']['email']
    submit_date = payload['form_response']['submitted_at']
    answers = {answer['field']['ref']: answer['number'] if answer['type'] == 'number' else answer['choice']['label']
               for answer in payload['form_response']['answers']}
    
    result = {
            'email': email,
            'date_of_review': submit_date,
            'corrected_date_of_review': last_thursday_getter(submit_date).strftime("%Y-%m-%d"),
            "instruction": answers.get('question_6'),
            "mentorship": answers.get('question_10'),
            "overall_experience": answers.get('question_12')
    }
    
    
    return result
