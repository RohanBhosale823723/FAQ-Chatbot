from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# FAQ Questions and Answers
faqs = [
    {
        "question": "What are the college timings?",
        "answer": "The college timing is from 9:00 AM to 4:00 PM."
    },
    {
        "question": "What courses are available?",
        "answer": "The college offers courses in Computer Science, Artificial Intelligence, Data Science and other fields."
    },
    {
        "question": "How can I get admission?",
        "answer": "You can get admission by completing the college admission process and submitting the required documents."
    },
    {
        "question": "What are the library timings?",
        "answer": "The library is open from 9:00 AM to 5:00 PM."
    },
    {
        "question": "When are the exams?",
        "answer": "The exam schedule is announced by the college department."
    },
    {
        "question": "How can I contact the college?",
        "answer": "You can contact the college office during working hours."
    },
    {
        "question": "What documents are required for admission?",
        "answer": "Required documents generally include academic certificates, identity proof and passport-size photographs."
    },
    {
        "question": "Is there a canteen in the college?",
        "answer": "Yes, the college has a canteen for students and staff."
    },
        {
        "question": "What is the attendance requirement?",
        "answer": "Students are required to maintain the minimum attendance as per college rules."
    },
    {
        "question": "What is the fee structure?",
        "answer": "The fee structure depends on the course. Please contact the college office for details."
    },
    {
        "question": "Does the college provide scholarships?",
        "answer": "Yes, eligible students can apply for available scholarships according to college and government rules."
    },
    {
        "question": "Is hostel facility available?",
        "answer": "Please contact the college administration for information about hostel facilities."
    },
    {
        "question": "What are the office timings?",
        "answer": "The college office is generally open during regular college working hours."
    },
    {
        "question": "How can I get my ID card?",
        "answer": "Students can collect their ID card from the college office after completing the required process."
    },
    {
        "question": "Where can I get the exam timetable?",
        "answer": "The exam timetable is published by the college department."
    },
    {
        "question": "Can I use the library after college hours?",
        "answer": "Library access depends on the library working hours and college rules."
    },
    {
        "question": "How can I apply for a scholarship?",
        "answer": "You can apply through the applicable scholarship portal and submit the required documents."
    },
    {
        "question": "Does the college have computer labs?",
        "answer": "Yes, computer labs are available for students according to their academic requirements."
    }
]

# Prepare FAQ questions
questions = [faq["question"] for faq in faqs]

# Convert questions into numerical vectors
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(questions)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json.get("question", "")

    if not user_question.strip():
        return jsonify({
            "answer": "Please enter a question."
        })

    # Convert user question into vector
    user_vector = vectorizer.transform([user_question])

    # Calculate similarity
    similarities = cosine_similarity(user_vector, faq_vectors)

    # Find most similar FAQ
    best_match_index = similarities.argmax()
    best_score = similarities[0][best_match_index]

    # Minimum similarity threshold
    if best_score < 0.20:
        answer = "Sorry, I don't understand your question. Please ask a college-related FAQ."
    else:
        answer = faqs[best_match_index]["answer"]

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)