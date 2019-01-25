import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import glob
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'test_image.png' # replace with your own image
open(image_filename, 'rb')
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(children=[
    html.H1(children='super-duper-chainsaw'),

    html.Div(children='''
        Distributed image processing
    '''),

html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
]),


# app.layout =
    #
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # )
])

if __name__ == '__main__':
    app.run_server(debug=True)