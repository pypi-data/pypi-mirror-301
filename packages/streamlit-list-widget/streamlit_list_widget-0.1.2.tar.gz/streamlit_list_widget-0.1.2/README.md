# streamlit-list-widget
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-list-widget-component.streamlit.app/)

Streamlit component that allows you to create a list of clickable items.

## Installation instructions

```sh
pip install streamlit-list-widget
```

## Usage instructions

```python
import streamlit as st

from streamlit_list_widget import streamlit_list_widget

images = {
    "Golden Retriever": "https://www.zooplus.it/magazine/wp-content/uploads/2017/05/fotolia_66749097.jpg",
    "Labrador": "https://www.tuttogreen.it/wp-content/uploads/2019/03/shutterstock_1212827962.jpg",
    "Pomerania": "https://www.purina.it/sites/default/files/2021-02/BREED%20Hero_0095_pomeranian.jpg",
    "Alberto": "https://m.media-amazon.com/images/I/61k4ead-zGL._AC_UF350,350_QL80_.jpg",
}

with st.sidebar:
    selected = streamlit_list_widget(items=list(images.keys()), title="Dogs")

if selected:
    st.title(selected)
    st.image(images[selected], caption=selected)
```
