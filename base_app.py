import streamlit as st

st.set_page_config(page_title="Anime Recommendation System")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Team", "Project Overview", "EDA", "Anime Recommendation"])

    # Team Page
    if page == "Team":
        st.title("Meet the team")
        st.write("Details about team members.")

    # Project Overview Page
    elif page == "Project Overview":
        st.title("Project Overview")
        st.write("Details about the project, objectives, and goals.")

    # EDA Page
    elif page == "EDA":
        st.title("Exploratory Data Analysis (EDA)")
        st.write("## Data Insights and Visualizations")
        st.write("Visualizations and insights will go here.")

    # Anime Recommendation Page
    elif page == "Anime Recommendation":
        st.title("Anime Recommendation System")

        st.write("## Select an Algorithm")
        algorithm = st.radio("Select an algorithm:", ("Content Based Filtering", "Collaborative Based Filtering"))

        st.write("## Enter Your Three Favorite Anime")
        first_anime = st.text_input("First Option")
        second_anime = st.text_input("Second Option")
        third_anime = st.text_input("Third Option")

        if st.button("Recommend"):
            if algorithm == "Content Based Filtering":
                # content-based filtering logic
                pass
            else:
                # model-based collaborative filtering logic (loading a pickled model)
                pass

# Running the app
if __name__ == '__main__':
    main()








