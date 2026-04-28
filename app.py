from flask import Flask, render_template,redirect,url_for,request,flash
from m_gestor_gastos_sql import obtener_movimientos,calcular_movimientos,agregar_movimiento,eliminar_movimiento,editar_movimiento,obtener_un_movimiento,obtener_movimientos_por_mes,meses

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Necesario para sesiones


@app.route("/")
def home():
    mes = request.args.get("mes")
    movimientos_por_mes = obtener_movimientos_por_mes(mes)
    mestitulo = meses(mes)
    saldo,total_gastado,total_ingresos = calcular_movimientos(movimientos_por_mes)
    return render_template('index.html',saldo=saldo,total_gastado=total_gastado,total_ingresos=total_ingresos,movimientos_por_mes=movimientos_por_mes,mestitulo=mestitulo)

@app.route("/agregar_datos", methods = ["POST", "GET"])
def agregar():
    if request.method == "POST":
        id_usuario = 1
        monto = int(request.form["monto"])
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]
        agregar_movimiento(id_usuario,monto,categoria,tipo,fecha)
        flash('Dato agregado correctamente','success') # Mensaje flash
        return redirect('/')
    else:
        return render_template('agregar.html')

@app.route("/eliminar", methods = ["POST"])
def eliminar():
    id_movimiento = request.form["id_movimiento"]
    eliminar_movimiento(id_movimiento)
    flash('Dato eliminado correctamente','error') # Mensaje flash
    return redirect("/")

@app.route("/editar", methods = ["GET", "POST"])
def editar():
    if request.method == "GET":
        id_movimiento = request.args.get("id_movimiento")
        movimiento = obtener_un_movimiento(id_movimiento)
        return render_template('editar.html',movimiento=movimiento)
    elif request.method == "POST":
        id_movimiento = request.form["id_movimiento"]
        monto = request.form["monto"]
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]
        editar_movimiento(id_movimiento,monto,tipo,categoria,fecha)
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