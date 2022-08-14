import PySimpleGUIQt as sg
import os

''' layoutPhotos = [[sg.B(size_px=(240, 320), image_filename=rf'../cache/{}.jpg') for unidade in range(4)] for linha in range(0, quantidadeLinhas)]
    linha = [sg.B(size_px=(240, 320)) for unidade in range(restoLinha)]
    layoutPhotos.append(linha)'''

font1 = 'calibri'

typeClouth = ['Shorts', 'Camiseta', 'Camisa', 'Calça', 'Camiseta', 'Moletom', 'Jaqueta']
tamanhos = ['PP', 'P', 'M', 'G', 'GG']
genero = ['Masculino', 'Feminino', 'Unissex']
tecido = ['Jeans', 'Algodão', 'Malha', 'Microfibra', 'Cetim', 'Elastano']
cor = ['Preto', 'Branco', 'Azul', 'Amarelo', 'Vermelho', 'Verde', 'Roxo', 'Cinza', 'Marrom', 'Rosa', 'Ciano', 'Dourado',
       'Prata', 'Estampada']


# ______________________________________________________________________________________________________________________
def layout_frame_search(quantidadesFotos):
    filePathAll = os.getcwd()
    filePathFrontEnd = os.path.dirname(__file__)
    inlayout = [[sg.Combo(genero, font=[font1, 25], readonly=True, size=[25, 1], visible_items=3),
                 sg.Combo(tamanhos, font=[font1, 25], readonly=True, size=[25, 1]),
                 sg.Combo(typeClouth, font=[font1, 25], readonly=True, size=[25, 1]),
                 sg.Combo(tecido, font=[font1, 25], size=[25, 1], readonly=True),
                 sg.B(image_filename=rf'{filePathFrontEnd}\Imagens\lupaRI.png',
                      image_size=[70, 70], size_px=(40, 40), tooltip='Aplicar os filtros', key='-SEARCH-'),
                 sg.B(image_filename=rf'{filePathFrontEnd}\Imagens\Xvermelho.png', tooltip='Desfazer filtro', key='-CANCEL-', size_px=(40, 40), visible=False)]]
    layoutPhotos = [[sg.T('Não existe nenhum arquivo no momento ! Caso ja tenha adicionado algum, reinicie o programa',
                          font=[font1, 20])]]
    if quantidadesFotos > 0:
        quantidadeLinhas = quantidadesFotos // 4

        restoLinha = quantidadesFotos % 4
        contador_id = 0
        layoutPhotos = []
        linhaPhotos = []
        for c in range(quantidadeLinhas):
            for x in range(0, 4):
                contador_id += 1
                linhaPhotos.append(sg.Image(filename=rf'{filePathAll}\cache\{contador_id}.jpg',
                                        key=f'-{contador_id}-', enable_events=True, size=(220, 293)))
            layoutPhotos.append(linhaPhotos)
            linhaPhotos = []
        for c in range(restoLinha):
            contador_id += 1
            linhaPhotos.append(
                sg.Image(filename=rf'{filePathAll}\cache\{contador_id}.jpg', key=f'-{contador_id}-', enable_events=True, size=(220, 293)))
        layoutPhotos.append(linhaPhotos)
        linhaPhotos = []  # Não colocar .clear(), quebra o codigo

    layoutColuna = [[sg.Column(layoutPhotos, scrollable=True, size=(1015, 600))]]
    layoutBotoes = [[sg.B('Adicionar Peça', font=[font1, 25], size=[25, 1.3])]]
    return inlayout + layoutColuna + layoutBotoes


