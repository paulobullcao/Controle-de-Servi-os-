'''
Esse software tem como função inserir e listar os dados que forem adicionados no banco de dados so sistema da BULC
bem como fornecer toda a interação com o usuário que vai informar os dados solicitados para a inserção e consulta. 
'''

#importa o módulo de Designer do QTdesigner
from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas # importa a biblioteca para gerar o pdf.

num_id = 0
#Conectando ao banco de dados.
banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "*****",
    database = "bdbulc"
)

def editar_dados():
    global num_id 
    linha = segunda_tela.tableWidget.currentRow() # seleciona a linha da coluna 

    cursor = banco.cursor()
    cursor.execute("SELECT ID FROM controle") #Seleciona os ids da tabela controle
    dados_lidos = cursor.fetchall() #Pega os valores do banco de dados e retorna
    valor_id = dados_lidos[linha][0] #Pega o valor do indice que vai ser editado
    cursor.execute("SELECT * FROM controle WHERE ID =" + str(valor_id)) #seleciona todas as informações onde o id for igual o informado anteriormente
    produto = cursor.fetchall()
    tela_editar.show() # exibe a tela de edição das informações 

    num_id = valor_id
    
    tela_editar.lineEdit.setText(str(produto[0][1])) #Edita a 1º informação da tabela
    tela_editar.lineEdit_2.setText(str(produto[0][2])) #Edita a 2º informação da tabela
    tela_editar.lineEdit_3.setText(str(produto[0][3])) #Edita a 3º informação da tabela
    tela_editar.lineEdit_4.setText(str(produto[0][4])) #Edita a 4º informação da tabela

    

def dados_editados():
    global num_id
    #valores digitados no line edite
    produto = tela_editar.lineEdit.text()
    valor = tela_editar.lineEdit_2.text()
    cliente = tela_editar.lineEdit_3.text()
    data = tela_editar.lineEdit_4.text()

    #Atualiza as informações do banco de dados 
    comando_sql = "UPDATE controle SET Produto = '{}', Valor ='{}', Cliente = '{}', Data='{}' WHERE ID ={}".format(produto,valor,cliente,data,num_id) 
    
    #atualiza os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute(comando_sql)# Executa o comando no banco de dados
    banco.commit() #Salava as alterações no banco de dados 
    tela_editar.close() #Fecha a tela de edição dos dados 
    segunda_tela.close() #Fecha a tela de listagem para atualizar 
    chama_Tela2()


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow() # seleciona a linha da coluna 
    segunda_tela.tableWidget.removeRow(linha) # Remove a linha da coluna 

    cursor = banco.cursor()
    cursor.execute("SELECT ID FROM controle") #Seleciona o banco dados e lista os ids do banco.
    dados_lidos = cursor.fetchall() #Pega os valores do banco de dados 
    valor_id = dados_lidos[linha][0] #Pega o valor do indice que vai ser removido 
    cursor.execute("DELETE FROM  controle WHERE ID =" + str(valor_id)) #Deleta a linha passada pelo valor do indice a ser removido  e converte em string
    banco.commit()


def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM controle"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() #retorna as informações do banco de dados 

    y = 0 # variavél para escrever no pdf
    pdf = canvas.Canvas("SoftwareBulc.pdf") # Diretório para salvar o pdf 
    pdf.setFont("Times-Bold",25) # escreve o título  com a font e em negrito e tamanho
    pdf.drawString(200, 800, "Informações Produtos: ") #posição de escrita no pdf 
    pdf.setFont("Times-Roman", 18) #Diminui

    # Informação para a escrita da barra central do PDF 10 eixo x, 750 eixo y
    pdf.drawString(10, 750, "ID")
    pdf.drawString(130, 750, "Produto")
    pdf.drawString(300, 750, "Valor")
    pdf.drawString(380, 750, "Cliente")
    pdf.drawString(480, 750, "Data")

    for i in range(0,len(dados_lidos)):
        y = y + 50 # escreve e pula uma linha 
        pdf.drawString(10,750 - y, str(dados_lidos[i][0])) #Informações para a escrita do ID do PDF, 10 eixo x, 750 eixo y
        pdf.drawString(80,750 - y, str(dados_lidos[i][1])) #Informações para a escrita do Produto do PDF, 10 eixo x, 750 eixo y
        pdf.drawString(300,750 - y, str(dados_lidos[i][2])) #Informações para a escrita do Valor da do PDF, 10 eixo x, 750 eixo y
        pdf.drawString(380,750 - y, str(dados_lidos[i][3])) #Informações para a escrita do Cliente do PDF, 10 eixo x, 750 eixo y
        pdf.drawString(480,750 - y, str(dados_lidos[i][4])) #Informações para a escrita da Data do PDF, 10 eixo x, 750 eixo y

        pdf.save()
        print("PDF FOI GERADO COM SUCESSO! ")


