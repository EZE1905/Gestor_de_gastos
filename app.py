from flask import Flask, render_template,redirect,url_for

app = Flask(__name__)

@app.route("/")
def home():
    #return "Hola Flask!"
    return render_template('index.html')

@app.route("/agregar_datos")
def agregar():
    return render_template('agregar.html')

def pagina_no_encontrada(error):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    #debug es el modo de depuracion activo que significa que muestra los cambios cuando guardas
    app.run(debug=True)