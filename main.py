#################################################################################################
############################################ IMPORTS ############################################
#################################################################################################
from flask import Flask, render_template, request, redirect, session, flash
from bd import tratamentos, pacientes, usuarios
from functions import pacientesTable_toHTML
from time import sleep
import bcrypt

##################
#### FLASK APP ###
##################

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

#############
### ROTAS ###
#############

# HOME
@app.route('/home')
def home():
    return render_template('home.html')

# LOGOUT
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return render_template('landing_page.html')

#############
### LOGIN ###
#############

# ROTA LOGIN
@app.route('/')
def login_page():
    return render_template('login.html', boolean = True)

# Rota de login
@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Buscar o usuário no banco de dados
    user = usuarios.find_one({'username': username})

    # Verificar usuário e senha
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        flash('Login feito com sucesso!', category='success')
        return redirect('/home')
    else:
        flash('Usuário ou senha incorreto!', category='error')
        sleep(2)
        return redirect("/")

################
### PACIENTE ###
################

@app.route('/paciente', methods = ['GET', 'POST'])
def paciente_novo():

    if request.method == 'POST':
        paciente_dict = request.form.to_dict()

        # Inserir o novo usuário no banco de dados
        pacientes.insert_one(paciente_dict)

        flash('Paciente cadastrado com sucesso!', category='success')
        return redirect('/tratamento')

    return render_template('paciente.html')

################
### CONSULTA ###
################

@app.route('/consulta')
def paciente_consulta():
    pacientesTable_toHTML()
    return render_template('consulta.html')

##################
### TRATAMENTO ###
##################

@app.route('/tratamento', methods = ['GET', 'POST'])
def tratamento():

    if request.method == 'POST':
        tratamento_dict = request.form.to_dict()

        # Inserir o novo usuário no banco de dados
        tratamentos.insert_one(tratamento_dict)

        flash('Tratamento cadastrado com sucesso!', category='success')
        return redirect('/tratamento')

    return render_template('tratamento.html')

#################################
############## RUN ##############
#################################

if __name__ == '__main__':
    app.run(debug=True)