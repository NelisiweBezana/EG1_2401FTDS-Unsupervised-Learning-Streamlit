import streamlit as st

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
        st.title("Project Overview")
        st.write("Details about the project, objectives, and goals.")

    # Team Page
    elif page == "Team":
        st.title("Meet the team")
        st.write("Details about team members.")
        
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

    