from app import create_app
from app.services.telegram_service import start_bot
import threading

app = create_app()

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot, args=(app,), daemon=True)
    bot_thread.start()
    run_flask()
