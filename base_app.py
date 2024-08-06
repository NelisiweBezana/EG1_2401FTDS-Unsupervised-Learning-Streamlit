import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import surprise
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split

st.set_page_config(page_title="Anime Recommender", 
                   page_icon=":shark:", 
                   layout="centered", 
                   initial_sidebar_state="expanded",
                   )

# Loading data
anime_data = pd.read_csv('Data/anime.csv')
anime_data['genre'] = anime_data['genre'].fillna('')
train_data = pd.read_csv('Data/train.csv')
test_data = pd.read_csv('Data/test.csv')

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
        
        all_anime_titles = anime_data['name'].tolist()
        first_anime = st.selectbox("First Option", options=[""] + all_anime_titles)
        second_anime = st.selectbox("Second Option", options=[""] + all_anime_titles)
        third_anime = st.selectbox("Third Option", options=[""] + all_anime_titles)

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
                    sim_scores = [i for i in sim_scores if i[0] not in indices]  # Excluding user input anime
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
                # model-based collaborative filtering logic
                # Load collaborative filtering model
                with open('models/Collaboration_filtering_model.pkl', 'rb') as file:
                    collaborative_filtering_model = pickle.load(file)

                # Collaborative filtering logic
                def get_collaborative_recommendations(user_anime):
                    # Ensure user_anime titles are in the dataset
                    user_anime_ids = anime_data[anime_data['name'].isin(user_anime)]['anime_id'].tolist()
                    
                    if not user_anime_ids:
                        st.write("None of the entered anime titles were found in the dataset.")
                        return []

                    # Prepare dataset for predictions
                    reader = Reader(rating_scale=(0, 10))
                    data = Dataset.load_from_df(train_data[['user_id', 'anime_id', 'rating']], reader)
                    trainset = data.build_full_trainset()

                    # Load collaborative filtering model
                    with open('models/Collaboration_filtering_model.pkl', 'rb') as file:
                        collaborative_filtering_model = pickle.load(file)

                    # Predict ratings for all anime
                    predictions = []
                    for anime_id in anime_data['anime_id']:
                        if anime_id not in user_anime_ids:
                            pred = collaborative_filtering_model.predict(uid='user_id', iid=anime_id)
                            predictions.append((anime_id, pred.est))
                    
                    # Sort predictions by estimated rating and get top 10
                    predictions.sort(key=lambda x: x[1], reverse=True)
                    top_recommendations = [anime_data[anime_data['anime_id'] == anime_id]['name'].values[0] for anime_id, _ in predictions[:10]]

                    return top_recommendations

                recommendations = get_collaborative_recommendations([first_anime, second_anime, third_anime])
                
                if len(recommendations) > 0:
                    st.write("### Recommended Anime:")
                    for rec in recommendations:
                        st.write(f"- {rec}")
                else:
                    st.write("No recommendations available.")


   
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

        anime_palette = sns.color_palette(["#00BFFF", "#1E90FF"])

        # Set the custom palette globally
        sns.set_palette(anime_palette)
        
        visualization_choice = st.selectbox("Choose a visualization:", list(visualizations.keys()))
        
        # Display selected visualization with insights
        if visualization_choice == "Genre Distribution":
            st.subheader("Genre Distribution")
            fig, ax = plt.subplots(figsize=(10, 8))
            genre_counts = anime_data['genre'].str.split(', ').explode().value_counts()
            sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax)
            ax.set_xlabel('Count')
            ax.set_ylabel('Genre')
            ax.set_title('Genre Distribution')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - Comedy is the most common genre, followed by Action, Adventure, and Fantasy.
            - The genres are sorted in descending order, with Comedy having the highest count and Yaoi the lowest.
            - Popular genres like Drama, Sci-Fi, and Romance also appear frequently, while niche genres like Yuri, Yaoi, and Josei are less common.
            - This chart indicates that anime often incorporates humor and action, with a diverse range of other themes also being well-represented.
            - The variety of genres suggests a wide array of anime content to cater to different audience preferences.
            """)

        elif visualization_choice == "Rating Distribution":
            st.subheader("Rating Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(anime_data['rating'].dropna(), bins=20, kde=True, ax=ax)
            ax.set_xlabel('Rating')
            ax.set_ylabel('Count')
            ax.set_title('Rating Distribution')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - Most anime ratings are around 6-7, meaning people generally rate shows in this range. 
            - The ratings spread from about 2 to 10, but very few shows get really low or really high scores. 
                     This pattern shows that most anime are seen as average or slightly above average. 
            - The shape of the ratings looks like a bell curve, with most scores clustering in the middle. 
            - Overall, it indicates that people tend to rate anime favorably.
            """)

        elif visualization_choice == "Top 10 Most Popular Anime":
            st.subheader("Top 10 Most Popular Anime")
            top_10_anime = anime_data.nlargest(10, 'members')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=top_10_anime['members'], y=top_10_anime['name'], ax=ax)
            ax.set_xlabel('Members')
            ax.set_ylabel('Anime')
            ax.set_title('Top 10 Most Popular Anime')
            st.pyplot(fig)
            st.write("""
            **Insights:**
            - “Death Note” leads with the highest number of members.
            - “Shingeki no Kyojin” and “Sword Art Online” follow closely.
            - Diverse Selection: The list includes a mix of genres, 
                     from action-packed series like “Naruto” to emotional dramas like “Angel Beats!”.
            - The number of members ranges from around 1.6 million for “Death Note” to lower numbers for others on the list.
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
            - Rating Scale: Ratings are on a scale from 0 to 10, with most top-rated anime scoring above 8.
            - Top Anime: “Fullmetal Alchemist: Brotherhood” and “Steins Gate” are among the highest-rated.
            - The list includes a variety of genres, from action-packed series like “Gintama” to emotional dramas like “Kimi no Na wa.”
            - This chart provides a visual representation of anime rankings, 
                    useful for recommendations or understanding popular preferences.
            """)


    # Team Page
    elif page == "About Us":
        st.title("Meet the team")
        st.write("Our team is a group of passionate individuals dedicated to creating an innovative anime recommender system. Each member brings unique skills and expertise to the project, contributing to its success. Below, you will find the team members behind the system, their roles, and how to connect with them.")
        
        def display_team_member(image, name, surname, role, email, github, linkedin):
            st.image(image, width=120)
            st.markdown(f"**{name} {surname}**")
            st.markdown(f"{role}")
            st.markdown(f"{email}")
            st.markdown(f"[GitHub]({github}) / [LinkedIn]({linkedin})")

        team_members = [
            {
                "image": "visuals/team/NelisiweBezana.jpg",
                "name": "Nelisiwe",
                "surname": "Bezana",
                "role" : "Model Dev | Streamlit Dev",
                "email": "nelisiwebezana@gmail.com",
                "github": "https://github.com/NelisiweBezana",
                "linkedin": "https://www.linkedin.com/in/nelisiwebezana/"
            },
            {
                "image": "visuals/team/TshepisoMudau.jpg",
                "name": "Tshepiso",
                "surname": "Mudau",
                "role" : "Model Dev",
                "email": "mudaureneillwe@gmail.com",
                "github": "https://github.com/tshepisoMudau",
                "linkedin": "https://www.linkedin.com/in/tshepiso-mudau-34b10226a/"
            },
            {
                "image": "visuals/team/KhuthadzoTshifura.jpg",
                "name": "Khuthadzo",
                "surname": "Tshifura",
                "role" : "Data Cleaning | EDA",
                "email": "tshifurakhuthadzo@gmail.com",
                "github": "https://github.com/tshifurakm",
                "linkedin": "https://www.linkedin.com/in/khuthadzo-tshifura-642671120/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Charmaine",
                "surname": "Mduli",
                "role" : "Model Dev",
                "email": "charmainemdluli4@gmail.com",
                "github": "https://github.com/charmainemdluli",
                "linkedin": "https://www.linkedin.com/in/charmaine-mdluli-427a3b221/"
            },
            {
                "image": "visuals/team/profile.jpg",
                "name": "Britney",
                "surname": "Mmetja",
                "role" : "Data processing",
                "email": "mmetjabritney@gmail.com",
                "github": "https://github.com/Britney44",
                "linkedin": "https://www.linkedin.com/in/mmetja-britney-b997362bb/"
            },
            {
                "image": "visuals/team/SakhumuziMchunu.jpg",
                "name": "Sakhumuzi",
                "surname": "Mchunu",
                "role" : "EDA",
                "email": "sakhumuzimchunu@gmail.com",
                "github": "https://github.com/SakhumuziMchunu",
                "linkedin": "https://www.linkedin.com/in/sakhumuzi-mchunu-ab5a99130/"
            },
        ]

        cols = st.columns(3)
        for idx, member in enumerate(team_members):
            with cols[idx % 3]:
                display_team_member(
                    image=member["image"],
                    name=member["name"],
                    surname=member["surname"],
                    role=member["role"],
                    email=member["email"],
                    github=member["github"],
                    linkedin=member["linkedin"]
                )
                st.markdown("<br>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()