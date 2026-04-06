from flask import Flask, render_template,redirect,url_for,request
from m_gestor_de_gastos import leer_gastos,agregar_gasto,ordenar_gastos

app = Flask(__name__)

gastos = leer_gastos()

@app.route("/")
def home():
    #return "Hola Flask!"
    ordenar_gastos(gastos)
    return render_template('index.html', gastos=gastos)

@app.route("/agregar_datos", methods = ["POST", "GET"])
def agregar():
    if request.method == "POST":
        gasto = {
            "Monto" : int(request.form["monto"]),
            "Tipo" : request.form["tipo"],
            "Categoria" : request.form["categoria"],
            "Fecha" : request.form["fecha"]
         }
        agregar_gasto(gastos,gasto)
        return render_template('index.html', gastos=gastos)
    else:
        return render_template('agregar.html')

def pagina_no_encontrada(error):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    #debug es el modo de depuracion activo que significa que muestra los cambios cuando guardas
    app.run(debug=True)