import csv
from tabulate import tabulate

from quiz_program import db
from quiz_program.models import User, Question, Quiz, Chapter, Textbook

def create_textbook(title):
    new_textbook = Textbook(title=title)
    db.session.add(new_textbook)
    new_textbook = Textbook.query.filter_by(title=title).first()
    print(f"Successfully created Textbook({new_textbook.title}, {new_textbook.id})!")

def create_chapter(title, textbook_id):
    new_chapter = Chapter(title=title, textbook_id=int(textbook_id))
    db.session.add(new_chapter)
    new_chapter = Chapter.query.filter_by(title=title).first()
    print(f"Successfully created Chapter({new_chapter.title}, {new_chapter.id}, {new_chapter.textbook})!")

    new_quiz = Quiz(title=title, chapter_id=new_chapter.id)
    db.session.add(new_quiz)
    new_quiz = Quiz.query.filter_by(title=title).first()
    print(f"Successfully created Quiz({new_quiz.title}, {new_quiz.id}, {new_quiz.chapter})!")

def add_question(questions_filename, quiz_id):

    with open(f'quiz_program/static/questions/{questions_filename}.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            print(line)
            question = Question(term=line['Term'], definition=line['Definition'], quiz_id=quiz_id)
            db.session.add(question)

def view_database():

    print('\n--------- TEXTBOOK ---------')
    table = [["id", "title"]]
    for textbook in Textbook.query.all():
        table.append([textbook.id, textbook.title])
    # print(table)
    print(tabulate(table, headers="firstrow", tablefmt="github"))

    print('\n--------- CHAPTER ----------')
    table = [["id", "title", "textbookID"]]
    for chapter in Chapter.query.all():
        table.append([chapter.id, chapter.title, chapter.textbook_id])
    print(tabulate(table, headers="firstrow", tablefmt="github"))

    print('\n----------- QUIZ -----------')
    table = [["id", "title", "chapterID"]]
    for quiz in Quiz.query.all():
        table.append([quiz.id, quiz.title, quiz.chapter_id])
    print(tabulate(table, headers="firstrow", tablefmt="github"))

    print('\n--------- QUESTION ---------')
    table = [["id", "term", "definition", "quizID"]]
    for question in Question.query.all():
        table.append([question.id, question.term, question.definition, question.quiz_id])
    print(tabulate(table, headers="firstrow", tablefmt="github"))

    print('\n----------- USER -----------')
    table = [["id", "username", "email", "profile pic"]]
    for user in User.query.all():
        table.append([user.id, user.username, user.email, user.image_file])
    print(tabulate(table, headers="firstrow", tablefmt="github"))

def commit_changes():
    db.session.commit()

def menu():
    while True:
        print('\nWelcome to the Recuerda Database!\n\nChoose one of the following options:')
        print('\n\t1. Add data\n\t\ta) Textbook\n\t\tb) Chapter and Quiz\n\t\tc) Questions')
        print('\t2. View Data\n\t3. Commit Changes\n\t4. Quit (Any unsaved changes will be lost)')

        option = input('\n')

        if option == '1a':
            title = input('\nTextbook Name: ')
            create_textbook(title)
        
        elif option == '1b':
            title = input('\nChapter (and Quiz) Name: ')
            textbook_id = int(input('\nTextbookID: '))
            create_chapter(title, textbook_id)

        elif option == '1c':
            questions_filename = input('\nQuestions Filename (no extension): ')
            quiz_id = int(input('\nQuizID: '))
            add_question(questions_filename, quiz_id)

        elif option == '2':
            view_database()

        elif option == '3':
            commit_changes()

        elif option == '4':
            break

        else:
            print('\nOption invalid!')

menu()