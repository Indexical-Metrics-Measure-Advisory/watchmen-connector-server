

def hide_streamlit_style(streamlit):
	hide_streamlit_style = """
		            <style>
		            #MainMenu {visibility: hidden;}
		            footer {visibility: hidden;}
		            </style>
		            """
	streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)


def build_condition_bar(st):
	with st.sidebar:
		st.header(' Conditions :')

		checkbox = st.checkbox("By Month")

		year = st.selectbox('Year', reversed(range(2000, 2023)))
		if checkbox:
			month = st.selectbox('Month', range(1, 13))



	if checkbox:
		filters = [
			{
				"factor": "year",
				"operator": "equals",
				"value": year
			},
			{
				"factor": "month",
				"operator": "equals",
				"value": month
			},

		]
	else:
		filters = [
			{
				"factor": "year",
				"operator": "equals",
				"value": year
			}

		]




	return filters

