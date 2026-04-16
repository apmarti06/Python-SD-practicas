import json

from bottle import  Bottle, request, response, run

#Hacemos el código correspondiente a un endpoint

app = Bottle()

mis_elementos = [3, 1, 5, 7, 2]

@app.post('/inserta')
def inserta():
    datos = request.json

    if datos is None or 'elto' not in datos:
        response.status = 400
        return {'error' : 'Falta la clave "elemento" en el json de entrada'}

    elto = datos['elto']

    #evaluamos los datos obtenidos del json

    if not isinstance(elto, int):
        response.status = 400
        return {'error': 'La clave "elemento" debe contener un número entero'}
    
    # Si es correcta la lectura miramos que nos piden (si no existe insertamos en el final sino nada)

    if elto not in mis_elementos:
        mis_elementos.append(elto)

    response.content_type = 'application/json'
    return {'mis_elementos' : mis_elementos}
    
run(app, host='localhost', port=8080, debug=True)
