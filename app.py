from flask import Flask,render_template,request
import pickle
import numpy as np

top_50=pickle.load(open('top_50.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
book=pickle.load(open('book.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(top_50['Book-Title'].values),
                           book_author=list(top_50['Book-Author'].values),
                           book_image=list(top_50['Image-URL-M'].values),
                           book_votes=list(top_50['num_rating'].values),
                           book_rating=list(top_50['avg_rating'].values),



                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():

    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_item:
        item = []

        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('recommend.html',data=data)

if __name__ =='__main__':
    app.run(debug=True)


