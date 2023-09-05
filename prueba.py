
with open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/models.py', 'rb') as f: 
    code = f.read()

with open('models_c.py', 'wb') as f: 
    f.write(code.replace(b'\x00', b''))