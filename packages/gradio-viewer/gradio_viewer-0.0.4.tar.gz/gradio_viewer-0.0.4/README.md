---
tags: [gradio-custom-component, File]
title: gradio_viewer
short_description: Visualise files
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_viewer`
<a href="https://pypi.org/project/gradio_viewer/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_viewer"></a>  

Visualise files

## Installation

```bash
pip install gradio_viewer
```

## Usage

```python
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

```

## `Viewer`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
Any
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>info</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>load_fn</code></td>
<td align="left" style="width: 25%;">

```python
Callable[..., Any] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>n</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>0</code></td>
<td align="left">None</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` |  |
| `upload` |  |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, the data after preprocessing, sent to the user's function in the backend.
- **As input:** Should return, expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.

 ```python
 def predict(
     value: str
 ) -> str | list[str] | None:
     return value
 ```
 
