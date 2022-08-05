import streamlit as st
import base64


   
#             background-repeat: no-repeat;
#             background-size: 6% 10%;
#             background-position: right bottom;

import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file='milad-fakurian-nY14Fs8pxT8-unsplash.jpeg'):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://images.unsplash.com/photo-1547623641-d2c56c03e2a7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fGdyYWRpZW50JTIwYmFja2dyb3VuZHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60");
         }}
        [data-testid="stSidebar"] > div:first-child {{
          background: url("https://images.unsplash.com/photo-1547623641-d2c56c03e2a7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fGdyYWRpZW50JTIwYmFja2dyb3VuZHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60");
      }}
   
         </style>
         """,
         unsafe_allow_html=True
     )

def svg_to_html(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    svg_html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return svg_html
    
def flipside_logo(url="https://flipsidecrypto.xyz/"):
    svg = '<svg width="30" height="35" viewBox="0 0 76 80" fill="white" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M37.6274 80C34.584 79.9999 31.5925 79.212 28.9441 77.7136L8.69319 66.2436C6.06562 64.7709 3.87634 62.6273 2.34903 60.0323C0.821714 57.4372 0.0110999 54.4835 0 51.4729V28.5223C0.0110999 25.5117 0.821714 22.5579 2.34903 19.9629C3.87634 17.3678 6.06562 15.2247 8.69319 13.752L28.9441 2.28157C31.5953 0.786111 34.588 0 37.6323 0C40.6767 0 43.6694 0.786111 46.3206 2.28157L66.5715 13.752C69.1215 15.1993 71.2635 17.2679 72.798 19.7653L46.2211 35.0525C43.6452 36.5632 41.5016 38.711 39.9966 41.2891C38.4915 43.8671 37.6756 46.7889 37.6274 49.7732V80ZM75.2647 47.5271V51.503C75.2536 54.5135 74.443 57.4669 72.9156 60.0619C71.3883 62.6569 69.1991 64.8005 66.5715 66.2732L46.3206 77.7437C45.7556 78.0616 45.1746 78.3503 44.5799 78.6085V71.4916C44.6064 69.7139 45.0872 67.9725 45.9768 66.4329C46.8664 64.8933 48.1352 63.6064 49.6625 62.6948C57.2517 58.2816 64.8905 53.9678 72.4797 49.5645C73.4651 48.9669 74.397 48.2854 75.2647 47.5271ZM75.1155 26.3353C75.215 27.06 75.2649 27.7908 75.2647 28.5223V32.7267C75.2323 34.9476 74.6311 37.1231 73.5185 39.0458C72.4059 40.9685 70.8189 42.5741 68.9089 43.7099C61.3297 48.1132 53.6809 52.4272 46.0918 56.8305C45.5746 57.1486 45.0971 57.4865 44.5799 57.8245V49.8033C44.6082 48.0088 45.099 46.2516 46.005 44.7019C46.911 43.1523 48.2016 41.8623 49.7521 40.9566L75.1155 26.3353Z"></path></svg>'
    svg_html = svg_to_html(svg)
    st.sidebar.write(
        svg_html + f"&nbsp;&nbsp;&nbsp;{url}",
        unsafe_allow_html=True,
    )


def discord_logo(DISCORD_USERNAME):
    svg = '<svg focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="white" width="35" height="40" viewBox="0 0 32 32" aria-hidden="true"><path d="M13.647,14.907a1.4482,1.4482,0,1,0,1.326,1.443A1.385,1.385,0,0,0,13.647,14.907Zm4.745,0a1.4482,1.4482,0,1,0,1.326,1.443A1.385,1.385,0,0,0,18.392,14.907Z"></path><path d="M24.71,4H7.29A2.6714,2.6714,0,0,0,4.625,6.678V24.254A2.6714,2.6714,0,0,0,7.29,26.932H22.032l-.689-2.405,1.664,1.547L24.58,27.53,27.375,30V6.678A2.6714,2.6714,0,0,0,24.71,4ZM19.692,20.978s-.468-.559-.858-1.053a4.1021,4.1021,0,0,0,2.353-1.547,7.4391,7.4391,0,0,1-1.495.767,8.5564,8.5564,0,0,1-1.885.559,9.1068,9.1068,0,0,1-3.367-.013,10.9127,10.9127,0,0,1-1.911-.559,7.6184,7.6184,0,0,1-.949-.442c-.039-.026-.078-.039-.117-.065a.18.18,0,0,1-.052-.039c-.234-.13-.364-.221-.364-.221a4.0432,4.0432,0,0,0,2.275,1.534c-.39.494-.871,1.079-.871,1.079a4.7134,4.7134,0,0,1-3.965-1.976,17.409,17.409,0,0,1,1.872-7.579,6.4285,6.4285,0,0,1,3.653-1.365l.13.156a8.77,8.77,0,0,0-3.419,1.703s.286-.156.767-.377a9.7625,9.7625,0,0,1,2.951-.819,1.2808,1.2808,0,0,1,.221-.026,11,11,0,0,1,2.626-.026A10.5971,10.5971,0,0,1,21.2,11.917a8.6518,8.6518,0,0,0-3.237-1.651l.182-.208a6.4285,6.4285,0,0,1,3.653,1.365,17.409,17.409,0,0,1,1.872,7.579A4.752,4.752,0,0,1,19.692,20.978Z"></path></svg>'
    svg_html = svg_to_html(svg)
    st.sidebar.write(
        svg_html + f"&nbsp;&nbsp;&nbsp;{DISCORD_USERNAME}", unsafe_allow_html=True
    )
