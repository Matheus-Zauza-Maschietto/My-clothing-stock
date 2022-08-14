import os
from base64 import b64encode, b64decode
from PIL import Image


class images:
    def __init__(self, img, ):
        self.img = img

    def redimencionar_imagem(self, filepath):
        imagem = Image.open(self.img)
        imagem = imagem.resize((220, 293))
        imagem.save(filepath)
        return filepath

    def cria_novo_caminho(self, id):
        return fr'{os.getcwd()}/cache/{id + 1}.jpg'

    @classmethod
    def exclui_imagem_cache(cls, id):
        os.remove(f'{os.getcwd()}/cache/{id+1}.jpg')

    @staticmethod
    def codificar_imagem(path):
        with open(path, 'rb') as file:
            imgcode = b64encode(file.read())
        return imgcode

    @classmethod
    def decodificar_imagem(cls, path, imgcode):
        imgdecode = open(path, 'wb')
        imgdecode.write(b64decode(imgcode))
        imgdecode.close()
