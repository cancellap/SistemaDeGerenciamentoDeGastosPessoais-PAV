"""Ponto de entrada da interface gráfica.

Executar a partir da raiz do repositório:
    python -m interface.main
"""

from interface.views.main_window import MainWindow


def main() -> None:
    # Cria a janela e inicia o loop de eventos do Tkinter.
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
