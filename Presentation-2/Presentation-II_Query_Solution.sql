-- Presentation-II Query Solution
-- Query: Check Rohan Verma's application and job details

USE recruitmentdb;

SELECT
    a.applicant_name,
    ap.application_id,
    ap.application_date,
    ap.application_status,
    j.job_id,
    j.job_title,
    j.openings,
    j.salary,
    j.job_status
FROM applicant a
JOIN application ap
    ON a.applicant_id = ap.applicant_id
JOIN job j
    ON ap.job_id = j.job_id
WHERE a.applicant_name = 'Rohan Verma';

-- Expected result:
-- Rohan Verma | 403 | 2026-09-03 | Pending | 202 | Software Developer | 5 | 700000.00 | Open
