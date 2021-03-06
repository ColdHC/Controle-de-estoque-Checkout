from typing import Collection
from PyQt5 import  uic,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSortFilterProxyModel, qsrand,QPoint
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from reportlab.pdfgen import canvas
import random, string, sys
import mysql.connector
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

lucro = 0


banco = mysql.connector.connect(
*
)
def calculoluc():
    global lucro
    cursor = banco.cursor()
    cursor.execute("SELECT SUM(ROUND((preco*quantidade))) FROM historico")
    soma = cursor.fetchall()
    res = [list(ele) for ele in soma]
    
    lt = ' '.join([str(elem) for elem in res])
    
    lucro = (lt)[1:-1]
def gerar_pdf():
    calculoluc()
    global lucro
    cursor = banco.cursor()
    comando_SQL = "SELECT id,nomecliente,data,quantidade,preco FROM historico"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    width = 600
    height = 5000
    pdfmetrics.registerFont(TTFont('Rockwell', 'Rockwell.ttc'))
    pdf = canvas.Canvas("Vendas.pdf")
    pdf.setPageSize((width,height))
    pdf.drawImage (("650x5000px.png"),0,0)
    pdf.drawImage (("Logo wild BRANCA.png"),488,4932,mask='auto')
    pdf.setFont("Rockwell", 25)
    pdf.setFillColorRGB(255,255,255)
    pdf.setStrokeColorRGB(255,255,255)
    pdf.drawString(250,4950, "Vendas")
    pdf.setFont("Rockwell", 15)
    pdf.drawString(20,4930, "valor em vendas: ")
    pdf.drawString(155,4930, lucro)
    pdf.setFont("Rockwell", 15)

    pdf.drawString(40,4900, "ID")
    pdf.drawString(100,4900, "CLIENTE")
    pdf.drawString(210,4900, "DATA")
    pdf.drawString(310,4900, "QUANTIDADE")
    pdf.drawString(488,4900, "PRECO")

    y = 0
    y2 = 0
    for i in range(0, len(dados_lidos)):
        y = y + 30
        pdf.drawString(20,4905 - y, str(dados_lidos[i][0]))
        pdf.drawString(100,4905 - y, str(dados_lidos[i][1]))
        pdf.drawString(198,4905 - y, str(dados_lidos[i][2]))
        pdf.drawString(360,4905 - y, str(dados_lidos[i][3]))
        pdf.drawString(488,4905 - y, str(dados_lidos[i][4]))
    for j in range (164):
        pdf.line(0,y2,700,y2)
        y2 = y2 + 30
    pdf.rotate(90)
    pdf.line(0,-88,4920,-88)
    pdf.line(0,-188,4920,-188)   
    pdf.line(0,-288,4920,-288)
    pdf.line(0,-450,4920,-450)
    pdf.save()
    pdfs.show()

def fechar_pdfs():

    pdfs.close()

def vender_checkout():
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM historico")
    code = cursor.fetchall()
    codec = segunda_tela.lineEdit_6.text()
    clientecode = segunda_tela.lineEdit_4.text()
    cursor.execute("SELECT codigo FROM clientes")
    codigocli = cursor.fetchall()
    if codec in str(code):
        erro2.show()
    if clientecode not in str(codigocli):
        erro3.show()

    if codec not in str(code) and clientecode in str(codigocli):
        linha = segunda_tela.tableWidget.currentRow()
        cursor.execute("SELECT codigo FROM produtos")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]
        cursor.execute("SELECT quantidade FROM produtos WHERE codigo="+ str(valor_id))
        produto = cursor.fetchall()   
        quantidade1 = produto
        res = [list(ele) for ele in quantidade1]
        lt = ' '.join([str(elem) for elem in res])
        lt = (lt)[1:-1]
        inter = int(lt)
    


        venda = segunda_tela.lineEdit_2.text()
        sub = inter - int(venda)
    
    

        cursor = banco.cursor()
        cursor.execute("UPDATE produtos SET quantidade = '{}' WHERE codigo = {}".format(sub,valor_id))
    

        cursor.execute("SELECT nome FROM produtos WHERE codigo="+ str(valor_id))
        nome = cursor.fetchall()
        nomestr = [list(ele) for ele in nome]
        nomestr2 = ' '.join([str(elem) for elem in nomestr])
        nomestr2 = (nomestr2)[2:-2]
    
   
        cursor.execute("SELECT preco FROM produtos WHERE codigo="+ str(valor_id))
        preco = cursor.fetchall()
        precostr = [list(ele) for ele in preco]
        precostr2 = ' '.join([str(elem) for elem in precostr])
        precostr2 = (precostr2)[1:-1]
        precostr3 = float(precostr2)
    
    
    
        cursor.execute("SELECT categoria FROM produtos WHERE codigo="+ str(valor_id))
        categoria = cursor.fetchall()
        catstr = [list(ele) for ele in categoria]
        catstr2 = ' '.join([str(elem) for elem in catstr])
        catstr2 = (catstr2)[2:-2]
    
    
        cursor.execute("SELECT marca FROM produtos WHERE codigo="+ str(valor_id))
        marca= cursor.fetchall()
        marcastr = [list(ele) for ele in marca]
        marcastr2 = ' '.join([str(elem) for elem in marcastr])
        marcastr2 = (marcastr2)[2:-2]

        cursor.execute("SELECT contato FROM clientes WHERE codigo=" +str(clientecode))
        num = cursor.fetchall()
        num2 = [list(ele) for ele in num]
        num3 = ' '.join([str(elem) for elem in num2])
        numerocliente = (num3)[2:-2]




        codigo_compra = segunda_tela.lineEdit_6.text()
        data = segunda_tela.lineEdit_3.text()
        comando_SQL = "INSERT INTO historico (nomecliente,numerocliente,data,quantidade,nome,categoria,preco,marcar,codigo) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dados = clientecode,numerocliente,data,int(venda),nomestr2,catstr2,precostr3,marcastr2,codigo_compra
        cursor.execute(comando_SQL,dados)
    

        segunda_tela.close()
        segunda_tela.show()
        cursor.execute("SELECT quantidade FROM produtos")
        dados = cursor.fetchall()
        qtd = dados[linha][0]
    
        if qtd <= 0: 
            cursor.execute("SELECT codigo FROM produtos")
            dados = cursor.fetchall()
            valo2 = dados[linha][0]      
            cursor.execute("DELETE FROM produtos WHERE codigo="+ str(valo2))
            segunda_tela.tableWidget.removeRow(linha)
            chama_segunda_tela()
 



           
