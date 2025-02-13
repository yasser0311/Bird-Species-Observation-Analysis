import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import base64

# Set page config
st.set_page_config(page_title="🦅🦆Bird Monitoring Dashboard🦉🐦", layout="wide")

# ## Encode the local image file to base64
# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# # Set the background image using the encoded base64 string
# def set_background(png_file, opacity=0.5):
#     bin_str = get_base64(png_file)
#     page_bg_img = f'''
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{bin_str}");
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-attachment: overlay;
#         opacity: {opacity};
#     }}
#     </style>
#     '''
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# # Path to your local image file
# image_path = 'D:\\MTDM37\\Guvi\\DS_Birds_EDA\\bird.jpg'
# set_background(image_path, opacity=0.7)

# Load your dataset
@st.cache_data
def load_data():
    combined_df = pd.read_csv('D:\\MTDM37\\Guvi\\DS_Birds_EDA\\combined_data_cleaned_v3.csv', low_memory=False)
    combined_df["Date"] = pd.to_datetime(combined_df["Date"], errors='coerce')
    combined_df["Month"] = combined_df["Date"].dt.month

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"
        else:
            return None

    combined_df["Season"] = combined_df["Month"].apply(get_season)
    return combined_df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
if "Year" in df.columns:
    selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].dropna().unique()))
    filtered_df = df[df["Year"] == selected_year]
else:
    st.sidebar.warning("Year column not found in dataset.")
    filtered_df = df  # Keep entire dataset if Year column is missing
    

# Add buttons to toggle sections
st.sidebar.header("Toggle Sections")
show_temporal = st.sidebar.checkbox("1. Temporal Analysis📅🕒📊", value=True)
show_spatial = st.sidebar.checkbox("2. Spatial Analysis🌍🗺️📌", value=True)
show_species = st.sidebar.checkbox("3. Species Analysis🐦🔍📋", value=True)
show_environmental = st.sidebar.checkbox("4. Environmental Conditions🌤️🌧️🌿", value=True)
show_distance_observer = st.sidebar.checkbox("5. Distance and Behavior and Observer Trends🧑‍🔬📈👁️", value=True)
show_conservation = st.sidebar.checkbox("6. Conservation Insights🧑‍🔬📈👁️", value=True)

# Main dashboard metrics
st.title("🦅🦆Bird Monitoring Dashboard🦉🐦")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Admin Units", df["Admin_Unit_Code"].nunique())
col2.metric("Total Observers", df["Observer"].nunique())
col3.metric("Total Species", df["Scientific_Name"].nunique())
col4.metric("Total Habitat", df["Habitat"].nunique())

# --------------------------------------------1. Temporal Analysis----------------------------------------------------
if show_temporal:
    st.subheader("🌍Seasonal Trends and Observation Time📊")
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))

    # Define colors explicitly
    year_palette = "coolwarm"
    month_palette = "viridis"
    season_palette = "Set2"

    # Plot yearly trend
    sns.countplot(data=df, x="Year", hue="Year", palette=year_palette, order=sorted(df["Year"].dropna().unique()), ax=axes[0])
    axes[0].set_xlabel("Year", fontsize=20, fontweight="bold")
    axes[0].set_ylabel("Number of Observations", fontsize=20, fontweight="bold")
    axes[0].set_title("Bird Observations Over the Years", fontsize=25, fontweight="bold")
    axes[0].tick_params(axis='x', rotation=45)

    # Plot monthly trend
    sns.countplot(data=df, x="Month", hue="Month", palette=month_palette, order=range(1, 13), ax=axes[1])
    axes[1].set_xlabel("Month", fontsize=20, fontweight="bold")
    axes[1].set_ylabel("Number of Observations", fontsize=20, fontweight="bold")
    axes[1].set_title("Monthly Bird Observation Trends", fontsize=25, fontweight="bold")
    axes[1].set_xticks(range(1, 13))
    axes[1].set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fontsize=10, fontweight="bold")

    # Plot seasonal trend
    sns.countplot(data=df, x="Season", hue="Season", palette=season_palette, order=["Winter", "Spring", "Summer", "Fall"], ax=axes[2], hue_order=["Winter", "Spring", "Summer", "Fall"])
    axes[2].set_xlabel("Season", fontsize=20, fontweight="bold")
    axes[2].set_ylabel("Number of Observations", fontsize=20, fontweight="bold")
    axes[2].set_title("Bird Observations Across Seasons", fontsize=25, fontweight="bold")

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plots in Streamlit
    st.pyplot(fig)

    # Insights
    st.write("""
    **Insights:**
    - **Yearly Trends:** Bird observations have remained stable over the years, indicating possible changes in bird populations or observation efforts.
    - **Monthly Trends:** Observations peak during April, May and June, likely due to migration patterns, breeding seasons, or favorable weather conditions.
    - **Seasonal Trends:** The highest number of observations occurs in Summer, suggesting seasonal habitat preferences or migration patterns.
    """)

