import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Strategic HR Dashboard", layout="wide")

@st.cache_resource

def get_engine():
    def get_val(key):
        if key in st.secrets:
            return st.secrets[key]
        return os.getenv(key)

    user = get_val("DB_USER")
    pw = get_val("DB_PASSWORD")
    host = get_val("DB_HOST")
    db = get_val("DB_NAME")
    port = get_val("DB_PORT")
    
    conn_str = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?ssl_verify_cert=false&ssl_verify_identity=false"
    return create_engine(conn_str, pool_pre_ping=True)

engine = get_engine()

@st.cache_data(ttl=300)
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

st.title("📊 Strategic HR Analytics Dashboard")
st.caption("Data Source：https://www.kaggle.com/datasets/rhuebner/human-resources-data-set")
st.caption("更新頻率：資料庫每日凌晨 2 點更新；網頁每 5 分鐘自動讀取最新數據")

try:
    df_silver = load_data("hr_employees_silver")
except Exception as e:
    st.error(f"無法讀取基礎資料表: {e}")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["🏠 公司員工總覽", "📈 離職原因總覽", "🔍 招募管道分析", "💰 薪資公平性分析"])

# Tab 1: 公司員工總覽
with tab1:
    try:
        df_summary = load_data("gold_company_summary")
        df_dept = load_data("gold_dept_performance")
        
        total_count = len(df_silver)
        active_count = int(df_summary['Total_Employees'][0])
        
        # KPI
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("總公司人數", f"{total_count} 人")
        c2.metric("在職員工數", f"{active_count} 人", 
                  delta=f"{active_count - total_count} (已離職)", delta_color="inverse")
        c3.metric("在職平均薪資", f"${df_summary['Company_Avg_Salary'][0]:,.0f}")
        c4.metric("在職平均年資", f"{df_summary['Avg_Tenure_Years'][0]:.1f} 年")

        st.markdown("---")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("各部門在職員工平均薪資與年資")
            
            fig_combo = go.Figure()

            # 1. 平均薪資 (長條圖 - 左軸)
            fig_combo.add_trace(go.Bar(
                x=df_dept['Department'],
                y=df_dept['Avg_Salary'],
                name='平均薪資',
                marker_color='#636EFA',
                yaxis='y1'
            ))

            # 2. 平均年資 (折線圖 - 右軸)
            fig_combo.add_trace(go.Scatter(
                x=df_dept['Department'],
                y=df_dept['Avg_Tenure_Years'],
                name='平均年資',
                mode='lines+markers+text',
                text=df_dept['Avg_Tenure_Years'],
                textposition="top center",
                line=dict(color='#EF553B', width=3),
                marker=dict(size=10),
                yaxis='y2'
            ))

            fig_combo.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(title="平均薪資 ($)", side="left", showgrid=False),
                yaxis2=dict(title="平均年資 (年)", side="right", overlaying="y", showgrid=False),
                margin=dict(t=50, b=50, l=0, r=0),
                hovermode="x unified"
            )

            st.plotly_chart(fig_combo, use_container_width=True)

        with col_right:
            st.subheader("各部門在職員工數")
            fig_pie = px.pie(df_dept, values='Emp_Count', names='Department', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

    except Exception as e:
        st.error(f"Tab 1 載入失敗: {e}")

# Tab 2: 離職原因總覽
with tab2:
    try:
        df_attr = load_data("gold_attrition_detailed")

        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("為什麼員工選擇離開？ (全公司)")

            total_reasons = pd.DataFrame({
                "原因": ["薪資福利", "職涯發展", "工作環境", "個人因素"],
                "人數": [
                    df_attr['Count_Compensation'].sum(),
                    df_attr['Count_Career_Growth'].sum(),
                    df_attr['Count_Environment'].sum(),
                    df_attr['Count_Personal'].sum()
                ]
            })

            fig_reason = px.pie(
                total_reasons, 
                values='人數', 
                names='原因',
                color='原因',
                color_discrete_map={
                    "薪資福利": "#ff9999",
                    "職涯發展": "#66b3ff",
                    "工作環境": "#99ff99",
                    "個人因素": "#ffcc99"
                },
                hole=0.3 
            )
        
            fig_reason.update_traces(
                textposition='inside', 
                textinfo='percent+label'
            )
            
            fig_reason.update_layout(
                showlegend=False,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            
            st.plotly_chart(fig_reason, use_container_width=True)
        
        with col_r:
            
            dept_list = df_attr['Department'].unique().tolist()
            selected_dept = st.selectbox("部門選擇：", dept_list)
            
            dept_data = df_attr[df_attr['Department'] == selected_dept].iloc[0]
            
            dept_reasons = pd.DataFrame({
                "原因": ["薪資福利", "職涯發展", "工作環境", "個人因素", "其他"],
                "人數": [
                    dept_data['Count_Compensation'],
                    dept_data['Count_Career_Growth'],
                    dept_data['Count_Environment'],
                    dept_data['Count_Personal'],
                    dept_data['Count_Others']
                ]
            })
            
            dept_reasons = dept_reasons[dept_reasons['人數'] > 0]

            if not dept_reasons.empty:
                fig_dept_pie = px.pie(
                    dept_reasons, 
                    values='人數', 
                    names='原因',
                    hole=0.4,
                    color='原因',
                    color_discrete_map={
                        "薪資福利": "#ff9999", 
                        "職涯發展": "#66b3ff", 
                        "工作環境": "#99ff99", 
                        "個人因素": "#ffcc99",
                        "其他": "#d3d3d3"
                    }
                )
                
                fig_dept_pie.update_traces(textinfo='percent+label', textposition='inside')
                fig_dept_pie.update_layout(
                    showlegend=False,
                    legend=dict(orientation="h", y=-0.1),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_dept_pie, use_container_width=True)

                st.info(f"💡 {selected_dept} 部門共有 {int(dept_data['Attrition_Count'])} 人離職，離職率為 {dept_data['Attrition_Rate_Percentage']} %")
            else:
                st.warning(f"目前 {selected_dept} 部門尚無離職人員數據。")

        st.markdown("---")

        st.subheader("員工留任關鍵期：離職人員年資分佈")
        
        df_terminated = df_silver[df_silver['Termd'] == 1].copy()
        
        if not df_terminated.empty:
            df_terminated['Tenure_Year_Group'] = df_terminated['Tenure_Years'].apply(lambda x: f"{int(x)}-{int(x)+1} 年")
            
            year_order = sorted(df_terminated['Tenure_Year_Group'].unique(), key=lambda x: int(x.split('-')[0]))
            
            df_tenure_dist = df_terminated.groupby('Tenure_Year_Group').size().reset_index(name='離職人數')
            
            fig_tenure_peak = px.area(
                df_tenure_dist, 
                x='Tenure_Year_Group', 
                y='離職人數',
                category_orders={'Tenure_Year_Group': year_order},
                title="離職人數隨年資變化趨勢",
                markers=True,
                color_discrete_sequence=['#EF553B']
            )
            
            fig_tenure_peak.update_layout(
                xaxis_title="入職年資 (年)",
                yaxis_title="離職總人數",
                hovermode="x unified"
            )
            
            peak_group = df_tenure_dist.loc[df_tenure_dist['離職人數'].idxmax(), 'Tenure_Year_Group']
            peak_count = df_tenure_dist['離職人數'].max()
            
            c_text, c_plot = st.columns([1, 3])
            with c_text:
                st.warning(f"⚠️ **離職高峰預警**")
                st.write(f"數據顯示，公司離職高峰發生在入職 **{peak_group}** 間。")
                st.write(f"共有 **{peak_count}** 人在此階段離開。")
                st.info("💡 建議 HR 針對此年資區間的人員加強關懷或檢視升遷路徑。")
            
            with c_plot:
                st.plotly_chart(fig_tenure_peak, use_container_width=True)
        else:
            st.success("目前無離職人員數據可分析年資分佈。")

    except Exception as e:
        st.error(f"Tab 2 載入失敗: {e}")

# Tab 3: 招募管道分析
with tab3:
    try:
        st.subheader("招募管道成效分析")
        df_recru = load_data("gold_recruitment_quality")

        metric_type = st.radio(
            "分析維度選擇：", 
            ["成本與穩定度 (薪資/年資)", "品質與滿意度 (績效/分數)"], 
            horizontal=True
        )

        fig_rec_combo = go.Figure()

        # 長條圖：總招募人數 
        fig_rec_combo.add_trace(go.Bar(
            x=df_recru['RecruitmentSource'],
            y=df_recru['Total_Hires'],
            name='總招募人數',
            marker_color='rgba(99, 110, 250, 0.6)',
            yaxis='y1'
        ))

        if metric_type == "成本與穩定度 (薪資/年資)":
            # 平均年資 (折線圖 - 右軸)
            fig_rec_combo.add_trace(go.Scatter(
                x=df_recru['RecruitmentSource'],
                y=df_recru['Avg_Tenure_Years'],
                name='平均年資 (年)',
                mode='lines+markers+text',
                text=df_recru['Avg_Tenure_Years'],
                textposition="top center",
                line=dict(color='#EF553B', width=3),
                yaxis='y2'
            ))
            # 留任率 (右軸)
            fig_rec_combo.add_trace(go.Scatter(
                x=df_recru['RecruitmentSource'],
                y=df_recru['Retention_Rate_Percentage'],
                name='留任率 (%)',
                mode='lines+markers',
                line=dict(color='#00CC96', width=2, dash='dot'), 
                yaxis='y2'
            ))
            y2_title = "年資 (年) / 留任率 (%)"

        else:
            # 平均表現分數 (右軸)
            fig_rec_combo.add_trace(go.Scatter(
                x=df_recru['RecruitmentSource'],
                y=df_recru['Avg_Performance_Score'],
                name='平均績效分數',
                mode='lines+markers+text',
                line=dict(color='#AB63FA', width=3),
                yaxis='y2'
            ))
            # 工作滿意度 (右軸)
            fig_rec_combo.add_trace(go.Scatter(
                x=df_recru['RecruitmentSource'],
                y=df_recru['Avg_Satisfaction'],
                name='工作滿意度',
                mode='lines+markers',
                line=dict(color='#FFA15A', width=2), 
                yaxis='y2'
            ))
            y2_title = "評分指標 (1-5)"

        fig_rec_combo.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="總招募人數", side="left", showgrid=True),
            yaxis2=dict(title=y2_title, side="right", overlaying="y", showgrid=False),
            margin=dict(t=80, b=50, l=50, r=50),
            hovermode="x unified"
        )

        st.plotly_chart(fig_rec_combo, use_container_width=True)

    except Exception as e:
        st.error(f"招募品質圖表載入失敗: {e}")

