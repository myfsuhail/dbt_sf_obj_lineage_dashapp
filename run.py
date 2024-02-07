import pandas as pd
from dash import Dash, html, dcc, dependencies
import coordinates
import dash_cytoscape as cyto
 
# Initialize Dash app
app = Dash(__name__, title='CSOD')
 
# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = r'data/result.csv'

# to fetch columns
column_file_path = r'data/columns.xlsx'
df_columns = pd.read_excel(column_file_path)

def fetch_columns(schema_name, object_name):

    filtered_df = df_columns[(df_columns['TABLE_SCHEMA'] == schema_name) & (df_columns['TABLE_NAME'] == object_name)]
    conc_df = filtered_df['COLUMN_NAME']
    column_list = conc_df.tolist()
    return column_list

# Read the CSV file into a DataFrame
src_df = pd.read_csv(csv_file_path)
 
# Define initial lineage object ID
initial_lineage_object_id = 'DIM_LEAD_SOURCE'
 
schema_options=[]
 
# Extract unique models from the DataFrame
table_options = src_df['LINEAGE_OBJECT_ID'].drop_duplicates().tolist()

report_src = pd.read_csv(r'data/reports.csv')
report_options = report_src['TABLE_NAME'].drop_duplicates().tolist()


def node_color(x,y,object, object_id_list):

  if x == 0 and y == 0:
    return '#F96c4b'
  elif object in (object_id_list):
    return '#79EA79'
  else:
    return '#0080ff'


