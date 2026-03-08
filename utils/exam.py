



# from utils.chatbot import get_learning_response

# def generate_exam(topic):
#     prompt = f"Generate 5 multiple-choice questions on {topic}, without showing answers."
#     try:
#         response = get_learning_response(prompt)
#         return response  # Only questions, no answers
#     except Exception as e:
#         raise Exception(f"Error generating exam: {str(e)}")

# def evaluate_exam(questions, user_answers):
#     # Fetch correct answers separately
#     answer_prompt = f"Provide only correct answers (one per line) for these questions:\n{questions}"
#     correct_answers = get_learning_response(answer_prompt).splitlines()

#     print("Correct Answers:", correct_answers)  # Debugging Step

#     user_answer_lines = user_answers.splitlines()
#     marks = 0
#     mistakes = []

#     for i, (u_answer, correct_answer) in enumerate(zip(user_answer_lines, correct_answers)):
#         print(f"Q{i+1} - User: {u_answer}, Correct: {correct_answer}")  # Debugging Step
        
#         if u_answer.strip().lower() == correct_answer.strip().lower():
#             marks += 1
#         else:
#             mistakes.append(f"Q{i+1}: Your Answer: {u_answer}, Correct Answer: {correct_answer}")

#     feedback = "Great job! No mistakes." if not mistakes else "\n".join(mistakes)
#     return marks, feedback



# from utils.chatbot import get_learning_response
# import re

# def generate_exam(topic):
#     prompt = (
#         f"Generate 5 multiple-choice questions on the topic '{topic}'.\n"
#         f"Each question should be followed by four options labeled a), b), c), d), "
#         f"each on a separate line. Number the questions (e.g., 1., 2., etc.).\n"
#         f"Do NOT include the answers or explanations in this response.\n"
#         f"Example format:\n"
#         f"1. Question text\n"
#         f"a) Option 1\n"
#         f"b) Option 2\n"
#         f"c) Option 3\n"
#         f"d) Option 4\n"
#     )
#     try:
#         response = get_learning_response(prompt)
#         return format_mcq_text(response)
#     except Exception as e:
#         raise Exception(f"Error generating exam: {str(e)}")

# def format_mcq_text(text):
#     formatted = re.sub(r'(?<!\n)\s*([a-d]\))', r'\n\1', text)
#     return formatted.strip()

# def extract_option(answer):
#     match = re.search(r'([a-dA-D])', answer)
#     return match.group(1).lower() if match else None

# def evaluate_exam(questions, user_answers):
#     # Get correct answers
#     answer_prompt = (
#         f"Provide only the correct answer letters (a, b, c, or d) for these questions, one per line, numbered 1 to 5:\n"
#         f"{questions}"
#     )
#     correct_answers_raw = get_learning_response(answer_prompt).strip()
#     correct_answers = correct_answers_raw.splitlines()
    
#     # Get explanations
#     explanation_prompt = (
#         f"For these questions, provide a one-line explanation for each correct answer, "
#         f"numbered 1. to 5. to match the questions (e.g., '1. Explanation text'), one per line:\n"
#         f"{questions}"
#     )
#     explanations_raw = get_learning_response(explanation_prompt).strip()
#     explanations = explanations_raw.splitlines()

#     # Debugging: Print raw responses to inspect
#     print("Debug - Correct Answers Raw:\n", correct_answers_raw)
#     print("Debug - Explanations Raw:\n", explanations_raw)

#     user_answer_lines = user_answers.strip().splitlines()
#     marks = 0
#     mistakes = []

#     # Ensure we have 5 answers and explanations
#     if len(correct_answers) != 5 or len(explanations) != 5:
#         raise ValueError(f"Expected 5 answers and explanations, got {len(correct_answers)} answers and {len(explanations)} explanations")

#     for i, (u_answer, correct_answer, explanation) in enumerate(
#         zip(user_answer_lines, correct_answers, explanations)
#     ):
#         user_opt = extract_option(u_answer)
#         correct_opt = extract_option(correct_answer)
#         # Clean explanation by removing numbering
#         explanation_text = re.sub(r'^\d+\.\s*', '', explanation).strip()

#         if user_opt == correct_opt:
#             marks += 1
#         else:
#             mistakes.append(
#                 f"Q{i+1}: Your Answer: {user_opt}\n"
#                 f"Correct Answer: {correct_opt})\n"
#                 f"Explanation: {explanation_text}"
#             )

#     feedback = "🎉 Great job! No mistakes." if not mistakes else "\n\n".join(mistakes)
#     return marks, feedback

# # Example usage
# if __name__ == "__main__":
#     topic = "full-stack development"
#     questions = generate_exam(topic)
#     print("📄 Questions")
#     print(questions)

#     user_answers = "a\na\na\na\na"
#     marks, feedback = evaluate_exam(questions, user_answers)
#     print(f"\n✅ Exam submitted successfully!")
#     print(f"🎓 Your Score: {marks}/5")
#     print("🧠 Mistakes & Feedback:")
#     print(feedback)






from utils.chatbot import get_learning_response
import re