# ______________________________________________________________________________________________________________________
def add_window(listaMarcas):
    return [[sg.T('Adicione uma peça ao catalogo')],
            [sg.Frame('Foto', font=[font1, 15],
                      layout=[[sg.Image(filename=rf'{os.path.dirname(__file__)}\Imagens\desconhecidoI.png',
                                        size_px=(225, 300), key='-IMG-', tooltip='Adicione uma foto', enable_events=True
                                        )]]),
             sg.Frame('Informações', font=[font1, 15],
                      layout=[[sg.Combo(genero, visible_items=4, font=[font1, 20], size=(20, 1), readonly=True,
                                        key='-GEN-'),
                               sg.Combo(cor, font=[font1, 20], visible_items=4, size=(20, 1), readonly=True,
                                        key='-COR-')],
                              [sg.Combo(tecido, font=[font1, 20], visible_items=4, size=(20, 1), readonly=True,
                                        key='-FABRIC-'),
                               sg.Combo(typeClouth, font=[font1, 20], visible_items=4, size=(20, 1), readonly=True,
                                        key='-TYPE-')],
                              [sg.Combo(listaMarcas, font=[font1, 20], visible_items=4, size=(30, 1),
                                        default_value='', key='-BRAND-')],
                              [sg.HorizontalSeparator()],
                              [sg.Checkbox('PP', font=[font1, 20], key='-CPP-'),
                               sg.Combo(range(100), font=[font1, 20], readonly=True, key='-PP-', visible=False)],
                              [sg.Checkbox('P', font=[font1, 20], key='-CP-'),
                               sg.Combo(range(100), font=[font1, 20], readonly=True, key='-P-', visible=False)],
                              [sg.Checkbox('M', font=[font1, 20], key='-CM-'),
                               sg.Combo(range(100), font=[font1, 20], readonly=True, key='-M-', visible=False)],
                              [sg.Checkbox('G', font=[font1, 20], key='-CG-'),
                               sg.Combo(range(100), font=[font1, 20], readonly=True, key='-G-', visible=False)],
                              [sg.Checkbox('GG', font=[font1, 20], key='-CGG-'),
                               sg.Combo(range(100), font=[font1, 20], readonly=True, key='-GG-', visible=False)]])],
            [sg.B('Voltar', font=[font1, 20], size_px=(130, 50), border_width=(5, 1)),
             sg.B('Confirmar', font=[font1, 20], size_px=(160, 50), border_width=(5, 1))
             ]]


# ______________________________________________________________________________________________________________________
def clouth_window(imgPath, clouthType, clouthColor, clouthSex, clouthFabric, clouthBrand, QPP=0, QP=0, QM=0, QG=0,
                  QGG=0):
    return [[sg.Column(layout=[[sg.T('Editar', font=[font1, 16], enable_events=True, size=(6, 1), key='-EDT1-'),
                                sg.Image(filename=rf'{os.path.dirname(__file__)}/Imagens/edit.png', size_px=(48, 48),
                                         enable_events=True, key='-EDT2-'),
                                sg.T('MODO DE EDIÇÃO LIGADO, SELECIONE QUAL CAMPO DESEJA ALTERAR', font=[font1, 14],
                                     key='aviso', visible=False)]], element_justification='center')],
            [sg.Column(layout=[[sg.Image(filename=imgPath, size_px=(240, 320), key='-IMG-', enable_events=True)]]),
             sg.Column(layout=[[sg.T(f'Tipo: ', font=[font1, 20], key='-TYPE-', enable_events=True, size=(10, 1)),
                                sg.T(f'{clouthType}', font=[font1, 20], key='-TYPE-R')],
                               [sg.T(f'Tecido: ', font=[font1, 20], key='-FABRIC-', enable_events=True, size=(10, 1)),
                                sg.T(f'{clouthFabric}', font=[font1, 20], key='-FABRIC-R')],
                               [sg.T(f'Gênero: ', font=[font1, 20], key='-SEX-', enable_events=True, size=(10, 1)),
                                sg.T(f'{clouthSex}', font=[font1, 20], key='-SEX-R')],
                               [sg.T(f'Marca: ', font=[font1, 20], key='-BRAND-', enable_events=True, size=(10, 1)),
                                sg.T(f'{clouthBrand}', font=[font1, 20], key='-BRAND-R')],
                               [sg.T(f'Cor: ', font=[font1, 20], key='-COLOR-', enable_events=True, size=(10, 1)),
                                sg.T(f'{clouthColor}', font=[font1, 20], key='-COLOR-R')],
                               [sg.HorizontalSeparator()],
                               [sg.T(f'PP: ', font=[font1, 20], key='-PP-', size=(5, 1), enable_events=True),
                                sg.T(f'{QPP}', font=[font1, 20], key='-PP-R'),
                                sg.T(f'G: ', font=[font1, 20], key='-G-', size=(5, 1), enable_events=True),
                                sg.T(f'{QG}', font=[font1, 20], key='-G-R')],
                               [sg.T(f'P: ', font=[font1, 20], key='-P-', size=(5, 1), enable_events=True),
                                sg.T(f'{QP}', font=[font1, 20], key='-P-R'),
                                sg.T(f'GG: ', font=[font1, 20], key='-GG-', size=(5, 1), enable_events=True),
                                sg.T(f'{QGG}', font=[font1, 20], key='-GG-R')],
                               [sg.T(f'M: ', font=[font1, 20], key='-M-', size=(5, 1), enable_events=True),
                                sg.T(f'{QM}', font=[font1, 20], key='-M-R')]])],
            [sg.B('Voltar', font=[font1, 20]), sg.B('Excluir', font=[font1, 20])]]


