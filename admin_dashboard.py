import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

def get_connection():
    return pymysql.connect(
        host='localhost', user='root', password='Admin12@', 
        db='skillsmart_db', cursorclass=pymysql.cursors.DictCursor
    )

def run_admin_dashboard():
    st.title("📊 Recruitment Data Mining Dashboard")
    st.markdown("### Extracting Market Insights & Talent Trends")

    try:
        # Fetch Data from MySQL
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM recruitment_analytics", conn)
        conn.close()

        if df.empty:
            st.info("No data mined yet. Data will appear once candidates start applying.")
            return

        # --- ROW 1: KPI METRICS ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Resumes Analyzed", len(df))
        c2.metric("Top Domain", df['predicted_domain'].mode()[0])
        c3.metric("Primary Tier", df['technocrat_tier'].mode()[0])

        # --- ROW 2: VISUAL ANALYTICS (The Mining Part) ---
        col_left, col_right = st.columns(2)

        with col_left:
            st.write("#### 🎯 Domain Distribution (Talent Supply)")
            fig_pie = px.pie(df, names='predicted_domain', hole=0.4, 
                             color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_right:
            st.write("#### 🥇 Seniority Split (Technocrat Tiers)")
            fig_bar = px.bar(df, x='technocrat_tier', color='technocrat_tier', 
                             title="Beginner vs. Advanced Supply")
            st.plotly_chart(fig_bar, use_container_width=True)

        # --- ROW 3: COMPANY TARGETING ---
        st.write("#### 🏢 Company Interest Mining")
        fig_trend = px.histogram(df, x='target_company', color='predicted_domain', 
                                 barmode='group', title="Which companies are attracting specific domains?")
        st.plotly_chart(fig_trend, use_container_width=True)

        # --- RAW DATA TABLE ---
        with st.expander("View Full Mined Dataset"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Database Connection Error: {e}")