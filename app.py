from fastapi import FastAPI, Request, File, UploadFile
import requests
from starlette.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder
from json import JSONDecodeError
from fastapi.responses import JSONResponse
import os
from starlette.responses import FileResponse
import csv

app = FastAPI()




conn = sqlite3.connect('db.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS contas(tipo VARCHAR(10), valor VARCHAR(20))')

@app.get("/")
async def inicio():
    return {'ok':'ok'}

@app.post("/enviar")
async def enviar(request: Request):
    try:
        dict_json = await request.json();

    except Exception as e:
        print(e)

    print("-----------")
    print(dict_json)
    print("-----------")
    tipo = dict_json['0']
    valor = dict_json['1']
    
    #print(tipo + " " + valor);
    #print('----------------');

    try:
        cur = conn.cursor();
        cur.execute("INSERT INTO contas(tipo,valor) VALUES(?,?)",(tipo,valor));
        conn.commit();

    except Exception as e:
        #print('error')
        print(e)

    
    return 'enivado'

@app.get("/receber")
async def receber(request: Request):
    cur = conn.cursor();
    cur.execute('SELECT * FROM contas')
    resultados= cur.fetchall()
    json_compatible_item_data = jsonable_encoder(resultados)
    print(json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/deletar")
async def deletar(request: Request):
    cur = conn.cursor();
    cur.execute('DROP TABLE contas')
    conn.commit();
    return 'ok'

#@app.get("/resultado")
@app.post("/resultado")
@app.get("/resultado")
async def resultado(request: Request):
    cur = conn.cursor();
    cur.execute('SELECT * FROM contas')
    resultados= cur.fetchall()
    #print(resultados)
    #print('-------')
    #print(type(resultados))
    #print('-------')

    
    d = {}
    for x, y in resultados:
        d.setdefault(x, []).append(y)
    print(d)
    #print('-------')
    valores_entrada = d['Entrada']
    valores_saida = d['Saida']

    #print(valores_entrada)
    #print('-------')
    #print(valores_saida)
    #print('-------')

    #print("------ENTRADA")
    valores_entrada_convertido = [s.replace(',','.') for s in valores_entrada]
    #print(valores_entrada_convertido)
    valores_entrada_sem_vazio = list(filter(None,valores_entrada_convertido))
    #print(valores_entrada_sem_vazio)
    valores_entrada_convertido_final = [float(val) for val in valores_entrada_sem_vazio]
    #print(sum(valores_entrada_convertido_final))
    soma_entrada = sum(valores_entrada_convertido_final)
    #print(soma_entrada)
    #print("------SA??DA")

    valores_saida_convertido = [s.replace(',','.') for s in valores_saida]
    #print(valores_saida_convertido)
    valores_saida_sem_vazio = list(filter(None,valores_saida_convertido))
    #print(valores_saida_sem_vazio)
    valores_saida_convertido_final = [float(val) for val in valores_saida_sem_vazio]
    #print(sum(valores_saida_convertido_final))
    soma_saida = sum(valores_saida_convertido_final)
    #print(soma_saida)

    valor_final = soma_entrada-soma_saida
    #print('----SOMA')
    
    #df = pd.DataFrame(d)
    #print(df)
    valor_final_formatado = round(valor_final,2)
    #print({'valor':valor_final_formatado})

    json_compatible_item_data = jsonable_encoder(valor_final_formatado)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/datatable")
async def datatable(request: Request):
    cur = conn.cursor();
    cur.execute('SELECT * FROM contas')
    resultados= cur.fetchall()
    #print(resultados)
    #print('-------')
    #print(type(resultados))
    #print('-------')

    
    d = {}
    for x, y in resultados:
        d.setdefault(x, []).append(y)
    #print(d)
    #print('-------')
    

    
    return d

@app.get("/create_file/")
@app.post("/create_file/")
async def image():

    cur = conn.cursor();
    cur.execute('SELECT * FROM contas')
    resultados= cur.fetchall()
    print(resultados)
    #print('-------')
    print(type(resultados))
    #print('-------')

    
    d = {}
    for x, y in resultados:
        d.setdefault(x, []).append(y)
    print(d)
    print('-------D')
    print(type(d))

    # data to be written row-wise in csv fil
    
    # opening the csv file in 'w+' mode
    
    # writing the data into the file
    with open('meu_extrato.csv', 'w+', newline ='') as file:   
        
        write = csv.writer(file)
        
        write.writerows(resultados)


    csv_columns = ['Entrada', 'Saida']

    csv_file = "meu_extrato.csv"
    '''
    with open(csv_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames = csv_columns)
        for key in d.keys():
            writer.writerow(d[key])'''


    return FileResponse(path=csv_file, media_type='text/csv',filename=csv_file)
    #return 'ok'
    



app.add_middleware(CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["GET","POST"],
allow_headers=["*"],)