# --------------------------------------------2. Spatial Analysis----------------------------------------------------
if show_spatial:
    st.subheader("🗺️📌Location Insights and Plot-Level Analysis📊")
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))

    # Count unique bird species observed per Location_Type
    location_biodiversity = df.groupby("Location_Type")["Common_Name"].nunique().sort_values(ascending=False)

    # Count unique bird species per Plot_Name
    plot_biodiversity = df.groupby("Plot_Name")["Common_Name"].nunique().sort_values(ascending=False)

    # Display the top biodiversity locations and plots
    st.write("Top Biodiversity Hotspots by Location Type:", location_biodiversity.head(10))
    st.write("Top 10 Plots by Species Count:", plot_biodiversity.head(10))

    # Create a bar chart for Location-Type biodiversity
    sns.barplot(x=location_biodiversity.index, y=location_biodiversity.values, palette="viridis", ax=axs[0], hue=location_biodiversity.index)
    axs[0].set_xlabel("Location Type", fontsize=15, fontweight="bold")
    axs[0].set_ylabel("Unique Bird Species Count", fontsize=15, fontweight="bold")
    axs[0].set_title("Biodiversity Hotspots by Location Type", fontsize=25, fontweight="bold")
    axs[0].tick_params(axis='x', rotation=45)

    # Create a bar chart for top 10 biodiversity plots
    sns.barplot(x=plot_biodiversity.head(10).index, y=plot_biodiversity.head(10).values, palette="magma", ax=axs[1], hue=plot_biodiversity.head(10).index)
    axs[1].set_xlabel("Plot Name", fontsize=15, fontweight="bold")
    axs[1].set_ylabel("Unique Bird Species Count", fontsize=15, fontweight="bold")
    axs[1].set_title("Top 10 Plots by Species Count", fontsize=20, fontweight="bold")
    axs[1].tick_params(axis='x', rotation=90)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plots in Streamlit
    st.pyplot(fig)

    # Insights
    st.write("""
    **Insights:**
    - **Biodiversity Hotspots:** Forest have the highest species diversity, indicating potential conservation priorities eco-tourism opportunities.
    - **Habitat Preferences:** Certain species are more frequently observed in Forest, suggesting habitat-specific conservation strategies.
    """)

