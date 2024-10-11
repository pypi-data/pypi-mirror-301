import os
import streamlit.components.v1 as components
from typing import Callable, Optional

_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_tree_independent_components",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_tree_independent_components", path=build_dir)


def tree_independent_components(treeItems={},checkItems=[], disable=False, single_mode=False, show_select_mode=False, on_change: Optional[Callable[[], None]] = None, y_scroll=False, x_scroll=False, x_scroll_width=60, frameHeight=50, border=False ,key=None):
    component_value = _component_func(treeItems=treeItems,checkItems=checkItems, disable=disable,single_mode=single_mode, show_select_mode=show_select_mode, on_change=on_change, y_scroll=y_scroll,x_scroll=x_scroll, default={'setSelected': checkItems, 'single_mode': single_mode}, x_scroll_width=x_scroll_width, frameHeight=frameHeight,border=border, key=key)
    if on_change is not None:
        on_change()
    return component_value



# import streamlit as st
# from streamlit_tree_independent_components import tree_independent_components


# st.subheader("Component with input args")


# treeItems = {
#    "id":"0",
#    "name":"Project Dashboard",
#    "icon":"",
#    "disable":False,
#    "children":[
#       {
#          "id":"1",
#          "name":"Technology Expense Summary",
#          "icon":"",
#          "disable":False,
#          "children":[
#             {
#                "id":"2",
#                "name":"Cost Efficiency Analysis",
#                "icon":"",
#                "disable":False,
#                "children":[
#                   {
#                      "id":"3",
#                      "name":"Financial Data Preparation",
#                      "icon":"",
#                      "disable":False
#                   },
#                   {
#                      "id":"4",
#                      "name":"Database Operations Review",
#                      "icon":"",
#                      "disable":False,
#                      "children":[
#                         {
#                            "id":"5",
#                            "name":"Data Entry for Operations",
#                            "icon":"",
#                            "disable":False,
#                            "children":[
#                               {
#                                  "id":"6",
#                                  "name":"User Data Extension",
#                                  "icon":"",
#                                  "disable":False,
#                                  "children":[
#                                     {
#                                        "id":"7",
#                                        "name":"Data Enhancement Process",
#                                        "icon":"",
#                                        "disable":False,
#                                        "children":[
#                                           {
#                                              "id":"8",
#                                              "name":"Business Analysis Report",
#                                              "icon":"",
#                                              "disable":False
#                                           },
#                                           {
#                                              "id":"9",
#                                              "name":"Performance Overview",
#                                              "icon":"",
#                                              "disable":False,
#                                              "children":[
#                                                 {
#                                                    "id":"10",
#                                                    "name":"Manual Input for Performance",
#                                                    "icon":"",
#                                                    "disable":False
#                                                 },
#                                                 {
#                                                    "id":"11",
#                                                    "name":"Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation",
#                                                    "icon":"",
#                                                    "disable": False
#                                                 }
#                                              ]
#                                           }
#                                        ]
#                                     }
#                                  ]
#                               }
#                            ]
#                         }
#                      ]
#                   }
#                ]
#             }
#          ]
#       }
#    ]
# }

# checkItems = ["0","1","2","3","4","5","6","7","9","8"]
# if "change" not in st.session_state:
#     st.session_state["change"] = checkItems
# if "i" not in st.session_state:
#     st.session_state["i"] = 0
# if "disable" not in st.session_state:
#     st.session_state["disable"] = False 
# if "single_mode" not in st.session_state:
#     st.session_state["single_mode"] = False 
# if "show_select_mode" not in st.session_state:
#     st.session_state["show_select_mode"] = False 
    
# change = st.button("Select index from 0 to 9")
# if change:
#     st.session_state["change"] = ["0", "1", "2", "3", "4", "5", "6", "7", "9", "8"]

# change2 = st.button("Deselect all")
# if change2:
#     st.session_state["change"] = []

# disable_toggle = st.button("Toggle Treeview View Enable/Disable")
# if disable_toggle:
#     st.session_state["disable"] = not st.session_state["disable"]

# st.warning(f"Treeview disable! Current set: {st.session_state['disable']}")

# single_mode = st.button("Toggle Single Select True/False")
# if single_mode:
#     st.session_state["single_mode"] = not st.session_state["single_mode"]

# st.warning(f"Treeview select_mode ! Current set: {st.session_state['single_mode']}")

# show_select_mode = st.button("Toggle To Show Select Mode")
# if show_select_mode:
#     st.session_state["show_select_mode"] = not st.session_state["show_select_mode"]

# result = tree_independent_components(treeItems, checkItems=st.session_state["change"],disable=st.session_state['disable'], single_mode=st.session_state["single_mode"],show_select_mode=st.session_state["show_select_mode"], x_scroll=True, y_scroll=True, x_scroll_width=40, frameHeight=20, border=True)
# st.warning(result)
# try:
#    st.write(sorted(result["setSelected"], key=int))
#    #st.session_state["change"] = sorted(result["setSelected"], key=int)
# except:
#   pass

