import streamlit as st

# Set up the page
st.set_page_config(
    page_title="Preditive Analytics for Small to Medium Business",
    page_icon="📊",
)

# Main title
st.write("# Business Viability Analysis for Philippine Regions 📊")

# Brief introduction
st.markdown(
    """
    Welcome to the Business Viability Analysis application, part of our research to assess and classify 
    business potential across regions in the Philippines using data-driven insights.

    This project leverages socio-economic data, household expenditures, and demographic factors to provide 
    a comprehensive overview of regional market conditions. Our goal is to support data-driven decision-making 
    for entrepreneurs and policy makers by identifying regions with high potential for various business types.

    ### What You’ll Find Here:
    - **Exploratory Data Analysis**: Insights into key features and socio-economic distributions across regions.
    - **Factor Analysis and Clustering**: Uncover patterns to identify regional profiles based on factors like income, spending, and assets.
    - **Business Viability Scoring**: See scores and clusters indicating which regions are more business-friendly.

    ### Learn More
    - [Project Documentation](#)  
    - [Research Methodology](#)

    **👈 Use the sidebar** to navigate through the sections and explore the data and models.
    """
)

st.sidebar.success("Select a section to begin exploring.")