import streamlit as st

def main():
    st.image("visuals/assets/background_image.png", use_column_width=True)

    st.title("Movie Recommendation System")

    st.header("Select an algorithm")
    algorithm = st.radio("Select an algorithm:",
                         ('Content Based Filtering', 'Collaborative Based Filtering'))

    st.header("Enter Your Three Favorite Movies")
    first_option = st.text_input("First Option")
    second_option = st.text_input("Second Option")
    third_option = st.text_input("Third Option")

    if st.button("Recommend"):
        pass

if __name__ == "__main__":
    main()



