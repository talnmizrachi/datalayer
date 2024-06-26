def v3_catch_new_job_ready(_data):
    identifying_dict = dict(company=_data.get("company"),
                            dealname=_data.get("dealname").replace(chr(127881), ""),
                            job_title=_data.get("job_title"),
                            hs_object_id=str(_data.get("hs_object_id")),
                            hs_is_closed_won=_data.get("hs_is_closed_won"))
    
    return identifying_dict
    

if __name__ == '__main__':
    data = {'company': 'Cognosante', 'dealname': '🎉Ranga Hande', 'job_title': 'DOL-NCC Junior Reports Analyst',
            'hs_object_id': 19238354435, 'hs_is_closed_won': False}
    data_2 = {'company': 'New River Strategies', 'dealname': '🎉Michael DePasquale', 'job_title': 'Data Analyst',
              'hs_object_id': 58997101, 'hs_is_closed_won': True}
    