# Define the layout for the Dash app
app.layout = html.Div([
 
        html.Div(
        dcc.Dropdown([i for i in table_options], initial_lineage_object_id, id='lineage-object-id-input',
                     clearable=True,
                     placeholder="Select a model...",
                     style={
                            # 'width': '50%',
                            # 'display': 'inline-block',
                            'height': '25px',
                            # 'margin':'0 auto',
                            'border-radius':'20px',
                            # 'margin-left': '14%',
                            # 'background-color': '#F6FBFF',
                            # 'border-color': '#DFE6E9',
                            # 'textAlign': 'center',
                            'font-family': 'Roboto',
                            # 'font-size': '40px',
                            'verticalAlign': 'middle',
                            'justify-content': 'center',
                            "top": "10px", "right": "20px"
                            } ),
                            style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'middle',
                                   'margin-left': '20px','margin-bottom': '40px'}
        ),
 
        # Number of nodes & edges display
        html.Div([
            html.Div(id='node-count',style={'display': 'flex','position': 'static','font-family': 'Roboto', 'font-size': '12px'}),
            html.Div(id='edge-count', style={'display': 'flex','position': 'relative','font-size': '12px','font-family': 'Roboto','float':'right',
                                             'padding-left': '17px'})
        ], style={'display': 'flex','position': 'absolute', 'margin-right': '20px', 'bottom': '10px', 'left': '10px'}),

        # column list
        # html.Div([
        # html.P(id='table_name', style={'font-size': '10px','font-family': 'Roboto','font-weight':'bold'}),  # Adjust font size here
        # html.Ul(id='column-list', style={'list-style-type': 'decimal', 'padding': '10px', 'margin': '10px','line-height':'1.2',
        #                                  'font-family': 'Roboto'}), #decimal
        #         ], style={'display': 'inline-block','position': 'absolute', 'right' : '5px', 'backgroundColor': '#FFDAB9','opacity':0.8,
        #       'padding': '13px', 'font-size': '10px','width': '17%', 'height': '50%', 'overflow': 'auto', 'border': '0.5px'}),

        html.Div([
        html.P(id='table_name', style={'font-size': '12px', 'font-family': 'Roboto', 'font-weight': 'bold','margin-bottom': '6px',
                                       'position': 'sticky','top': '10px', 'display': 'block','margin-left': '-10px'}),
        html.Ul(id='column-list',
                style={'list-style-type': 'decimal', 'padding': '5px', 'padding-top': '0px',
                       'font-family': 'Roboto','font-size': '10px', 'overflow': 'auto','height': '83%','overflow-wrap': 'break-word',
                        'padding-inline-start': '20px','margin-inline-start': '-5px', 'margin-right': '0px','scroll-behavior': 'smooth','scrollbar-width': 'thin'}),
                ], style={'display': 'inline-block', 'position': 'absolute', 'right': '5px', 'backgroundColor': '#FFDAB9',
              'opacity': 0.8,
              'padding': '13px', 'width': '17%', 'height': '40%','padding-right': '0px','padding-left': '25px',
              'border': '0.5'}),

        #report list
        html.Div([
        html.P(id='report_name', style={'font-size': '12px', 'font-family': 'Roboto', 'font-weight': 'bold','margin-bottom': '6px',
                                       'position': 'sticky','top': '10px', 'display': 'block','margin-left': '-10px'}),
        html.Ul(id='report-list',
                style={'list-style-type': 'decimal', 'padding': '5px', 'margin': '5px',
                       'font-family': 'Roboto','font-size': '10px', 'overflow': 'auto','height': '70%','overflow-wrap': 'break-word',
                        'padding-inline-start': '20px','margin-inline-start': '-5px', 'margin-right': '0px','scroll-behavior': 'smooth','scrollbar-width': 'thin'
                        }),
                ], style={'display': 'inline-block', 'position': 'absolute', 'right': '5px', 'backgroundColor': '#FFDAB9',
              'opacity': 0.8,
              'padding': '13px', 'width': '17%', 'height': '23.4%','padding-right': '0px','padding-left': '25px','margin-top':'330px',
              'border': '0.5'}),

        # Checklist for selecting schemas
        dcc.Checklist(
            id='schema-checklist',
            options=[schema for schema in schema_options],
            value=[schema for schema in schema_options],  # Default selected values
            style={                   
                    'display': 'flex',
                    'position': 'relative',
                    'margin-bottom': '10px',
                    'width': '81%',
                    'flex-wrap': 'wrap',
                    'align-items': 'flex-end',
                    'line-height': '1.6'},
            inline=True,
            inputStyle={"transform": "scale(1.2)"},
            labelStyle={"paddingright": "20px", "inline": True , "display": "flex", "justifyContent": "center","alignItems": "center",
                        "fontSize": "0.8em", "paddingLeft": "10px","fontFamily": 'Roboto'}
        ),

        #Legend
        html.Div(
            id="dummy-legend",
            children=[
                html.Span(
                    style={
                        "background-color": "#F96c4b",
                        "padding": "5px",
                        "margin-right": "-12px",
                        'width': '6px',
                        'height': '6px'
                    }
                ),
                html.Span("Object Selected", style={'font-size': '12px', 'font-family': 'Roboto'}),

                html.Span(
                    style={
                        "background-color": "#79EA79",
                        "padding": "5px",
                        "margin-right": "-12px",
                        'width': '6px',
                        'height': '6px'
                    }
                ),
                html.Span("Downstream with Reports", style={'font-size': '12px', 'font-family': 'Roboto'}),

                html.Span(
                    style={
                        "background-color": "#0080ff ",
                        "padding": "5px",
                        "margin-right": "-12px",
                        'width': '6px',
                        'height': '6px'
                    }
                ),
                html.Span("Upstream/Downstream", style={'font-size': '12px', 'font-family': 'Roboto'})
            ],
            style={
                "display": "flex",
                "justify-content": "space-between",
                "width": '450px',  # Adjust width as needed
                "padding": "5px",
                "margin-bottom": "10px",
                'top': '22px',
                'position': 'fixed',
                'left': '350px'
            },
        ),

        # Button to trigger the update
        html.Button('Update', id='update-button', style={"display": "inline-block",'position': 'static','margin-bottom': '0px','margin-top': '5px','margin-left': '10px',
                                                         'left': '10px'}),
 
        # Lineage object ID display
        html.Div(id='lineage-object-id-display', style={'margin-bottom': '4px', 'font-size': '18px','font-family': 'Roboto','font-weight':'bold',
                                                        'display': 'inline-block','position': 'absolute', 'bottom': '30px', 'left': '10px'}),

        html.Div([

        html.P(id='my-list-header', style={'font-size': '12px','font-weight':'bold','font-family': 'Roboto',
                                           'margin-bottom': '-10px'}),

        html.Div(
            id="my-list-container",style={'margin': '1px','font-size': '10px', 'border': '0.5px','list-style-type': 'disc',
                                          'white-space': 'normal','overflow-wrap': 'break-word'
                                          }),

        ],style={'margin-top': '0px','display': 'inline-block','position': 'absolute', 'right' : '4px', 'backgroundColor': '#FFDAB9','opacity':0.8,
              'padding': '13px','width': '17%', 'height': '24%', 'overflow': 'auto', 'border': '0.5px','scroll-behavior': 'smooth','scrollbar-width': 'thin',
              'bottom':'0px'}),        

        # Cytoscape component
        cyto.Cytoscape(
            id='cytoscope-data-lineage-view',
            # elements=elements,
            zoom=1,
            style={'width': '80%', 'height': '600px','margin-top':'0px','position': 'relative',
                   "top": "0px", "left": "10px"},
            layout={
                'name': 'preset',
                'avoidOverlap': 'true',
                'flow': { 'axis': 'y', 'minSeparation': 30 },
                'spacingFactor': 1.5,
                'nodeDimensionsIncludeLabels': False,
                'idealEdgeLength': 100,
                'edgeElasticity': 0.8
            },
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        # 'content': 'data(schema\n)' + 'data(model)',
                        "text-wrap": "wrap",
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'line-height': 2,
                        'text-justification' : 'center',
                        # "antialiasing": True,
                        'font-size': '0.8em',
                        # 'min-zoomed-font-size': 4,
                        "letter-spacing": '2em',
                        'font-family': 'Roboto',
                        'color': 'data(font_color)',
                        'width':'label',
                        'height':'label',
                        'shape':'round-rectangle',
                        'background-opacity': 'data(opacity)',
                        'padding': '10px',
                        'border-color': 'grey',
                        'border-style': 'solid',
                        'border-opacity': 0.7,
                        'border-width' : 2,                        
                        'background-color': 'data(color)'
                    }
                },              

                {
                    'selector': 'edge',
                    'style': {
                        'curve-style': 'bezier',
                        # 'target-arrow-color': 'black',
                        'target-arrow-shape': 'triangle-backcurve',
                        'arrow-scale': 2,
                        'width': 3,
                        'opacity':0.5
                        # 'line-color': 'grey'
                    }
                }
            ]
        ),
   
    # Store to save elements for Cytoscape
    dcc.Store(id='cytoscape-elements-store', data=[])
])
 
