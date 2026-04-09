from ui import LactateApp

if __name__ == "__main__":
    app = LactateApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Application closed by user.")