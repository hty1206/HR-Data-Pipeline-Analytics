CREATE OR REPLACE VIEW gold_dept_performance AS
SELECT
	Department,
    COUNT(*) as Emp_Count,
    ROUND(AVG(Salary), 0) as Avg_Salary,
    ROUND(AVG(SatisfactionScore), 2) as Avg_Satisfaction,
    ROUND(AVG(EngagementScore), 2) as Avg_Engagement,
    ROUND(AVG(Absences), 1) as Avg_Absences,
    ROUND(AVG(Tenure_Years), 1) as Avg_Tenure_Years,
    ROUND(AVG(Age), 1) as Avg_Age
FROM hr_employees_silver
WHERE EmploymentStatus = 'Active'
GROUP BY Department;

SELECT * FROM gold_dept_performance