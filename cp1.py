import os
import streamlit as st
from openai import OpenAI
import requests

st.markdown(
    """
        
		<!-- Favicon -->
        <link rel="icon" href="https://www.cancepro.com/img/favicon.png">

		<!-- Google Fonts -->
		<link href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap" rel="stylesheet">

		<!-- Bootstrap CSS -->
		<link rel="stylesheet" href="https://www.cancepro.com/css/bootstrap.min.css">
		<!-- Nice Select CSS -->
		<link rel="stylesheet" href="https://www.cancepro.com/css/nice-select.css">
		<!-- Font Awesome CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/font-awesome.min.css">
		<!-- icofont CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/icofont.css">
		<!-- Slicknav -->
		<link rel="stylesheet" href="https://www.cancepro.com/css/slicknav.min.css">
		<!-- Owl Carousel CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/owl-carousel.css">
		<!-- Datepicker CSS -->
		<link rel="stylesheet" href="https://www.cancepro.com/css/datepicker.css">
		<!-- Animate CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/animate.min.css">
		<!-- Magnific Popup CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/magnific-popup.css">

		<!-- Medipro CSS -->
        <link rel="stylesheet" href="https://www.cancepro.com/css/normalize.css">
        <link rel="stylesheet" href="https://www.cancepro.com/style.css">
        <link rel="stylesheet" href="https://www.cancepro.com/css/responsive.css">


    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden !important;}
    footer, .stFooter {display: none !important;}
    div._container_gzau3_1 {display:none !important;}
    div._profileContainer_gzau3_53 {display:none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <script>
    const footer = document.querySelector('footer');
    if (footer) {
        footer.style.display = 'none';
    }
    </script>
    """,
    unsafe_allow_html=True
)

response = requests.get('https://canceproit.pythonanywhere.com/ttthais')
data = response.json()
take_this = data[0]


st.markdown(
    """
        <!-- Header Area -->
		<header class="header" id="header">
			<!-- Header Inner -->
			<div class="header-inner">
				<div class="container">
					<div class="inner">
						<div class="row">
							<div class="col-lg-5 col-md-3 col-12">
								<!-- Start Logo -->
								<div class="logo">
									<a href="index.html"><img src="https://www.cancepro.com/img/icon/CancePro_Icon.png" alt="#"></a>
								</div>
								<!-- End Logo -->
								<!-- Mobile Nav -->
								<div class="mobile-nav"></div>
								<!-- End Mobile Nav -->
							</div>
							<div class="col-lg-7 col-md-9 col-12">
								<!-- Main Menu -->
								<div class="main-menu">
									<nav class="navigation">
										<ul class="nav menu" style="float: right;">
											<li><a href="https://www.cancepro.com">Go Home</a></li>
											<li><a href="https://canceproit.pythonanywhere.com/">Ask Me </a></li>
											<li><a href="https://canceproit.pythonanywhere.com/getxray">X-Ray Analysis</a></li>
											<li><a href="https://canceproit.pythonanywhere.com/getliveanalysis">Cancer Records</a></li>
										</ul>
									</nav>
								</div>
								<!--/ End Main Menu -->
							</div>
						</div>
					</div>
				</div>
			</div>
			<!--/ End Header Inner -->
		</header>
		<!-- End Header Area -->
    """,
    unsafe_allow_html=True
)

# Show title and description.
st.title("CancePro")
st.write(
    "Our information relies on well known Cancer research institutes research documents that are publicly available. Ask a question in the below box, get relevant information."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# Setting the API key

# st.write(
#     "Has environment variables been set:",
#     os.environ["OPENAI_API_KEY"] == st.secrets["abcd_keyyy"]
# )
# st.write(st.secrets["abcd_keyyy"])
os.environ["OPENAI_API_KEY"] = take_this
api_key = take_this


# Create an OpenAI client.
client = OpenAI()

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


st.markdown(
    """
        <!-- Footer Area -->
		<footer id="footer" class="footer ">
			<!-- Footer Top -->
			<!--/ End Footer Top -->
			<!-- Copyright -->
			<div class="copyright">
				<div class="container">
					<div class="row">
						<div class="col-lg-12 col-md-12 col-12">
							<div class="copyright-content">
								<p> © Copyright 2024  |  All Rights Reserved by <a href="#header">cancepro.com</a> </p>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!--/ End Copyright -->
		</footer>
		<!--/ End Footer Area -->
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
        <!-- jquery Min JS -->
        <script src="https://www.cancepro.com/js/jquery.min.js"></script>
		<!-- jquery Migrate JS -->
		<script src="https://www.cancepro.com/js/jquery-migrate-3.0.0.js"></script>
		<!-- jquery Ui JS -->
		<script src="https://www.cancepro.com/js/jquery-ui.min.js"></script>
		<!-- Easing JS -->
        <script src="https://www.cancepro.com/js/easing.js"></script>
		<!-- Color JS -->
		<script src="https://www.cancepro.com/js/colors.js"></script>
		<!-- Popper JS -->
		<script src="https://www.cancepro.com/js/popper.min.js"></script>
		<!-- Bootstrap Datepicker JS -->
		<script src="https://www.cancepro.com/js/bootstrap-datepicker.js"></script>
		<!-- Jquery Nav JS -->
        <script src="https://www.cancepro.com/js/jquery.nav.js"></script>
		<!-- Slicknav JS -->
		<script src="https://www.cancepro.com/js/slicknav.min.js"></script>
		<!-- ScrollUp JS -->
        <script src="https://www.cancepro.com/js/jquery.scrollUp.min.js"></script>
		<!-- Niceselect JS -->
		<script src="https://www.cancepro.com/js/niceselect.js"></script>
		<!-- Tilt Jquery JS -->
		<script src="https://www.cancepro.com/js/tilt.jquery.min.js"></script>
		<!-- Owl Carousel JS -->
        <script src="https://www.cancepro.com/js/owl-carousel.js"></script>
		<!-- counterup JS -->
		<script src="https://www.cancepro.com/js/jquery.counterup.min.js"></script>
		<!-- Steller JS -->
		<script src="https://www.cancepro.com/js/steller.js"></script>
		<!-- Wow JS -->
		<script src="https://www.cancepro.com/js/wow.min.js"></script>
		<!-- Magnific Popup JS -->
		<script src="https://www.cancepro.com/js/jquery.magnific-popup.min.js"></script>
		<!-- Counter Up CDN JS -->
		<script src="http://cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js"></script>
		<!-- Bootstrap JS -->
		<script src="https://www.cancepro.com/js/bootstrap.min.js"></script>
		<!-- Main JS -->
		<script src="https://www.cancepro.com/js/main.js"></script>
    """,
    unsafe_allow_html=True
)
