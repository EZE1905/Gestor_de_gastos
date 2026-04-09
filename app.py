from flask import Flask, render_template,redirect,url_for,request
import json
from m_gestor_de_gastos import leer_gastos,agregar_gasto,ordenar_gastos,calcular_gastos,eliminar_gasto

app = Flask(__name__)

gastos = leer_gastos()

@app.route("/")
def home():
    #return "Hola Flask!"
    ordenar_gastos(gastos)
    saldo, total_gastado, total_ingresos = calcular_gastos(gastos)
    saldo_formateado = f"{saldo:,}".replace(",", ".")
    ingreso_formateado = f"{total_ingresos:,}".replace(",", ".")
    gasto_formateado = f"{total_gastado:,}".replace(",", ".")
    return render_template('index.html', gastos=gastos,saldo = saldo_formateado,total_gastado = gasto_formateado,total_ingresos = ingreso_formateado )

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
        return redirect('/')
    else:
        return render_template('agregar.html')

@app.route("/eliminar", methods = ["POST"])
def eliminar():
    indice = int(request.form["indice"])
    eliminar_gasto(gastos,indice)
    return redirect("/")

@app.route("/editar", methods = ["GET", "POST"])
def editar():
    if request.method == "GET":
        indice = request.args.get("indice")
        indice = int(indice)
        gasto = gastos[indice]
        return render_template('editar.html',gasto = gasto,indice = indice)
    elif request.method == "POST":
        nuevo_gasto = {
            "Monto" : int(request.form["monto"]),
            "Tipo" : request.form["tipo"],
            "Categoria" : request.form["categoria"],
            "Fecha" : request.form["fecha"]
        }
        indice = int(request.form["indice"])
        gastos[indice] = nuevo_gasto
        with open ("gastos.json", "w") as archivo:
            json.dump(gastos,archivo,indent=4) 
        return redirect("/")

def pagina_no_encontrada(error):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    #debug es el modo de depuracion activo que significa que muestra los cambios cuando guardas
    app.run(debug=True)