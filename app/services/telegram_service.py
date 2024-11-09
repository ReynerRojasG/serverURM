import telebot
from telebot import types
import time
from flask import current_app as app
from app import db 
from app.models import User, Assignment, Submission  


TELEGRAM_TOKEN = '7791610358:AAH1iKhjC4VPbZ3IZLlpZQORUg8awJQWkoM'
bot = telebot.TeleBot(TELEGRAM_TOKEN)
CHAT_ID = '-1002258035871' # Grupo

#TODO BOT COMANDO Stats
@bot.message_handler(commands=['stats'])
def stats_command(message):
    print("Comando /stats recibido.")
    chat_id = message.chat.id
    
    with app.app_context():
        professors = User.query.filter_by(user_type="Profesor").all()
        keyboard = types.InlineKeyboardMarkup()
        for professor in professors:
            keyboard.add(types.InlineKeyboardButton(professor.user_name, callback_data=f"prof_{professor.user_id}"))
    
        bot.send_message(chat_id, "Seleccione un profesor para ver estadisticas:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("prof_"))
def select_professor(call):
    professor_id = int(call.data.split("_")[1])

    with app.app_context():
        assignments = Assignment.query.filter_by(professor_id=professor_id).all()
        assignment_ids = [assignment.assignment_id for assignment in assignments]
        
        total_submissions = Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).count()
        late_submissions = Submission.query.join(Assignment, Submission.assignment_id == Assignment.assignment_id)\
            .filter(Submission.assignment_id.in_(assignment_ids))\
            .filter(Submission.submission_date > Assignment.final_date).count()
        min_score = Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).with_entities(db.func.min(Submission.submission_score)).scalar()
        max_score = Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).with_entities(db.func.max(Submission.submission_score)).scalar()
        avg_score = Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).with_entities(db.func.avg(Submission.submission_score)).scalar()
        
        stats_message = f"""
        Estadísticas para el profesor seleccionado:
        - Total de entregas: {total_submissions}
        - Entregas tardias: {late_submissions}
        - Nota mas baja: {min_score if min_score is not None else "N/A"}
        - Nota mas alta: {max_score if max_score is not None else "N/A"}
        - Nota promedio: {avg_score if avg_score is not None else "N/A"}
        """

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, stats_message)

def notify_assignment(student_name, start_date, final_date):
    message = f"Distinguido estudiante @{student_name}. Tiene una nueva asignacion.\n-Fecha inicial {start_date}\n-Fecha final {final_date}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_score(student_name, score):
    message = f"Querido estudiante @{student_name}. Una asignación le ha sido calificada\nNota obtenida: {score}."
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_register(student_name, course_name):
    message = f"El estudiante @{student_name} se ha matriculado en el curso {course_name}."
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_submission(professor_name):
    message = f"Querido profesor @{professor_name}. Una asignacion esta lista para calificar"
    bot.send_message(chat_id=CHAT_ID, text=message)
    
def start_bot():
    print("Iniciando el bot de Telegram.")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error en el polling: {e}")
            time.sleep(15)