CREATE OR REPLACE VIEW gold_attrition_detailed AS
WITH all_depts AS (
    SELECT 
        Department, 
        COUNT(*) as Total_Dept_Emp,
        ROUND(AVG(SatisfactionScore), 1) as Dept_Avg_SatisfactionScore
    FROM hr_employees_silver 
    GROUP BY Department
),
attrition_breakdown AS (
    SELECT 
        Department,
        COUNT(*) as Total_Attrition_Count,
        -- 1. 薪資與金錢
        SUM(CASE WHEN TermReason IN ('more money') THEN 1 ELSE 0 END) as Cat_Compensation,
        -- 2. 職業發展與職位
        SUM(CASE WHEN TermReason IN ('Another position', 'retrain', 'career change') THEN 1 ELSE 0 END) as Cat_Career_Growth,
        -- 3. 工作環境與感受
        SUM(CASE WHEN TermReason IN ('unhappy', 'hours', 'attendance', 'no-call, no-show') THEN 1 ELSE 0 END) as Cat_Environment,
        -- 4. 個人與家庭原因
        SUM(CASE WHEN TermReason IN ('relocation', 'maternity leave', 'military', 'medical', 'return to school') THEN 1 ELSE 0 END) as Cat_Personal,
        -- 5. 其他
        SUM(CASE WHEN TermReason NOT IN ('more money', 'Another position', 'retrain', 'career change', 
                                         'unhappy', 'hours', 'attendance', 'no-call, no-show',
                                         'relocation', 'maternity leave', 'military', 'medical', 'return to school') 
                 THEN 1 ELSE 0 END) as Cat_Others,
        
        AVG(SatisfactionScore) AS Avg_Attr_Satisfaction,
        AVG(Tenure_Years) as Avg_Attr_Tenure,
        AVG(Salary) as Avg_Attr_Salary
    FROM hr_employees_silver
    WHERE Termd = 1
    GROUP BY Department
)
SELECT 
    d.Department,
    d.Total_Dept_Emp,
    COALESCE(a.Total_Attrition_Count, 0) as Attrition_Count,
    ROUND(COALESCE(a.Total_Attrition_Count, 0) * 100.0 / d.Total_Dept_Emp, 1) as Attrition_Rate_Percentage,
    
    -- 分類計數
    COALESCE(a.Cat_Compensation, 0) as Count_Compensation,
    COALESCE(a.Cat_Career_Growth, 0) as Count_Career_Growth,
    COALESCE(a.Cat_Environment, 0) as Count_Environment,
    COALESCE(a.Cat_Personal, 0) as Count_Personal,
    COALESCE(a.Cat_Others, 0) as Count_Others,
    
    -- 對比指標
    ROUND(COALESCE(a.Avg_Attr_Satisfaction, 0), 1) as Attrition_Avg_Satisfaction,
    d.Dept_Avg_SatisfactionScore as Overall_Avg_Satisfaction,
    ROUND(COALESCE(a.Avg_Attr_Tenure, 0), 1) as Attrition_Avg_Tenure_Years,
    ROUND(COALESCE(a.Avg_Attr_Salary, 0), 0) as Attrition_Avg_Salary
FROM all_depts d
LEFT JOIN attrition_breakdown a ON d.Department = a.Department;

SELECT * FROM gold_attrition_detailed;