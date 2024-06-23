from global_functions.LoggingGenerator import Logger
import os
from flask_smorest import abort

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def job_ready_catch_deal_stage(_data):
    """ Whewnever a deal (student) changes their deal stage, we need to update the deal stage in the database."""
    
    id_to_name = {
            175176966: "Job Ready",
            175176967: "1st CSA Meeting Conducted",
            175175968: "Material Ready",
            175176969: "Job Seeking",
            175176970: "Contacted by Employer",
            175176971: "Closed Won",
            175176972: "Closed Lost"
    }
    
    if _data.get("dealstage") not in id_to_name.keys():
        logger.error(f"Deal with details: {_data} is not matching")
        abort(404, message='no deal stage found')

    if str(_data.get('hs_object_id')) == '210181603':
        logger.error(f"Deal with details: {_data} is not matching")
        abort(404, message='no deal stage found')

    identifying_dict = dict(hubspot_id=str(_data.get("hs_object_id")),
                            csa_fullname=_data.get("hubspot_owner_id"),
                            hubspot_current_deal_stage=id_to_name[_data.get("dealstage")])
    
    return identifying_dict


if __name__ == '__main__':
    data = {'company': 'Cognosante', 'dealname': '🎉Ranga Hande', 'job_title': 'DOL-NCC Junior Reports Analyst',
            'hs_object_id': 19238354435, 'hs_is_closed_won': False}
    data_2 = {'company': 'New River Strategies', 'dealname': '🎉Michael DePasquale', 'job_title': 'Data Analyst',
              'hs_object_id': 58997101, 'hs_is_closed_won': True}
