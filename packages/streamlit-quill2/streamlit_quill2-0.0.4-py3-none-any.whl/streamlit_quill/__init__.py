import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _st_quill = components.declare_component("streamlit_quill", url="http://localhost:3001")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_quill = components.declare_component("streamlit_quill", path=build_dir)


def st_quill(
    value="",
    placeholder="",
    html=False,
    toolbar=None,
    history=None,
    preserve_whitespace=True,
    readonly=False,
    key=None
):
    """Quill Editor component.

    Parameters
    ----------
    value : any
        The text value of this widget when it first renders. This will be
        cast to str internally.
    placeholder : any
        The text value of this widget when the editor is empty. It will be
        cast to str internally.
    html : bool
        Choose whether component return editor's content as HTML or regular
        text. Return regular text by default.
    toolbar : list or None
        Quill toolbar configuration. For more information, see
        https://quilljs.com/docs/modules/toolbar/.
    history : dict or None
        Quill history configuration. For more information, see
        https://quilljs.com/docs/modules/history/.
    preserve_whitespace : bool
        Choose whether multiple spaces are preserved on copy/paste or trimmed.
        Spaces are preserved by default.
    readonly : bool
        Make the editor read only.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    str
        The current content of Quill editor.

    """
    if toolbar is None:
        toolbar=[
            [
                "bold", "italic", "underline", "strike",
                {"script": "sub"},
                {"script": "super"},
            ],
            [
                {"background": []},
                {"color": [] },
            ],          
            [
                {"list": "ordered"},
                {"list": "bullet"},
                {"indent": "-1"},
                {"indent": "+1"},
                {"align": []},
            ],
            [
                {"header": 1},
                {"header": 2},
                {"header": [1, 2, 3, 4, 5, 6, False]},
                {"size": ["small", False, "large", "huge"]},
            ],
            [
                "blockquote", "code", "code-block", "clean"
            ],
            [
                "link", "image"
            ],
            [
                {"font": []}
            ],
        ]
    
    if history is None:
        history={
            "delay": 1000,
            "maxStack": 500,
            "userOnly": False
        }

    return _st_quill(
        defaultValue=str(value),
        placeholder=str(placeholder),
        html=html,
        toolbar=toolbar,
        history=history,
        preserveWhitespace=preserve_whitespace,
        readOnly=readonly or False,
        name=key or "quill",
        key=key,
        default=str(value),
    )


if not _RELEASE:
  import streamlit as st

  st.sidebar.title(":computer: Quill Editor")
  placeholder = st.sidebar.text_input("Placeholder", "Type some content...", placeholder="Type some content...")
  test_html = ""
  html = st.sidebar.checkbox("Return HTML", False)
  read_only = st.sidebar.checkbox("Read only", False)

  
  if "edit_mode" not in st.session_state:
      st.session_state.edit_mode = False
  
  if "test_html" not in st.session_state:
      st.session_state.test_html = test_html

  def handle_edit_click():
      if st.session_state.edit_mode == bool(True):
          st.session_state.edit_mode = False
      else:
          st.session_state.edit_mode = True
  
  def handle_save_click(data):
      if st.session_state.edit_mode == bool(True):
          st.session_state.edit_mode = False
          st.session_state.test_html = data
          

  if st.session_state.edit_mode == bool(False):
    edit_button = st.button("Edit" , key="edit_button", on_click=handle_edit_click)

  if st.session_state.edit_mode == bool(True):
      content = st_quill(
        placeholder=placeholder,
        html=html,
        readonly=read_only,
        value=st.session_state.test_html,
      )
      save_button = st.button("Save" , key="save_button", on_click=handle_save_click, args=(content,))
  else:
      st.html(st.session_state.test_html)

else:
    import streamlit as st

    st.sidebar.title(":computer: Quill Editor")
    placeholder = st.sidebar.text_input("Placeholder", "Type some content...", placeholder="Type some content...")
    test_html = ""
    html = st.sidebar.checkbox("Return HTML", False)
    read_only = st.sidebar.checkbox("Read only", False)

    
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    
    if "test_html" not in st.session_state:
        st.session_state.test_html = test_html

    def handle_edit_click():
        if st.session_state.edit_mode == bool(True):
            st.session_state.edit_mode = False
        else:
            st.session_state.edit_mode = True
    
    def handle_save_click(data):
        if st.session_state.edit_mode == bool(True):
            st.session_state.edit_mode = False
            st.session_state.test_html = data
            

    if st.session_state.edit_mode == bool(False):
      edit_button = st.button("Edit" , key="edit_button", on_click=handle_edit_click)

    if st.session_state.edit_mode == bool(True):
        content = st_quill(
          placeholder=placeholder,
          html=html,
          readonly=read_only,
          value=st.session_state.test_html,
        )
        save_button = st.button("Save" , key="save_button", on_click=handle_save_click, args=(content,))
    else:
        st.html(st.session_state.test_html)
        st.write(st.session_state.test_html)
