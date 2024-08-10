
def create_cohort_dict(this_student_hs_id_, active_cohort_):
    cohort_dict = {
            "hubspot_id": this_student_hs_id_,
            "student_cohort": active_cohort_
        
    }
    return cohort_dict


def create_stage_dict(this_student_hs_id_, this_stage_, company_=None):
    stage_dict = {
            "hubspot_id": this_student_hs_id_,
            "stage": this_stage_
    }
    if company_ is not None:
        stage_dict["company_if_rel"] = company_
    
    return stage_dict
