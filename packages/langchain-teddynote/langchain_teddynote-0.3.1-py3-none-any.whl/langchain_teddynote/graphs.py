from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph


def visualize_graph(graph):
    try:
        # 그래프 시각화
        if isinstance(graph, CompiledStateGraph):
            display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass
