datos = {
    'nombre': 'producto nuevo probando json',
    'cantidad': 10,
    'precio': 15,
    'categoria': 'Alimentos'
    }

if datos.keys() in ['nombre', 'cantidad', 'precio']:
    print('si')
else:
    print('no')

print(datos.keys())

requerido = ['nombre', 'cantidad', 'precio']

# if all(key in datos for key in requerido):
#     print(all(key in datos for key in requerido))

for key in requerido:
    print(key in datos.keys())

data = [key in datos.keys() for key in requerido]
print(data)