# Callback to update the Cytoscape component based on input
@app.callback(
    [dependencies.Output('cytoscope-data-lineage-view', 'elements'),
     dependencies.Output('node-count', 'children'),
     dependencies.Output('edge-count', 'children'),
     dependencies.Output('schema-checklist', 'options'),
     dependencies.Output('schema-checklist', 'value'),
     dependencies.Output('lineage-object-id-display', 'children'),
     dependencies.Output("my-list-container", "children"),
     dependencies.Output("my-list-header", "children"),
     dependencies.Output('cytoscape-elements-store', 'data')],
    [dependencies.Input('update-button', 'n_clicks')],
    [dependencies.State('lineage-object-id-input', 'value')]
)
def update_cytoscape(n_clicks, lineage_object_id):
    # Filter DataFrame based on the input lineage_object_id and selected schemas
    lineage_df = src_df[(src_df['LINEAGE_OBJECT_ID'] == lineage_object_id) &
                        (src_df['LEVEL_NUM'] != 0)]
 
    # Extract unique target and source table IDs from the filtered DataFrame
    target_table_id_df = lineage_df['TARGET_TABLE_ID'].drop_duplicates()
    source_table_id_df = lineage_df['SOURCE_TABLE_ID'].drop_duplicates()
 
    # Create nodes DataFrame by concatenating unique target and source table IDs
    nodes_df = pd.concat([target_table_id_df, source_table_id_df], ignore_index=True).drop_duplicates()

    schema_df1 = src_df['TARGET_SCHEMA'][src_df['LINEAGE_OBJECT_ID'] == lineage_object_id].drop_duplicates()
    schema_df2 = src_df['SOURCE_SCHEMA'][src_df['LINEAGE_OBJECT_ID'] == lineage_object_id].drop_duplicates()
    total_schema_df = pd.concat([schema_df1, schema_df2], ignore_index=True).drop_duplicates()
    schema_options = total_schema_df.tolist()
   
    # Convert Series to DataFrames if needed
    if isinstance(nodes_df, pd.Series):
        nodes_df = nodes_df.to_frame()

   
    # Rename the column to 'OBJECT_ID'
    nodes_df = nodes_df.rename(columns={0: 'OBJECT_ID'})
    coordinate_df = coordinates.get_coordinates(lineage_object_id)[0]
 
    position_df = coordinate_df.drop_duplicates() 
 
    nodes_df = nodes_df.merge(position_df, left_on='OBJECT_ID', right_on='MODEL_NAME')
 
    # Create nodes and edges for Cytoscape

    nodes = []
    edges = []

    for index, row in nodes_df.iterrows():
        node_c=node_color(row['X'],row['Y'],row['OBJECT_ID'], report_options)
        bg_opacity = 0.8 if row['X'] == 0 and row['Y'] == 0 else 0.3
        node_element = {
            'data': {'id': row['OBJECT_ID'], 'label': row['OBJECT'].split('.')[0] + '\n' +  row['OBJECT'].split('.')[1] ,
                    'model': row['OBJECT'].split('.')[1], 
                    'schema': row['OBJECT'].split('.')[0],
                    'color': node_c,
                    'font_color': 'black',
                    'opacity': bg_opacity},
            'position': {'x': row['X']*240, 'y': row['Y']*200}
        }
        nodes.append(node_element)

    edges_df = lineage_df[['SOURCE_TABLE_ID', 'TARGET_TABLE_ID']].drop_duplicates()
    edges = [{'data': {'id': row['SOURCE_TABLE_ID'].split('.')[0] + '.'+ row['TARGET_TABLE_ID'].split('.')[0], 'source': row['SOURCE_TABLE_ID'], 'target': row['TARGET_TABLE_ID']}}
             for index, row in edges_df.iterrows()]

    # Count of nodes and edges
    node_count = f"Number of Models: {len(nodes_df)}"
    edge_count = f"Number of Relations: {len(edges_df)}"

    jobs_df = coordinates.get_coordinates(lineage_object_id)[1]

    ul_list = []
    for index, row in jobs_df.iterrows():
        inner_list = [html.Li(dcc.Markdown(children=f"**{col}**: {col_value}"), style={'list-style-type': 'disc','line-height': '1.3','margin': '-8px','margin-bottom': '-5px',
                                                                                       'white-space': 'normal'}) for col, col_value in zip(jobs_df.columns[1:], row[1:])]  # Append column name before each value
        outer_list = [html.P(dcc.Markdown(children=f"**{jobs_df.columns[0]}**: {row[0]}"),style={'font-size': '11px','font-family': 'Roboto','margin-right':'0px','line-height': '0.8','padding-top': '8px','padding-bottom': '1px'
                                                                      }), html.Ul(inner_list,style={'font-size': '10px','font-family': 'Roboto'})]
        ul_list.append(html.Ul(outer_list, style={'list-style-type': 'disc'}))



    return nodes + edges, node_count, edge_count,schema_options,schema_options, f"Lineage for {lineage_object_id}",[html.Div(ul_list,style={'margin-left': '-38px'})] , f"DBT job details for {lineage_object_id}", nodes + edges
 