# --------------------------------------------3. Species Analysis----------------------------------------------------
if show_species:
    st.subheader("🐦🔍Species Diversity📋")

    # 1. Diversity Metrics - Unique species per Location_Type
    species_diversity = df.groupby("Location_Type")["Scientific_Name"].nunique().sort_values(ascending=False)

    # 2. Activity Patterns - Count occurrences of Interval_Length & ID_Method
    interval_counts = df["Interval_Length"].value_counts()
    id_method_counts = df["ID_Method"].value_counts()

    # 3. Sex Ratio Analysis - Count male vs. female occurrences
    sex_counts = df["Sex"].value_counts()

    # Display results
    st.write("By location Type:", species_diversity)
    st.write("Top Interval Lengths:", interval_counts.head(10))
    st.write("Top Identification Methods:", id_method_counts.head(10))
    st.write("Sex Counts:", sex_counts)

    # Create visualizations for species diversity, activity patterns, and sex ratio
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Bar chart for species diversity across Location_Type
    sns.barplot(x=species_diversity.index, y=species_diversity.values, palette="coolwarm", ax=axes[0], hue=species_diversity.index, dodge=False)
    axes[0].set_title("Species Diversity by Location Type", fontsize=20, fontweight="bold")
    axes[0].set_xlabel("Location Type", fontsize=15, fontweight="bold")
    axes[0].set_ylabel("Unique Species Count", fontsize=15, fontweight="bold")

    # 2. Bar chart for ID Method distribution
    sns.barplot(x=id_method_counts.index, y=id_method_counts.values, palette="viridis", ax=axes[1], hue=id_method_counts.index, dodge=False)
    axes[1].set_title("Most Common Identification Methods", fontsize=20, fontweight="bold")
    axes[1].set_xlabel("ID Method", fontsize=15, fontweight="bold")
    axes[1].set_ylabel("Observation Count", fontsize=15, fontweight="bold")
    for tick in axes[1].get_xticklabels():
        tick.set_rotation(45)

    # 3. Pie chart for Sex Ratio
    axes[2].pie(sex_counts.values, labels=sex_counts.index, autopct='%1.1f%%', colors=["blue", "red", "gray"], startangle=90)
    axes[2].set_title("Sex Ratio Distribution", fontsize=20, fontweight="bold")

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plots in Streamlit
    st.pyplot(fig)

    # Insights
    st.write("""
    **Insights:**
    - **Species Diversity:** Forest have the highest species diversity, indicating potential conservation priorities.
    - **Identification Methods:** Singing are most commonly used, suggesting observer preferences or effectiveness.
    - **Sex Ratio:** The sex ratio is skewed, which may indicate observation biases.
    """)

