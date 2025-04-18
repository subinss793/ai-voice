from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from django.shortcuts import render, redirect
from django.contrib.auth import login
# from .forms import RegistrationForm  # Import the form
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Import the updated form
import speech_recognition as sr
import pyttsx3
from django.views.decorators.csrf import csrf_exempt

import speech_recognition as sr
from django.http import JsonResponse


from .models import PronunciationRecord


from django.shortcuts import render
from django.db.models import Count, Avg
from .models import PronunciationRecord
from datetime import datetime
import random




from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TestProgress


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from .models import TestProgress, Question

@login_required
def get_question(request):
    # Get or create the user’s progress
    progress, _ = TestProgress.objects.get_or_create(user=request.user)

    # Determine the level based on progress
    if progress.progress >= 100:
        level = "Advanced"
    elif progress.progress >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"
    print(level)
    # Fetch questions for the determined level
    questions = list(Question.objects.filter(level=level))

    if not questions:
        return JsonResponse({'error': f'No questions available for {level} level'}, status=404)

    # Pick a random question for variety
    question = random.choice(questions)

    return JsonResponse({
        'question': question.question,
        'answer_key': question.answer_key,
        'level': level,
    })



@login_required
@login_required
def check_answer(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        # Get user progress or create if not exists
        progress, _ = TestProgress.objects.get_or_create(user=request.user)

        # Fetch the current level directly from the TestProgress table
        level = progress.level

        # Check the recorded answer against the correct answer
        recorded_answer = data.get('recorded_answer', '').strip().lower()
        correct_answer = data.get('correct_answer', '').strip().lower()

        question = Question.objects.filter(answer_key=correct_answer).first()

        if  correct_answer in recorded_answer.split():
            # Increment progress based on the level
            increment = 5 if level == "Beginner" else 10 if level == "Intermediate" else 15
            progress.progress = min(100, progress.progress + increment)

            # Update the level based on progress
            if progress.progress >= 100:
                progress.level = "Advanced"
            elif progress.progress >= 50:
                progress.level = "Intermediate"
            else:
                progress.level = "Beginner"

            progress.save()

            return JsonResponse({
                'correct': True,
                'progress': progress.progress,
                'level': progress.level
            })

        else:
            # Provide a hint if available, otherwise show a default message
            hint = question.hint if question and question.hint else "Try again! Think carefully."

            return JsonResponse({
                'correct': False,
                'hint': hint
            })

    return JsonResponse({'error': 'Invalid request method'}, status=405)




# Get Progress
@login_required
def get_test_progress(request):
    progress, created = TestProgress.objects.get_or_create(user=request.user)
    return JsonResponse({'progress': progress.progress, 'level': progress.level})

from .models import TestProgress
def test_view(request):
    # Fetch or create user's progress
    progress, _ = TestProgress.objects.get_or_create(user=request.user)

    # Determine the user's level based on progress
    if progress.progress >= 100:
        level = "Advanced"
    elif progress.progress >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    # Get questions for the user's level
    questions = Question.objects.filter(level=level)

    # Pick a random question if available
    if questions.exists():
        question = random.choice(questions)
    else:
        question = None  # Handle the case where no questions exist for the level

    # Pass the question and level to the template
    return render(request, 'test.html', {"question": question, "level": level})
# Update Progress
@csrf_exempt
@login_required

def update_progress(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body)
            increment = int(data.get('increment', 0))

            # Fetch or create progress record
            progress, created = TestProgress.objects.get_or_create(user=request.user)

            # Update Progress

            # Update Level
            if progress.progress >= 100:
                progress.level = 'Advanced'
            elif progress.progress >= 50:
                progress.level = 'Intermediate'
            else:
                progress.level = 'Beginner'

            progress.save()
            return JsonResponse({'progress': progress.progress, 'level': progress.level})

        except (ValueError, TypeError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid increment value'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def dashboard(request):
    # Get all records for the logged-in user
    records = PronunciationRecord.objects.filter(user=request.user).order_by('-timestamp')

    # Group records by date
    sessions = {}
    for record in records:
        date = record.timestamp.date()
        if date not in sessions:
            sessions[date] = {
                "words_practiced": 0,
                "correct_words": 0
            }
        sessions[date]["words_practiced"] += 1

        # Count as correct if accuracy is 80% or higher
        if record.accuracy >= 80:
            sessions[date]["correct_words"] += 1

    # Calculate accuracy and add feedback
    session_data = []
    for date, data in sessions.items():
        accuracy = (data["correct_words"] / data["words_practiced"]) * 100 if data["words_practiced"] > 0 else 0
        
        # Feedback logic
        if accuracy > 90:
            feedback = "✅ Excellent"
        elif accuracy > 70:
            feedback = "👍 Good"
        elif accuracy > 50:
            feedback = "⚠️ Needs Improvement"
        else:
            feedback = "❌ Poor"

        session_data.append({
            "date": date.strftime('%Y-%m-%d'),
            "words_practiced": data["words_practiced"],
            "accuracy": round(accuracy, 2),
            "feedback": feedback
        })

    # Calculate total practice sessions and overall accuracy
    practice_sessions = len(sessions)
    total_words_practiced = sum(data["words_practiced"] for data in sessions.values())
    total_correct_words = sum(data["correct_words"] for data in sessions.values())
    progress_score = (total_correct_words / total_words_practiced) * 100 if total_words_practiced > 0 else 0

    context = {
        "user": request.user,
        "practice_sessions": practice_sessions,
        "progress_score": round(progress_score, 2),
        "sessions": session_data
    }

    return render(request, "dashboard.html", context)

# TEST_QUESTIONS = [
#     {"question": "What colour is your car?", "answer_key": "green"},
#     {"question": "Where do you live?", "answer_key": "city"},
#     {"question": "What is your favorite food?", "answer_key": "pizza"},
#     {"question": "What is the capital of France?", "answer_key": "paris"},
# ]

@login_required
def get_next_question(request):
    questions = list(Question.objects.all())  # Fetch all questions
    if questions:
        question = random.choice(questions)
        return JsonResponse({
            'question': question.question,
            'answer_key': question.answer_key,
        })
    return JsonResponse({'error': 'No questions found'}, status=404)

@login_required
def test_view(request):
    # Fetch or create user's progress
    progress, _ = TestProgress.objects.get_or_create(user=request.user)

    # Determine the user's level based on progress
    if progress.progress >= 100:
        level = "Advanced"
    elif progress.progress >= 50:
        level = "Intermediate"
    else:
        level = "Beginner"

    # Get questions for the user's level
    questions = Question.objects.filter(level=level)

    # Pick a random question if available
    if questions.exists():
        question = random.choice(questions)
    else:
        question = None  # Handle the case where no questions exist for the level

    # Pass the question and level to the template
    return render(request, 'test.html', {"question": question, "level": level})


@login_required
def get_progress(request):
    records = PronunciationRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
    data = [
        {
            "word": record.word,
            "spoken_word": record.spoken_word,
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for record in records
    ]
    return render(request, "progress.html", {"records": records})



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create the user but don't save yet
            user = form.save(commit=False)

            # Set custom fields
            user.age = form.cleaned_data.get("age")
            user.gender = form.cleaned_data.get("gender")
            
            # Save the user with custom fields
            user.save()
            
            return redirect("login")  # Redirect to login page
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

# def dashboard(request):
#     return render(request, "dashboard.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("/login/")

@login_required
def view_progress(request):
    records = PronunciationRecord.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, "progress.html", {"records": records})

@login_required
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError:
        return "Error: Speech recognition service unavailable"

@csrf_exempt
def record_audio(request):
    if request.method == "POST":
        spoken_word = recognize_speech()
        return JsonResponse({"message": f"You said: {spoken_word}"})
    return JsonResponse({"error": "Invalid request"}, status=400)


from .models import PronunciationRecord
from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import PronunciationRecord
import difflib
import json


@login_required
def check_pronunciation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            word = data.get("word", "").strip().lower()
            spoken_word = data.get("spoken_word", "").strip().lower()

            if not word or not spoken_word:
                return JsonResponse({"message": "⚠️ Please enter a valid word and try again."})

            # Calculate similarity
            similarity = difflib.SequenceMatcher(None, spoken_word, word).ratio()

            print(similarity)
            accuracy = int(round(similarity * 100)) 

            # Provide feedback message
            if accuracy >= 80:
                message = "✅ Correct pronunciation!"
            else:
                message = f"❌ Incorrect! You said '{spoken_word}', but the correct word is '{word}' (Accuracy: {accuracy}%)."

            # Save the record
            PronunciationRecord.objects.create(user=request.user, accuracy=accuracy, word=word, spoken_word=spoken_word)
            print("Record created:", word, spoken_word, "Accuracy:", accuracy)

            return JsonResponse({"message": message})
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid data format"}, status=400)

    return render(request, "check_pronunciation.html")


from django.shortcuts import render
from googletrans import Translator

def translate_text(request):
    translated_text = None  # Default value
    original_text = ""  # Default value
    target_language = "en"  # Default target language

    if request.method == "POST":
        original_text = request.POST.get("text")
        target_language = request.POST.get("language")

        # Use Google Translator
        translator = Translator()
        translated_text = translator.translate(original_text, dest=target_language).text

    return render(request, "translate.html", {
        "translated_text": translated_text,
        "original_text": original_text,
        "target_language": target_language
    })


from django.shortcuts import render

def home(request):
    return render(request, 'base.html')
