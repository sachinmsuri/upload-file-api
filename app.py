from api import create_app
import os

app=create_app()

if __name__ == "__main__":
    #create uploads folder
    folder = 'uploads/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    app.run()

