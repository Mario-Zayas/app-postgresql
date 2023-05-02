from flask import Flask, render_template, abort, request
import json

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("inicio.html")

# @app.route('/listajuegos', methods=["POST"])
# def listajuegos():
#     with open("msx.json", "r") as archivo:
#         juegos = json.load(archivo)
        
#     parametro_busqueda = request.form.get('busqueda')
#     juegos_encontrados = []
#     busqueda_anterior = parametro_busqueda 
    
#     if parametro_busqueda:
#         juegos_encontrados = buscar_juego(juegos, parametro_busqueda)
#         if juegos_encontrados:
#             return render_template("listajuegos.html", juegos=juegos_encontrados, busqueda=busqueda_anterior)  
#         else:
#             mensaje = f"No se encontró ningún juego con el nombre '{parametro_busqueda}'."
#             return render_template("listajuegos.html", mensaje=mensaje, busqueda=busqueda_anterior)  
#     else:    
#         return render_template("listajuegos.html", juegos=juegos_encontrados, busqueda=busqueda_anterior)  

@app.route('/juegos', methods=['GET', 'POST'])
def juegos():
    with open("msx.json", "r") as archivo:
        juegos = json.load(archivo)
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        juegos_encontrados = buscar_juego(juegos, nombre)
        return render_template('juegos.html', juegos=juegos_encontrados)
        
    return render_template('juegos.html', juegos=juegos)


def buscar_juego(lista_juegos, nombre):
    juegos_encontrados = []
    for juego in lista_juegos:
        if juego["nombre"].lower() == nombre.lower():
            juegos_encontrados.append(juego)
    return juegos_encontrados



@app.route('/juego/<int:identificador>', methods=["GET", "POST"])
def juego(identificador):
    with open("msx.json", "r") as archivo:
        jueg = json.load(archivo)
        juego_encontrado2 = None
        encontrado = False
        for juego in jueg:
            if juego["id"] == identificador:
                juego_encontrado2 = juego
                encontrado = True
        if encontrado:
            return render_template("juego.html", nombre=juego_encontrado2["nombre"], año=juego_encontrado2["año"], identificador=identificador, id=juego_encontrado2["id"], sistema=juego_encontrado2["sistema"], distribuidor=juego_encontrado2["distribuidor"], desarrollador=juego_encontrado2["desarrollador"], categoria=juego_encontrado2["categoria"])
        else:
            abort(404)
            
app.run("0.0.0.0",5000,debug=True)