def generate_exam(topic, difficulty="medium", num_questions=5):
    """Generate exam with configurable difficulty and number of questions
    
    Args:
        topic: Topic for the exam
        difficulty: 'easy', 'medium', or 'hard'
        num_questions: Number of questions (5-20)
    """
    difficulty_prompt = {
        "easy": "Generate simple, beginner-level questions.",
        "medium": "Generate moderate difficulty questions.",
        "hard": "Generate challenging, advanced-level questions that require deep understanding."
    }
    
    prompt = (
        f"Generate {num_questions} multiple-choice questions on '{topic}'.\n"
        f"{difficulty_prompt.get(difficulty, 'Generate moderate difficulty questions.')}\n"
        f"For each question, provide the question text followed by four options labeled a), b), c), d), "
        f"each on its own line with no extra text or formatting.\n"
        f"Number questions as 1., 2., etc.\n"
        f"Do NOT include answers or explanations.\n"
        f"Example:\n"
        f"1. What is X?\n"
        f"a) Option 1\n"
        f"b) Option 2\n"
        f"c) Option 3\n"
        f"d) Option 4\n"
    )
    response = get_learning_response(prompt).strip()
    return parse_questions(response)

def parse_questions(text):
    """Parse questions into structured format for button selection"""
    lines = text.splitlines()
    questions = []
    current_question = None
    current_options = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a question line (starts with digit followed by period)
        if re.match(r'^\d+\.\s', line):
            if current_question:
                questions.append({
                    "question": current_question,
                    "options": current_options
                })
            current_question = re.sub(r'^\d+\.\s', '', line)
            current_options = {}
        
        # Check if it's an option line (a), b), c), d))
        elif re.match(r'^[a-d]\)\s', line):
            option_key = line[0]
            option_text = re.sub(r'^[a-d]\)\s*', '', line)
            current_options[option_key] = option_text
    
    # Don't forget the last question
    if current_question:
        questions.append({
            "question": current_question,
            "options": current_options
        })
    
    return questions

def extract_option(answer):
    """Extract option letter (a, b, c, d) from user input"""
    for char in str(answer).lower():
        if char in 'abcd':
            return char
    return None

def evaluate_exam(questions_list, user_answers_dict):
    """Evaluate exam with answers stored as a dictionary {question_index: option}"""
    # Convert questions_list to text format for API calls
    questions_text = "\n".join([
        f"{i+1}. {q['question']}\n" +
        "\n".join([f"{opt}) {text}" for opt, text in q['options'].items()])
        for i, q in enumerate(questions_list)
    ])
    
    num_questions = len(questions_list)
    
    # Get correct answers
    answer_prompt = (
        f"For these questions, provide only the correct answer letters (a, b, c, or d), "
        f"one per line, in order:\n{questions_text}"
    )
    correct_answers = get_learning_response(answer_prompt).strip().splitlines()

    # Get explanations
    explanation_prompt = (
        f"For these questions, provide a one-line explanation for each correct answer, "
        f"one per line, numbered 1. to {num_questions}. (e.g., '1. Explanation text'):\n{questions_text}"
    )
    explanations = get_learning_response(explanation_prompt).strip().splitlines()

    marks = 0
    feedback_html = ['<div style="font-family: Arial; margin: 20px; color: #fff;">']

    for i in range(len(questions_list)):
        user_opt = user_answers_dict.get(i)
        correct_opt = extract_option(correct_answers[i]) if i < len(correct_answers) else None
        explanation = explanations[i].replace(f"{i+1}. ", "").strip() if i < len(explanations) else ""

        if user_opt and user_opt.lower() == correct_opt:
            marks += 1
        else:
            feedback_html.append(
                f'<div style="margin-top: 10px; padding: 12px; background-color: #2a2a2a; border-left: 4px solid #f44336; border-radius: 5px; color: #fff;">'
                f'<strong style="color: #f44336; font-size: 16px;">Q{i+1}: Your Answer: {user_opt or "Not Answered"}</strong><br>'
                f'<strong style="color: #4CAF50; font-size: 16px;">Correct Answer: {correct_opt}</strong><br>'
                f'<span style="color: #bbb; font-style: italic; font-size: 15px;">Explanation: {explanation}</span>'
                f'</div>'
            )

    if marks == len(questions_list):
        feedback_html.append('<div style="margin-top: 20px; padding: 15px; background-color: #1b5e20; border-radius: 5px; color: #4CAF50;"><h3 style="margin: 0; font-size: 18px;">🎉 Perfect! All answers correct!</h3></div>')
    elif marks > 0:
        feedback_html.append(f'<div style="margin-top: 20px; padding: 15px; background-color: #1a1a1a; border-left: 4px solid #FF9800; border-radius: 5px; color: #FF9800;"><h3 style="margin: 0; font-size: 18px;">Good effort! You got {marks}/{len(questions_list)} correct.</h3></div>')
    else:
        feedback_html.append('<div style="margin-top: 20px; padding: 15px; background-color: #1a1a1a; border-left: 4px solid #f44336; border-radius: 5px; color: #f44336;"><h3 style="margin: 0; font-size: 18px;">Keep studying! Review the explanations above.</h3></div>')
    
    feedback_html.append('</div>')
    return marks, '\n'.join(feedback_html)