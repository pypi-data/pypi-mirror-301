import gradio as gr
from gradio_viewer import Viewer


with gr.Blocks() as demo:
    with gr.Row():
        pdf = (
            Viewer(
                value=[
                    "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
                    "./demo/data/mermaid_graph-2.html",
                    "./demo/data/graphique_couts_annuels.png",
                    "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
                ],
                elem_classes=["visualisation"],
                n=1,
            ),
        )

if __name__ == "__main__":
    demo.launch()