def funcao_principal():
    linha1 = formulario.lineEdit.text() #Obtem  a informação passada na caixa de entrada do Serviço.
    linha2 = formulario.lineEdit_2.text() #Obtem  a informação passada na caixa de entrada do valor.
    linha3 = formulario.lineEdit_3.text() #Obtem  a informação passada na caixa de entrada do Cliente.
    linha4 = formulario.lineEdit_4.text() #Obtem  a informação passada na caixa de entrada do Data.


    categoria = "" #Limpa a categoria 

    if formulario.radioButton.isChecked(): # Checa o botão selecionado no menú.
        print("Categoria Produtos foi selecionada ")
        categoria = "Produtos"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Serviços foi selecionada ")
        categoria = "Serviços"
    elif formulario.radioButton_3.isChecked():
        print("Categoria Vendas foi selecionada ")
        categoria ="Vendas"
    cursor = banco.cursor()

    # Insere as informações no banco de dados
    comando_sql = f'INSERT INTO controle (Produto, Valor, Cliente, Data ) VALUES ("{linha1}",{linha2}, "{linha3}","{linha4}")' 
    cursor.execute(comando_sql)
    banco.commit() #Atualiza o banco de dados
    formulario.lineEdit.setText("") # Limpa os campos dos dados para receber um novo
    formulario.lineEdit_2.setText("") # Limpa os campos dos dados para receber um novo
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")


def chama_Tela2(): # Cria uma função para chamar a segunda tela.
    segunda_tela.show() #exibe a segunda tela

    cursor = banco.cursor() # cria um Cursor para o banco de dados 
    comando_SQL = "SELECT * FROM controle" # Comando SQL para selecionar tudo da tabela controle
    cursor.execute(comando_SQL) # Executa o comando que foi passado no banco de dados
    dados_lidos = cursor.fetchall() # retorna os dados da tabela do banco de dados


    #Pega a segunda tela no componente tabela e define quantas linhas a tabela vai ter através dos dados lidos
    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) 
    segunda_tela.tableWidget.setColumnCount(5) # define o num de colunas, já definidos na criaçao da tabela

    #Cria um for para percorer o banco de dados e preenxer a tabela e efetuar a listagem das informações.
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5 ):
            segunda_tela.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            #É passado a posição do elemento na tabela  com o setItem 


app = QtWidgets.QApplication([])
formulario = uic.loadUi("Formulario 2.ui")  # faz o link entre o programa e o layout do software
segunda_tela = uic.loadUi("listar_dados.ui")  # faz o link entre o programa e o layout do software
tela_editar= uic.loadUi("Menu_editar.ui") # faz o link entre o programa e o layout da tela de editar
formulario.pushButton.clicked.connect(funcao_principal) # Quando ele é clicado chama a função principal 
formulario.pushButton_2.clicked.connect(chama_Tela2) # Quando é clicado chama a segunda tela.
segunda_tela.pushButton_3.clicked.connect(gerar_pdf) # Quando é clicado, gera um PDF.
segunda_tela.pushButton_2.clicked.connect(excluir_dados) # Quando é clicado, exclui uma linha da tabela   
segunda_tela.pushButton.clicked.connect(editar_dados) # Quando é clicado, edita uma informação da linha da tabela
tela_editar.pushButton.clicked.connect(dados_editados) # Quando é clicado, salva os itens que foram editados

formulario.show() # exibe a tela de início
app.exec() # Executa o app