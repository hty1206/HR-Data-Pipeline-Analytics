CREATE OR REPLACE VIEW gold_recruitment_quality AS
SELECT 
    RecruitmentSource,
    COUNT(*) as Total_Hires,
    -- 1. 表現度
    ROUND(AVG(PerfScoreID), 2) as Avg_Performance_Score,
    -- 2. 戰力
    ROUND(SUM(CASE WHEN PerfScoreID >= 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as High_Performer_Ratio,
    -- 3. 穩定度
    ROUND(AVG(Tenure_Years), 1) as Avg_Tenure_Years,
    -- 4. 留任度
    100 - ROUND(SUM(CASE WHEN Termd = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as Retention_Rate_Percentage,
    -- 5. 滿意度
    ROUND(AVG(SatisfactionScore), 1) as Avg_Satisfaction
FROM hr_employees_silver
GROUP BY RecruitmentSource;

SELECT * FROM gold_recruitment_quality 
ORDER BY Avg_Performance_Score DESC;