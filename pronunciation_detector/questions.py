from pronunciation.models import Question


# Test questions for each level
TEST_QUESTIONS = {
    "Beginner": [
        {"question": "What colour is your car?", "answer_key": "green", "hint": "It's the color of grass."},
        {"question": "Where do you live?", "answer_key": "city", "hint": "A large town with many buildings."},
        {"question": "What is your favorite food?", "answer_key": "pizza", "hint": "It's round, cheesy, and often has toppings."},
        {"question": "What is the capital of France?", "answer_key": "paris", "hint": "It's known as the 'City of Light'."},
        {"question": "How many legs does a cat have?", "answer_key": "4", "hint": "It's more than two but less than five."},
        {"question": "What sound does a dog make?", "answer_key": "bark", "hint": "Dog's sound is often loud and sharp."},
        {"question": "What do you use to write?", "answer_key": "pen", "hint": "It's mightier than the sword."},
        {"question": "What is the opposite of hot?", "answer_key": "cold", "hint": "You feel this in winter."},
        {"question": "What do you drink when thirsty?", "answer_key": "water", "hint": "It's clear, essential, and found in rivers."},
        {"question": "What shape has three sides?", "answer_key": "triangle", "hint": "It has three angles."},
        {"question": "What color is the sky on a clear day?", "answer_key": "blue", "hint": "The sky is ___."},
        {"question": "What do you wear on your feet?", "answer_key": "shoes", "hint": "You wear ___ to walk outside."},
        {"question": "What do you use to brush your teeth?", "answer_key": "toothbrush", "hint": "A ___ keeps your teeth clean."},
        {"question": "What animal says 'meow'?", "answer_key": "cat", "hint": "A ___ says 'meow'."},
        {"question": "What do you open to enter a room?", "answer_key": "door", "hint": "You open a ___ to go inside."},
        {"question": "What do you drink from?", "answer_key": "glass", "hint": "You drink water from a ___."},
        {"question": "What do you sleep on?", "answer_key": "bed", "hint": "You sleep on a ___."},
        {"question": "What do you use to eat soup?", "answer_key": "spoon", "hint": "You need a ___ to eat soup."},
        {"question": "What do birds build to lay eggs?", "answer_key": "nest", "hint": "A bird makes a ___ for its eggs."},
        {"question": "What do you turn on to see in the dark?", "answer_key": "light", "hint": "You turn on the ___ in the dark."},
    ],
    "Intermediate": [
        {"question": "Name a continent where lions live.", "answer_key": "africa", "hint": "Home to the Sahara Desert."},
        {"question": "What is the currency of Japan?", "answer_key": "yen", "hint": "It's a three-letter word."},
        # {"question": "What gas do plants absorb?", "answer_key": "carbondioxide", "hint": "Humans exhale this."},
        {"question": "Who painted the Mona Lisa?", "answer_key": "da vinci", "hint": "His first name is Leonardo."},
        {"question": "What is the largest planet?", "answer_key": "jupiter", "hint": "Named after the king of Roman gods."},
        {"question": "What do bees produce?", "answer_key": "honey", "hint": "It's sweet and made by bees."},
        {"question": "How many seconds are in a minute?", "answer_key": "sixty", "hint": "It's a multiple of ten."},
        {"question": "What color is an emerald?", "answer_key": "green", "hint": "The same color as grass."},
        {"question": "What do you call a baby dog?", "answer_key": "puppy", "hint": "It's playful and cute."},
        {"question": "What instrument has black and white keys?", "answer_key": "piano", "hint": "You play it by pressing keys."},
    ],
    "Advanced": [
        {"question": "What is the powerhouse of the cell?", "answer_key": "mitochondria", "hint": "It generates energy for the cell."},
        {"question": "Who discovered gravity?", "answer_key": "newton", "hint": "An apple famously fell on his head."},
        {"question": "What is the hardest natural substance?", "answer_key": "diamond", "hint": "It’s often used in engagement rings."},
        {"question": "Which element has the chemical symbol 'O'?", "answer_key": "oxygen", "hint": "Essential for breathing."},
        {"question": "What is the speed of light in vacuum?", "answer_key": "299792458", "hint": "It's a very large number."},
        {"question": "In which year did World War II end?", "answer_key": "1945", "hint": "It ended in the mid-40s."},
        {"question": "What planet is known as the 'Red Planet'?", "answer_key": "mars", "hint": "Named after the Roman god of war."},
        {"question": "What is the study of fossils called?", "answer_key": "paleontology", "hint": "It involves studying ancient life forms."},
        {"question": "What language has the most native speakers?", "answer_key": "chinese", "hint": "Spoken by over a billion people."},
        {"question": "What organ produces insulin?", "answer_key": "pancreas", "hint": "Located behind the stomach."},
    ]
}
# Add questions to the database
for level, questions in TEST_QUESTIONS.items():
    for q in questions:
        Question.objects.create(
            level=level,
            question=q['question'],
            answer_key=q['answer_key'],
            hint=q.get('hint', 'No hint available')
        )

print("Questions added successfully!")

