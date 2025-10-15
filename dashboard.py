import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('ds_salaries.csv')

st.title('Data Science Job Salaries Analysis Dashboard')
st.markdown("""
Analyze salary metrics and distributions for selected jobs, countries, experience levels, and remote work ratios.
""")

# Sidebar filters
st.sidebar.header('Filters')
all_countries = sorted(df['employee_residence'].dropna().unique())
all_jobs = sorted(df['job_title'].dropna().unique())
all_experience = sorted(df['experience_level'].dropna().unique())
all_remote_ratio = sorted(df['remote_ratio'].dropna().unique())

selected_countries = st.sidebar.multiselect('Select Countries', all_countries, default=all_countries)
selected_jobs = st.sidebar.multiselect('Select Job Roles', all_jobs, default=all_jobs)
selected_experience = st.sidebar.multiselect('Select Experience Levels', all_experience, default=all_experience)
selected_remote = st.sidebar.multiselect('Select Remote Work Ratios', all_remote_ratio, default=all_remote_ratio)

# Filter dataframe
filtered_df = df[
    df['employee_residence'].isin(selected_countries) &
    df['job_title'].isin(selected_jobs) &
    df['experience_level'].isin(selected_experience) &
    df['remote_ratio'].isin(selected_remote)
]

# Salary summary stats per job and country
st.header('Salary Summary Statistics')
summary = filtered_df.groupby(['job_title', 'employee_residence'])['salary_in_usd'].agg(['mean', 'median', 'min', 'max']).reset_index()
st.dataframe(summary)

# Combined distribution by experience and job role
st.header('Salary Distribution by Experience Level and Job Role')
plt.figure(figsize=(10, 6))
sns.boxplot(x='experience_level', y='salary_in_usd', hue='job_title', data=filtered_df, palette='Set3')
plt.title('Salary Distribution by Experience Level and Job Role')
plt.xlabel('Experience Level')
plt.ylabel('Salary (USD)')
st.pyplot(plt.gcf())
plt.clf()

# Combined distribution by remote ratio and job role
st.header('Salary Distribution by Remote Work Ratio and Job Role')
plt.figure(figsize=(10, 6))
sns.boxplot(x='remote_ratio', y='salary_in_usd', hue='job_title', data=filtered_df, palette='Paired')
plt.title('Salary Distribution by Remote Work Ratio and Job Role')
plt.xlabel('Remote Work Ratio')
plt.ylabel('Salary (USD)')
st.pyplot(plt.gcf())
plt.clf()

# Average salary comparison by job role (combined for selected countries)
st.header('Average Salary Comparison by Job Role')
avg_salary_job = filtered_df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_salary_job.values, y=avg_salary_job.index, palette='Blues_d')
plt.xlabel('Average Salary (USD)')
plt.ylabel('Job Role')
plt.title('Average Salary across Selected Countries')
st.pyplot(plt.gcf())
plt.clf()

# Average salary comparison by country (combined for selected jobs)
st.header('Average Salary Comparison by Country')
avg_salary_country = filtered_df.groupby('employee_residence')['salary_in_usd'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_salary_country.values, y=avg_salary_country.index, palette='Greens_d')
plt.xlabel('Average Salary (USD)')
plt.ylabel('Country')
plt.title('Average Salary across Selected Job Roles')
st.pyplot(plt.gcf())
plt.clf()

# Individual salary comparison graphs per job role and per country
st.header('Individual Salary Comparison: By Job Role per Country')
for job in selected_jobs:
    job_df = filtered_df[filtered_df['job_title'] == job]
    if job_df.empty:
        st.write(f"No data for job role: {job}")
        continue
    salary_by_country = job_df.groupby('employee_residence')['salary_in_usd'].mean().sort_values(ascending=False)
    st.subheader(f'Average Salary by Country for Job Role: {job}')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=salary_by_country.values, y=salary_by_country.index, palette='viridis')
    plt.xlabel('Average Salary (USD)')
    plt.ylabel('Country')
    st.pyplot(plt.gcf())
    plt.clf()

st.header('Individual Salary Comparison: By Country per Job Role')
for country in selected_countries:
    country_df = filtered_df[filtered_df['employee_residence'] == country]
    if country_df.empty:
        st.write(f"No data for country: {country}")
        continue
    salary_by_job = country_df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)
    st.subheader(f'Average Salary by Job Role for Country: {country}')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=salary_by_job.values, y=salary_by_job.index, palette='coolwarm')
    plt.xlabel('Average Salary (USD)')
    plt.ylabel('Job Role')
    st.pyplot(plt.gcf())
    plt.clf()

# Additional Salary vs Remote Work Ratio Graphs for Comparison
st.header('Average Salary by Remote Work Ratio')
avg_salary_remote = filtered_df.groupby('remote_ratio')['salary_in_usd'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_salary_remote.values, y=avg_salary_remote.index, palette='coolwarm')
plt.xlabel('Average Salary (USD)')
plt.ylabel('Remote Work Ratio')
plt.title('Average Salary by Remote Work Ratio')
st.pyplot(plt.gcf())
plt.clf()

st.header('Salary Distribution by Remote Work Ratio for Different Job Roles')
plt.figure(figsize=(12, 7))
sns.boxplot(x='remote_ratio', y='salary_in_usd', hue='job_title', data=filtered_df, palette='Set2')
plt.xlabel('Remote Work Ratio')
plt.ylabel('Salary (USD)')
plt.title('Salary Distribution by Remote Work Ratio Across Job Roles')
st.pyplot(plt.gcf())
plt.clf()

st.header('Salary Distribution by Remote Work Ratio for Different Countries')
plt.figure(figsize=(12, 7))
sns.boxplot(x='remote_ratio', y='salary_in_usd', hue='employee_residence', data=filtered_df, palette='Paired')
plt.xlabel('Remote Work Ratio')
plt.ylabel('Salary (USD)')
plt.title('Salary Distribution by Remote Work Ratio Across Countries')
st.pyplot(plt.gcf())
plt.clf()

# Career recommendations section
st.header('Career Recommendations')
top_roles = filtered_df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(5)
top_experience = filtered_df.groupby('experience_level')['salary_in_usd'].mean().sort_values(ascending=False).head(3)
st.markdown(f"**Top 5 Highest Paying Job Roles:** {', '.join(top_roles.index)}")
st.markdown(f"**Experience Levels with Best Pay:** {', '.join(top_experience.index)}")
st.markdown("Focus on the above roles and experience levels to improve your career prospects and salary.")

# Filtered dataset sample at the end
st.header('Filtered Dataset Sample')
st.dataframe(filtered_df.reset_index(drop=True))
