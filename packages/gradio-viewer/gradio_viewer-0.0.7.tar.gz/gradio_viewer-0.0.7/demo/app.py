import gradio as gr
from gradio_viewer import Viewer


def set_interface():
    pdf = Viewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
        ],
        elem_classes=["visualisation"],
        n=1,
        height=300,
        visible=True,
    )

    pdf2 = Viewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
        ],
        elem_classes=["visualisation"],
        n=2,
        height=300,
        visible=True,
    )
    return pdf, pdf2


with gr.Blocks() as demo:
    with gr.Row():
        pdf = Viewer(visible=False)
        pdf2 = Viewer(visible=False)
    demo.load(set_interface, outputs=[pdf, pdf2])

if __name__ == "__main__":
    demo.launch()
