"""Widgets auxiliares para um visual mais moderno no Tkinter."""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

from interface.tema import (
    ALTURA_LINHA_LISTA,
    COR_BLOCO,
    COR_DESTAQUE,
    COR_DESTAQUE_HOVER,
    COR_FUNDO,
    COR_LISTA_CABECALHO,
    COR_LISTA_FUNDO,
    COR_PAINEL,
    COR_PERIGO,
    COR_PERIGO_FUNDO,
    COR_TEXTO,
    COR_TEXTO_SUAVE,
    fonte,
)

# Limites da altura dinâmica da lista (em linhas visíveis).
ALTURA_LISTA_MIN = 1
ALTURA_LISTA_MAX = 12
# Precisa coincidir com o rowheight da Treeview.
ALTURA_LINHA_ACAO = ALTURA_LINHA_LISTA



def criar_retangulo_arredondado(canvas, x1, y1, x2, y2, raio, **kwargs):
    """Desenha um retângulo com cantos arredondados no Canvas."""
    pontos = [
        x1 + raio, y1,
        x2 - raio, y1,
        x2, y1,
        x2, y1 + raio,
        x2, y2 - raio,
        x2, y2,
        x2 - raio, y2,
        x1 + raio, y2,
        x1, y2,
        x1, y2 - raio,
        x1, y1 + raio,
        x1, y1,
    ]
    return canvas.create_polygon(pontos, smooth=True, **kwargs)


class PainelArredondado(tk.Frame):
    """Card branco com cantos arredondados."""

    def __init__(
        self,
        master,
        raio: int = 20,
        cor: str = COR_PAINEL,
        padding: int = 12,
        altura_minima: int = 0,
        expandir: bool = False,
        **kwargs,
    ):
        fundo_pai = COR_FUNDO
        try:
            fundo_pai = master.cget("background")
        except tk.TclError:
            pass

        super().__init__(master, bg=fundo_pai, **kwargs)
        self.raio = raio
        self.cor = cor
        self.padding = padding
        self.altura_minima = altura_minima
        # True = o card preenche o espaço do pai (listas); False = altura do conteúdo.
        self.expandir = expandir

        self.canvas = tk.Canvas(
            self, bg=fundo_pai, highlightthickness=0, bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.corpo = tk.Frame(self.canvas, bg=cor)
        self._janela_corpo = self.canvas.create_window(
            padding, padding, anchor=tk.NW, window=self.corpo
        )

        self.corpo.bind("<Configure>", self._ao_mudar_conteudo)
        self.canvas.bind("<Configure>", self._ao_mudar_canvas)

    def _ao_mudar_conteudo(self, _evento=None) -> None:
        if self.expandir:
            self._desenhar_fundo()
            return
        self.corpo.update_idletasks()
        largura = self.corpo.winfo_reqwidth() + 2 * self.padding
        altura = max(
            self.corpo.winfo_reqheight() + 2 * self.padding,
            self.altura_minima,
        )
        self.canvas.configure(width=largura, height=altura)
        self._desenhar_fundo()

    def _ao_mudar_canvas(self, evento=None) -> None:
        largura_util = max(evento.width - 2 * self.padding, 10)
        if self.expandir:
            altura_util = max(evento.height - 2 * self.padding, 10)
            self.canvas.itemconfigure(
                self._janela_corpo, width=largura_util, height=altura_util
            )
        else:
            self.canvas.itemconfigure(self._janela_corpo, width=largura_util)
        self._desenhar_fundo()

    def _desenhar_fundo(self) -> None:
        self.canvas.delete("fundo")
        largura = max(self.canvas.winfo_width(), 20)
        altura = max(self.canvas.winfo_height(), 20)
        criar_retangulo_arredondado(
            self.canvas,
            1,
            1,
            largura - 1,
            altura - 1,
            self.raio,
            fill=self.cor,
            outline="",
            tags="fundo",
        )
        self.canvas.tag_lower("fundo")


class Secao(tk.Frame):
    """Título em destaque + painel arredondado (botões Cadastrar / Atualizar)."""

    def __init__(
        self,
        master,
        titulo: str,
        altura_minima: int = 0,
        expandir: bool = False,
        ao_adicionar=None,
        texto_adicionar: str = "Cadastrar",
        ao_atualizar=None,
        **kwargs,
    ):
        fundo_pai = COR_FUNDO
        try:
            fundo_pai = master.cget("background")
        except tk.TclError:
            pass

        super().__init__(master, bg=fundo_pai, **kwargs)

        barra = tk.Frame(self, bg=fundo_pai)
        barra.pack(fill=tk.X, pady=(0, 10))

        self.rotulo_titulo = tk.Label(
            barra,
            text=titulo,
            bg=fundo_pai,
            fg=COR_TEXTO,
            font=fonte(13, True),
            anchor=tk.W,
        )
        self.rotulo_titulo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Ordem à direita: Atualizar dados | Cadastrar (verde).
        if ao_adicionar is not None:
            BotaoSecao(
                barra,
                texto_adicionar,
                comando=ao_adicionar,
                destaque=True,
            ).pack(side=tk.RIGHT, padx=(8, 0))
        if ao_atualizar is not None:
            BotaoSecao(
                barra,
                "Atualizar dados",
                comando=ao_atualizar,
            ).pack(side=tk.RIGHT, padx=(8, 0))

        self.painel = PainelArredondado(
            self,
            altura_minima=altura_minima,
            expandir=expandir,
        )
        self.painel.pack(fill=tk.BOTH, expand=True)
        self.corpo = self.painel.corpo

    def definir_titulo(self, titulo: str) -> None:
        self.rotulo_titulo.config(text=titulo)


def _centralizar_janela(janela: tk.Toplevel, master, largura: int, altura: int) -> None:
    janela.update_idletasks()
    try:
        px = master.winfo_rootx() + (master.winfo_width() - largura) // 2
        py = master.winfo_rooty() + (master.winfo_height() - altura) // 2
        janela.geometry(f"{largura}x{altura}+{max(px, 40)}+{max(py, 40)}")
    except tk.TclError:
        janela.geometry(f"{largura}x{altura}")


class ModalFormulario(tk.Toplevel):
    """Janela modal para cadastrar ou editar um registro."""

    def __init__(
        self,
        master,
        titulo: str,
        ao_salvar,
        ao_cancelar=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.title(titulo)
        self.configure(bg=COR_FUNDO)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._ao_salvar = ao_salvar
        self._ao_cancelar = ao_cancelar

        _centralizar_janela(self, master, 480, 420)

        tk.Label(
            self,
            text=titulo,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=fonte(14, True),
            anchor=tk.W,
        ).pack(fill=tk.X, padx=24, pady=(20, 12))

        painel = PainelArredondado(self, raio=16, padding=16)
        painel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 12))
        self.corpo = painel.corpo
        self.corpo.columnconfigure(1, weight=1)

        barra = tk.Frame(self, bg=COR_FUNDO)
        barra.pack(fill=tk.X, padx=20, pady=(0, 20))

        BotaoAcao(
            barra, "Cancelar", self._cancelar, variante="secundario"
        ).pack(side=tk.RIGHT, padx=(8, 0))
        BotaoAcao(
            barra, "Salvar", self._salvar, variante="primario"
        ).pack(side=tk.RIGHT)

        self.protocol("WM_DELETE_WINDOW", self._cancelar)
        self.bind("<Escape>", lambda _e: self._cancelar())

    def _salvar(self) -> None:
        if self._ao_salvar:
            self._ao_salvar(self)

    def _cancelar(self) -> None:
        if self._ao_cancelar:
            self._ao_cancelar(self)
        self.destroy()


