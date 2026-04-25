CREATE OR REPLACE VIEW gold_pay_equity_analysis AS
WITH position_metrics AS (
    -- 1. 計算每個職位的平均薪資與平均年資
    SELECT 
        Position, 
        AVG(Salary) as Pos_Avg_Salary,
        AVG(Tenure_Years) as Pos_Avg_Tenure
    FROM hr_employees_silver
    GROUP BY Position
)
SELECT 
    s.Employee_Name,
    s.Department,
    s.Position,
    s.Salary,
    s.Tenure_Years,
    ROUND(p.Pos_Avg_Salary, 0) as Avg_Salary_For_Position,
    s.PerfScoreID,
    CASE 
        -- 資深、高績效、但薪資低於平均
        WHEN s.Tenure_Years >= p.Pos_Avg_Tenure AND s.PerfScoreID >= 3 AND s.Salary < p.Pos_Avg_Salary 
            THEN 'Underpaid Veteran (High Risk)'
        
        -- 年資淺、高績效、薪資稍低
        WHEN s.Tenure_Years < p.Pos_Avg_Tenure AND s.PerfScoreID >= 3 AND s.Salary < p.Pos_Avg_Salary 
            THEN 'Rising Star (Monitor Growth)'
        
        -- 年資淺、績效低、但薪資卻高於平均
        WHEN s.Tenure_Years < p.Pos_Avg_Tenure AND s.PerfScoreID <= 2 AND s.Salary > p.Pos_Avg_Salary 
            THEN 'Overpaid Newcomer'
            
        ELSE 'Market Aligned'
    END as Pay_Equity_Status
FROM hr_employees_silver s
JOIN position_metrics p ON s.Position = p.Position
WHERE s.EmploymentStatus = 'Active';

SELECT * FROM gold_pay_equity_analysis;