from flask import Flask, render_template,redirect,url_for,request,flash
import json
from m_gestor_de_gastos import total_meses,leer_movimientos,agregar_gasto,ordenar_movimientos,calcular_movimientos,eliminar_gasto,calcular_por_categoria,filtrar_mes,meses
from m_gestor_gastos_sql import obtener_movimientos

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Necesario para sesiones

movimientos = obtener_movimientos()

@app.route("/")
def home():
    #return "Hola Flask!"
    mes = request.args.get("mes")
    movimientos_mes = filtrar_mes(mes,movimientos)
    mes_titulo = meses(mes)
    ordenar_movimientos(movimientos)
    saldo, total_gastado, total_ingresos = calcular_movimientos(movimientos_mes)
    saldo_formateado = f"{saldo:,}".replace(",", ".")
    ingreso_formateado = f"{total_ingresos:,}".replace(",", ".")
    gasto_formateado = f"{total_gastado:,}".replace(",", ".")
    return render_template('index.html',mes_titulo=mes_titulo,mes=mes,movimientos_mes=movimientos_mes, movimientos=movimientos,saldo = saldo_formateado,total_gastado = gasto_formateado,total_ingresos = ingreso_formateado )

@app.route("/agregar_datos", methods = ["POST", "GET"])
def agregar():
    if request.method == "POST":
        gasto = {
            "Monto" : int(request.form["monto"]),
            "Tipo" : request.form["tipo"],
            "Categoria" : request.form["categoria"],
            "Fecha" : request.form["fecha"]
         }
        agregar_gasto(movimientos,gasto)
        flash('Dato agregado correctamente','success') # Mensaje flash
        return redirect('/')
    else:
        return render_template('agregar.html')

@app.route("/eliminar", methods = ["POST"])
def eliminar():
    indice = int(request.form["indice"])
    eliminar_gasto(movimientos,indice)
    flash('Dato eliminado correctamente','error') # Mensaje flash
    return redirect("/")

@app.route("/editar", methods = ["GET", "POST"])
def editar():
    if request.method == "GET":
        indice = request.args.get("indice")
        indice = int(indice)
        gasto = movimientos[indice]
        return render_template('editar.html',gasto = gasto,indice = indice)
    elif request.method == "POST":
        nuevo_gasto = {
            "Monto" : int(request.form["monto"]),
            "Tipo" : request.form["tipo"],
            "Categoria" : request.form["categoria"],
            "Fecha" : request.form["fecha"]
        }
        indice = int(request.form["indice"])
        movimientos[indice] = nuevo_gasto
        with open ("movimientos.json", "w") as archivo:
            json.dump(movimientos,archivo,indent=4) 
        flash('Dato editado correctamente','info') # Mensaje flash
        return redirect("/")

@app.route("/resumen")
def resumen():
    mes = request.args.get("mes")
    movimientos_mes = filtrar_mes(mes,movimientos)
    mes_titulo = meses(mes)
    cat_movimientos, cat_ingresos = calcular_por_categoria(movimientos_mes)
    saldo, total_gastado, total_ingresos = calcular_movimientos(movimientos_mes)
    totales = {
        "movimientos" : total_gastado,
        "ingresos" : total_ingresos,
        "saldo" : saldo
    }
    ingreso,gasto = total_meses(movimientos)
    return render_template('resumen.html',ingreso=ingreso,gasto=gasto,mes_titulo = mes_titulo,mes = mes,movimientos_mes=movimientos_mes,cat_movimientos=cat_movimientos,cat_ingresos=cat_ingresos,totales=totales)

def pagina_no_encontrada(error):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    #debug es el modo de depuracion activo que significa que muestra los cambios cuando guardas
    app.run(debug=True)