class ModalMensagem(tk.Toplevel):
    """Modal moderno de feedback (sucesso / erro / alerta / confirmação)."""

    CORES = {
        "sucesso": ("#0D9488", "#CCFBF1", "✓"),
        "erro": ("#DC2626", "#FEE2E2", "!"),
        "alerta": ("#D97706", "#FEF3C7", "!"),
        "info": ("#0284C7", "#E0F2FE", "i"),
        "confirmar": ("#0D9488", "#CCFBF1", "?"),
    }

    def __init__(
        self,
        master,
        titulo: str,
        mensagem: str,
        tipo: str = "info",
        confirmar: bool = False,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.title(titulo)
        self.configure(bg=COR_FUNDO)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.resultado = False
        self._confirmar = confirmar

        cor, fundo_icone, simbolo = self.CORES.get(
            tipo, self.CORES["info"]
        )
        _centralizar_janela(self, master, 420, 260)

        painel = PainelArredondado(self, raio=18, padding=20)
        painel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        corpo = painel.corpo

        # Ícone circular colorido.
        icone = tk.Canvas(
            corpo, width=48, height=48, bg=COR_PAINEL, highlightthickness=0, bd=0
        )
        icone.pack(pady=(4, 12))
        icone.create_oval(4, 4, 44, 44, fill=fundo_icone, outline="")
        icone.create_text(24, 24, text=simbolo, fill=cor, font=fonte(16, True))

        tk.Label(
            corpo,
            text=titulo,
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=fonte(13, True),
        ).pack()
        tk.Label(
            corpo,
            text=mensagem,
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=fonte(10),
            wraplength=320,
            justify=tk.CENTER,
        ).pack(pady=(8, 16))

        barra = tk.Frame(corpo, bg=COR_PAINEL)
        barra.pack()

        if confirmar:
            BotaoAcao(
                barra, "Não", self._nao, variante="secundario"
            ).pack(side=tk.LEFT, padx=(0, 8))
            BotaoAcao(
                barra, "Sim", self._sim, variante="primario"
            ).pack(side=tk.LEFT)
        else:
            BotaoAcao(barra, "OK", self._sim, variante="primario").pack()

        self.protocol("WM_DELETE_WINDOW", self._nao)
        self.bind("<Escape>", lambda _e: self._nao())
        self.wait_window(self)

    def _sim(self) -> None:
        self.resultado = True
        self.destroy()

    def _nao(self) -> None:
        self.resultado = False
        self.destroy()


def mostrar_sucesso(master, mensagem: str, titulo: str = "Sucesso") -> None:
    ModalMensagem(master, titulo, mensagem, tipo="sucesso")


def mostrar_erro(master, mensagem: str, titulo: str = "Erro") -> None:
    ModalMensagem(master, titulo, mensagem, tipo="erro")


def mostrar_alerta(master, mensagem: str, titulo: str = "Atenção") -> None:
    ModalMensagem(master, titulo, mensagem, tipo="alerta")


def confirmar_acao(
    master, mensagem: str, titulo: str = "Confirmação"
) -> bool:
    modal = ModalMensagem(
        master, titulo, mensagem, tipo="confirmar", confirmar=True
    )
    return bool(modal.resultado)


class BotaoPilula(tk.Canvas):
    """Botão arredondado de navegação (abas)."""

    def __init__(self, master, texto: str, comando, ativo: bool = False, **kwargs):
        super().__init__(
            master,
            width=118,
            height=40,
            bg=COR_FUNDO,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **kwargs,
        )
        self.texto = texto
        self.comando = comando
        self.ativo = ativo
        self._desenhar()
        self.bind("<Button-1>", lambda _e: self.comando())
        self.bind("<Enter>", lambda _e: self._desenhar(hover=True) if not self.ativo else None)
        self.bind("<Leave>", lambda _e: self._desenhar())

    def definir_ativo(self, ativo: bool) -> None:
        self.ativo = ativo
        self._desenhar()

    def _desenhar(self, hover: bool = False) -> None:
        self.delete("all")
        if self.ativo:
            cor, cor_texto = COR_DESTAQUE, "#FFFFFF"
        elif hover:
            cor, cor_texto = "#E2E8F0", COR_TEXTO
        else:
            cor, cor_texto = "#E8EEF4", COR_TEXTO_SUAVE
        criar_retangulo_arredondado(self, 2, 4, 116, 36, 16, fill=cor, outline="")
        self.create_text(
            59, 20, text=self.texto, fill=cor_texto, font=fonte(10, True)
        )


class BotaoAcao(tk.Canvas):
    """Botão-pílula das ações (Limpar/Salvar/Excluir...) — mesmo visual das abas."""

    def __init__(
        self,
        master,
        texto: str,
        comando,
        variante: str = "secundario",
        **kwargs,
    ):
        # Largura automática conforme o texto.
        metrica = tkfont.Font(
            family=fonte(10, True)[0],
            size=fonte(10, True)[1],
            weight="bold",
        )
        largura = max(int(metrica.measure(texto) + 36), 110)
        altura = 40

        fundo = COR_FUNDO
        try:
            fundo = master.cget("background")
        except tk.TclError:
            pass

        super().__init__(
            master,
            width=largura,
            height=altura,
            bg=fundo,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **kwargs,
        )
        self.texto = texto
        self.comando = comando
        self.variante = variante
        self._largura = largura
        self._desenhar()
        self.bind("<Button-1>", lambda _e: self.comando())
        self.bind("<Enter>", lambda _e: self._desenhar(hover=True))
        self.bind("<Leave>", lambda _e: self._desenhar())

    def _cores(self, hover: bool = False):
        if self.variante == "primario":
            return (COR_DESTAQUE if not hover else "#0F766E", "#FFFFFF")
        if self.variante == "perigo":
            return (COR_PERIGO_FUNDO if not hover else "#FEE2E2", COR_PERIGO)
        # secundario
        return ("#E8EEF4" if not hover else "#E2E8F0", COR_TEXTO)

    def _desenhar(self, hover: bool = False) -> None:
        self.delete("all")
        cor, cor_texto = self._cores(hover)
        criar_retangulo_arredondado(
            self, 2, 4, self._largura - 2, 36, 16, fill=cor, outline=""
        )
        self.create_text(
            self._largura // 2,
            20,
            text=self.texto,
            fill=cor_texto,
            font=fonte(10, True),
        )


class ScrollModern(tk.Frame):
    """Scroll com setas claras + polegar visível (contraste bom no fundo cinza)."""

    def __init__(self, master, comando=None, cor_fundo: str | None = None, **kwargs):
        self.cor_fundo = cor_fundo or COR_FUNDO
        super().__init__(master, bg=self.cor_fundo, width=22, **kwargs)
        self.pack_propagate(False)
        self.comando = comando
        self._inicio = 0.0
        self._fim = 1.0
        self._arrastando = False
        self._y_inicial = 0
        self._inicio_inicial = 0.0

        self.btn_cima = tk.Label(
            self,
            text="▲",
            bg=self.cor_fundo,
            fg="#64748B",
            font=fonte(8, True),
            cursor="hand2",
            width=2,
        )
        self.btn_cima.pack(side=tk.TOP, pady=(2, 2))
        self.btn_cima.bind("<Button-1>", lambda _e: self._passo(-1))
        self.btn_cima.bind(
            "<Enter>", lambda _e: self.btn_cima.config(fg=COR_DESTAQUE)
        )
        self.btn_cima.bind(
            "<Leave>", lambda _e: self.btn_cima.config(fg="#64748B")
        )

        self.trilha = tk.Canvas(
            self,
            width=14,
            bg="#E2E8F0",
            highlightthickness=0,
            bd=0,
        )
        self.trilha.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=4)

        self.btn_baixo = tk.Label(
            self,
            text="▼",
            bg=self.cor_fundo,
            fg="#64748B",
            font=fonte(8, True),
            cursor="hand2",
            width=2,
        )
        self.btn_baixo.pack(side=tk.BOTTOM, pady=(2, 2))
        self.btn_baixo.bind("<Button-1>", lambda _e: self._passo(1))
        self.btn_baixo.bind(
            "<Enter>", lambda _e: self.btn_baixo.config(fg=COR_DESTAQUE)
        )
        self.btn_baixo.bind(
            "<Leave>", lambda _e: self.btn_baixo.config(fg="#64748B")
        )

        self.trilha.bind("<Configure>", lambda _e: self._desenhar())
        self.trilha.bind("<Button-1>", self._ao_clicar)
        self.trilha.bind("<B1-Motion>", self._ao_arrastar)
        self.trilha.bind("<ButtonRelease-1>", self._ao_soltar)
        self.trilha.bind("<MouseWheel>", self._ao_rodinha)

    def set(self, inicio, fim) -> None:
        """Chamado pelo widget via yscrollcommand."""
        try:
            self._inicio = float(inicio)
            self._fim = float(fim)
        except (TypeError, ValueError):
            self._inicio, self._fim = 0.0, 1.0
        self._desenhar()

    def _passo(self, direcao: int) -> None:
        if self.comando:
            self.comando("scroll", direcao, "units")

    def _ao_rodinha(self, evento):
        if self.comando:
            self.comando("scroll", int(-1 * (evento.delta / 120)), "units")
        return "break"

    def _desenhar(self) -> None:
        self.trilha.delete("all")
        altura = max(self.trilha.winfo_height(), 24)
        fracao = max(min(self._fim - self._inicio, 1.0), 0.0)
        # Conteúdo cabe inteiro: sem polegar.
        if fracao >= 0.995:
            return

        util = max(altura - 6, 10)
        # Polegar proporcional (mínimo só para facilitar o clique).
        tamanho = max(int(util * fracao), 24)
        tamanho = min(tamanho, util)
        espaco = max(util - tamanho, 0)
        # Progresso 0→1: no fim do scroll o polegar encosta embaixo.
        progresso = self._inicio / max(1.0 - fracao, 1e-6)
        progresso = min(max(progresso, 0.0), 1.0)
        topo = 3 + int(progresso * espaco)
        criar_retangulo_arredondado(
            self.trilha,
            2,
            topo,
            12,
            topo + tamanho,
            5,
            fill="#64748B",
            outline="",
            tags="polegar",
        )

    def _ao_clicar(self, evento) -> None:
        # Clique fora do polegar: pagina na direção do clique.
        if self.comando and not self._arrastando:
            altura = max(self.trilha.winfo_height(), 1)
            fracao = evento.y / altura
            if fracao < self._inicio:
                self.comando("scroll", -1, "pages")
            elif fracao > self._fim:
                self.comando("scroll", 1, "pages")
        self._arrastando = True
        self._y_inicial = evento.y
        self._inicio_inicial = self._inicio

    def _ao_arrastar(self, evento) -> None:
        if not self.comando or not self._arrastando:
            return
        altura = max(self.trilha.winfo_height() - 6, 1)
        fracao = max(min(self._fim - self._inicio, 0.999), 0.05)
        tamanho = max(int(altura * fracao), 24)
        espaco = max(altura - tamanho, 1)
        delta = (evento.y - self._y_inicial) / espaco
        novo = min(max(self._inicio_inicial + delta, 0.0), max(1.0 - fracao, 0.0))
        self.comando("moveto", novo)

    def _ao_soltar(self, _evento=None) -> None:
        self._arrastando = False


