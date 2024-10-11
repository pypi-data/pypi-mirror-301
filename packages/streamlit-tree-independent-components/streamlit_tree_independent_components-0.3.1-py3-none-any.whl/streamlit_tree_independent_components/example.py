import streamlit as st
from streamlit_tree_independent_components import tree_independent_components
import time

st.subheader("Component with input args")


treeItems = {
   "id":"0",
   "name":"Project Dashboard",
   "icon":"",
   "disable":False,
   "children":[
      {
         "id":"1",
         "name":"Technology Expense Summary",
         "icon":"",
         "disable":False,
         "children":[
            {
               "id":"2",
               "name":"Cost Efficiency Analysis",
               "icon":"",
               "disable":False,
               "children":[
                  {
                     "id":"3",
                     "name":"Financial Data Preparation",
                     "icon":"",
                     "disable":False
                  },
                  {
                     "id":"4",
                     "name":"Database Operations Review",
                     "icon":"",
                     "disable":False,
                     "children":[
                        {
                           "id":"5",
                           "name":"Data Entry for Operations",
                           "icon":"",
                           "disable":False,
                           "children":[
                              {
                                 "id":"6",
                                 "name":"User Data Extension",
                                 "icon":"",
                                 "disable":False,
                                 "children":[
                                    {
                                       "id":"7",
                                       "name":"Data Enhancement Process",
                                       "icon":"",
                                       "disable":False,
                                       "children":[
                                          {
                                             "id":"8",
                                             "name":"Business Analysis Report",
                                             "icon":"",
                                             "disable":False
                                          },
                                          {
                                             "id":"9",
                                             "name":"Performance Overview",
                                             "icon":"",
                                             "disable":False,
                                             "children":[
                                                {
                                                   "id":"10",
                                                   "name":"Manual Input for Performance",
                                                   "icon":"",
                                                   "disable":False
                                                },
                                                {
                                                   "id":"11",
                                                   "name":"Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation Post-Report Evaluation",
                                                   "icon":"",
                                                   "disable": False
                                                }
                                             ]
                                          }
                                       ]
                                    }
                                 ]
                              }
                           ]
                        }
                     ]
                  }
               ]
            }
         ]
      }
   ]
}

checkItems = ["0","1","2","3","4","5","6","7","9","8"]
if "change" not in st.session_state:
    st.session_state["change"] = checkItems
if "i" not in st.session_state:
    st.session_state["i"] = 0
if "disable" not in st.session_state:
    st.session_state["disable"] = False 
if "single_mode" not in st.session_state:
    st.session_state["single_mode"] = False 
if "show_select_mode" not in st.session_state:
    st.session_state["show_select_mode"] = False 
    
change = st.button("Select index from 0 to 9")
if change:
    st.session_state["change"] = ["0", "1", "2", "3", "4", "5", "6", "7", "9", "8"]

change2 = st.button("Deselect all")
if change2:
    st.session_state["change"] = []

disable_toggle = st.button("Toggle Treeview View Enable/Disable")
if disable_toggle:
    st.session_state["disable"] = not st.session_state["disable"]

st.warning(f"Treeview disable! Current set: {st.session_state['disable']}")

single_mode = st.button("Toggle Single Select True/False")
if single_mode:
    st.session_state["single_mode"] = not st.session_state["single_mode"]

st.warning(f"Treeview select_mode ! Current set: {st.session_state['single_mode']}")

show_select_mode = st.button("Toggle To Show Select Mode")
if show_select_mode:
    st.session_state["show_select_mode"] = not st.session_state["show_select_mode"]
with st.spinner():
   time.sleep(1)
   result = tree_independent_components(treeItems, checkItems=st.session_state["change"],disable=st.session_state['disable'], single_mode=st.session_state["single_mode"],show_select_mode=True, x_scroll=True, y_scroll=True, x_scroll_width=40, frameHeight=20, border=True)
   st.warning(result)
   try:
      st.write(sorted(result["setSelected"], key=int))
      #st.session_state["change"] = sorted(result["setSelected"], key=int)
   except:
      pass

