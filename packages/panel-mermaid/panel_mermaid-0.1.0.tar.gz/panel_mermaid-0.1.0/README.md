# panel-mermaid

## Overview

`panel-mermaid` is an interactive widget-based tool designed to integrate [Mermaid JS](https://mermaid.js.org/) diagramming functionality with [HoloViz Panel](https://panel.holoviz.org/).

This package provides a seamless interface for creating and customizing Mermaid diagrams directly in Python, with the ability to edit configurations and styles interactively.

### Key Features

- **Interactive Mermaid Diagrams**: Easily create flowcharts, sequence diagrams, class diagrams, and more using the familiar Mermaid syntax.
- **Configurable Themes and Looks**: Choose from a variety of themes (`default`, `dark`, `forest`, etc.) and looks (`classic`, `handDrawn`).
- **Real-time Configuration Updates**: Use the `MermaidConfiguration` widget to dynamically update your diagram’s configuration.
- **Customizable Events**: Handle diagram interactions with event subscriptions (e.g., click, mouseover).
- **Font-Awesome Icon Support**: Leverage Font-Awesome icons in your diagrams by including the Font-Awesome CSS in your application.

## Installation

You can install the package using `pip`:

```bash
pip install panel-mermaid
```

## Usage

### 1. Basic Mermaid Diagram

Here’s how to create a simple Mermaid diagram using the `MermaidDiagram` widget:

```python
import panel as pn
from panel_mermaid import MermaidDiagram

pn.extension()

diagram = MermaidDiagram(
    object="""
        graph LR
            A[Hello] --- B[World]
            B-->C[forbidden]
            B-->D[allowed]
    """
)
diagram.servable()
```

### 2. Customizing the Configuration

Use the `MermaidConfiguration` widget to interactively modify the Mermaid diagram configuration. Here's an example of how to integrate it:

```python
from panel_mermaid import MermaidDiagram, MermaidConfiguration

config = MermaidConfiguration()

diagram = MermaidDiagram(
    object="""
        graph TD
            E --> F
            F --> G[End]
    """,
    configuration=config,
)

pn.Column(config, diagram).servable()
```

### 3. Event Handling

You can also add event listeners to the diagram, allowing interactivity such as responding to clicks on diagram nodes:

```python
diagram.event_configuration = [("click", ".node")]

@pn.depends(diagram.param.event, watch=True)
def handle_event(event):
    print(f"Diagram event: {event}")

pn.Column(diagram).servable()
```

## Mermaid Configuration

The `MermaidConfiguration` widget allows you to adjust diagram styling and themes, making it simple to adapt to various visual preferences. You can customize:

- **Look**: Choose between `classic` or `handDrawn`.
- **Theme**: Choose from several themes like `default`, `dark`, `forest`, etc.

Example:

```python
config = MermaidConfiguration(look='handDrawn', theme='dark')
```

## Font-Awesome Icons

To use Font-Awesome icons in your Mermaid diagrams, include the Font-Awesome CSS:

```python
pn.extension(
    css_files=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"]
)
```

Once included, you can add icons to your diagrams by prefixing with `fa:`.

## Contributions

We welcome contributions to this project! Please feel free to submit issues or pull requests to the [GitHub repository](https://github.com/awesome-panel/panel-mermaid).

## License

This project is licensed under the MIT License.

---

Start building rich, interactive diagrams directly in your Python applications with `panel-mermaid`!

## Known Issues

- JSON and CodeEditor widgets do not work with theme
- JSON widget has no label

## Feature Request

- RowSplitter, ColumnSplitter