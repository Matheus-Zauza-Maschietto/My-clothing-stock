from verificacoes import verificacoes, arquivos_temporarios
import PySimpleGUIQt as sg
import frontEnd
from BancoDados import BDD
from images import images

sg.theme('SystemDefault')

banco_dados = BDD()

verificacoes.verifica_existencia_pasta_cache()
listaGetCache = verificacoes.verifica_fotos_out_cache(banco_dados.get_max_id())

pasta_temporaria = arquivos_temporarios()

edit = alternaCor = False
lista_update = ['-TYPE-', '-FABRIC-', '-SEX-', '-BRAND-', '-COLOR-', '-PP-', '-P-', '-M-', '-G-', '-GG-']
lista_update_database = ['clouthType', 'tecido', 'genero', 'marca', 'clouthColor', 'quantidadePP', 'quantidadeP', 'quantidadeM', 'quantidadeG', 'quantidadeGG']

# Carrega as imagens que não tiverem presente no local
imagens = banco_dados.get_B64_images()


if len(listaGetCache) > 0 and len(imagens) > 0:
    for c in range(0, len(listaGetCache)):
        images.decodificar_imagem(fr'./cache/{listaGetCache[c]}.jpg', imagens[c][1])
window = sg.Window('tela Inicial', frontEnd.layout_frame_search(len(imagens)), resizable=True, size=[1100, 400])
while True:
    key, value = window.read()
    print(key, value)
    if key == '-SEARCH-':
        window['-CANCEL-'].update(visible=True)
        for item in range(1, len(imagens)+1):
            if item not in banco_dados.filter_search(value[0], value[1], value[2], value[3]):
                window[f'-{item}-'].update(visible=False)
    if key == '-CANCEL-':
        window['-CANCEL-'].update(visible=False)
        for elemento_id in range(1, len(imagens)+1):
            window[f'-{elemento_id}-'].update(visible=True)


    if key == sg.WIN_CLOSED:
        break
    for id_usuario in range(1, banco_dados.get_max_id() + 1):
        if key == f'-{id_usuario}-':
            window.hide()
            dados = banco_dados.get_clouth_Infos(id_usuario)[0]
            lista_personaliza_tela_edicao = [['TIPO', dados[0], frontEnd.typeClouth], ['TECIDO', dados[3], frontEnd.tecido],
                                             ['GÊNERO', dados[2], frontEnd.genero], ['MARCA', dados[4], banco_dados.get_marcas()],
                                             ['COR', dados[1], frontEnd.cor], ['Tamanho PP', dados[5]], ['Tamanho P', dados[6]],
                                             ['Tamanho M', dados[7]], ['Tamanho G', dados[8]], ['Tamanho GG', dados[9]]]
            windowView = sg.Window('Tela de visualização',
                                   layout=frontEnd.clouth_window(f'./cache/{id_usuario}.jpg', dados[0], dados[1], dados[2],
                                                                 dados[3], dados[4], dados[5], dados[6], dados[7],
                                                                 dados[8], dados[9]), size=(700, 400))
            while True:
                key, value = windowView.read(timeout=500)
                if key == sg.WIN_CLOSED or key == 'Voltar':
                    edit = False
                    windowView.close()
                    window.un_hide()
                    break

                if key == '-EDT1-' or key == '-EDT2-':
                    if edit:
                        edit = False
                        windowView['aviso'].update(visible=False)
                        for item in lista_update:
                            windowView[item].update(text_color='black')
                    elif not edit:
                        edit = True
                        windowView['aviso'].update(visible=True, text_color='red')

                if key == '__TIMEOUT__' and edit:
                    if alternaCor:
                        alternaCor = False
                        for item in lista_update:
                            windowView[item].update(text_color='red')
                    else:
                        alternaCor = True
                        for item in lista_update:
                            windowView[item].update(text_color='black')

                if key == 'Excluir':
                    resposta = sg.PopupYesNo('Tem certeza que deseja excluir esse cadastro ?', keep_on_top=True)
                    if resposta == 'Yes':
                        try:
                            banco_dados.remove_data(id_usuario)
                            images.exclui_imagem_cache(id_usuario)
                        except Exception as erro:
                            sg.popup_ok(f'Erro: {erro} durante a Exclusão do arquivo, contate um administrador')
                        else:
                            sg.popup_ok('Exclusão concluida com sucesso, Reinicie o aplicativo efetivar a mudança.')
                            windowView.close()
                            window.un_hide()

                if key in lista_update and edit or key == '-IMG-' and edit:
                    if key == '-IMG-':

                        window_edita = sg.Window('Editando imagem', frontEnd.edicao_tipo_img(id_usuario))
                        img_nova = None
                        while True:
                            key, value = window_edita.read()
                            if key == sg.WIN_CLOSED or key == 'Cancelar':
                                window_edita.close()
                                break
                            if key == '-IMG-':
                                img_nova = sg.PopupGetFile(no_window=True, message='Escolha a imagem da roupa')
                                if not verificacoes.verifica_imagem_path(img_nova):
                                    sg.PopupOK('ERRO, você selecionou um arquivo invalido, tente novamente!')
                                    img_nova = None
                                else:
                                    imagemAmostragem = images(img_nova)
                                    path_imagem = pasta_temporaria.arquivo_path() + '/imagemAmostragem.jpeg'
                                    imagemAmostragem.redimencionar_imagem(path_imagem)
                                    window_edita['-IMG-'].update(size=(225, 300), filename=path_imagem)
                            if key == 'Confirmar':
                                if img_nova == None:
                                    sg.PopupOK('Adicione uma imagem para poder proseguir')
                                else:
                                    try:
                                        banco_dados.update_data(id_usuario, 'img', images.codificar_imagem(path_imagem))
                                        img_update = images(img_nova)
                                        img_update.redimencionar_imagem(rf'./cache/{id_usuario}.jpg')

                                    except Exception as error:
                                        sg.PopupOK(f'Ocorreu o erro: {error} durante a tentativa de atualização dos dados, contate o administrador')
                                    else:
                                        windowView['-IMG-'].update(filename=f'./cache/{id_usuario}.jpg')
                                        window[f'-{id_usuario}-'].update(filename=f'./cache/{id_usuario}.jpg')
                                        sg.PopupOK('Atualização feita com sucesso!')
                                        window_edita.close()
                                        break
                    else:
                        for index in range(0, len(lista_update)):
                            if index < 5:
                                if key == lista_update[index]:
                                    try:
                                        alterar_valor, valor = frontEnd.edicao_tipo_list(lista_personaliza_tela_edicao[index])
                                    except:
                                        alterar_valor = False
                                    if alterar_valor:
                                        try:
                                            banco_dados.update_data(id_usuario, column=lista_update_database[index], novo_valor=valor)
                                        except Exception as erro:
                                            sg.PopupOK(f'Ocorreu o erro {erro}, contate o administrador')
                                        else:
                                            sg.popup_ok('Alteração feita com sucesso!')
                                            windowView[f'{lista_update[index]+"R"}'].update(f'{valor}')
                            elif index >= 5:
                                if key == lista_update[index]:
                                    try:
                                        alterar_valor, valor = frontEnd.edicao_tipo_spin(lista_personaliza_tela_edicao[index])
                                    except:
                                        alterar_valor = False
                                    if alterar_valor:
                                        try:
                                            banco_dados.update_data(id_usuario, column=lista_update_database[index], novo_valor=valor)
                                        except Exception as erro:
                                            sg.PopupOK(f'Ocorreu o erro {erro}, contate o administrador')
                                        else:
                                            sg.popup_ok('Alteração feita com sucesso!')
                                            windowView[f'{lista_update[index]+"R"}'].update(f'{valor}')

    if key == 'Adicionar Peça':
        window.hide()
        windowADD = sg.Window('Tela ADD peça ', frontEnd.add_window(banco_dados.get_marcas()))
        img = None
        while True:
            key, value = windowADD.read(timeout=500)
            if key == sg.WIN_CLOSED:
                windowADD.close()
                break

            if key == 'Voltar':
                windowADD.close()
                window.un_hide()

            if key == 'Confirmar':
                if img is not None:
                    if sg.PopupYesNo('Tem certeza que deseja confirmar o cadastro ?'):
                        windowADD.close()
                        window.un_hide()
                        imagem = images(img)
                        img_path = imagem.cria_novo_caminho(banco_dados.get_max_id())
                        imagem.redimencionar_imagem(img_path)
                        imgCodificada = imagem.codificar_imagem(img_path)
                        banco_dados.add_data(imgCodificada, value['-GEN-'], value['-TYPE-'], value['-FABRIC-'],
                                             value['-BRAND-'],
                                             value['-COR-'], value['-PP-'], value['-P-'], value['-M-'], value['-G-'],
                                             value['-GG-'])
                        sg.PopupOK('Seu cadastro foi adicionado, reinicie o programa para poder visualizar', keep_on_top=True)
                else:
                    sg.PopupOK('Adicione uma imagem para confirmar o cadastro')

            if key == '-IMG-':
                img = sg.PopupGetFile(no_window=True, message='Escolha a imagem da roupa')
                if not verificacoes.verifica_imagem_path(img):
                    sg.PopupOK('ERRO, você selecionou um arquivo invalido, tente novamente!')
                    img = None
                else:
                    imagemAmostragem = images(img)
                    path = pasta_temporaria.arquivo_path() + '/imagemAmostragem.jpeg'
                    imagemAmostragem.redimencionar_imagem(path)
                    windowADD['-IMG-'].update(size=(225, 300), filename=path)

            if key == sg.TIMEOUT_KEY:
                # Gambiarra arrumar depois
                # Laço que varre quais checkboxes estão ativas e caso esteja ativa os Combos referentes
                for item in frontEnd.tamanhos:
                    if value['-C' + item + '-']:
                        windowADD['-' + item + '-'].update(visible=True)
                # Laço que varre quais checkboxes estão desativas e caso esteja desativam os Combos referentes
                for item in frontEnd.tamanhos:
                    if not value['-C' + item + '-']:
                        windowADD['-' + item + '-'].update(visible=False)
