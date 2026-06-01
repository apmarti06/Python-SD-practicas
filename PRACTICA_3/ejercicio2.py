import json
from bottle import Bottle, request, response, run

# Hacemos el código correspondiente a un endpoint

app = Bottle()

mis_elementos = [3, 1, 5, 7, 2]

@app.get('/inserta')
def inserta_get():
    """Endpoint GET para ver el estado actual y saber cómo usar el POST"""
    response.content_type = 'application/json'
    return {
        'mensaje': 'Para insertar un elemento usa POST con un JSON que contenga "elto"',
        'ejemplo': {'elto': 10},
        'mis_elementos_actuales': mis_elementos
    }

@app.post('/inserta')
def inserta():
    datos = request.json

    if datos is None or 'elto' not in datos:
        response.status = 400
        return {'error': 'Falta la clave "elto" en el json de entrada'}

    elto = datos['elto']

    # evaluamos los datos obtenidos del json

    if not isinstance(elto, int):
        response.status = 400
        return {'error': 'La clave "elto" debe contener un número entero'}

    # Si es correcta la lectura miramos que nos piden (si no existe insertamos en el final sino nada)

    if elto not in mis_elementos:
        mis_elementos.append(elto)

    response.content_type = 'application/json'
    return {'mis_elementos': mis_elementos}

run(app, host='localhost', port=8080, debug=True)