# Tab 4: 薪資公平性分析
with tab4:
    try:
        df_equity = load_data("gold_pay_equity_analysis")

        st.subheader("薪資公平性與保留風險名單")

        risk_counts = df_equity['Pay_Equity_Status'].value_counts().reset_index()
        risk_counts.columns = ['Status', 'Count']
        
        col_chart, col_stat = st.columns([2, 1])
        
        with col_chart:
            fig_risk = px.bar(
                risk_counts, x='Count', y='Status', orientation='h',
                color='Status',
                color_discrete_map={
                    'Underpaid Veteran (High Risk)': '#FF4B4B',
                    'Rising Star (Monitor Growth)': '#FFA15A',
                    'Overpaid Newcomer': '#AB63FA',
                    'Market Aligned': '#00CC96'
                },
                title="人才薪資狀態分佈"
            )
            fig_risk.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with col_stat:
            high_risk_num = len(df_equity[df_equity['Pay_Equity_Status'] == 'Underpaid Veteran (High Risk)'])
            st.metric("核心資深人才流失風險", f"{high_risk_num} 人", delta="需優先處理", delta_color="inverse")
            st.info("💡 **定義：** 資深且績效佳，但薪資低於該職位平均。")

        st.markdown("---")

        st.subheader("詳細分析名單")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            selected_status = st.multiselect(
                "篩選狀態：", 
                options=df_equity['Pay_Equity_Status'].unique()
            )
        with col_f2:
            selected_dept = st.multiselect("篩選部門：", options=df_equity['Department'].unique())
        with col_f3:
            search_name = st.text_input("搜尋員工姓名：")

        df_filtered = df_equity.copy()
        if selected_status:
            df_filtered = df_filtered[df_filtered['Pay_Equity_Status'].isin(selected_status)]
        if selected_dept:
            df_filtered = df_filtered[df_filtered['Department'].isin(selected_dept)]
        if search_name:
            df_filtered = df_filtered[df_filtered['Employee_Name'].str.contains(search_name, case=False)]

        def highlight_risk(val):
            color = ''
            if val == 'Underpaid Veteran (High Risk)':
                color = 'background-color: #FF4B4B; color: white'
            elif val == 'Rising Star (Monitor Growth)':
                color = 'background-color: #FFA15A; color: black'
            elif val == 'Overpaid Newcomer':
                color = 'background-color: #00AEAE; color: white'
            return color

        st.dataframe(
            df_filtered.style.map(highlight_risk, subset=['Pay_Equity_Status'])
            .format({'Salary': '${:,.0f}', 'Avg_Salary_For_Position': '${:,.0f}'}),
            use_container_width=True,
            height=500
        )
        
        # 下載按鈕
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 下載篩選後的名單 (CSV)", csv, "pay_equity_report.csv", "text/csv")

    except Exception as e:
        st.error(f"Tab 3 報表載入失敗: {e}")