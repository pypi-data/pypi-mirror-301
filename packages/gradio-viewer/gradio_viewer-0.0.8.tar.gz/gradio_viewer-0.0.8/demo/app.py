import gradio as gr
from gradio_viewer import Viewer


def set_interface():
    view_with_ms = Viewer(
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

    view_without_ms = Viewer(
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
        ms_files=False,
    )
    return view_with_ms, view_without_ms


with gr.Blocks() as demo:
    with gr.Row():
        view_with_ms = Viewer(visible=False)
        view_without_ms = Viewer(visible=False)
    demo.load(set_interface, outputs=[view_with_ms, view_without_ms])

if __name__ == "__main__":
    demo.launch()
