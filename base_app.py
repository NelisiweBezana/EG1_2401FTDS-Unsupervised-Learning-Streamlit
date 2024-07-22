import streamlit as st
from PIL import Image

st.set_page_config(page_title="Anime Recommendation System")

def display_team_member(image, name, surname, email, github, linkedin):
    st.image(image, width=120)
    st.markdown(f"**{name} {surname}**")
    st.markdown(f"Email: {email}")
    st.markdown(f"[GitHub]({github}) / [LinkedIn]({linkedin})")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Team", "EDA", "Anime Recommendation"])

    # Home Page
    if page == "Home":
        st.title("Anime Recommender System")
        # Introduction
        st.write("""
            In the rapidly evolving landscape of today's technology-driven world, recommender systems have become pivotal in shaping our digital experiences. These systems play a crucial role in assisting individuals in making informed choices about the content they engage with on a daily basis. One particularly compelling application is in the realm of movie content recommendations, where intelligent algorithms have the potential to guide viewers through an overwhelming array of options and connect them with titles that align with their preferences.
        """)

        # Display a picture
        image = Image.open("visuals/assets/background_image.png")  # Make sure to replace this with your image path
        st.image(image, caption="Anime Recommender System Overview", use_column_width=True)

        # Grid layout for the relevant information
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Overview**")
            st.write("""
                The anime recommender system aims to enhance user experience by delivering personalized recommendations. By leveraging user interaction data and anime metadata, the system helps users discover content that aligns with their preferences, increasing engagement and retention.
            """)

            st.write("**Objectives of the Project**")
            st.write("""
                The primary objective is to develop a robust anime recommender system that provides accurate, diverse, and personalized recommendations. The system seeks to enhance user experience, increase engagement, and drive revenue growth for the platform.
            """)

            st.write("**Data Source**")
            st.write("""
                The dataset includes anime content information (anime.csv) and user ratings (training.csv). The test.csv file is used for creating rating predictions. The submissions.csv file shows the expected format for submissions.
            """)

        with col2:
            st.write("**Importance of the Study**")
            st.write("""
                Developing an anime recommender system is crucial for enhancing user experience, driving business growth, and maintaining a competitive edge. This project also contributes to advancements in technology and ethics within the field.
            """)

            st.write("**Problem Statement**")
            st.write("""
                With the vast amount of anime content available and diverse viewer preferences, users often face decision fatigue. Traditional discovery methods are insufficient for meeting the dynamic needs of modern users.
            """)

            st.write("**Hypothesis**")
            st.write("""
                Testing the effectiveness of the recommender system will help validate its ability to improve user experience, increase retention, drive revenue, and ensure fair and inclusive recommendations.
            """)

    # Team Page
    elif page == "Team":
        st.title("Meet the team")
        st.write("Our team is a group of passionate individuals dedicated to creating an innovative anime recommender system. Each member brings unique skills and expertise to the project, contributing to its success. Below, you can learn more about the team members, their roles, and how to connect with them.")
        
        team_members = [
            {
                "image": "visuals/team/NelisiweBezana.jpg",
                "name": "Nelisiwe",
                "surname": "Bezana",
                "email": "nelisiwebezana@gmail.com",
                "github": "https://github.com/NelisiweBezana",
                "linkedin": "https://www.linkedin.com/in/nelisiwebezana/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Tshepiso",
                "surname": "Mudau",
                "email": "mudaureneillwe@gmail.com",
                "github": "https://github.com/janesmith",
                "linkedin": "https://www.linkedin.com/in/janesmith/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Khuthadzo",
                "surname": "Tshifura",
                "email": "tshifurakhuthadzo@gmail.com",
                "github": "https://github.com/janesmith",
                "linkedin": "https://www.linkedin.com/in/janesmith/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Charmaine",
                "surname": "Mduli",
                "email": "charmainemdluli4@gmail.com",
                "github": "https://github.com/janesmith",
                "linkedin": "https://www.linkedin.com/in/janesmith/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Britney",
                "surname": "Mmetja",
                "email": "mmetjabritney@gmail.com",
                "github": "https://github.com/janesmith",
                "linkedin": "https://www.linkedin.com/in/janesmith/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Sakhumuzi",
                "surname": "Mchunu",
                "email": "sakhumuzimchunu@gmail.com",
                "github": "https://github.com/janesmith",
                "linkedin": "https://www.linkedin.com/in/janesmith/"
            },
        ]

        cols = st.columns(3)
        for idx, member in enumerate(team_members):
            with cols[idx % 3]:
                display_team_member(
                    image=member["image"],
                    name=member["name"],
                    surname=member["surname"],
                    email=member["email"],
                    github=member["github"],
                    linkedin=member["linkedin"]
                )
                st.markdown("<br>", unsafe_allow_html=True)

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