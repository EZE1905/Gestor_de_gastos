from flask import Flask, render_template,redirect,url_for,request,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import sqlite3
from m_gestor_gastos_sql import obtener_movimientos,calcular_movimientos,agregar_movimiento,eliminar_movimiento,editar_movimiento,obtener_un_movimiento,obtener_movimientos_por_mes,meses,total_meses,calcular_por_categoria, crear_tabla_usuarios, agregar_usuario, verificar_usuario, obtener_usuario_por_id
app = Flask(__name__)
app.secret_key = 'super_secret_key' # Necesario para sesiones

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    usuario = obtener_usuario_por_id(user_id)
    if usuario:
        return User(usuario['id_usuario'], usuario['username'])
    return None

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


@app.route("/")
@login_required
def home():
    mes = request.args.get("mes")
    movimientos_por_mes = obtener_movimientos_por_mes(mes, current_user.id)
    mestitulo = meses(mes)
    saldo,total_gastado,total_ingresos = calcular_movimientos(movimientos_por_mes)
    return render_template('index.html',saldo=saldo,total_gastado=total_gastado,total_ingresos=total_ingresos,movimientos_por_mes=movimientos_por_mes,mestitulo=mestitulo)

@app.route("/agregar_datos", methods = ["POST", "GET"])
@login_required
def agregar():
    if request.method == "POST":
        id_usuario = current_user.id
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
@login_required
def eliminar():
    id_movimiento = request.form["id_movimiento"]
    eliminar_movimiento(id_movimiento, current_user.id)
    flash('Dato eliminado correctamente','error') # Mensaje flash
    return redirect("/")

@app.route("/editar", methods = ["GET", "POST"])
@login_required
def editar():
    if request.method == "GET":
        id_movimiento = request.args.get("id_movimiento")
        movimiento = obtener_un_movimiento(id_movimiento, current_user.id)
        return render_template('editar.html',movimiento=movimiento)
    elif request.method == "POST":
        id_movimiento = request.form["id_movimiento"]
        monto = request.form["monto"]
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]
        editar_movimiento(id_movimiento,monto,tipo,categoria,fecha, current_user.id)
        flash('Dato editado correctamente','info') # Mensaje flash
        return redirect("/")

@app.route("/resumen")
@login_required
def resumen():
    mes = request.args.get("mes")
    movimientos_por_mes = obtener_movimientos_por_mes(mes, current_user.id)
    mestitulo = meses(mes)
    cat_gastos, cat_ingresos = calcular_por_categoria(movimientos_por_mes)
    saldo, total_gastado, total_ingresos = calcular_movimientos(movimientos_por_mes)
    totales = {
        "gastos" : total_gastado,
        "ingresos" : total_ingresos,
        "saldo" : saldo
    }
    movimientos = obtener_movimientos(current_user.id)
    ingresos_meses,gastos_meses = total_meses(movimientos)
    return render_template('resumen.html',ingresos_meses=ingresos_meses,gastos_meses=gastos_meses,mestitulo = mestitulo,mes = mes,movimientos_por_mes=movimientos_por_mes,cat_gastos=cat_gastos,cat_ingresos=cat_ingresos,totales=totales)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = verificar_usuario(form.username.data, form.password.data)
        if usuario:
            user_obj = User(usuario['id_usuario'], usuario['username'])
            login_user(user_obj)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            agregar_usuario(form.username.data, form.password.data)
            flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario ya existe', 'error')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

def pagina_no_encontrada(error):
    return redirect(url_for("index"))

if __name__ == "__main__":
    crear_tabla_usuarios()
    app.register_error_handler(404,pagina_no_encontrada)
    #debug es el modo de depuracion activo que significa que muestra los cambios cuando guardas
    app.run(debug=True)