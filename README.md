# Movie Recommendation System
## Tools I used
1) IDE : Visual Studio Code
2) GitHub
3) Front-End : Streamlit
4) Back-End : Pandas, Cosine-Similarity, TfidfVectorizer, SVD, Matplotlib, Plotly 
5) Language : Python
6) Storing Dataset : HuggingFace
7) Deployment : Streamlit Cloud

## Process
1> Download dataset from Kaggle
2> Import necessary libraries
3> Clean and transform dataset
4> Data analysis
5> Vectorize the data then reduce dimensions to increase the cosine score
6> Calculate the cosine similarity
7> Build recommendation function to show the results
8> Get API from https://www.themoviedb.org to access the poster of each movies
9> Upload .pkl(contains movies dataset and cosine similarity scores) files on HuggingFace
10> Setup streamlit UI and connect data from HuggingFace 
11> Deploy to Streamlit Cloud

## Conclusion
Through this project, i can improve my data process, cleaning, analysis and visualize skills very much. Due to limitation of knowledge so my recommendation results can not be 100% right, i always try to upgrade my project for a better results.

## Instruction  
1> Click the link in description above, or you can access here : https://movierecys.streamlit.app/ 

2> Waiting a moment until the data loaded successfully, then expand the box to find your movie or you can type your movie's name directly in the box  
<img width="1779" height="600" alt="image" src="https://github.com/user-attachments/assets/6c232b0c-aae9-4322-9dd4-d4ace0d1622b" />

3> After typing your movie's name, click "Get Recommendations", then the app will show you the top 10 movies base on your choice 
<img width="1748" height="820" alt="image" src="https://github.com/user-attachments/assets/8d04353b-8223-4eb6-a8b0-d186d5467894" />