# Callback to update Cytoscape layout based on stored elements
@app.callback(
    dependencies.Output('cytoscope-data-lineage-view', 'layout'),
    [dependencies.Input('cytoscape-elements-store', 'data')]
)
def update_cytoscape_layout(elements):
    return {'name': 'preset', 'elements': elements}


@app.callback(
    dependencies.Output('report-list', 'children'),
    dependencies.Input('cytoscope-data-lineage-view', 'selectedNodeData')
)
def displaySelectedNodeReportData(data):

    if data:
        temp = [data['label'] for data in data]
        string_with_newline = temp[0]
        schema, table = string_with_newline.split('\n')

        #report data
        reports_df = coordinates.get_coordinates(table)[2]

        reports = reports_df['Report'].tolist()
    
        report_list = []
        for item in reports:
            # Splitting the item into two parts at the first space
            first_part, second_part = item.split("^", 1)
            # Adding styling to the text parts using HTML components
            formatted_item = html.Li([
                html.Span(first_part, style={'font-size': '10px','font-family': 'Roboto','margin-right':'2px'}),
                ' ',
                html.Span(second_part, style={'font-size': '9px','font-family': 'Roboto','font-weight':'bold'})
            ],style={'line-height': '1.3','margin-top': '5px'})
            report_list.append(formatted_item)

        return report_list
 
    return "Select any node to view Reports..."

