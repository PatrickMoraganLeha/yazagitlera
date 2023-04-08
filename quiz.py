# Здесь будет код веб-приложения
import os 
from random import shuffle
from flask import Flask,session, request, redirect , render_template ,url_for
from db_scripts import get_question_after , get_quises, check_answer 
quiz = 0
last_question = 0

def start_quiz(quiz_id):
    '''создает нужные значения в словаре session'''
    session['quiz'] = quiz_id 
    session['last_question'] = 0
    session['answer'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    '''функция получает список викторин из базы и формурирует форму с выподающим списком'''
    q_lest = get_quises()
    return render_template('start.html',q_lest=q_lest)

def index():
    global quiz , last_question
    quiz = 1
    last_question = 0
    
    
    return '<img src="\images.jpg" alt="ал"> <h1 style="font-family: Georgia; margin: auto;">это игра тест но не тесто</h1> <h2>Нажми что бы начать</h2> <a href="/test" style="font-size: 30px;">samal</a>'
    
    '''Первая страница: если пришли запросам GET, то выбрать викторину если 
    POST - то запомнить id викторниы и отпровлять на вопросы'''
    if request.method == 'GET':
        #Викторнина не выброна сбрасываем id викторины и показываем форму выбора
        start_quiz(-1)
        return quiz_form()
    else:
        #получаем допалнительные данные в вопросе Используем их:
        quest_id = request.form.get('quiz')#выбранный номер викторины 
        start_quiz(quest_id)
        return redirect(url_for('test'))

def save_answer():
    '''Получает данные из формы, проверяет , верен ли ответ , записывает итоги в сессию'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    #этот вопрос уже задан
    session['last_question'] = quest_id
    # Увеличиваем счетчик вопросов:
    session['total'] +=1
    #проверить, совподает ли ответ с верным для этого 
    if check_answer(quest_id,answer):
        session['answers'] += 1

def question_form(question):
    '''получает строку из базы данных соответсвующий вопросу возврощяет html  с формой'''
    #question = результат работы get_question_after
    #поля:
        # [0] - номер вопроса в викторине 
        # [1] - текст вопроса
        # [2] - правильный ответ, [3],[4],][5] - неверные 
    #перемешивает ответы
    answer_list = [
        question[2],question[3],question[4],question[5]
    ]
    shuffle(answer_list)
    #передаем в шаблон возврощяем резулшьтат
    return render_template('test.html',question=question[1],quest_id=question[0], answer_list=answer_list)
    
def test():
    result = get_question_after(last_question,quiz)
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        last_question = result[0]
        return '<h1>' + str(quiz) + '<br>' + str(result) + '</h1>'
    '''Возврощяет страницу вопроса
    # что если пользователь без выбора викторины пошел сразу на адрес '/test'?
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        #если нам пришли данные , то их надо прочитать и обновить информацию 
        if request.method == 'POST':
            save_answers()
    #в любом случаем разбираемся с текущим id вопроса
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            #вопросы закончились:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)'''

        
        
def result():
    #html = render_template('result.html',right=session['answers'], total=session['total'])
    #end_quiz()
    return '<h1 style="font-size:40px;">Поздраляю вы прошли тест это ваш итог:</h1> <h2 style"font-size:50px;">-300</h2>'
    #return html
    

folder = os.getcwd() #запомнили текущую рабочую папку
#создаем обьект веб-прилажения 
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/','index',index, methods=['post','get']) #создаем правило для URL '/'
app.add_url_rule('/test','test',test,methods=['post','get']) #создаем правило для URL '/test'
app.add_url_rule('/result','result',result,) #создаем правило для URL '/test'
#Устанавливаем ключ шифрования
app.config['SECRET_KEY'] = 'THisIsSecretSecretLifePretty'

if __name__ == "__main__":
    #Запускаем сервер
    app.run()
    