class AreaRolavel(tk.Frame):
    """Área com scroll da página inteira (evita cortar o formulário)."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COR_FUNDO, **kwargs)

        self.canvas = tk.Canvas(
            self, bg=COR_FUNDO, highlightthickness=0, bd=0
        )
        self.scroll = ScrollModern(
            self, comando=self.canvas.yview, cor_fundo=COR_FUNDO
        )
        self.canvas.configure(yscrollcommand=self._ao_scroll)
        self._scroll_visivel = False

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.corpo = tk.Frame(self.canvas, bg=COR_FUNDO)
        self._janela = self.canvas.create_window(
            0, 0, anchor=tk.NW, window=self.corpo
        )

        self.corpo.bind("<Configure>", self._ao_mudar_conteudo)
        self.canvas.bind("<Configure>", self._ao_mudar_canvas)
        self._ativar_rodinha(self)
        self._ativar_rodinha(self.corpo)
        self._ativar_rodinha(self.canvas)

    def _ao_scroll(self, inicio, fim) -> None:
        self.scroll.set(inicio, fim)
        self._atualizar_visibilidade_scroll()

    def _atualizar_visibilidade_scroll(self) -> None:
        """Só mostra a barra quando o conteúdo realmente passa da tela."""
        precisa = (self.scroll._fim - self.scroll._inicio) < 0.995
        if precisa and not self._scroll_visivel:
            self.canvas.pack_forget()
            self.scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 2), pady=4)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self._scroll_visivel = True
        elif not precisa and self._scroll_visivel:
            self.scroll.pack_forget()
            self._scroll_visivel = False
            self.canvas.yview_moveto(0)

    def _atualizar_regiao(self) -> None:
        """Recalcula a área rolável com a altura real do conteúdo (sem folga fantasma)."""
        self.corpo.update_idletasks()
        # reqheight evita bbox inflado após expandir/recolher cards.
        largura = max(self.corpo.winfo_reqwidth(), self.canvas.winfo_width())
        altura = self.corpo.winfo_reqheight()
        self.canvas.configure(scrollregion=(0, 0, largura, altura))
        self._atualizar_visibilidade_scroll()

    def _ao_mudar_conteudo(self, _evento=None) -> None:
        self._atualizar_regiao()

    def _ao_mudar_canvas(self, evento=None) -> None:
        self.canvas.itemconfigure(self._janela, width=evento.width)
        self._atualizar_regiao()

    def _ativar_rodinha(self, widget) -> None:
        widget.bind("<MouseWheel>", self._rolar, add="+")

    def ativar_rodinha_em_arvore(self, widget) -> None:
        """Liga a rodinha também nos filhos (formulario, labels, etc.)."""
        self._ativar_rodinha(widget)
        for filho in widget.winfo_children():
            self.ativar_rodinha_em_arvore(filho)

    def _rolar(self, evento):
        # Sem overflow, não rola (evita “scroll fantasma”).
        if (self.scroll._fim - self.scroll._inicio) >= 0.995:
            return "break"
        self.canvas.yview_scroll(int(-1 * (evento.delta / 120)), "units")
        return "break"


class NavegacaoAbas(tk.Frame):
    """Abas em formato de pílula (substitui o Notebook)."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COR_FUNDO, **kwargs)
        self._botoes: list[BotaoPilula] = []
        self._telas: list[tk.Widget] = []
        self._indice_atual = 0

        self.barra = tk.Frame(self, bg=COR_FUNDO)
        self.barra.pack(fill=tk.X, padx=4, pady=(0, 12))

        self.area = tk.Frame(self, bg=COR_FUNDO)
        self.area.pack(fill=tk.BOTH, expand=True)

    def adicionar(self, titulo: str, tela: tk.Widget) -> None:
        indice = len(self._telas)
        botao = BotaoPilula(
            self.barra,
            texto=titulo,
            comando=lambda i=indice: self.mostrar(i),
            ativo=(indice == 0),
        )
        botao.pack(side=tk.LEFT, padx=(0, 8))
        self._botoes.append(botao)
        self._telas.append(tela)

    def mostrar(self, indice: int) -> None:
        if indice < 0 or indice >= len(self._telas):
            return
        self._telas[self._indice_atual].pack_forget()
        self._indice_atual = indice
        self._telas[indice].pack(fill=tk.BOTH, expand=True)
        for i, botao in enumerate(self._botoes):
            botao.definir_ativo(i == indice)
        tela = self._telas[indice]
        if hasattr(tela, "ao_exibir"):
            tela.ao_exibir()

    def mostrar_primeira(self) -> None:
        if not self._telas:
            return
        self._indice_atual = 0
        self._telas[0].pack(fill=tk.BOTH, expand=True)
        for i, botao in enumerate(self._botoes):
            botao.definir_ativo(i == 0)
        if hasattr(self._telas[0], "ao_exibir"):
            self._telas[0].ao_exibir()


