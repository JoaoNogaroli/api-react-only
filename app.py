from fastapi import FastAPI, Request

import sqlite3
import pandas as pd
import numpy as np


app = FastAPI()

conn = sqlite3.connect('db.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS contas(tipo VARCHAR(10), valor VARCHAR(20))')

@app.get("/")
def inicio():
    return {'ok':'ok'}

@app.get("/enviar")
def enviar(request: Request):
    dict_json =request.json;
    #print(dict_json)
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
def receber(request: Request):
    cur = conn.cursor();
    cur.execute('SELECT * FROM contas')
    resultados= cur.fetchall()
    return jsonify(resultados)

@app.get("/deletar")
def deletar(request: Request):
    cur = conn.cursor();
    cur.execute('DROP TABLE contas')
    conn.commit();
    return 'ok'

#@app.get("/resultado")
@app.get("/resultado")
def resultado(request: Request):
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
    valores_entrada = d['Entrada']
    valores_saida = d['Saída']

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
    #print("------SAÍDA")

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
    return jsonify(valor_final_formatado)


@app.get("/datatable")
def datatable(request: Request):
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
    

    
    return jsonify(d)
