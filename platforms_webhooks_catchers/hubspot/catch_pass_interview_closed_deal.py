def v3_pass_close_deal_webhook_catcher(_data):
    identifying_dict = dict(company=_data.get("company"),
                            dealstage=_data.get("dealstage"),
                            job_title=_data.get("job_title"),
                            hs_object_id=str(_data.get("hs_object_id")),
                            deal_status=_data.get("deal_status"))
    
    return identifying_dict
    

if __name__ == '__main__':
    data = {'company': 'Cognosante', 'dealname': '🎉Ranga Hande', 'job_title': 'DOL-NCC Junior Reports Analyst',
            'hs_object_id': 19238354435, 'hs_is_closed_won': False}
    data_2 = {'company': 'New River Strategies', 'dealname': '🎉Michael DePasquale', 'job_title': 'Data Analyst',
              'hs_object_id': 58997101, 'hs_is_closed_won': True}
    
    a = v3_pass_close_deal_webhook_catcher(data)
    b = v3_pass_close_deal_webhook_catcher(data_2)
    
    print(a)
    print(b)