# --------------------------------------------4. Environmental Analysis----------------------------------------------------
if show_environmental:
    st.subheader("🌤️🌧️ Weather Impact on Bird Observations 🌿")
    
    # Encode categorical columns 'Sky' and 'Wind'
    if "Sky" in df.columns and "Wind" in df.columns:
        sky_encoded = pd.get_dummies(df['Sky'], prefix='Sky')
        wind_encoded = pd.get_dummies(df['Wind'], prefix='Wind')
        
        # Combine encoded columns
        df = pd.concat([df, sky_encoded, wind_encoded], axis=1)
        
        # Define weather factors for correlation analysis
        weather_factors = ["Temperature", "Humidity", "Initial_Three_Min_Cnt"] + list(sky_encoded.columns) + list(wind_encoded.columns)
        available_factors = [col for col in weather_factors if col in df.columns]
        
        if available_factors:
            # Compute correlation matrix
            correlation_matrix = df[available_factors].corr()
            
            # Display correlation of weather factors with bird observations
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0, linewidths=0.5, ax=ax)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No weather-related columns found for correlation analysis.")
    else:
        st.warning("Columns 'Sky' and 'Wind' not found in the dataset.")
    
    # Disturbance Effect Analysis
    if "Disturbance" in df.columns:
        disturbance_effect = df.groupby("Disturbance")["Initial_Three_Min_Cnt"].sum().sort_values(ascending=False)
        
        st.subheader("🚧 Impact of Disturbance on Bird Observations")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=disturbance_effect.index, y=disturbance_effect.values, palette="rocket", ax=ax)
        ax.set_xlabel("Disturbance Level", fontsize=12)
        ax.set_ylabel("Total Bird Observations", fontsize=12)
        ax.set_title("Impact of Disturbance on Bird Observations", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Column 'Disturbance' not found in the dataset.")
    
    # Insights
    st.write("""
    **Insights:**
    - **Weather Impact:** Temperature and humidity are positively and negatively correlated with bird observations, suggesting behavioral adaptations or observation biases.
    - **Disturbance Impact:** Higher disturbance levels decrease bird observations, indicating habitat sensitivity or avoidance behavior.
    """)

# --------------------------------------------5. Distance and Behavior and Observer Trends----------------------------------------------------
if show_distance_observer:
    st.subheader("↔️📈Distance Analysis📊")
    file_path = 'D:\\MTDM37\\Guvi\\DS_Birds_EDA\\combined_data_cleaned_v3.csv'
    df = pd.read_csv(file_path, dtype=str)  # Load as text to inspect
    df["Distance"] = df["Distance"].replace({
        "<= 50 Meters": 50,
        "50 - 100 Meters": 75
    }).astype(float, errors='ignore')

    species_distance = df.groupby("Common_Name")["Distance"].mean().sort_values()

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # 1. Top 10 Closest Observed Species
    sns.barplot(x=species_distance.head(10).values, y=species_distance.head(10).index, palette="Blues_r", ax=axes[0], hue=species_distance.head(10).index, dodge=False)
    axes[0].set_title("Top 10 Closest Observed Species", fontsize=20, fontweight="bold")
    axes[0].set_xlabel("Average Observation Distance", fontsize=15, fontweight="bold")

    # 2. Top 10 Farthest Observed Species
    sns.barplot(x=species_distance.tail(10).values, y=species_distance.tail(10).index, palette="Reds_r", ax=axes[1], hue=species_distance.tail(10).index, dodge=False)
    axes[1].set_title("Top 10 Farthest Observed Species", fontsize=20, fontweight="bold")
    axes[1].set_xlabel("Average Observation Distance", fontsize=15, fontweight="bold")

    #3. Flyover Observations
    flyover_counts = df["Flyover_Observed"].value_counts()

    sns.barplot(x=flyover_counts.index, y=flyover_counts.values, palette="viridis", ax=axes[2], hue=flyover_counts.index, dodge=False)
    axes[2].set_title("Flyover Observations Frequency", fontsize=18, fontweight="bold")
    axes[2].set_xlabel("Flyover Observed (Yes/No)", fontsize=15, fontweight="bold")
    axes[2].set_ylabel("Number of Observations", fontsize=15, fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig)

    # Observer trend Analysis
    st.subheader("🧑‍🔬📈Observer Bias and visit Patterns👁️")
    # Count the total number of observations reported by each observer
    observer_counts = df["Observer"].value_counts()

    # Analyze if specific observers tend to report certain species more frequently
    observer_species_counts = df.groupby("Observer")["Common_Name"].nunique().sort_values(ascending=False)

    # Count unique species observed per visit
    species_per_visit = df.groupby("Visit")["Common_Name"].nunique().sort_values(ascending=False)

    # Count the number of visits per plot
    visit_counts = df.groupby("Plot_Name")["Visit"].nunique().sort_values(ascending=False)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 5))

    # 1. Observers Reporting the Most Unique Species
    sns.barplot(x=observer_species_counts.head(10).values, y=observer_species_counts.head(10).index, palette="magma", ax=axes[0], hue=observer_species_counts.head(10).index, dodge=False)
    axes[0].set_title("Top 10 Observers Reporting Unique Species", fontsize=18, fontweight="bold")
    axes[0].set_xlabel("Number of Unique Species", fontsize=15, fontweight="bold")
    axes[0].set_ylabel("Observer", fontsize=15, fontweight="bold")

    # 3. Species Diversity per Visit
    sns.lineplot(x=species_per_visit.index, y=species_per_visit.values, marker="o", ax=axes[1], color="green")
    axes[1].set_title("Species Diversity per Visit", fontsize=18, fontweight="bold")
    axes[1].set_xlabel("Number of Unique Species Observed per Visit", fontsize=15, fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig)

    # Insights
    st.write("""
    **Insights:**
    - **Distance Analysis:** Species observed at closer distances may indicate habitat familiarity or observer proximity], while distant observations suggest [elusive species or specific habitat preferences].
    - **Observer Bias:** Certain observers report more unique species, indicating specific observation techniques.
    - **Visit Patterns:** Species diversity per visit decreases over time, suggesting  observer consistency.
    """)

