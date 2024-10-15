import time
import uuid


def open_browser_window_from_notebook(url_to_open: str) -> None:
    try:
        from IPython.display import (  # type:ignore # pylint: disable=import-error, import-outside-toplevel
            Javascript,
            display,
            update_display,
        )
    except ImportError as error:
        raise Exception('Unexpected environment. This function can only be called from a notebook.') from error

    display_id = str(uuid.uuid4())
    js_code = f"""
    if (!localStorage.getItem('windowOpened_{display_id}')) {{
        window.open('{url_to_open}');
        localStorage.setItem('windowOpened_{display_id}', 'true');
    }}
    """
    display(Javascript(js_code), display_id=display_id)
    time.sleep(1)
    # update_display clears the javascript so we don't re-open the same window.
    # However, this doesn't work in all cacses, hence the above localStorage solution.
    update_display(Javascript(''), display_id=display_id)