class CartaoExpansivel(tk.Frame):
    """
    Card clicável no estilo da referência:
    ícone + título + subtítulo + seta; corpo expansível abaixo.
    """

    def __init__(
        self,
        master,
        titulo: str,
        subtitulo: str = "",
        ao_alternar=None,
        **kwargs,
    ):
        fundo_pai = COR_FUNDO
        try:
            fundo_pai = master.cget("background")
        except tk.TclError:
            pass

        super().__init__(master, bg=fundo_pai, **kwargs)
        self.ao_alternar = ao_alternar
        self.expandido = False

        self.painel = PainelArredondado(self, raio=18, padding=10)
        self.painel.pack(fill=tk.X)

        self.cabecalho = tk.Frame(self.painel.corpo, bg=COR_PAINEL, cursor="hand2")
        self.cabecalho.pack(fill=tk.X)

        # Ícone simples (barras) à esquerda.
        self.icone = tk.Canvas(
            self.cabecalho,
            width=40,
            height=40,
            bg=COR_PAINEL,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.icone.pack(side=tk.LEFT, padx=(2, 12), pady=2)
        self._desenhar_icone()

        textos = tk.Frame(self.cabecalho, bg=COR_PAINEL, cursor="hand2")
        textos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.rotulo_titulo = tk.Label(
            textos,
            text=titulo,
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=fonte(12, True),
            anchor=tk.W,
            cursor="hand2",
        )
        self.rotulo_titulo.pack(fill=tk.X)

        self.rotulo_sub = tk.Label(
            textos,
            text=subtitulo,
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=fonte(9),
            anchor=tk.W,
            cursor="hand2",
        )
        self.rotulo_sub.pack(fill=tk.X)

        self.rotulo_seta = tk.Label(
            self.cabecalho,
            text="›",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SUAVE,
            font=fonte(18),
            width=2,
            cursor="hand2",
        )
        self.rotulo_seta.pack(side=tk.RIGHT, padx=(8, 4))

        # Corpo oculto até expandir.
        self.corpo = tk.Frame(self.painel.corpo, bg=COR_PAINEL)
        # Não faz pack até expandir.

        for widget in (
            self.cabecalho,
            self.icone,
            textos,
            self.rotulo_titulo,
            self.rotulo_sub,
            self.rotulo_seta,
        ):
            widget.bind("<Button-1>", self._ao_clicar)
            widget.bind("<Enter>", self._ao_entrar)
            widget.bind("<Leave>", self._ao_sair)

    def _desenhar_icone(self) -> None:
        self.icone.delete("all")
        criar_retangulo_arredondado(
            self.icone, 2, 2, 38, 38, 10, fill="#E0F2FE", outline=""
        )
        # Três barras estilo gráfico.
        self.icone.create_rectangle(10, 22, 15, 30, fill=COR_DESTAQUE, outline="")
        self.icone.create_rectangle(18, 16, 23, 30, fill=COR_DESTAQUE, outline="")
        self.icone.create_rectangle(26, 10, 31, 30, fill=COR_DESTAQUE, outline="")

    def _ao_entrar(self, _evento=None) -> None:
        if not self.expandido:
            self.rotulo_seta.config(fg=COR_DESTAQUE)

    def _ao_sair(self, _evento=None) -> None:
        if not self.expandido:
            self.rotulo_seta.config(fg=COR_TEXTO_SUAVE)

    def _ao_clicar(self, _evento=None) -> None:
        self.definir_expandido(not self.expandido)
        if self.ao_alternar:
            self.ao_alternar(self, self.expandido)

    def definir_expandido(self, expandido: bool) -> None:
        self.expandido = expandido
        if expandido:
            if not hasattr(self, "_separador"):
                self._separador = tk.Frame(
                    self.painel.corpo, bg="#E2E8F0", height=1
                )
            self._separador.pack(fill=tk.X, pady=(10, 0))
            self.corpo.pack(fill=tk.X, pady=(12, 4), padx=2)
            self.rotulo_seta.config(text="˅", fg=COR_DESTAQUE)
        else:
            if hasattr(self, "_separador"):
                self._separador.pack_forget()
            self.corpo.pack_forget()
            self.rotulo_seta.config(text="›", fg=COR_TEXTO_SUAVE)
        self.painel._ao_mudar_conteudo()
        self.after_idle(self._avisar_area_rolavel)

    def _avisar_area_rolavel(self) -> None:
        """Recalcula o scroll da página após abrir/fechar o card."""
        widget = self
        while widget is not None:
            if hasattr(widget, "_atualizar_regiao"):
                widget._atualizar_regiao()
                return
            pai = widget.winfo_parent()
            if not pai:
                return
            widget = widget.nametowidget(pai)

    def atualizar_textos(self, titulo: str | None = None, subtitulo: str | None = None):
        if titulo is not None:
            self.rotulo_titulo.config(text=titulo)
        if subtitulo is not None:
            self.rotulo_sub.config(text=subtitulo)


COR_ACAO = "#3B82F6"
COR_BOTAO_SECAO_TEXTO = "#1E3A5F"
COR_BOTAO_SECAO_FUNDO = "#F1F5F9"
COR_BOTAO_SECAO_BORDA = "#C7D2E0"

class BotaoSecao(tk.Canvas):
    """Pílula da barra da seção (Cadastrar / Atualizar dados)."""

    def __init__(
        self,
        master,
        texto: str,
        comando,
        destaque: bool = False,
        **kwargs,
    ):
        fundo = COR_FUNDO
        try:
            fundo = master.cget("background")
        except tk.TclError:
            pass

        self.texto = texto
        self.comando = comando
        self.destaque = destaque
        metrica = tkfont.Font(
            family=fonte(10)[0],
            size=fonte(10)[1],
            weight="bold" if destaque else "normal",
        )
        self._largura = max(int(metrica.measure(texto) + 28), 110)
        self._altura = 34

        super().__init__(
            master,
            width=self._largura,
            height=self._altura,
            bg=fundo,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **kwargs,
        )
        self._desenhar()
        self.bind("<Button-1>", lambda _e: self.comando())
        self.bind("<Enter>", lambda _e: self._desenhar(hover=True))
        self.bind("<Leave>", lambda _e: self._desenhar())

    def _desenhar(self, hover: bool = False) -> None:
        self.delete("all")
        if self.destaque:
            fundo = COR_DESTAQUE_HOVER if hover else COR_DESTAQUE
            borda = fundo
            cor_texto = "#FFFFFF"
            peso = True
        else:
            fundo = "#E2E8F0" if hover else COR_BOTAO_SECAO_FUNDO
            borda = "#94A3B8" if hover else COR_BOTAO_SECAO_BORDA
            cor_texto = COR_BOTAO_SECAO_TEXTO
            peso = False
        criar_retangulo_arredondado(
            self,
            1,
            1,
            self._largura - 1,
            self._altura - 1,
            16,
            fill=fundo,
            outline=borda,
            width=1,
        )
        self.create_text(
            self._largura // 2,
            self._altura // 2,
            text=self.texto,
            fill=cor_texto,
            font=fonte(10, peso),
        )


class BotaoTextoAcao(tk.Canvas):
    """Pílula de texto para ações da lista (Atualizar / Excluir)."""

    def __init__(self, master, texto: str, comando, perigo: bool = False, **kwargs):
        fundo = COR_LISTA_FUNDO
        try:
            fundo = master.cget("background")
        except tk.TclError:
            pass
        self.texto = texto
        self.comando = comando
        self.perigo = perigo
        metrica = tkfont.Font(
            family=fonte(9, True)[0],
            size=fonte(9, True)[1],
            weight="bold",
        )
        self._largura = max(int(metrica.measure(texto) + 22), 76)
        super().__init__(
            master,
            width=self._largura,
            height=30,
            bg=fundo,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **kwargs,
        )
        self._desenhar()
        self.bind("<Button-1>", lambda _e: self.comando())
        self.bind("<Enter>", lambda _e: self._desenhar(hover=True))
        self.bind("<Leave>", lambda _e: self._desenhar())

    def _desenhar(self, hover: bool = False) -> None:
        self.delete("all")
        if self.perigo:
            fundo = "#FECACA" if hover else COR_PERIGO_FUNDO
            texto = COR_PERIGO
            borda = "#FECACA"
        else:
            fundo = "#DBEAFE" if hover else "#EFF6FF"
            texto = "#1D4ED8" if hover else COR_ACAO
            borda = "#BFDBFE"
        criar_retangulo_arredondado(
            self,
            1,
            1,
            self._largura - 1,
            29,
            10,
            fill=fundo,
            outline=borda,
            width=1,
        )
        self.create_text(
            self._largura // 2,
            15,
            text=self.texto,
            fill=texto,
            font=fonte(9, True),
        )


def criar_bloco_secao(master, titulo: str) -> tk.Frame:
    """Bloco interno arejado: título + área da tabela (sem bordas duras)."""
    bloco = tk.Frame(master, bg=COR_BLOCO)
    bloco.pack(fill=tk.X, pady=(0, 12))

    interno = tk.Frame(bloco, bg=COR_BLOCO)
    interno.pack(fill=tk.X, padx=14, pady=14)

    tk.Label(
        interno,
        text=titulo,
        bg=COR_BLOCO,
        fg=COR_DESTAQUE,
        font=fonte(11, True),
        anchor=tk.W,
    ).pack(fill=tk.X, pady=(0, 10))

    conteudo = tk.Frame(interno, bg=COR_BLOCO)
    conteudo.pack(fill=tk.X)
    return conteudo


def criar_lista_moderna(
    master,
    colunas: list[str],
    titulos: list[str],
    altura: int = 1,
    larguras: list[int] | None = None,
    com_acoes: bool = False,
    coluna_flexivel: str | None = None,
) -> ttk.Treeview:
    """
    Lista moderna: cabeçalho colorido + botões Atualizar/Excluir à direita.
    """
    colunas = list(colunas)
    titulos = list(titulos)
    if larguras is None:
        larguras = [70 if coluna == "id" else 160 for coluna in colunas]
    else:
        larguras = list(larguras)

    if coluna_flexivel is None:
        for coluna in colunas:
            if coluna != "id":
                coluna_flexivel = coluna
                break

    colunas_dados = list(colunas)
    titulos_dados = list(titulos)
    larguras_dados = list(larguras)
    largura_acoes = 184
    # Colunas de texto longo podem stretch junto com a flexível.
    colunas_stretch = {c for c in colunas if c in {coluna_flexivel, "categoria", "nome", "descricao", "email"}}

    # Faixa de cabeçalho com cor suave (sem linha cinza).
    faixa = tk.Frame(master, bg=COR_LISTA_CABECALHO, height=38)
    faixa.pack(fill=tk.X)
    faixa.pack_propagate(False)

    rotulos: list[tk.Label] = []
    for titulo in titulos_dados:
        rotulo = tk.Label(
            faixa,
            text=titulo,
            bg=COR_LISTA_CABECALHO,
            fg=COR_TEXTO,
            font=fonte(10, True),
            anchor=tk.W,
        )
        rotulos.append(rotulo)

    rotulo_acoes = None
    if com_acoes:
        rotulo_acoes = tk.Label(
            faixa,
            text="Ações",
            bg=COR_LISTA_CABECALHO,
            fg=COR_TEXTO,
            font=fonte(10, True),
            anchor=tk.CENTER,
        )

    area = tk.Frame(master, bg=COR_LISTA_FUNDO)
    area.pack(fill=tk.X, pady=(0, 2))

    tree = ttk.Treeview(
        area,
        columns=colunas,
        show="",
        height=altura,
        selectmode="browse",
        cursor="hand2",
    )
    tree.column("#0", width=0, minwidth=0, stretch=False)

    for coluna, largura in zip(colunas, larguras):
        if coluna in colunas_stretch:
            tree.column(
                coluna,
                width=largura,
                minwidth=max(90, min(largura, 120)),
                anchor=tk.W,
                stretch=True,
            )
        else:
            tree.column(
                coluna,
                width=largura,
                minwidth=largura,
                anchor=tk.W,
                stretch=False,
            )

    tree.tag_configure("zebra", background="#ECFEFF")

    scroll = ScrollModern(area, comando=tree.yview, cor_fundo=COR_LISTA_FUNDO)
    tree._scroll_lista = scroll
    tree._com_acoes = com_acoes

    if com_acoes:
        frame_acoes = tk.Frame(area, bg=COR_LISTA_FUNDO, width=largura_acoes)
        frame_acoes.pack(side=tk.RIGHT, fill=tk.Y)
        frame_acoes.pack_propagate(False)
        tree._frame_acoes = frame_acoes
        tree._ao_editar = None
        tree._ao_excluir = None

    tree.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _ao_rolar_lista(*args) -> None:
        scroll.set(*args)
        if com_acoes:
            tree.after_idle(lambda: atualizar_botoes_acoes(tree))

    tree.configure(yscrollcommand=_ao_rolar_lista)

    def _sincronizar_cabecalho(_evento=None) -> None:
        filhos = tree.get_children()
        if filhos:
            for i, col in enumerate(colunas_dados):
                caixa = tree.bbox(filhos[0], col)
                if not caixa:
                    continue
                x, _y, largura_col, _h = caixa
                rotulos[i].place(x=x, y=7, width=max(largura_col, 20), height=24)
        else:
            x = 8
            for i, largura_col in enumerate(larguras_dados):
                rotulos[i].place(x=x, y=7, width=largura_col, height=24)
                x += largura_col
        if rotulo_acoes is not None:
            largura_faixa = max(faixa.winfo_width(), largura_acoes)
            rotulo_acoes.place(
                x=largura_faixa - largura_acoes,
                y=7,
                width=largura_acoes,
                height=24,
            )

    tree._sincronizar_cabecalho = _sincronizar_cabecalho
    faixa.bind("<Configure>", _sincronizar_cabecalho)
    tree.bind("<Configure>", _sincronizar_cabecalho)
    area.bind("<Configure>", _sincronizar_cabecalho)
    faixa.after_idle(_sincronizar_cabecalho)

    def _rolar(evento):
        tree.yview_scroll(int(-1 * (evento.delta / 120)), "units")
        if com_acoes:
            tree.after_idle(lambda: atualizar_botoes_acoes(tree))
        return "break"

    tree.bind("<MouseWheel>", _rolar)
    area.bind("<MouseWheel>", _rolar)
    if com_acoes:
        frame_acoes.bind("<MouseWheel>", _rolar)

    return tree


def configurar_acoes_lista(tree: ttk.Treeview, ao_editar, ao_excluir) -> None:
    """Define os callbacks dos ícones de ação da lista."""
    tree._ao_editar = ao_editar
    tree._ao_excluir = ao_excluir


def atualizar_botoes_acoes(tree: ttk.Treeview) -> None:
    """Posiciona Atualizar/Excluir alinhados à bbox de cada linha visível."""
    frame = getattr(tree, "_frame_acoes", None)
    if frame is None:
        return
    for filho in frame.winfo_children():
        filho.destroy()

    ao_editar = getattr(tree, "_ao_editar", None)
    ao_excluir = getattr(tree, "_ao_excluir", None)
    if not ao_editar or not ao_excluir:
        return

    for iid in tree.get_children():
        caixa = tree.bbox(iid)
        if not caixa:
            continue
        _x, y, _largura, altura = caixa
        if altura <= 1:
            continue

        linha = tk.Frame(frame, bg=COR_LISTA_FUNDO)
        linha.place(x=0, y=y, relwidth=1, height=altura)

        centro = tk.Frame(linha, bg=COR_LISTA_FUNDO)
        centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        BotaoTextoAcao(
            centro,
            "Atualizar",
            lambda i=iid: ao_editar(int(i)),
        ).pack(side=tk.LEFT, padx=(0, 4))
        BotaoTextoAcao(
            centro,
            "Excluir",
            lambda i=iid: ao_excluir(int(i)),
            perigo=True,
        ).pack(side=tk.LEFT)


def ajustar_altura_lista(tree: ttk.Treeview, quantidade: int) -> None:
    """Faz a tabela crescer/encolher e só mostra scroll se precisar."""
    if quantidade <= 0:
        linhas = ALTURA_LISTA_MIN
    else:
        linhas = min(max(quantidade, ALTURA_LISTA_MIN), ALTURA_LISTA_MAX)
    tree.configure(height=linhas)

    scroll = getattr(tree, "_scroll_lista", None)
    if scroll is not None:
        if quantidade <= ALTURA_LISTA_MAX:
            scroll.pack_forget()
        else:
            scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))

    tree.update_idletasks()
    sincronizar = getattr(tree, "_sincronizar_cabecalho", None)
    if callable(sincronizar):
        sincronizar()
    if getattr(tree, "_com_acoes", False):
        atualizar_botoes_acoes(tree)
        tree.after_idle(lambda: atualizar_botoes_acoes(tree))

    # Avisa o card pai para recalcular a altura (sem buraco branco).
    widget = tree
    while widget is not None:
        if hasattr(widget, "_ao_mudar_conteudo"):
            widget._ao_mudar_conteudo()
            break
        pai = widget.winfo_parent()
        if not pai:
            break
        widget = widget.nametowidget(pai)


def inserir_linha_lista(
    tree: ttk.Treeview,
    valores,
    iid: str | None = None,
    indice: int = 0,
) -> str:
    """Insere linha com zebrado suave e devolve o iid."""
    tags = ("zebra",) if indice % 2 else ()
    kwargs = {"values": valores, "tags": tags}
    if iid is not None:
        kwargs["iid"] = iid
    return tree.insert("", tk.END, **kwargs)
