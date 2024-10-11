import gradio as gr
from gradio_viewer import Viewer

import sys

sys.path = list(dict.fromkeys(sys.path))
print(sys.path)
print(sys.prefix)

with gr.Blocks() as demo:
    with gr.Row():
        pdf = (
            Viewer(
                value=[
                    "../../.neo-sandbox/dummy-email/6dbf7d358da06263/Le_Petit_Chaperon_Rouge_Modifie.pdf",
                    "../../.neo-sandbox/dummy-email/6dbf7d358da06263/Polytechnique_IA_generative.pdf",
                    "../../.neo-sandbox/dummy-email/6dbf7d358da06263/comparaison_couts.png",
                ],
                elem_classes=["visualisation"],
                n=1,
                # value="../../.neo-sandbox/dummy-email/6dbf7d358da06263/mermaid_graph-2.html",
                # value="../../.neo-sandbox/dummy-email/6dbf7d358da06263/demonstration_pythagore.md",
                # value="../../.neo-sandbox/dummy-email/6dbf7d358da06263/calcul_pythagore.py",
            ),
        )  # interactive version of your component

if __name__ == "__main__":
    demo.launch()
