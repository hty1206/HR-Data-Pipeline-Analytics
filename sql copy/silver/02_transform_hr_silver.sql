TRUNCATE TABLE hr_employees_silver;

REPLACE INTO hr_employees_silver
SELECT 
    CAST(NULLIF(TRIM(EmpID), '') AS UNSIGNED),
    TRIM(Employee_Name),
    
    CAST(NULLIF(NULLIF(NULLIF(TRIM(MarriedID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(MaritalStatusID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(GenderID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(EmpStatusID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(DeptID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(PerfScoreID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(PositionID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(ManagerID), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(FromDiversityJobFairID), 'NaN'), '?'), '') AS UNSIGNED),

    CAST(NULLIF(NULLIF(NULLIF(TRIM(Salary), 'NaN'), '?'), '') AS DECIMAL(12, 2)),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(Termd), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(EngagementSurvey), 'NaN'), '?'), '') AS DECIMAL(5, 2)),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(EmpSatisfaction), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(SpecialProjectsCount), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(DaysLateLast30), 'NaN'), '?'), '') AS UNSIGNED),
    CAST(NULLIF(NULLIF(NULLIF(TRIM(Absences), 'NaN'), '?'), '') AS UNSIGNED),

    CASE 
        WHEN STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y') > CURDATE()
        THEN DATE_SUB(STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y'), INTERVAL 100 YEAR)
        ELSE STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y')
    END,
    STR_TO_DATE(NULLIF(NULLIF(TRIM(DateofHire), 'NaN'), ''), '%m/%d/%Y'),
    STR_TO_DATE(NULLIF(NULLIF(TRIM(DateofTermination), 'NaN'), ''), '%m/%d/%Y'),
    STR_TO_DATE(NULLIF(NULLIF(TRIM(LastPerformanceReview_Date), 'NaN'), ''), '%m/%d/%Y'),

    UPPER(TRIM(Sex)),
    TRIM(Position),
    TRIM(State),
    TRIM(Zip),
    TRIM(MaritalDesc),
    TRIM(CitizenDesc),
    TRIM(HispanicLatino),
    TRIM(RaceDesc),
    TRIM(TermReason),
    TRIM(EmploymentStatus),
    TRIM(Department),
    TRIM(ManagerName),
    TRIM(RecruitmentSource),
    TRIM(PerformanceScore),

    TIMESTAMPDIFF(YEAR, 
        CASE 
            WHEN STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y') > CURDATE()
            THEN DATE_SUB(STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y'), INTERVAL 100 YEAR)
            ELSE STR_TO_DATE(NULLIF(NULLIF(TRIM(DOB), 'NaN'), ''), '%m/%d/%y')
        END, CURDATE()) AS Age,
    ROUND(TIMESTAMPDIFF(MONTH, 
        STR_TO_DATE(NULLIF(NULLIF(TRIM(DateofHire), 'NaN'), ''), '%m/%d/%Y'), 
        COALESCE(STR_TO_DATE(NULLIF(NULLIF(TRIM(DateofTermination), 'NaN'), ''), '%m/%d/%Y'), CURDATE())
    ) / 12, 1) AS Tenure_Years
FROM hr_raw_data;