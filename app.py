# First, import the elements you need
import streamlit as st
import pandas as pd
from streamlit_elements import elements, mui, html
from urllib.request import urlopen
import numpy as np
import time
import webbrowser

import pdb

from drisk_api import GraphClient

token = "eyJraWQiOiJNVFJkMjJsYk1VMURFcmMzTmM1bmFRZzg5UDhpRVBJdlwvb0VkNWlobVwvTDA9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlZDIyMDhhZi1jNWUwLTRjNjktOGNjNC1mMDliMjM0N2U2MTciLCJjb2duaXRvOmdyb3VwcyI6WyJuZXdfdXNlcnMiXSwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTIuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0yX1Z0cEtiQ3dDOCIsImNvZ25pdG86dXNlcm5hbWUiOiJzYWJyaW5hY2hldW5nIiwib3JpZ2luX2p0aSI6Ijc1ZDNiZDU5LTM2MjgtNDcxZC05OTI1LTZjYWY3OTU0Y2IyMiIsImF1ZCI6IjN0aWZsbGp0cWxwMjYxaDBmZDR2ODk4MDhvIiwiZXZlbnRfaWQiOiJjNTJiNDJlNS1iOTQ4LTQ3MzMtYTg4My1kYzA0MGQ2YmMyNmUiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTcxODM5MDE0NSwiZXhwIjoxNzE4NjgxMDQyLCJpYXQiOjE3MTg2Mzc4NDIsImp0aSI6ImFmNTkzMDAwLWIxYjQtNDhlMy04NmJiLTA3Yjk2YzJhYzY2YiIsImVtYWlsIjoic2FicmluYUBoZWx5bnguY29tIn0.JtFnuLY_o7sBjmMHOuixat2AQYGoVJicRg85TGE5xU5ggIbdxsuwvOdg_UTPXHxEcRK5g9sciVjLz1v5POXZplGqEA7HfgekyYjcLXOJE1jbSmegJJkKWBjEiOhVNMUjWcHfMg-Uwf65DBCtmUXEIcI6KQrk1SmHNkWHWpvTFhpObAVoAahGO5_BmvnHBqM8Dw6LNpCS_pbQx0Ww9IwiCImUGRKw6idDRh5-78qFEMP2TbTu5-uMRXICb7VwuJWP6XmBvVUXCGSXVf_-X-NbsO0N7ndhE3QAM1rYiuarEvwha-t995mKZw7MpeQxsXA5UamO6RLlsEVHCfRevgEDAg"
url = "https://server-01.graph.drisk.ai/v3/graphs"


# create or conntect to a graph
graph = GraphClient(graph_id="411e73fa-0416-43a9-ab01-d3c22907d01b", auth_token=token, url = url)
plot_trace_0_node = graph.get_node("37965c90-421f-4366-a250-8caf48498d69")
print("ok if we can get this node then everything else will be easy...")
print(".....?")
print(plot_trace_0_node)
if plot_trace_0_node:
    print("YAAAAAS!")
else:
    print("boo")
# let's get some graph data baby!
view_node = graph.get_node("5c527f64-0d9b-4055-8097-783eca9bebaf");
# x_and_y_nodes = graph.get_successors(view_node.id); this is the right way but I'm lazy
x_node_id = "bc23f344-5860-4645-8695-274d2c6e17af";
y_node_id = "808453f0-5fe5-468e-bb45-c64c8b652b84";

to_dash_insert = graph.get_successors(y_node_id,weights=True);
x_wts = graph.get_successors(x_node_id,weights=True);
x_wts_by_node = {x_wts[0][ii]:x_wts[1][ii] for ii in range(len(x_wts[0]))}
y_wts_by_node = {to_dash_insert[0][ii]:to_dash_insert[1][ii] for ii in range(len(to_dash_insert[0]))}
by_xynode = [[x_wts_by_node[_node],y_wts_by_node[_node],_node] for _node in x_wts_by_node];
by_xynode.sort();
xs,ys,nodes =  zip(*list(by_xynode))
print(to_dash_insert)
print("xs, ys, nodes: ")
print(xs)
print(ys)
print(nodes)



to_make_into_dataframe = np.zeros([15, 3]); #np.random.randn(15, 3);
for ii in range(len(ys)):
    to_make_into_dataframe[ii,0] = ys[ii]
    # to_make_into_dataframe[ii,0] = to_dash_insert[1][ii];
df = pd.DataFrame(to_make_into_dataframe, columns=(["A", "B", "C"]))

#pdb.set_trace();



# GENERAL PAGE
st.set_page_config(layout="wide")

bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background: rgb(32,59,108);
background: radial-gradient(circle, rgba(32,59,108,1) 20%, rgba(32,46,97,1) 50%);
}
</style>
"""

st.markdown(bg_img, unsafe_allow_html=True)

# TABS & COLUMNS
tab1, tab2, tab3 = st.tabs(["ANALYTICS", "TESTING", "CONTENT"])

with tab1:
    col1, col2, col3 = st.columns([20,1,6])
    with col1:
        # DATA & GRAPH
        with st.container(height=450):
            my_data_element = st.line_chart(df)

            def link():
                webbrowser.open_new_tab('https://dev-app.drisk.ai/?graphId=411e73fa-0416-43a9-ab01-d3c22907d01b&viewId=5c527f64-0d9b-4055-8097-783eca9bebaf')

            column1, column2, column3 = st.columns ([2,2,9])
            with column1:
                st.button("update graph!")
            with column2:
                st.button('edit graph!', on_click=link)

  
        # DASHBOARD
        with elements("dashboard"):
            from streamlit_elements import dashboard
            layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
                dashboard.Item("first_item", 0, 0, 4, 1.3, isResizable=False, className="custom-paper"),
                dashboard.Item("second_item", 4, 0, 4, 1.3, isResizable=False, className="custom-paper"),
                dashboard.Item("third_item", 8, 0, 4, 1.3, isResizable=False, className="custom-paper"),
                dashboard.Item("fourth_item", 0, 2, 4, 1.3, isResizable=False, className="custom-paper"),
                dashboard.Item("fifth_item", 4, 2, 4, 1.3, isResizable=False, className="custom-paper"),
                dashboard.Item("sixth_item", 8, 2, 4, 1.3, isResizable=False, className="custom-paper"),
            ]


        cardstyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "bgcolor": "background.paper",
            "boxShadow": 1,
            "borderRadius": 3,
            "p": 4,
            "minWidth": 300,
        }


        numberstyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "fontSize": 35,
            "padding": 1,
        }

        posiconstyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "fontSize": 45,
            "align-self": "flex-end",
            "color": "#64CDF6",
        }

        negiconstyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "fontSize": 45,
            "align-self": "flex-end",
            "color": "#FA3DA2",
        }

        positivestyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "fontSize": 15,
            "color": "#64CDF6",
        }

        negativestyle={
            "display": "flex",
            "flex-direction": "column",
            "fontFamily": "verdana",
            "fontSize": 15,
            "color": "#FA3DA2",
        }

    with elements("demo"):   
        with dashboard.Grid(layout):
            with mui.Paper(sx=cardstyle, key="first_item"):
                mui.Box("ADD TO CART OCCURENCES PER USER", key="first_item")
                mui.Box("25%", sx=numberstyle)
                mui.Box("-10 ▼", sx=negativestyle)
                mui.Box("☹︎", sx=negiconstyle)
            with mui.Paper(sx=cardstyle, key="second_item"):
                mui.Box("AVERAGE REVENUE PER DAILY USER", key="first_item")
                mui.Box("23,025", sx=numberstyle)
                mui.Box("-10 ▼", sx=negativestyle)
                mui.Box("☹︎", sx=negiconstyle)
            with mui.Paper(sx=cardstyle, key="third_item"):
                mui.Box("AVERAGE REVENUE PER PURCHASE", key="first_item")
                mui.Box("16,642", sx=numberstyle)
                mui.Box("+4 ▲", sx=positivestyle)
                mui.Box("☺︎", sx=posiconstyle)
            with mui.Paper(sx=cardstyle, key="fourth_item"):
                mui.Box("TIME IN ITEM PER DAILY USER", key="first_item")
                mui.Box("12%", sx=numberstyle)
                mui.Box("+4 ▲", sx=positivestyle)
                mui.Box("☺︎", sx=posiconstyle)
            with mui.Paper(sx=cardstyle, key="fifth_item"):
                mui.Box("TIME UNTIL USER FIRST ADD TO CART", key="first_item")
                mui.Box("52%", sx=numberstyle)
                mui.Box("+50% ▲", sx=positivestyle)
                mui.Box("☺︎", sx=posiconstyle)
            with mui.Paper(sx=cardstyle, key="sixth_item"):
                mui.Box("PERCENT OF DAILY USERS WHO LOGIN", key="first_item")
                mui.Box("22%", sx=numberstyle)
                mui.Box("+50% ▲", sx=positivestyle)
                mui.Box("☺︎", sx=posiconstyle)


    # NOTIFICATIONS
    with col3:
        st.subheader("Notifications")
        st.divider()
        st.write("Welcome to shop stock!")
        st.divider()
        st.write("Clearance items to double your discount")
        st.divider()
        st.write("For the next 3 days, you get 25% OFF!")
        st.divider()

