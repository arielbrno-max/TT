from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label

ORDEM = {
    "4": 1, "5": 2, "6": 3, "7": 4,
    "Q": 5, "J": 6, "K": 7, "A": 8,
    "2": 9, "3": 10
}

def forca_carta(carta, manilha):
    if carta == manilha:
        return 100
    return ORDEM.get(carta, 0)

def classificar_mao(cartas, manilha):
    fortes = sum(1 for c in cartas if forca_carta(c, manilha) >= 8)
    if fortes >= 2:
        return "FORTE"
    elif fortes == 1:
        return "MEDIA"
    else:
        return "FRACA"

def avaliar_mesa(cartas_jogadas, manilha):
    if not cartas_jogadas:
        return "FRACA"
    max_forca = max(forca_carta(c, manilha) for c in cartas_jogadas)
    if max_forca >= 100:
        return "FORTE"
    elif max_forca >= 7:
        return "MEDIA"
    else:
        return "FRACA"

def melhor_carta(cartas, manilha):
    return max(cartas, key=lambda c: forca_carta(c, manilha))

def pior_carta(cartas, manilha):
    return min(cartas, key=lambda c: forca_carta(c, manilha))

def decidir(posicao, cartas, cartas_jogadas, manilha, perfil):
    mao = classificar_mao(cartas, manilha)
    mesa = avaliar_mesa(cartas_jogadas, manilha)

    melhor = melhor_carta(cartas, manilha)
    pior = pior_carta(cartas, manilha)

    if posicao == "MAO":
        if mao == "FORTE":
            return f"JOGAR {pior}"
        elif mao == "MEDIA":
            return "TRUCAR" if mesa == "FRACA" else f"JOGAR {pior}"
        else:
            return "TRUCAR (BLEFE)" if perfil == "PASSIVO" else f"JOGAR {pior}"

    if posicao == "CONTRAMAO":
        if mao == "FORTE":
            return f"JOGAR {melhor}"
        elif mao == "MEDIA":
            return f"JOGAR {melhor}" if mesa == "FRACA" else f"JOGAR {pior}"
        else:
            return "TRUCAR (BLEFE)" if perfil == "PASSIVO" and mesa == "FRACA" else f"JOGAR {pior}"

    if posicao == "PE":
        if mao == "FORTE":
            return "TRUCAR" if mesa == "FRACA" else f"JOGAR {melhor}"
        elif mao == "MEDIA":
            return f"JOGAR {melhor}" if mesa == "FRACA" else f"JOGAR {pior}"
        else:
            return "TRUCAR (BLEFE)" if perfil == "PASSIVO" and mesa == "FRACA" else f"JOGAR {pior}"

    return "SEM DECISÃO"


class TrucoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.manilha = Spinner(text='Manilha', values=list(ORDEM.keys()))
        self.posicao = Spinner(text='Posição', values=["MAO","CONTRAMAO","PE"])
        self.perfil = Spinner(text='Perfil', values=["PASSIVO","NORMAL","AGRESSIVO"])

        self.c1 = Spinner(text='Carta 1', values=list(ORDEM.keys()))
        self.c2 = Spinner(text='Carta 2', values=list(ORDEM.keys()))
        self.c3 = Spinner(text='Carta 3', values=list(ORDEM.keys()))

        self.mesa = Spinner(text='Carta mesa', values=list(ORDEM.keys()))

        self.result = Label(text="Resultado aparecerá aqui")

        btn = Button(text="Calcular jogada")
        btn.bind(on_press=self.calcular)

        layout.add_widget(self.manilha)
        layout.add_widget(self.posicao)
        layout.add_widget(self.perfil)
        layout.add_widget(self.c1)
        layout.add_widget(self.c2)
        layout.add_widget(self.c3)
        layout.add_widget(self.mesa)
        layout.add_widget(btn)
        layout.add_widget(self.result)

        return layout

    def calcular(self, instance):
        cartas = [self.c1.text, self.c2.text, self.c3.text]
        cartas_mesa = [self.mesa.text]

        resultado = decidir(
            self.posicao.text,
            cartas,
            cartas_mesa,
            self.manilha.text,
            self.perfil.text
        )

        self.result.text = resultado


TrucoApp().run()
