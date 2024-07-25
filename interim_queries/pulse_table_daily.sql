-- CTE for counting students who are ready for job placement or onboarding
with job_ready_students_count as (
    select count(*) as job_ready_students_count
    from job_ready_students
    where hubspot_current_deal_stage in ('Job Ready', 'Onboarding')
),

-- CTE for counting the number of applications received today
daily_applications as (
    select count(*) as daily_applications
    from student_applications
    where student_applied is true
    and date(student_response_timestamp) = current_date
),

-- CTE for counting students actively seeking jobs
active_job_searchers as (
    select count(*) as active_job_searchers
    from job_ready_students
    where hubspot_current_deal_stage in ('Job Seeking', 'Contacted by Employer', 'Closed Won - Got an Interview', 'First Interview Scheduled', 'First Interview', 'Additional Interview', 'Final Interview', 'Job Offer Received')
),

-- CTE for counting ongoing interview processes and distinct students involved
interview_processes as (
    select
        count(*) as interview_process_count,
        count(distinct hubspot_id) as students_with_interview_process
    from job_ready_students
    where hubspot_current_deal_stage in (
        'First Interview Scheduled', 'First Interview', 'Additional Interview', 'Final Interview', 'Job Offer Received'
    )
),

-- CTE for counting callbacks made to students today
daily_callbacks as (
    select count(*) as daily_callbacks_count
    from student_deal_stages
    where date(created_at) = current_date
    and stage = 'Contacted by Employer'
),

-- CTE for counting callbacks made this month
cummulative_callbacks as (
    select count(*) as this_month_callbacks
    from student_deal_stages
    where extract(month from created_at) = extract(month from current_date)
    and extract(year from created_at) = extract(year from current_date)
    and stage = 'Contacted by Employer'
),

-- CTE for counting applications received this month
cummulative_monthly_applications as (
    select count(*) as cumm_monthly_applications
    from student_applications
    where student_applied is true
    and extract(month from student_response_timestamp) = extract(month from current_date)
    and extract(year from student_response_timestamp) = extract(year from current_date)
),

-- CTE for counting job placements made today
daily_placements as (
    select count(*) as daily_placements
    from student_deal_stages
    where date(created_at) = current_date
    and stage = 'Closed Won - Job Secured'
),

-- CTE for counting cumulative monthly job placements
monthly_cummulative_placements as (
    select count(*) as monthly_cummulative_placements
    from student_deal_stages
    where extract(month from created_at) = extract(month from current_date)
    and extract(year from created_at) = extract(year from current_date)
    and stage = 'Closed Won - Job Secured'
),

-- CTE for counting cumulative yearly job placements
yearly_cummulative_placements as (
    select count(*) as yearly_cummulative_placements
    from student_deal_stages
    where extract(year from created_at) = extract(year from current_date)
    and stage = 'Closed Won - Job Secured'
),

-- CTE for summing revenue from placements made today
daily_placements_revenue as (
    select coalesce(sum(amount), 0) as todays_revenue
    from student_new_payment
    where date(created_at) = current_date
),

-- CTE for summing revenue from placements made this month
monthly_placements_revenue as (
    select coalesce(sum(amount), 0) as monthly_placements_revenue
    from student_new_payment
    where extract(month from created_at) = extract(month from current_date)
    and extract(year from created_at) = extract(year from current_date)
),

-- CTE for summing revenue from placements made this year
yearly_placements_revenue as (
    select coalesce(sum(amount), 0) as yearly_placements_revenue
    from student_new_payment
    where extract(year from created_at) = extract(year from current_date)
)

-- Main select statement combining results from above CTEs
select
    current_date as date,
    (select job_ready_students_count from job_ready_students_count) as job_ready_students,
    (select active_job_searchers from active_job_searchers) as active_job_searchers,
    (select daily_applications from daily_applications) as daily_applications,
    (select interview_process_count from interview_processes) as interview_process_count,
    (select students_with_interview_process from interview_processes) as students_with_interview_process,
    (select daily_callbacks_count from daily_callbacks) as daily_callbacks,
    (select this_month_callbacks from cummulative_callbacks) as this_month_callbacks,
    (select cumm_monthly_applications from cummulative_monthly_applications) as cummulative_monthly_applications,
    100 * round((select this_month_callbacks::decimal from cummulative_callbacks) / (select cumm_monthly_applications from cummulative_monthly_applications), 4) as cvr_callback_to_applications,
    (select daily_placements from daily_placements) as daily_placements,
    (select monthly_cummulative_placements from monthly_cummulative_placements) as monthly_cummulative_placements,
    (select yearly_cummulative_placements from yearly_cummulative_placements) as yearly_cummulative_placements,
    100 * round((select monthly_cummulative_placements::decimal from monthly_cummulative_placements) / (select this_month_callbacks::decimal from cummulative_callbacks), 4) as cvr_placement_to_callback,
    (select todays_revenue from daily_placements_revenue) as placement_revenue,
    (select monthly_placements_revenue from monthly_placements_revenue) as monthly_placements_revenue,
    (select yearly_placements_revenue from yearly_placements_revenue) as yearly_placements_revenue;