def chama_segunda_tela():

    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT id, codigo,quantidade,nome,preco,categoria,marca  FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(7)
    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def search(dados_lidos):

    
    segunda_tela.tableWidget.setCurrentItem(None)
    
    
    if not str(dados_lidos):

        return

    matching_items = segunda_tela.tableWidget.findItems(str(dados_lidos), Qt.MatchContains)
    if matching_items:
            # We have found something.
            for item in matching_items:  # Take the first.
                item.setSelected(True)


def registro():
    regist.show()
    global lucro
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM historico"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    regist.tableWidget.setRowCount(len(dados_lidos))
    regist.tableWidget.setColumnCount(10)
    for i in range(0, len(dados_lidos)):
        for j in range(0, 10):
           regist.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    calculoluc()
    regist.label_2.setText(lucro)

def search2(dados_lidos):

    
    regist.tableWidget.setCurrentItem(None)
    
    
    if not str(dados_lidos):

        return

    matching_items = regist.tableWidget.findItems(str(dados_lidos), Qt.MatchContains)
    if matching_items:
            # We have found something.
            for item in matching_items:  # Take the first.
                item.setSelected(True)

def editar_dados():
   
    linha = regist.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM historico")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM historico WHERE codigo="+ str(valor_id))
    compra = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(compra[0][0]))
    tela_editar.lineEdit_2.setText(str(compra[0][1]))
    tela_editar.lineEdit_3.setText(str(compra[0][2]))
    tela_editar.lineEdit_4.setText(str(compra[0][3]))
    tela_editar.lineEdit_5.setText(str(compra[0][4]))
    tela_editar.lineEdit_6.setText(str(compra[0][5]))
    tela_editar.lineEdit_7.setText(str(compra[0][6]))
    tela_editar.lineEdit_8.setText(str(compra[0][7]))
    tela_editar.lineEdit_9.setText(str(compra[0][8]))
    
def salvar_dados():
        linha = regist.tableWidget.currentRow()
        cursor = banco.cursor()
        cursor.execute("SELECT id FROM historico")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]

        cliente = tela_editar.lineEdit_2.text()
        contato = tela_editar.lineEdit_3.text()
        data = tela_editar.lineEdit_4.text()
        quantidade = tela_editar.lineEdit_5.text()
        nome = tela_editar.lineEdit_6.text()
        categoria = tela_editar.lineEdit_7.text()
        preco = tela_editar.lineEdit_8.text()
        marca = tela_editar.lineEdit_9.text()
        cursor = banco.cursor()
        cursor.execute("UPDATE historico SET nomecliente = '{}', numerocliente = '{}', data = '{}', quantidade ='{}', nome ='{}', categoria ='{}',preco = '{}', marcar ='{}'  WHERE id = {}".format(cliente,contato,data,quantidade,nome,categoria,preco,marca,valor_id))
        banco.commit()
        tela_editar.close()
        regist.close()
        registro()

