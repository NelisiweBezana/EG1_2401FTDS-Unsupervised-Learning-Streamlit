import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Anime Recommender", 
                   page_icon=":shark:", 
                   layout="centered", 
                   initial_sidebar_state="expanded",
                   )

def display_team_member(image, name, surname, email, github, linkedin):
    st.image(image, width=120)
    st.markdown(f"**{name} {surname}**")
    st.markdown(f"Email: {email}")
    st.markdown(f"[GitHub]({github}) / [LinkedIn]({linkedin})")

# Loading data
anime_data = pd.read_csv('Data/anime.csv')
anime_data['genre'] = anime_data['genre'].fillna('')

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Get Started", "Recommender",  "EDA", "About Us",])

    # Anime Recommendation Page
    if page == "Recommender":
        st.title("Anime Recommendation")

        image = Image.open("visuals/assets/home_page.jpg") 
        st.image(image, use_column_width=True)

        st.write("## Select an Algorithm")
        algorithm = st.radio("Select an algorithm:", ("Content Based Filtering", "Collaborative Based Filtering"))

        st.write("## Enter Your Three Favorite Anime")
        first_anime = st.text_input("First Option")
        second_anime = st.text_input("Second Option")
        third_anime = st.text_input("Third Option")

        if st.button("Recommend"):
            if algorithm == "Content Based Filtering":
                # content-based filtering logic
                tfidf = TfidfVectorizer(stop_words='english')
                tfidf_matrix = tfidf.fit_transform(anime_data['genre'])
                cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

                def get_recommendations(anime_list):
                    # Ensure that user input anime are in the dataset
                    user_anime = anime_data[anime_data['name'].str.contains('|'.join(anime_list), case=False, na=False)]
                    if user_anime.empty:
                        st.write("None of the entered anime titles were found in the dataset.")
                        return []

                    # Find the indices of the user-selected anime
                    indices = user_anime.index.tolist()

                    # Calculate the average similarity score for each anime in the dataset
                    sim_scores = []
                    for idx in indices:
                        sim_scores.extend(list(enumerate(cosine_sim[idx])))

                    # Sort by similarity score and exclude the anime in the user’s list
                    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                    sim_scores = [i for i in sim_scores if i[0] not in indices]  # Exclude user input anime
                    sim_scores = sim_scores[:10]  # Get top 10 recommendations

                    # Extract anime names for recommended indices
                    anime_indices = [i[0] for i in sim_scores]
                    return anime_data.iloc[anime_indices]['name'].values

                recommendations = get_recommendations([first_anime, second_anime, third_anime])
                
                if len(recommendations) > 0:
                    st.write("### Recommended Anime:")
                    for rec in recommendations:
                        st.write(f"- {rec}")
                else:
                    st.write("No recommendations available.")
            else:
                # model-based collaborative filtering logic (loading a pickled model)
                pass

   
    # About Page
    elif page == "Get Started":
        st.title("Discover Your Next Favorite Anime")

        st.write("""
            Welcome to Anime Experts, where our passion for anime meets the power of cutting-edge technology. At Anime Experts, we strive to enhance the anime viewing experience for enthusiasts around the globe by leveraging advanced data-driven solutions. Our latest endeavor involves developing an intelligent Anime Recommender System, designed to provide personalized and highly accurate anime recommendations to our users.
        """)

        st.write("\n")
        image = Image.open("visuals/assets/about_page.jpg") 
        st.image(image, use_column_width=True)
        st.write("\n")

        # Get Started Section
        st.header("Get Started")
        st.write("""
            To begin exploring personalized anime recommendations, navigate to the Recomender page. Select your preferred recommendation method and input your top three anime choices. The recommender system will analyze your preferences and generate tailored recommendations, enhancing your viewing experience.
        """)

        # How It Works Section
        st.header("How It Works")
        st.write("""
            The recommender system suggests anime titles for you to watch by examining the anime you have already liked or rated and finding similar shows and movies you might enjoy. You can choose between two recommendation methods:
            - **Content-Based Filtering:** Recommends anime similar to what you already like.
            - **Collaborative Filtering:** Recommends anime based on what users with similar tastes enjoy.
        """)

        # Grid layout for "Why Use It" and "How to Use the App" sections
        col1, col2 = st.columns(2)

        with col1:
            # Why Use It Section
            st.header("Why Use It")
            st.write("""
                - **Discover New Anime:** Easily find new shows and movies that match your interests.
                - **Save Time:** No more endless searching for something to watch. Get personalized recommendations quickly.
                - **Enjoy More:** Spend more time enjoying great anime and less time deciding what to watch.
            """)

        with col2:
            # How to Use the App Section
            st.header("How to Use It")
            st.write("""
                1. **Select an Algorithm:** Choose either Content-Based Filtering or Collaborative Filtering.
                2. **Enter Your Favorites:** Input your three favorite anime titles.
                3. **Get Recommendations:** Click on the "Recommend" button to see your personalized anime suggestions.
            """)

    # EDA Page
    elif page == "EDA":
        st.title("Exploratory Data Analysis (EDA)")
        st.write("## Data Insights and Visualizations")
        
        # Define available visualizations
        visualizations = {
            "Genre Distribution": "genre_distribution",
            "Rating Distribution": "rating_distribution",
            "Top 10 Most Popular Anime": "top_10_popular",
            "Top Rated Anime": "top_rated",
        }
        
        visualization_choice = st.selectbox("Choose a visualization:", list(visualizations.keys()))
        
        # Display selected visualization with insights
        if visualization_choice == "Genre Distribution":
            st.subheader("Genre Distribution")
            fig, ax = plt.subplots(figsize=(10, 8))  # Increase figure size
            genre_counts = anime_data['genre'].str.split(', ').explode().value_counts()
            sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax)
            ax.set_xlabel('Count')
            ax.set_ylabel('Genre')
            ax.set_title('Genre Distribution')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - This bar chart shows the distribution of genres across the anime dataset.
            - The most common genres are Action, Comedy, and Drama.
            """)

        elif visualization_choice == "Rating Distribution":
            st.subheader("Rating Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size
            sns.histplot(anime_data['rating'].dropna(), bins=20, kde=True, ax=ax)
            ax.set_xlabel('Rating')
            ax.set_ylabel('Count')
            ax.set_title('Rating Distribution')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - This histogram shows the distribution of ratings across the anime dataset.
            - Most anime have ratings between 6 and 8.
            """)

        elif visualization_choice == "Top 10 Most Popular Anime":
            st.subheader("Top 10 Most Popular Anime")
            top_10_anime = anime_data.nlargest(10, 'members')
            fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size
            sns.barplot(x=top_10_anime['members'], y=top_10_anime['name'], ax=ax)
            ax.set_xlabel('Members')
            ax.set_ylabel('Anime')
            ax.set_title('Top 10 Most Popular Anime')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - This bar chart shows the top 10 most popular anime based on the number of members.
            - These anime titles have a high number of followers, indicating their popularity.
            """)

        elif visualization_choice == "Top Rated Anime":
            st.subheader("Top Rated Anime")
            top_rated_anime = anime_data.nlargest(10, 'rating')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=top_rated_anime['rating'], y=top_rated_anime['name'], ax=ax)
            ax.set_xlabel('Rating')
            ax.set_ylabel('Anime')
            ax.set_title('Top Rated Anime')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - This bar chart shows the top 10 highest-rated anime.
            - These titles are highly rated by viewers, indicating their quality and viewer satisfaction.
            """)


    # Team Page
    elif page == "About Us":
        st.title("Meet the team")
        st.write("Our team is a group of passionate individuals dedicated to creating an innovative anime recommender system. Each member brings unique skills and expertise to the project, contributing to its success. Below, you will find the team members behind the system, their roles, and how to connect with them.")
        
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


# Running the app
if __name__ == '__main__':
    main()