# ______________________________________________________________________________________________________________________
def edicao_tipo_list(content_list):
    layout = [[sg.T(f'Editando o campo: {content_list[0]}', font=[font1, 20], justification='center', pad=(1, 10))],
              [sg.T('Valor Atual: ', font=[font1, 20], size=(14, 1), pad=(1, 20)),
               sg.T(f'{content_list[1]}', font=[font1, 20], pad=(1, 20))],
              [sg.T('Novo Valor: ', font=[font1, 20], size=(14, 1), pad=(1, 20)),
               sg.Combo(values=content_list[2], font=[font1, 20], readonly=True, pad=(1, 20), key='-valor-')],
              [sg.B('Cancelar', font=[font1, 20], pad=(0, 15)), sg.B('Confirmar', font=[font1, 20], pad=(0, 15))]]

    window_edita = sg.Window('Tela de edição', layout=layout, size=(500, 150))
    while True:
        key, value = window_edita.read()
        if key == 'Cancelar' or key == sg.WIN_CLOSED:
            window_edita.close()
            break
        if key == 'Confirmar':
            confirmar = sg.PopupYesNo(
                f'Tem certeza que deseja alterar o valor de {content_list[0]} de {content_list[1]} para {value["-valor-"]}')
            if confirmar == 'Yes':
                window_edita.close()
                return True, value['-valor-']


# ______________________________________________________________________________________________________________________
def edicao_tipo_spin(content_list):
    layout = [[sg.T(f'Editando o campo: {content_list[0]}', font=[font1, 20], justification='center', pad=(1, 10))],
              [sg.T('Valor Atual: ', font=[font1, 20], size=(14, 1), pad=(1, 20)),
               sg.T(f'{content_list[1]}', font=[font1, 20], pad=(1, 20))],
              [sg.T('Novo Valor: ', font=[font1, 20], size=(14, 1), pad=(1, 20)),
               sg.Spin(values=range(0, 1000), font=[font1, 20], pad=(1, 20), key='-valor-')],
              [sg.B('Cancelar', font=[font1, 20], pad=(0, 15)), sg.B('Confirmar', font=[font1, 20], pad=(0, 15))]]
    window_edita = sg.Window('Tela de edição', layout, size=(500, 150))
    while True:
        key, value = window_edita.read()
        if key == sg.WIN_CLOSED or key == 'Cancelar':
            window_edita.close()
            break
        if key == 'Confirmar':
            confirmar = sg.PopupYesNo(
                f'Tem certeza que deseja alterar o valor de {content_list[0]} de {content_list[1]} para {value["-valor-"]}')
            if confirmar == 'Yes':
                window_edita.close()
                return True, value['-valor-']


# ______________________________________________________________________________________________________________________

def edicao_tipo_img(content_list):
    return [[sg.T(f'Editando o campo: Imagem', font=[font1, 20], justification='center', pad=(1, 10))],
              [sg.T('Imagem Atual:  ', font=[font1, 20], size=(17, 1), pad=(1, 20)),
               sg.Image(fr'.\cache\{content_list}.jpg', size_px=(240, 320))],
              [sg.T('Nova Imagem: ', font=[font1, 20], size=(17, 1), pad=(1, 20)),
               sg.Image(rf'{os.path.dirname(__file__)}\Imagens\desconhecidoI.png', size_px=(240, 320), enable_events=True, key='-IMG-')],
              [sg.B('Cancelar', font=[font1, 20], pad=(0, 15)), sg.B('Confirmar', font=[font1, 20], pad=(0, 15))]]