def excluir_dados():
    linha = regist.tableWidget.currentRow()
    regist.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM historico")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM historico WHERE codigo="+ str(valor_id))
    regist.close()
    registro()

def calcular():
    linha = segunda_tela.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT preco FROM produtos WHERE codigo="+ str(valor_id))
    preco = cursor.fetchall()
    res = [list(ele) for ele in preco]
    
    lt = ' '.join([str(elem) for elem in res])
    
    lt = (lt)[1:-1]

    desconto = segunda_tela.lineEdit_7.text()
    desc = float(lt) * float(desconto)/100
    final = float(lt) - desc
    segunda_tela.label_2.setText(str(final))

def registclientes():
    clientes.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM clientes"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    clientes.tableWidget.setRowCount(len(dados_lidos))
    clientes.tableWidget.setColumnCount(4)
    for i in range(0, len(dados_lidos)):
        for j in range(0, 4):
           clientes.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
def cadas():
    clientescad.show()

def cadas2():
    nome = clientescad.lineEdit_3.text()
    contato = clientescad.lineEdit_6.text()
    codigo = clientescad.lineEdit_7.text()
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM clientes")
    dados_lidos = cursor.fetchall()
    codigo2 = '('+ codigo +',)'
    dados_lidos = str(dados_lidos)
    print(dados_lidos)
    print(type(dados_lidos))
    print(codigo2)
    print(type(codigo2))
    

    if codigo2 in dados_lidos:
        erro1.show()
    if codigo2 not in dados_lidos:

        cursor = banco.cursor()
        comando_SQL = "INSERT INTO clientes (cliente,contato,codigo) VALUES (%s,%s,%s)"
        dados = (str(nome),str(contato),int(codigo))
        cursor.execute(comando_SQL,dados)
        banco.commit()
        clientescad.lineEdit_3.setText('')
        clientescad.lineEdit_6.setText('')
        clientescad.lineEdit_7.setText('')
        clientescad.close()
        clientes.close()
        registclientes ()
def editcad():
    linha = clientes.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    
    
    cursor.execute("SELECT * FROM clientes WHERE codigo=" +str(valor_id))
    clientex = cursor.fetchall()
    print (clientex)
    edit.show()

    edit.lineEdit_3.setText(str(clientex[0][0]))
    edit.lineEdit_6.setText(str(clientex[0][1]))
    edit.lineEdit_7.setText(str(clientex[0][2]))

def confedit():
    nome = edit.lineEdit_3.text()
    contato = edit.lineEdit_6.text()
    codigo = edit.lineEdit_7.text()
    linha = clientes.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    if codigo != valor_id:
        cursor.execute("UPDATE clientes SET cliente = '{}', contato = '{}',codigo= {} WHERE codigo = {}".format(nome,contato,codigo,valor_id))
        edit.lineEdit_3.setText('')
        edit.lineEdit_6.setText('')
        edit.lineEdit_7.setText('')
        edit.close()
        clientes.close()
        registclientes()
    else:
        erro1.show()
def exclucli():
    linha = clientes.tableWidget.currentRow()
    clientes.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT codigo FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM clientes WHERE codigo="+ str(valor_id))
    clientes.close()
    registclientes()


app=QtWidgets.QApplication([])
erro3=uic.loadUi("erro3.ui")
erro2=uic.loadUi("erro2.ui")
erro1=uic.loadUi("erro1.ui")
segunda_tela=uic.loadUi("checkout.ui")
regist=uic.loadUi("registro.ui")
pdfs=uic.loadUi("pdfsalvo.ui")
tela_editar=uic.loadUi("menu_editar.ui")
clientes=uic.loadUi("clientes.ui")
clientescad=uic.loadUi("cadcliente.ui")
edit=uic.loadUi("edit.ui")
segunda_tela.pushButton.clicked.connect(chama_segunda_tela)
segunda_tela.lineEdit.textChanged.connect(search)
segunda_tela.pushButton_2.clicked.connect(vender_checkout)
segunda_tela.pushButton_3.clicked.connect(registro)
regist.pushButton_3.clicked.connect(gerar_pdf)
pdfs.pushButton.clicked.connect(fechar_pdfs)
regist.lineEdit.textChanged.connect(search2)
regist.pushButton_2.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados)
regist.pushButton.clicked.connect(excluir_dados)
regist.pushButton_4.clicked.connect(registclientes)
segunda_tela.pushButton_4.clicked.connect(calcular)
clientes.pushButton_4.clicked.connect(cadas)
clientescad.pushButton.clicked.connect(cadas2)
clientes.pushButton_2.clicked.connect(editcad)
clientes.pushButton_5.clicked.connect(exclucli)
edit.pushButton.clicked.connect(confedit)
segunda_tela.show()
app.exec()