# --------------------------------------------6. Conservation Insights----------------------------------------------------
if show_conservation:
    st.subheader("🌳🛡️Watchlist Trends and AOU Code Patterns📉")
    # PIF Watchlist Status Distribution
    watchlist_counts = df["PIF_Watchlist_Status"].value_counts()
    # Regional Stewardship Status Distribution
    stewardship_counts = df["Regional_Stewardship_Status"].value_counts()
    # Count species based on AOU_Code
    aou_counts = df["AOU_Code"].value_counts().head(15)  # Top 15 for readability

    # Create subplots with 1 row and 3 columns
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # 1. PIF Watchlist Status Distribution
    sns.barplot(x=watchlist_counts.index.astype(str), y=watchlist_counts.values, palette="Reds_r", ax=axes[0], hue=watchlist_counts.index)
    axes[0].set_title("PIF Watchlist Status Distribution", fontsize=14)
    axes[0].set_xlabel("Watchlist Status")
    axes[0].set_ylabel("Number of Observations")

    # 2. Regional Stewardship Status Distribution
    sns.barplot(x=stewardship_counts.index.astype(str), y=stewardship_counts.values, palette="Blues_r", ax=axes[1], hue=stewardship_counts.index)
    axes[1].set_title("Regional Stewardship Status Distribution", fontsize=14)
    axes[1].set_xlabel("Stewardship Status")
    axes[1].set_ylabel("Number of Observations")

    # 3. Top 15 Most Observed AOU Codes
    sns.barplot(x=aou_counts.index, y=aou_counts.values, palette="viridis", ax=axes[2], hue=aou_counts.index)
    axes[2].set_title("Top 15 Most Observed AOU Codes", fontsize=14)
    axes[2].set_xlabel("AOU Code")
    axes[2].set_ylabel("Number of Observations")
    axes[2].tick_params(axis='x', rotation=45)

    # Adjust layout and show plots
    plt.tight_layout()
    st.pyplot(fig)

    # Insights
    st.write("""
    **Insights:**
    - **Watchlist Status:** Forest Habitat are most common, indicating conservation priorities.
    - **Stewardship Status:** Forest Habitat dominate, suggesting regional conservation efforts.
    - **AOU Codes:** The most observed AOU codes correspond to NOCA, highlighting observation biases.
    """)

# --------------------------------------------Concise Report----------------------------------------------------
st.subheader("📋Concise Report📋")
st.write("""
**Approach:**
This analysis focuses on understanding bird species' temporal and spatial distribution across forest and grassland habitats. The dataset was cleaned, preprocessed, and analyzed using exploratory data analysis (EDA) techniques. Visualizations were created to highlight trends, patterns, and insights.

**🔍Key Findings:🔍**
1. **Temporal Trends:** Bird observations peak during April, May and June for Spring and Summer Season, indicating migration or breeding patterns.
2. **Spatial Distribution:** Forest habitat have the highest species diversity, indicating potential conservation priorities eco-tourism opportunities.
3. **Species Diversity:** Forest support the most diverse bird populations.
4. **Environmental Impact:** Weather conditions and disturbance levels significantly influence bird observations.
5. **Observer Trends:** Elizabeth Oswald report the most unique species.
6. **Conservation Insights:** ANTI-0105 are most frequently observed plot name, highlighting common species.

**📉Actionable Insights:📉**
- **Conservation Planning:** Focus on protecting BGGN AOU Code to enhance biodiversity.
- **Resource Allocation:** Allocate resources to Spring for effective monitoring.
- **Eco-Tourism:** Develop bird-watching programs in Grassland to boost local economies.
- **Policy Support:** Use data-driven insights to create policies for Grassland habitat.
""")