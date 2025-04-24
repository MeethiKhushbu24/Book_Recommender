import streamlit as st
import pickle
import numpy as np
def recommend_book(book, num_recommend=5):
    index = np.where(pt.index == book)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:num_recommend+1]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

popular = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

st.header("Book Recommender System")

book_list = pt.index.values
image_url = popular['Image-URL-M'].tolist()
book_title = popular['Book-Title'].tolist()
book_author = popular['Book-Author'].tolist()
total_ratings = popular['total Ratings'].tolist()
avg_ratings = popular['Total Average Ratings'].tolist()

# Search + Recommend Section
st.sidebar.title("Recommend Books")
search_term = st.sidebar.text_input("Search a Book Title")
filtered_books = [title for title in book_list if search_term.lower() in title.lower()] if search_term else book_list
selected_book = st.sidebar.selectbox("Or pick from list", filtered_books)

num_recommend = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

if st.sidebar.button("Recommend Me"):
    recommended_books = recommend_book(selected_book, num_recommend)
    columns = st.columns(num_recommend)
    for i in range(num_recommend):
        with columns[i]:
            st.image(recommended_books[i][2])
            st.text(recommended_books[i][0])
            st.text(recommended_books[i][1])


# Top Books Display
st.sidebar.title("Top 20 Books")
if st.sidebar.button("SHOW"):
    for i in range(0, 20, 5):
        col1, col2, col3, col4, col5 = st.columns(5)
        for j, col in enumerate([col1, col2, col3, col4, col5]):
            idx = i + j
            col.image(image_url[idx])
            col.text(book_author[idx])
            col.text("Ratings: " + str(total_ratings[idx]))
            col.text("Avg.Rating: " + str(round(avg_ratings[idx], 2)))
