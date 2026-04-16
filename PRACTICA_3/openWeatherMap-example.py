import json
import requests
from requests.structures import CaseInsensitiveDict

mykey = "TU_API_KEY_REAL"
mycity = "Cadiz"
units = "metric"

url = "https://api.openweathermap.org/data/2.5/weather?appid=" + mykey + "&q=" + mycity + "&units=" + units

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print("Metodo usado:", resp.request.method)
print("Status code:", resp.status_code)
print("URL enviada:", resp.request.url)
print("Respuesta cruda:", resp.text)

if resp.status_code == 200:
    json_data = json.loads(resp.text)
    print("Temperature:", json_data["main"]["temp"], "º")
else:
    print("Error en la petición")

#Por defecto, la temperatura está en grados Kelvin, para obtener grados Fahrenheit->imperial y Celsius->metric
#Con el código http podemos ver si ha habido algún error
#Mostramos la temperatura en la ciudad indicada
#Mostramos los datos crudos para que se vea todo lo que devuelve el endpoint "weather"