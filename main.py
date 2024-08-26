from shot_timer_app import ShotTimerApp

if __name__ == "__main__":
    app = ShotTimerApp()
    try:
        app.start()
    finally:
        app.close()
