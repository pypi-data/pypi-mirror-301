import importlib.resources
import json
from typing import Any

import webview

from beni.btype import Null


def show(
    itemList: Any,
    *,
    title: str = '标题',
    width: int = 500,
    height: int = 400,
    labelWidth: int = 160,
    resizable: bool = False,
    debug: bool = False,
):
    '''
    bform.show([
        bform.makeInputItem('username', 'Username', placeholder='Enter your username'),
        bform.makePasswordItem('password', 'Password', placeholder='Enter your password'),
        bform.makeCheckboxItem('remember', 'Remember', label='Remember me'),
    ])
    '''

    # test start
    with importlib.resources.path('beni.resources.web-form', 'index.html') as file:
    # file = r'./beni/resources/web-form/index.html'
    # test end

        result = Null

        class Api():

            def done(self, value: Any):
                nonlocal result
                result = value
                window.destroy()

        def init():
            value = json.dumps({
                'labelWidth': f'{labelWidth}px',
                'itemList': itemList,
            })
            window.evaluate_js('window.__show( JSON.parse(`' + value + '`) );')

        window = webview.create_window(
            title,
            str(file),
            js_api=Api(),
            width=width,
            height=height,
            resizable=resizable,
        )
        webview.start(init, debug=debug)

        return result


def makeInputItem(
    key: str,
    name: str,
    *,
    placeholder: str = '',
):
    return {
        'key': key,
        'name': name,
        'type': 'InputItem',
        'placeholder': placeholder,
    }


def makePasswordItem(
    key: str,
    name: str,
    *,
    placeholder: str = '',
):
    return {
        'key': key,
        'name': name,
        'type': 'PasswordItem',
        'placeholder': placeholder,
    }


def makeCheckboxItem(
    key: str,
    name: str,
    label: str,
):
    return {
        'key': key,
        'name': name,
        'type': 'CheckboxItem',
        'label': label,
    }

# ----------------------------

# import webview
# import importlib.resources

# def show():

#     with importlib.resources.path('beni.data', 'index.html') as file:
#         print(file)
#         webview.create_window(
#             'Simple browser',
#             str(file),
#         )
#         webview.start()

#     # file = f'./beni/data/index.html'
