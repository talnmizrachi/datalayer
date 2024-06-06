def v3_pass_close_deal_webhook_catcher(data):
    identifying_dict = dict(company=data.get("company"),
                            dealname=data.get("dealname").replace(chr(127881), ""),
                            job_title=data.get("job_title"),
                            hs_object_id=data.get("hs_object_id"),
                            hs_is_closed_won=data.get("hs_is_closed_won"))
    
    return identifying_dict
    
    
data = {'company': 'Cognosante', 'dealname': '🎉Ranga Hande', 'job_title': 'DOL-NCC Junior Reports Analyst',
        'hs_object_id': 19238354435, 'hs_is_closed_won': False}
data_2 = {'company': 'New River Strategies', 'dealname': '🎉Michael DePasquale', 'job_title': 'Data Analyst',
          'hs_object_id': 58997101, 'hs_is_closed_won': True}

if __name__ == '__main__':
    a = v3_pass_close_deal_webhook_catcher(data)
    b = v3_pass_close_deal_webhook_catcher(data_2)
    
    print(a)
    print(b)