@app.callback(
    dependencies.Output('column-list', 'children'),
    dependencies.Input('cytoscope-data-lineage-view', 'selectedNodeData')
)
def displaySelectedNodeData(data):

    if data:
        temp = [data['label'] for data in data]
        string_with_newline = temp[0]
        schema, table = string_with_newline.split('\n')
        columns = fetch_columns(schema, table)
        # print(columns)
        # return [html.Li(item) for item in columns]

        column_list = []
        for item in columns:
            # Splitting the item into two parts at the first space
            first_part, second_part = item.split(" ", 1)
            # Adding styling to the text parts using HTML components
            formatted_item = html.Li([
                html.Span(first_part, style={'font-size': '10px','font-family': 'Roboto','margin-right':'2px'}),
                ' ',
                html.Span(second_part, style={'font-size': '9px','font-family': 'Roboto','font-weight':'bold'})
            ],style={'line-height': '1.3','margin-top': '5px'})
            column_list.append(formatted_item)

        return column_list

    return "Select any node to view columns..."

@app.callback(
    dependencies.Output('table_name', 'children'),
    dependencies.Input('cytoscope-data-lineage-view', 'selectedNodeData')
)
def displaySelectedNode(data_list):
    result = []
    if data_list is None:
        return None

    temp = [data['model'] for data in data_list]
    
    return f"Columns present in  {temp[0]}:"

@app.callback(
    dependencies.Output('report_name', 'children'),
    dependencies.Input('cytoscope-data-lineage-view', 'selectedNodeData')
)
def displaySelectedNode(data_list):
    result = []
    if data_list is None:
        return None

    temp = [data['model'] for data in data_list]
    
    return f"Reports using {temp[0]}:"

@app.callback(
    dependencies.Output('cytoscope-data-lineage-view', 'stylesheet'),
    [dependencies.Input('schema-checklist', 'value')]
)
def update_stylesheet(selected_schemas):

    stylesheet= [
                
                    {
                        'selector': f'node[schema != "{schema}"]',
                        'style': {
                            # 'background-color': '#4CAF50',
                            'shape':'ellipse',
                            'width':10,
                            'height':10
                        }
                    } for schema in selected_schemas]  + [

                    {
                        'selector': f'node[schema = "{schema}"]',
                        'style': {
                            'label': 'data(label)',
                            # 'content': 'data(schema\n)' + 'data(model)',
                            "text-wrap": "wrap",
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'line-height': 2,
                            'text-justification' : 'center',
                            # "antialiasing": True,
                            'font-size': '0.8em',
                            # 'min-zoomed-font-size': 4,
                            "letter-spacing": '2em',
                            'font-family': 'Roboto',
                            'color': 'data(font_color)',
                            'width':'label',
                            'height':'label',
                            'shape':'round-rectangle',
                            'background-opacity': 'data(opacity)',
                            'padding': '10px',
                            'border-color': 'grey',
                            'border-style': 'solid',
                            'border-opacity': 0.7,
                            'border-width' : 2,                        
                            'background-color': 'data(color)'
                        }
                    } for schema in selected_schemas] + [              

                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            # 'target-arrow-color': 'black',
                            'target-arrow-shape': 'triangle-backcurve',
                            'arrow-scale': 2,
                            'width': 3,
                            'opacity':0.5
                            # 'line-color': 'grey'
                        }
                    } ]
                    
                    
                    # [              

                    # {
                    #     'selector': f'edge[id !^= "{schema}" or id !$= "{schema}"]',
                    #     'style': {
                    #         'curve-style': 'bezier',
                    #         # 'target-arrow-color': 'black',
                    #         'target-arrow-shape': 'triangle-backcurve',
                    #         'arrow-scale': 2,
                    #         'width': 3,
                    #         'opacity':0.5,
                    #         'line-color': 'red'
                    #         # 'line-color': 'grey'
                    #     }
                    # } for schema in selected_schemas] + [              

                    # {
                    #     'selector': f'edge[id !*= "{schema}"]',
                    #     'style': {
                    #         'curve-style': 'bezier',
                    #         # 'target-arrow-color': 'black',
                    #         'target-arrow-shape': 'triangle-backcurve',
                    #         'arrow-scale': 2,
                    #         'width': 3,
                    #         'opacity':0.5
                    #     }
                    # } for schema in selected_schemas]                  
                       
    return stylesheet

if __name__ == '__main__':
    app.run(debug=False,port=8052)
    # app.run_server(debug=False,host='0.0.0.0',port=8050)
    
