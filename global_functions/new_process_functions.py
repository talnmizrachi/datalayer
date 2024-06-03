from uuid import uuid4
from datetime import date


def payload_to_new_process_dict(payload):
	job_ready_student_dict = {
		"job_id": payload.get("job_id"),
		"student_id": payload.get("student_id"),
		"student_firstname": payload.get("student_firstname"),
		"student_lastname": payload.get("student_lastname"),
		"domain": payload.get("domain"),
		"company_name": payload.get("company_name"),
		"job_title": payload.get("job_title"),
		"job_description": payload.get("job_description"),
		"drive_url": payload.get("drive_url"),
		"process_start_date": date.today(),
		"process_end_date": payload.get("process_end_date"),
		"is_process_active": payload.get("is_process_active", True),
		"is_closed_won": payload.get("is_closed_won"),
	}
	return job_ready_student_dict





if __name__ == '__main__':
	print(date.today())
