import sys
import os
import imghdr
import tempfile


class verificacoes:
    @staticmethod
    def verifica_extensao(imgPath):
        listaExtensoes = ['jpeg', 'png', 'jpg', 'webp', 'JEPG', 'JPG']
        if imghdr.what(imgPath) in listaExtensoes:
            return True
        else:
            return False

    @classmethod
    def verifica_imagem_path(cls, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                if cls.verifica_extensao(path):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return

    @staticmethod
    def verifica_existencia_pasta_cache():
        os.makedirs('cache', exist_ok=True)

    @classmethod
    def lista_fotos_cache(cls):
        return os.listdir(fr'{os.getcwd()}/cache')

    @classmethod
    def verifica_fotos_out_cache(cls, IdMax):
        # Loop for começa em 1 pela indexação do SQLite começar em 1
        listaFotosCache = cls.lista_fotos_cache()
        listaFotoOutCache = []
        for c in range(1, IdMax + 1):
            if f'{c}.jpg' not in listaFotosCache:
                listaFotoOutCache.append(c)
        return listaFotoOutCache


class arquivos_temporarios:
    def __init__(self):
        self.temp_file = tempfile.TemporaryDirectory()

    def arquivo_path(self):
        path = self.temp_file.name
        return path
