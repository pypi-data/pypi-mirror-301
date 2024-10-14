import flet as ft       
import json  
# from os import path  
import os
from time import sleep
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Acessa a variável de ambiente
connection_string = os.getenv("MYSQL_CONNECTION_STRING")

from bancodadosmysql import DatabaseManager

# script_dir = path.dirname(path.abspath(__file__))
            
class TemaSelectSysten(ft.IconButton):
    def __init__(self, page = None):
        super().__init__()    
        self.pastalocal = 'assets'
        # self.verificar_pasta()
        if page:
            self.page = page
        self.col = 2
        self.db = DatabaseManager(connection_string, 'temas', pprint=print)
        self.EditarTema = self.JanelaEditarTema()
        self.icon = ft.icons.PALETTE
        self.sair = ft.FilledTonalButton('Sair', on_click=self.RestaurarJanela)
        self.em_edicao = False
        self.on_click = self.Edit


    def did_mount(self):
        self.ct_old = self.page.controls.copy() 
        try:       
            # with open('mytheme.txt', 'r') as arq:
            #     tema = arq.read()
            sleep(0.7)
            t = self.db.LerJson("mytheme", "temas")  #.get('mytheme','black')
            # print(t)
            tema = t.get("mytheme", 'black')
        except:
            tema = None
            # print('tema')
        if tema:
            self.page.bgcolor = 'surface'
            self.dic_atributos = self.arquiv[tema].copy()

        #     cores_claras = ["white","deeppurple","indigo","lightblue","lightgreen","lime"
        # "yellow","bluegrey","grey"]
        #     cc = []
        #     for i in cores_claras:
        #         cc.extend([f"{i}{j}" for j in range(100, 600,100)])
        #     cores_claras += cc

            if self.dic_atributos.get("light", False):
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.DARK


            self.page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surface_variant"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                    # on_primary_container = self.dic_atributos["on_primary_container"],
                    # secondary = self.dic_atributos["secondary"],
                    # on_secondary = self.dic_atributos["on_secondary"],
                    # tertiary = self.dic_atributos["tertiary"],
                    # on_tertiary = self.dic_atributos["on_tertiary"],
                    # tertiary_container = self.dic_atributos["tertiary_container"],
                    # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                    # error = self.dic_atributos["error"],
                    # on_error = self.dic_atributos["on_error"],
                    # error_container = self.dic_atributos["error_container"],
                    # on_error_container = self.dic_atributos["on_error_container"],
                    # background = self.dic_atributos["background"],
                    # on_background = self.dic_atributos["on_background"],
                    # outline_variant = self.dic_atributos["outline_variant"],
                    # scrim = self.dic_atributos["scrim"],
                    # inverse_surface = self.dic_atributos["inverse_surface"],
                    # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                    # inverse_primary = self.dic_atributos["inverse_primary"],
                    # surface_tint = self.dic_atributos["surface_tint"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            self.menus.update()                  
            self.page.update()
        


    def verificar_pasta(self):
        # user_profile = os.environ.get('USERPROFILE')
        # print(user_profile)
        # if not user_profile:
        #     # return False  # USERPROFILE não está definido
        #     self.local = None

        # caminho = os.path.join(user_profile, self.pastalocal)
        caminho = self.pastalocal
        
        if os.path.exists(caminho):
            self.local = caminho
            # return self.caminho
        else:
            os.mkdir(caminho)
            # print(caminho)
            if os.path.exists(caminho):
                self.local = caminho
                # return self.caminho
            # else:
                # return None
    
    def caminho(self, nome):
        # self.verificar_pasta()
        return os.path.join(self.local, nome)


    def Caixa(self, ct):
        return ft.Container(
            content = ct,
            shadow=ft.BoxShadow(
                blur_radius = 300,
                blur_style = ft.ShadowBlurStyle.OUTER,
                color = ft.colors.with_opacity(0.5,ft.colors.CYAN)
            ),
            border= ft.border.all(3, ft.colors.CYAN_500),
            border_radius=8,
            # alignment=ft.Alignment(0, 0),
            expand = True,
            padding= 8,

        ) 

    def Edit(self, e):
        if not self.em_edicao:
            self.em_edicao = True
            self.tamanho_old = self.page.window.width,self.page.window.height
            # self.page.window.width = 700
            # self.page.window.height = 750
            self.page.controls = [self.Caixa(ft.ListView([self.EditarTema,self.sair], width = 700, expand=True))]
            self.page.update()

    def RestaurarJanela(self, e):
        # e.page.window.width,e.page.window.height = self.tamanho_old
        e.page.controls = self.ct_old
        e.page.update()
        self.em_edicao = False

    def GerarMenus(self, i):
        return ft.PopupMenuButton(
            content = ft.Container(
                ft.Text(self.funcoes[i], no_wrap=False,), 
                border=ft.border.all(5,'blue'),
                padding = ft.Padding(5,0,5,0),
                margin=0,
                border_radius=12,
            ),                                      
            splash_radius = 0,
            tooltip = '',
            items=[
                ft.PopupMenuItem(
                    content = self.paleta(i), 
                                            
                ),
                ft.PopupMenuItem(
                    content = self.GerarCores(i),                          
                ),                            
                
            ],
            col = 1 if len(self.funcoes[i]) <= len('labels, cor da caixa do checkbox e cor do check do popMenubutton') else 3
        
        
        ) 

    def Change_dark_light(self, e):
        match e.data:
            case "DARK":
                e.page.theme_mode = ft.ThemeMode.DARK
                self.dic_atributos["light"] = False
            case "LIGHT":
                e.page.theme_mode = ft.ThemeMode.LIGHT
                self.dic_atributos["light"] = True
        e.page.update()

    def JanelaEditarTema(self):
        self.cores = [
            "white","black","red","pink","purple",
            "deeppurple","indigo", "blue","lightblue",
            "cyan","teal","green","lightgreen","lime"
        "yellow", "amber", "orange", "deeporange",
        "brown","bluegrey","grey"

        ]
        self.funcoes = {
            'primary': 'primary: texto principal, fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone,  texto do elevatebuton',
            'on_primary': 'on_primary: texto filledbutton e bolinha do swicth com True',
            'on_secondary_container': 'on_secondary_container: texto filledtonalbutton',
            'outline': 'outline: borda do outliedbutton',
            'shadow': 'shadow: sombras',
            'on_surface_variant': 'on_surface_variant: labels, cor da caixa do checkbox e cor do check do popMenubutton',
            'surface_variant': 'surface_variant: slider e fundo do texfield e do dropbox',
            'primary_container': 'primary_container: HOVERED da bolinha do switch',
            'on_surface': 'on_surface: HOVERED do checkbox e cor dos items do popmenubuton',
            'surface': 'surface: cor de fundo',
            'color_scheme_seed':'color_scheme_seed',

        }
        self.atributos_ColorScheme = list(self.funcoes.keys())
        
        self.dic_atributos = {i:None for i in self.atributos_ColorScheme}
        self.icones = {i:ft.Icon(name = ft.icons.SQUARE, data = [i, False], color = 'white') for i in self.atributos_ColorScheme}
        
        self.nome_tema = ft.TextField(hint_text='Digite o nome do tema', col = 24)
        self.conf = False
        self.confirmar = ft.FilledButton('Confirmar', on_click= self.Salvar)
        self.cancelar = ft.FilledButton('Cancelar', on_click= self.Cancelar)
        self.linha_salve = ft.ResponsiveRow([self.nome_tema, self.confirmar, self.cancelar], columns={'xs':24, 'sm':48 },visible = False, col =96)
        self.btn_save = ft.FilledButton('Salvar Tema', on_click=self.TornarVizivel, col = {'xs':96, 'sm':48 })
        # self.color_scheme_seed = self.GerarMenus('color_scheme_seed', 50)
               
        self.select_dark_light = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value='DARK', label="DARK",label_style= ft.TextStyle(weight='BOLD')),
                    ft.Radio(value="LIGHT", label="LIGHT",label_style= ft.TextStyle(weight='BOLD')),
                
                ]
            ),
        on_change=self.Change_dark_light,
        )

        
  
        # self.arquivo_temas = self.caminho('Tema')
        self.arquiv = self.ler_json(user_id = 'adm', 
        default=  {
                "black": {
                    "background": None,
                    "error": None,
                    "error_container": None,
                    "inverse_primary": None,
                    "inverse_surface": None,
                    "on_background": None,
                    "on_error": None,
                    "on_error_container": None,
                    "on_inverse_surface": None,
                    "on_primary": "limeyellow",
                    "on_primary_container": None,
                    "on_secondary": None,
                    "on_secondary_container": "grey",
                    "on_surface": "cyan",
                    "on_surface_variant": "lightgreen",
                    "on_tertiary": None,
                    "on_tertiary_container": None,
                    "outline": "bluegrey",
                    "outline_variant": None,
                    "primary": "lightblue",
                    "primary_container": "grey",
                    "scrim": None,
                    "secondary": None,
                    "secondary_container": "white",
                    "shadow": "bluegrey",
                    "surface": "limeyellow",
                    "surface_tint": None,
                    "surface_variant": "limeyellow",
                    "tertiary": None,
                    "tertiary_container": None
    }
}                       
        )
        self.tema_escolhido = ft.Dropdown(
            label='Selecione um tema',
            col = 3,
            options = [
                ft.dropdown.Option(i)
                for i in sorted(list(self.arquiv.keys()))
            ],
            on_change=self.CarregarTema
        )

        self.menus = {i:self.GerarMenus(i) for i in self.atributos_ColorScheme}
        self.ferramentas = ft.Container(
            bgcolor=ft.colors.SURFACE,           
            expand=True,
            content = ft.ResponsiveRow(
                [

                    ft.ElevatedButton('Botão',
                        # color = self.cor3            
                    ),
                    ft.FilledButton(
                        text = 'Botão1',
                        # style = ft.ButtonStyle(
                        #     bgcolor = ft.colors.ON_PRIMARY,
                        #     color = ft.colors.ON_INVERSE_SURFACE
                        # )
                        # ,
                    ),
                    # ft.FilledButton(
                    #     text = 'Botão2',
                    #     style = ft.ButtonStyle(
                    #         bgcolor = ft.colors.ON_SECONDARY,
                    #         color = ft.colors.ON_INVERSE_SURFACE
                    #     )
                    #     ,
                    # ),
                    # ft.FilledButton(
                    #     text = 'Botão3',
                    #     style = ft.ButtonStyle(
                    #         bgcolor = ft.colors.ON_TERTIARY,
                    #         color = ft.colors.ON_INVERSE_SURFACE
                    #     )
                    #     ,
                    # ),                                        
                    ft.FilledTonalButton(
                        text = 'FilledTonalButton'
                    ),
                    ft.OutlinedButton(
                        text = 'OutlinedButton'
                    ),
                    ft.TextField('ksajgh',label='texto', 
                                filled=True, dense = True,
            
                                ),
                    ft.Dropdown(label='drop', 
                                options=[ft.dropdown.Option(i) for i in range(10)],
                                dense = True,
                                filled = True,
                                # color = ft.colors.ON_PRIMARY,
                                # fill_color =ft.colors.,
                                # text_style = ft.TextStyle(
                                #     color=ft.colors.PRIMARY,
                                # )
                                # bgcolor = 'black,0.7',
                    ),
                    ft.Slider(
                        min = 1,
                        max = 100,
                        divisions = 100,
                        label='casa',
                        value=50,

                    ),
                    ft.Switch(label = 'valor swith') ,
                    ft.Checkbox(label ='checkbox'),
                    ft.Icon(name = ft.icons.BOOK),
                    ft.PopupMenuButton(
                        content=ft.Text('TEMA', weight=ft.FontWeight.W_900),
                        items = [
                            ft.PopupMenuItem('dark',checked=False),
                            ft.PopupMenuItem('light',checked=True ),
                        ],
                    ),   
                    ft.Text('título',
                            color=ft.colors.PRIMARY,
                            
                    ),              
                    

                ],
                
                columns={'xs':24, 'sm':50 },
                spacing = 0,
                run_spacing = 10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,            

            )
        )

        self.cts = [self.ferramentas, self.tema_escolhido, self.select_dark_light,]


           

        self.cts += [self.menus[i] for i in self.atributos_ColorScheme]
        
        self.cts += [ft.ResponsiveRow([self.btn_save, self.linha_salve], columns=96, spacing=0, run_spacing=0)]
    
        return ft.ResponsiveRow(self.cts,
                           columns={'xs':1, 'sm':3 },
                           spacing=20,
                        #    expand = True,
                           run_spacing = 0,
                           
            )

    def GerarCores(self, data):
        return ft.GridView(
            [
                # ft.IconButton(icon = ft.icons.SQUARE, icon_color = i, col = 0.2,splash_radius=0, padding = 0, on_focus=self.SelecColor) 
                ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor ) 
                for i in ft.colors.colors_list[ft.colors.colors_list.index('scrim')+1:]
            ],
            col = 2, 
            # columns=5,
            width=200,
            height=100,
            runs_count = 8,
            padding = 0,
            # aspect_ratio=1,
            run_spacing=0, 
            spacing=0
        )        

    def TornarVizivel(self, e):
        self.btn_save.visible = False
        self.linha_salve.visible = True
        self.linha_salve.update()
        self.btn_save.update()

    def Salvar(self, e):
        nome_tema = self.nome_tema.value
        if nome_tema not in ['', ' ', None]+list(self.arquiv.keys()):
            self.arquiv[nome_tema] = self.dic_atributos
            # self.escrever_json(self.arquiv, self.arquivo_temas)
            self.db.EditarJson(
                user_id='adm', 
                novos_dados_json=self.arquiv,
                tabela = 'temas'
            )            
            self.linha_salve.visible = False
            self.btn_save.visible = True
        else:
            self.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
            # self.nome_tema.hint_style = ft.TextStyle(size = 10)

        e.page.update()

    def CarregarTema(self, e):
        tema = self.tema_escolhido.value
        if tema:
            e.page.bgcolor = 'surface'

            self.dic_atributos = self.arquiv[tema].copy()

            if self.dic_atributos.get("light", False):
                e.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                e.page.theme_mode = ft.ThemeMode.DARK


            e.page.theme = ft.Theme(
                color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
                color_scheme=ft.ColorScheme(
                    primary = self.dic_atributos["primary"],
                    on_primary = self.dic_atributos["on_primary"],
                    on_secondary_container = self.dic_atributos["on_secondary_container"],
                    outline = self.dic_atributos["outline"],
                    shadow = self.dic_atributos["shadow"],
                    on_surface_variant = self.dic_atributos["on_surface_variant"],
                    surface_variant = self.dic_atributos["surface_variant"],
                    primary_container = self.dic_atributos["primary_container"],
                    on_surface = self.dic_atributos["on_surface"],
                    surface = self.dic_atributos["surface"],
                    # on_primary_container = self.dic_atributos["on_primary_container"],
                    # secondary = self.dic_atributos["secondary"],
                    # on_secondary = self.dic_atributos["on_secondary"],
                    # tertiary = self.dic_atributos["tertiary"],
                    # on_tertiary = self.dic_atributos["on_tertiary"],
                    # tertiary_container = self.dic_atributos["tertiary_container"],
                    # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                    # error = self.dic_atributos["error"],
                    # on_error = self.dic_atributos["on_error"],
                    # error_container = self.dic_atributos["error_container"],
                    # on_error_container = self.dic_atributos["on_error_container"],
                    # background = self.dic_atributos["background"],
                    # on_background = self.dic_atributos["on_background"],
                    # outline_variant = self.dic_atributos["outline_variant"],
                    # scrim = self.dic_atributos["scrim"],
                    # inverse_surface = self.dic_atributos["inverse_surface"],
                    # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                    # inverse_primary = self.dic_atributos["inverse_primary"],
                    # surface_tint = self.dic_atributos["surface_tint"],
                )
            )
                
            for i in list(self.dic_atributos.keys()):
            #     self.icones[i].color = self.dic_atributos[i]
                try:
                    self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
                except:
                    pass
            # self.menus[i].update()  

            # with open('mytheme.txt', 'w') as arq:
            #     arq.write(tema)

            self.db.EditarJson(
                user_id='mytheme', 
                novos_dados_json={"mytheme":tema},
                tabela = 'temas'
            )                 

            # self.icones[i].update()                
            e.page.update()
            
    def Cancelar(self, e):
        self.nome_tema.clean()
        self.linha_salve.visible = False
        self.btn_save.visible = True

        self.nome_tema.update()
        self.linha_salve.update()
        self.btn_save.update()

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json2(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}
        
    def ler_json(self, user_id = 'adm', default=None):
        r = self.db.LerJson(user_id=user_id)
        if isinstance(r, dict):
            return r
        else:
            return default or {}     



    def definirCor(self, e):
        # print('bgcolor = ',e.control.bgcolor,'---', 'data =',e.control.data )
        # self.icones[e.control.data].color = e.control.bgcolor
        # self.icones[e.control.data].data[1] = True
        # self.icones[e.control.data].update()

        self.menus[e.control.data].content.border = ft.border.all(5,e.control.bgcolor)
        self.menus[e.control.data].update()

        if e.control.data == 'surface':
            self.page.bgcolor = e.control.bgcolor

        # for i in self.atributos_ColorScheme:
        #     if self.icones[i].data[1] and self.icones[i].data[0] == e.control.data:
        #         self.dic_atributos[i] = e.control.bgcolor


        self.dic_atributos[e.control.data] = e.control.bgcolor


        self.page.theme = ft.Theme(
            color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
            color_scheme=ft.ColorScheme(
                primary = self.dic_atributos["primary"],
                on_primary = self.dic_atributos["on_primary"],
                on_secondary_container = self.dic_atributos["on_secondary_container"],
                outline = self.dic_atributos["outline"],
                shadow = self.dic_atributos["shadow"],
                on_surface_variant = self.dic_atributos["on_surface_variant"],
                surface_variant = self.dic_atributos["surface_variant"],
                primary_container = self.dic_atributos["primary_container"],
                on_surface = self.dic_atributos["on_surface"],
                surface = self.dic_atributos["surface"],
                # on_primary_container = self.dic_atributos["on_primary_container"],
                # secondary = self.dic_atributos["secondary"],
                # on_secondary = self.dic_atributos["on_secondary"],
                # tertiary = self.dic_atributos["tertiary"],
                # on_tertiary = self.dic_atributos["on_tertiary"],
                # tertiary_container = self.dic_atributos["tertiary_container"],
                # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
                # error = self.dic_atributos["error"],
                # on_error = self.dic_atributos["on_error"],
                # error_container = self.dic_atributos["error_container"],
                # on_error_container = self.dic_atributos["on_error_container"],
                # background = self.dic_atributos["background"],
                # on_background = self.dic_atributos["on_background"],
                # outline_variant = self.dic_atributos["outline_variant"],
                # scrim = self.dic_atributos["scrim"],
                # inverse_surface = self.dic_atributos["inverse_surface"],
                # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
                # inverse_primary = self.dic_atributos["inverse_primary"],
                # surface_tint = self.dic_atributos["surface_tint"],
            )
        )

        self.page.update()

    def paleta(self, data):
        return ft.GridView(
            [
                ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor) 
                for i in self.cores
            ],
            col = 2, 
            
            runs_count = 6,
            padding = 0,
            # aspect_ratio=16/9,
            run_spacing=0, 
            spacing=0
        )

    def Atributos(self, classe):
        return [attr for attr in dir(classe) if not attr.startswith('__')]
