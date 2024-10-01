from typing import Set, Dict

V3_PASSING_INTERVIEWS_DEAL_PROCESS_KEYS: Set[str] = {
    "id", "hubspot_id", "domain", "hubspot_deal_id",
    "company_name", "job_title", "process_start_date",
    "student_first_name", "student_last_name",
    "source_1", "source_2"
}

V3_PASSING_INTERVIEWS_DEAL_STAGE_IN_PROCESS_KEYS: Set[str] = {
    "id", "hubspot_deal_id", "stage_in_funnel",
    "type_of_stage", "deal_stage", "stage_date"
}

V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING: Dict[str, str] = {
    "62780568": "Dropped",
    "62515535": "Active",
    "62780567": "Graduated"
}

V2_OC2FP_STATUS_DEAL_STAGE_MAPPING: Dict[str, str] = {
    "161070366": "Closed won",
 "161070367": "Closed lost"}

MARKETING_MQL_DATE_OBJECTS = ['hubspot_created_at', 'date_mql_entered', 'date_sql_entered', 'date_bg_enrolled_entered',
                       'date_submitted_typeform_entered']


GETTING_INTERVIEW_KNOWN_STAGES: Set[str] = {
            "Job Ready", "1st CSA Meeting Conducted", "Material Ready", "Job Seeking",
            "Contacted by Employer", "Closed Lost - Ghost", "Closed Won - Got an Interview"}