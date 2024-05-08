from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def mark_answer(answer, user_answer, threshold=0.25):
    correct_answer = preprocess(answer)
    user_answer = preprocess(user_answer)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([correct_answer, user_answer])

    similarity_score = cosine_similarity(tfidf_matrix)[0,1]

    if similarity_score > threshold:
        return (True, similarity_score)
    else:
        return (False, similarity_score)
    
def main():
    answer = "Python is a programming language"
    user_answer = "Python is a programming language"
    print(mark_answer(answer, user_answer))

if __name__ == "__main__":
    main()