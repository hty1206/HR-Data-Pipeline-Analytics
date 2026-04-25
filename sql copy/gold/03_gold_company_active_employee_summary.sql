CREATE OR REPLACE VIEW gold_company_summary AS
SELECT 
    COUNT(*) as Total_Employees,
    ROUND(AVG(Salary), 2) as Company_Avg_Salary,
    ROUND(AVG(Age), 1) as Company_Avg_Age,
    ROUND(AVG(Tenure_Years), 1) as Avg_Tenure_Years
FROM hr_employees_silver;

SELECT * FROM gold_company_summary;