from padislib.renderer.console_render.render import ConsoleRenderStrategy
from padislib.renderer.html_render.render import HtmlRenderStrategy


def render(data, format_type, file_path=None):
    """
    Renders the results using the provided strategy according to the format
    type.

    Args:
        data (dict): Test data.
        format_type (str): Format type to use ('html', 'console', etc.).
        file_path (str): File path if necessary (optional).
    """
    if format_type == "html":
        strategy = HtmlRenderStrategy()
    elif format_type == "console":
        strategy = ConsoleRenderStrategy()
    else:
        raise ValueError(f"Unknown format type: {format_type}")

    strategy.render(data, file_path)
