import sqlite3 as sql
import sys


class BDD:
    def __init__(self):
        try:
            self.BancoDados = sql.connect('./BancoDados/banco_dados_roupas.db')
            self.mouse = self.BancoDados.cursor()
            self.mouse.execute('create table IF NOT EXISTS roupasEstoque('
                               'id INTEGER PRIMARY KEY,'
                               'img BLOB,'
                               'genero VARCHAR(10),'
                               'clouthType VARCHAR(15),'
                               'tecido VARCHAR(15),'
                               'marca VARCHAR(15) ,'
                               'clouthColor VARCHAR(12),'
                               'quantidadePP SMALLINT,'
                               'quantidadeP SMALLINT,'
                               'quantidadeM SMALLINT,'
                               'quantidadeG SMALLINT,'
                               'quantidadeGG SMALLINT)')
        except Exception as erro:
            print(f'Error "{erro}" ao iniciar o banco de dados, Reinicie o programa')
            sys.exit()

    def add_data(self, imgData, genero, tipoRoupa,  tecido, marca, clouthColor, QPP=0, QP=0, QM=0, QG=0, QGG=0):
        self.mouse.execute('INSERT INTO roupasEstoque(img, genero, clouthType, tecido, marca, clouthColor, quantidadePP, quantidadeP, quantidadeM, quantidadeG, quantidadeGG) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (imgData, genero, tipoRoupa, tecido, marca, clouthColor, QPP, QP, QM, QG, QGG))
        self.BancoDados.commit()

    def get_max_id(self):
        self.mouse.execute('Select id from roupasEstoque')
        dados = self.mouse.fetchall()
        if len(dados) > 0:
            return dados[-1][0]
        else:
            return 0

    def get_marcas(self):
        listaMarcas = ['', 'H&M', 'Zara', 'Louis Vuitton', 'Nike', 'Adidas', 'Uniqlo', 'ForBoys', 'Hermès', 'Gucci', 'Lacoste']
        self.mouse.execute('select marca from roupasEstoque')
        dados = self.mouse.fetchall()
        for c in range(len(dados)):
            marca = f'{dados[c][0]}'.capitalize().strip()
            if marca != '':
                listaMarcas.append(marca)
        return listaMarcas

    def get_B64_images(self):
        quary = 'select id, img from roupasEstoque'
        self.mouse.execute(quary)
        dadosIdImg = self.mouse.fetchall()
        return dadosIdImg

    def get_clouth_Infos(self, id):
        quarry = f'select clouthType, clouthColor, genero, tecido, marca,  quantidadePP, quantidadeP, quantidadeM, quantidadeG, quantidadeGG from roupasEstoque  where id = {id}'
        self.mouse.execute(quarry)
        return self.mouse.fetchall()

    def remove_data(self, id):
        quarry = f'DELETE FROM roupasEstoque WHERE ID={id}'
        self.mouse.execute(quarry)
        self.BancoDados.commit()
        self.arruma_id_apos_data_excluida(id)

    def update_data(self, id, column, novo_valor):
        if isinstance(novo_valor, str):
            quarry = f'Update roupasEstoque set {column} = "{novo_valor}" where id={id}'
            self.mouse.execute(quarry)
            self.BancoDados.commit()
        elif isinstance(novo_valor, bytes):
            quarry = f'Update roupasEstoque set {column} = ? where id=?'
            self.mouse.execute(quarry, (novo_valor, id))
            self.BancoDados.commit()
        else:
            quarry = f'Update roupasEstoque set {column} = {novo_valor} where id={id}'
            self.mouse.execute(quarry)
            self.BancoDados.commit()

    def arruma_id_apos_data_excluida(self, id_excluido):
        quarry = f'Update roupasEstoque set id=id-1  where id>{id_excluido}'
        self.mouse.execute(quarry)
        self.BancoDados.commit()

    def filter_search(self, sexo, tamanho, tipo, tecido):
        quarry = f'Select id from roupasEstoque where genero = "{sexo}" and clouthType = "{tipo}" and tecido = "{tecido}" and quantidade{tamanho} > 0'
        self.mouse.execute(quarry)
        lista_itens_selecionados = []
        for item in self.mouse.fetchall():
            lista_itens_selecionados.append(item[0])
        return lista_itens_selecionados