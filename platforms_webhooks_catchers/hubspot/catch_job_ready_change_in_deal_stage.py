def job_ready_catch_deal_stage(_data):
    """ Whewnever a deal (student) changes their deal stage, we need to update the deal stage in the database."""
    identifying_dict = dict(hubspot_id=_data.get("hs_object_id"),
                            hubspot_current_deal_stage=_data.get("dealstage")
                           )
    
    return identifying_dict
    

if __name__ == '__main__':
    data = {'company': 'Cognosante', 'dealname': '🎉Ranga Hande', 'job_title': 'DOL-NCC Junior Reports Analyst',
            'hs_object_id': 19238354435, 'hs_is_closed_won': False}
    data_2 = {'company': 'New River Strategies', 'dealname': '🎉Michael DePasquale', 'job_title': 'Data Analyst',
              'hs_object_id': 58997101, 'hs_is_closed_won': True}
    

