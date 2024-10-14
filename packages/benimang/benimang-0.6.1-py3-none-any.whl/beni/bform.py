import webview

def show():

    print('try...')

    file = f'./beni/data/index.html'
    webview.create_window(
        'Simple browser',
        file,
    )
    webview.start()
