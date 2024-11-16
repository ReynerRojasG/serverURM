import telebot
from telebot import types
import time
from flask import current_app as app
from app import create_app 
from app import db
from app.models import User, Assignment, Submission

TELEGRAM_TOKEN = '7791610358:AAH1iKhjC4VPbZ3IZLlpZQORUg8awJQWkoM'
bot = telebot.TeleBot(TELEGRAM_TOKEN)
CHAT_ID = '-1002258035871'  # ID del grupo
mi_aplication = create_app()

@bot.message_handler(commands=['stats'])
def stats_command(message):
    print("Comando /stats recibido.")
    chat_id = message.chat.id

    try:
        bot.send_message(chat_id, "Procesando estadísticas, por favor espere...")

        with mi_aplication.app_context():  
            try:
                professors = User.query.filter_by(user_type='profesor').all()
                if not professors:
                    bot.send_message(chat_id, "No se encontraron profesores en la base de datos.")
                    return

                markup = types.InlineKeyboardMarkup()  

                for professor in professors:
                    button = types.InlineKeyboardButton(text=professor.user_name, callback_data=f"prof_{professor.user_id}")
                    markup.add(button)

                bot.send_message(chat_id, "Seleccione un profesor:", reply_markup=markup)

            except Exception as db_error:
                bot.send_message(chat_id, f"Error al acceder a la base de datos: {db_error}")
                print(f"Error al acceder a la base de datos: {db_error}")

    except Exception as e:
        bot.send_message(chat_id, f"Error al procesar la solicitud: {e}")
        print(f"Error en el comando /stats: {e}")


# Callback para seleccionar profesor
@bot.callback_query_handler(func=lambda call: call.data.startswith("prof_"))
def select_professor(call):
    professor_id = int(call.data.split("_")[1])  

    try:
        with mi_aplication.app_context():  
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
            - Entregas tardías: {late_submissions}
            - Nota más baja: {min_score if min_score is not None else "N/A"}
            - Nota más alta: {max_score if max_score is not None else "N/A"}
            - Nota promedio: {avg_score if avg_score is not None else "N/A"}
            """

            bot.send_message(call.message.chat.id, stats_message)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al procesar las estadísticas del profesor: {e}")

    bot.answer_callback_query(call.id)

def notify_assignment(student_name, start_date, final_date):
    message = f"Estimado estudiante @{student_name}. Tiene una nueva asignación.\n- Fecha inicial: {start_date}\n- Fecha final: {final_date}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_score(student_name, score):
    message = f"Estimado estudiante @{student_name}. Una asignación ha sido calificada.\nNota obtenida: {score}."
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_register(student_name, course_name):
    message = f"El estudiante @{student_name} se ha matriculado en el curso {course_name}."
    bot.send_message(chat_id=CHAT_ID, text=message)

def notify_submission(professor_name):
    message = f"Estimado profesor @{professor_name}. Una asignación está lista para calificar."
    bot.send_message(chat_id=CHAT_ID, text=message)

def start_bot(flask_app):
    print("Iniciando el bot de Telegram.")
    with flask_app.app_context():
        while True:
            try:
                print("Esperando mensajes...")
                bot.polling(none_stop=True)
            except Exception as e:
                print(f"Error en el polling: {e}")
                time.sleep(15)
