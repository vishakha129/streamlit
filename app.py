import streamlit as st
import pandas as pd
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="User Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and file upload
st.title("👥 User Data Analysis Dashboard")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load and clean data
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Remove rows with null values in key columns
    df_clean = df.dropna(subset=['MaritalStatus', 'BoloAppLanguage', 'EmploymentStatus'])
    
    # Show raw data with expander
    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(df)
        st.caption(f"Total records: {len(df)} | Clean records: {len(df_clean)}")

    # Create three columns for charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Marital Status Chart (filtered for non-null)
        st.subheader("💍 Marital Status")
        marital_counts = df_clean['MaritalStatus'].value_counts().reset_index()
        marital_counts.columns = ['Status', 'Count']
        
        fig_marital = px.pie(
            marital_counts,
            names='Status',
            values='Count',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_marital.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_marital, use_container_width=True)

    with col2:
        # App Language Distribution
        st.subheader("🗣️ App Language")
        lang_counts = df_clean['BoloAppLanguage'].value_counts().reset_index()
        lang_counts.columns = ['Language', 'Count']
        
        fig_lang = px.bar(
            lang_counts,
            x='Language',
            y='Count',
            color='Language',
            text='Count'
        )
        fig_lang.update_layout(showlegend=False)
        st.plotly_chart(fig_lang, use_container_width=True)

    with col3:
        # Employment Status
        st.subheader("💼 Employment Status")
        emp_counts = df_clean['EmploymentStatus'].value_counts().reset_index()
        emp_counts.columns = ['Status', 'Count']
        
        fig_emp = px.treemap(
            emp_counts,
            path=['Status'],
            values='Count',
            color='Count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_emp, use_container_width=True)

    # Cross-analysis section
    st.subheader("🔍 Cross Analysis")
    
    # Create interactive filters
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        x_axis = st.selectbox(
            "X-axis variable",
            options=['MaritalStatus', 'BoloAppLanguage', 'EmploymentStatus'],
            index=0
        )
    
    with analysis_col2:
        y_axis = st.selectbox(
            "Y-axis variable",
            options=['MaritalStatus', 'BoloAppLanguage', 'EmploymentStatus'],
            index=1
        )
    
    # Create cross-tab visualization
    if x_axis != y_axis:
        cross_tab = pd.crosstab(df_clean[x_axis], df_clean[y_axis])
        st.write(f"### {x_axis} vs {y_axis}")
        fig_heatmap = px.imshow(
            cross_tab,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("Please select different variables for X and Y axes")

    # Download cleaned data
    st.download_button(
        "⬇️ Download Cleaned Data",
        df_clean.to_csv(index=False),
        "cleaned_user_data.csv",
        "text/csv"
    )

else:
    st.info("👆 Please upload an Excel file to begin analysis")