from flask import Flask, render_template, redirect, url_for, request, send_file

import random
import datetime

app = Flask(__name__)

secret_number = random.randint(1, 100)   #Αρχικοποίησε το παιχνίδι διαλέγοντας έναν τυχαίο αριθμό.
hints = []
tries = 0
gameover = False
time = datetime.datetime.now().strftime("%A %x %X")

@app.route("/")                             #Αρχική Σελίδα.
def mainpage():
    global secret_number
    global hints
    global tries
    global gameover

    secret_number = random.randint(1, 100)
    hints = []
    tries = 0
    gameover = False
    return render_template("index.html")

@app.route("/game", methods=["GET","POST"]) #Σελίδα Παιχνιδιού.
def gamepage():
    global secret_number
    global hints
    global tries
    global gameover
    global time

    if request.method == "POST":
        guess = int(request.form["guess"])
        tries +=1
        if tries == 1 and guess == secret_number:
            hints = [f"Συγχαρητήρια! Βρήκες τον αριθμό {guess} με την πρώτη!\nΠάτα το κουμπί 'Reset Game' για να παίξεις ξανά."]
            gameover = True
            with open("scoreboard.txt", "a", encoding="utf-8") as f:
                f.write(f"Ημερομηνία: {time}\nΑριθμός: {guess}, Προσπάθειες: {tries}\n\n")
        else:                               #Λογική Παιχνιδού.
            if guess < secret_number:
                hints.append(f"Ο αριθμός είναι μεγαλύτερος από το {guess}!")
            elif guess > secret_number:
                hints.append(f"Ο αριθμός είναι μικρότερος από το {guess}!")
            else:
                hints.append("Πάτα το κουμπί 'Reset Game' για να παίξεις ξανά.")
                hints.append(f"Συγχαρητήρια! Βρήκες τον αριθμό {guess} σε {tries} προσπάθειες!")
                with open("scoreboard.txt", "a", encoding="utf-8") as f:
                    f.write(f"Ημερομηνία: {time}\nΑριθμός: {guess}, Προσπάθειες: {tries}\n\n")
                gameover = True

    return render_template("game.html", hints=hints, tries=tries, gameover=gameover)

@app.route("/reset")                        #Επανακίννηση του παιχνιδού.
def resetgame():
    global secret_number
    global hints
    global tries
    global gameover

    secret_number = random.randint(1, 100)
    hints = []
    tries = 0
    gameover = False
    return redirect(url_for("gamepage"))

@app.route("/scoreboard")                   #Άνοιγμα του αρχείου με τα αποτελέσματα.
def scoreboard():
#ChatGPT Prompt: "How to open a plain txt file using Flask" ---> εντολή sent_file
    try:
        return send_file("scoreboard.txt", mimetype="text/plain")
    except FileNotFoundError:
        return "Δεν υπάρχουν αποτελέσματα ακόμα."
#Τέλος
if __name__ == "__main__":
    app.run()