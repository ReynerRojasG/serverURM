from app import create_app
from app.services.telegram_service import start_bot 
import threading

app = create_app()

if __name__ == "__main__":
    #bot_thread = threading.Thread(target=start_bot)
    #bot_thread.start()
    app.run(debug=True, use_reloader=False)

    
