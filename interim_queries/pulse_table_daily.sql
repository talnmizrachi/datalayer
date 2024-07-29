with job_ready_students_count as (
    select count(*) as job_ready_students_count
from job_ready_students
where true
    and hubspot_current_deal_stage in ('Job Ready', 'Onboarding')
),
daily_applications as (
select count(*) as daily_applications
from student_applications
where true
  and student_applied is true
and date(student_response_timestamp)=current_date
),
active_job_searchers as (
select count(*) active_job_searchers
from job_ready_students
where true
and hubspot_current_deal_stage in ('Job Seeking', 'Contacted by Employer', 'Closed Won - Got an Interview', 'First Interview Scheduled', 'First Interview', 'Additional Interview', 'Final Interview', 'Job Offer Received')
 ),
interview_processes as (
    select
    count(*) as interview_process_count
    , count(distinct hubspot_id) as students_with_interview_process
from job_ready_students
where true
and hubspot_current_deal_stage in (
    'First Interview Scheduled','First Interview','Additional Interview','Final Interview','Job Offer Received')
),
daily_callbacks as (
select count(*) daily_callbacks_count
from student_deal_stages
where true
and date(created_at) = current_date
and stage ='Contacted by Employer'
),
    cummulative_callbacks as (
        select count(*) this_month_callbacks
from student_deal_stages
where true
and extract(month from created_at) = extract(month from current_date)
and extract(year from created_at) = extract(year from current_date)
and stage ='Contacted by Employer'
    ),
    cummulative_monthly_applications as (
    select count(*) as cumm_monthly_applications
    from student_applications
    where true
    and student_applied is true
    and extract(month from student_response_timestamp) = extract(month from current_date)
    and extract(year from student_response_timestamp) = extract(year from current_date)
),
    daily_placements as (
        select count(*) daily_placements
        from student_deal_stages
        where true
        and date(created_at) = current_date
        and stage ='Closed Won - Job Secured'
    ),
    monthly_cummulative_placements as (
        select count(*) monthly_cummulative_placements
        from student_deal_stages
        where true
          and extract(month from created_at) = extract(month from current_date)
        and extract(year from created_at) = extract(year from current_date)
        and stage ='Closed Won - Job Secured'
    ),
    quarterly_cummulative_placements as (
        select count(*) quarterly_cummulative_placements
        from student_deal_stages
        where true
          and extract(quarter from created_at) = extract(quarter from current_date)
        and extract(year from created_at) = extract(year from current_date)
        and stage ='Closed Won - Job Secured'
    ),
        yearly_cummulative_placements as (
        select count(*) yearly_cummulative_placements
        from student_deal_stages
        where true
        and extract(year from created_at) = extract(year from current_date)
        and stage ='Closed Won - Job Secured'
    ),
    daily_placements_revenue as (
        select coalesce(sum(todays_revenue),0) todays_revenue from(
            select coalesce(sum(amount), 0) todays_revenue
            from student_new_payment
            where true
            and date(created_at)= current_date
            and type_of_collection ='New Placement'
            union
            select amount::double precision todays_revenue
            from another_payments_test_1
            where true
              and created_at <> ''
            and date(created_at) = current_date
          and type_of_collection_code in ('62515535', '62780568')
            and created_at is not null) as daily_placements_revenue
                ),
        monthly_placements_revenue as (
select sum(monthly_placements_revenue)  monthly_placements_revenue from (
select coalesce(sum(amount), 0) monthly_placements_revenue
        from student_new_payment
        where true
          and type_of_collection ='New Placement'
          and extract(month from created_at) = extract(month from current_date)
          and extract(year from created_at) = extract(year from current_date)
union
select sum(amount::double precision)::int monthly_placements_revenue
            from another_payments_test_1
            where true
              and created_at <> ''
            and extract(month from date(created_at)) = extract(month from current_date)
          and extract(year from date(created_at)) = extract(year from current_date)
              and type_of_collection_code in ('62515535', '62780568')
            and created_at is not null)
    ),
        quarterly_placements_revenue as (
            select sum(quarterly_placements_revenue) quarterly_placements_revenue from (
            select coalesce(sum(amount), 0) quarterly_placements_revenue
                    from student_new_payment
                    where true
                      and type_of_collection ='New Placement'
                      and extract(quarter from created_at) = extract(quarter from current_date)
                      and extract(year from created_at) = extract(year from current_date)
            union
            select sum(amount::double precision)::int quarterly_placements_revenue
                        from another_payments_test_1
                        where true
                          and created_at <> ''
                        and extract(quarter from date(created_at)) = extract(quarter from current_date)
                      and extract(year from date(created_at)) = extract(year from current_date)
                          and type_of_collection_code in ('62515535', '62780568')
                        and created_at is not null) quarterly_placements_revenue
                ),
    yearly_placements_revenue as (
select sum(yearly_placements_revenue) yearly_placements_revenue from (
select coalesce(sum(amount), 0) yearly_placements_revenue
        from student_new_payment
        where true
          and type_of_collection ='New Placement'
          and extract(year from created_at) = extract(year from current_date)
union
select sum(amount::double precision)::int yearly_placements_revenue
            from another_payments_test_1
            where true
              and created_at <> ''
          and extract(year from date(created_at)) = extract(year from current_date)
              and type_of_collection_code in ('62515535', '62780568')
            and created_at is not null) yearly_placements_revenue
    )


select
    current_date as date,
    (select job_ready_students_count from job_ready_students_count) as  job_ready_students,
    (select active_job_searchers from active_job_searchers) as  active_job_searchers,
    (select daily_applications from daily_applications) as  daily_applications,
    (select interview_process_count from interview_processes) as  interview_process_count,
    (select students_with_interview_process from interview_processes) as  students_with_interview_process,
    (select daily_callbacks_count from daily_callbacks) as  daily_callbacks,
    (select this_month_callbacks from cummulative_callbacks) as  this_month_callbacks,
    (select cumm_monthly_applications from cummulative_monthly_applications) as  cummulative_monthly_applications,
    100*round((select this_month_callbacks::decimal from cummulative_callbacks) / (select cumm_monthly_applications from cummulative_monthly_applications),4) as cvr_callback_to_applications,
    (select daily_placements from daily_placements) as  daily_placements,
    (select monthly_cummulative_placements from monthly_cummulative_placements) as  monthly_cummulative_placements,
    (select quarterly_cummulative_placements from quarterly_cummulative_placements) as  quarterly_cummulative_placements,
    (select yearly_cummulative_placements from yearly_cummulative_placements) as  yearly_cummulative_placements,
    100*round((select monthly_cummulative_placements from monthly_cummulative_placements) / (select this_month_callbacks::decimal from cummulative_callbacks),4) as cvr_placement_to_callback,
    (select todays_revenue from daily_placements_revenue) as  placement_revenue,
    (select monthly_placements_revenue from monthly_placements_revenue) as  monthly_placements_revenue,
    (select quarterly_placements_revenue from quarterly_placements_revenue) as  quarterly_placements_revenue,
    (select yearly_placements_revenue from yearly_placements_revenue) as  yearly_placements_revenue,
    current_timestamp as updated_at