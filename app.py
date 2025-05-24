from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, session
import xmlrpc.client 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from Model.database import get_medecin_info, get_all_incidents, get_medecin

app = Flask(__name__)
app.secret_key = "ton_secret_key"


@app.route('/')
def index():
    if "username" in session:
        username = session['username']
        print("Username en session:", username)  # Pour debug
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        record = get_medecin(username)
        if record and password == record[0]:  # Hash recommandé ici
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def get_rpc_client():
    return xmlrpc.client.ServerProxy("http://localhost:8000/")

@app.route("/get_temperature")
def get_temperature():
    try:
        rpc_client = get_rpc_client()
        temperature = rpc_client.get_temperature()
        return jsonify({"temperature": temperature})
    except Exception as e:
        print("Erreur RPC:", e)
        return jsonify({"temperature": None, "error": str(e)}), 500

        
@app.route("/set_temperature", methods=["POST"])
def set_temperature():
    try:
        new_temp = request.json.get("temperature")
        print("Nouvelle température reçue :", new_temp)
        rpc_client = get_rpc_client()
        message = rpc_client.set_temperature(new_temp)
        return jsonify({"message": message})
    except Exception as e:
        print("Erreur RPC:", e)
        return jsonify({"message": "Erreur lors de la mise à jour de la température", "error": str(e)}), 500

@app.route('/download_report')
def download_report():
    if "username" not in session:
        return redirect(url_for('login'))

    username = session['username']
    medecin = get_medecin_info(username)
    incidents = get_all_incidents()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Rapport d'incidents - Incubateur médical")

    # Infos médecin
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Médecin : {medecin[0]} {medecin[1]}")
    p.drawString(50, height - 100, f"Département : {medecin[2]}")

    # Table incidents
    p.drawString(50, height - 130, "Incidents enregistrés :")
    y = height - 150
    p.setFont("Helvetica", 10)
    p.drawString(50, y, "Date/Heure")
    p.drawString(150, y, "Température (°C)")
    p.drawString(300, y, "Type d'alerte")
    y -= 15

    for incident in incidents:
        if y < 50:
            p.showPage()
            y = height - 50
        date_heure, temperature, type_alerte = incident
        p.drawString(50, y, str(date_heure))
        p.drawString(150, y, f"{temperature}")
        p.drawString(300, y, type_alerte)
        y -= 15

    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="rapport_incidents.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
