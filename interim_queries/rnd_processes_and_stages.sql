

select *
     ,career_job_callback.career_job_id job_id
     ,contact_id hubspot_id
     , utoc.user_id student_ms_id

     , user_to_details.details->>'program' domain
from career_job_callback
left join assignment_career_job_callback icjc on career_job_callback.id = icjc.callback_id
join user_to_career_job on user_to_career_job.id = career_job_callback.career_job_id
join user_to_onboarded_cohort utoc on career_job_callback.user_id = utoc.user_id
join program on utoc.cohort_id =  program.cohort_id
join _users_with_deleted uwd on career_job_callback.prep_meeting_mentor_user_id = uwd.id
join user_to_details on user_to_career_job.user_id =user_to_details.user_id
-- contact_id => the hubspot id
where contact_id = '218399505'