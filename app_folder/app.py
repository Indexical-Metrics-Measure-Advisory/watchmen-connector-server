import sys

import pandas
import plotly.express as px
from client.achievement.watchmen_achievement_client import WatchmenStreamlitClient
from client.index import WatchmenClient
from plotly import graph_objects as go

from connect_server import streamlit as st
from connect_server.utils.utils import hide_streamlit_style, get_most_covered_index

achievement_id =sys.argv[1]

client = WatchmenStreamlitClient(WatchmenClient(token="0Z6ag50cdIPamBIgf8KfoQ"))
client.init(achievement_id)
# global_filters = build_condition_bar(st)
hide_streamlit_style(st)

with st.sidebar:
	st.header(' Conditions :')

	checkbox = st.checkbox("By Month")

	year = st.selectbox('Year', reversed(range(2000, 2023)))
	if checkbox:
		month = st.selectbox('Month', range(1, 13))

	if checkbox:
		global_filters = [
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
		global_filters = [
			{
				"factor": "year",
				"operator": "equals",
				"value": year
			}

		]
	promo_code = st.radio(
		"Select Your Promotion Code",
		('promo_code A', 'promo_code B'))

	section_filters = global_filters + [{
		"factor": "promotion code",
		"operator": "equals",
		"value": promo_code
	}]

st.title('Promotion Event and Customer Analysis')

st.markdown('### indicators for analysis')

# promo_code = st.radio(
# 	"Select Your Promotion Code",
# 	('promo_code A', 'promo_code B'))
#
#
# section_filters = global_filters+[{
# 				"factor": "promotion code",
# 				"operator": "equals",
# 				"value": promo_code
# 			}]


col1, col2, col3 = st.columns(3)

number_of_leads = client.load_indicator_value_by_name("number of leads", "count", section_filters)

number_of_quotations = client.load_indicator_value_by_name("number of quotation", "count", section_filters)

number_of_policy = client.load_indicator_value_by_name("number of Policy", "count", section_filters)
# print("number_of_policy",number_of_policy)

sum_annual_amt = client.load_indicator_value_by_name("annual amount", "sum", section_filters)

if number_of_quotations != 0 and number_of_leads != 0:
	rate_quota = (number_of_quotations / number_of_leads) * 100
else:
	rate_quota = 0

if number_of_policy != 0 and number_of_quotations != 0:
	rate_policy = (number_of_policy / number_of_quotations) * 100
else:
	rate_policy = 0

with col1:
	st.metric(label="Leads to Quotation Rate", value="{:.2f}%".format(rate_quota),
	          help="Measure the number of formal leads sent compared to the number of quotation .")

with col2:
	st.metric(label="Quotation to Policy Rate",
	          help="Measure the number of formal quotes sent compared to the number of deals closed."
	          , value="{:.2f}%".format(rate_policy))

with col3:
	st.metric(label="Annual Amount", value="{:,}".format(sum_annual_amt))

st.subheader('Conversion Rate Funnel for promotion code')

promo_code_list = st.multiselect("Add Promotion Code for Funnel",
                                 ('promo_code A', 'promo_code B'))

if promo_code_list:
	fig = go.Figure()
	for funnal_promo_code in promo_code_list:
		section_filters = global_filters + [{
			"factor": "promotion code",
			"operator": "equals",
			"value": funnal_promo_code
		}]

		number_of_leads = client.load_indicator_value_by_name("number of leads", "count", section_filters)
		number_of_quotations = client.load_indicator_value_by_name("number of quotation", "count", section_filters)
		number_of_policy = client.load_indicator_value_by_name("number of Policy", "count", section_filters)
		fig.add_trace(go.Funnel(
			name=funnal_promo_code,
			y=["Leads", "Quotation", "Policy Issued"],
			x=[number_of_leads, number_of_quotations, number_of_policy],
			textinfo="value+percent initial"))
	st.plotly_chart(fig, use_container_width=True)
else:
	st.write(f"⏳ Please select promotion code first")

with st.container():
	st.subheader('Proportion of new and old customers: ')

	policy_df = client.load_dataset("policy count by is new customer")
	quotation_df = client.load_dataset("quotation count by is new customer")
	lead_df = client.load_dataset("leads count by is new customer")

	##TODO  add date filter

	data_df = pandas.concat([lead_df, quotation_df, policy_df])

	fig2 = px.bar(data_df, x="status", y="count", color="is new customer",
	              title="Distribution of new and old customers")

	st.plotly_chart(fig2, use_container_width=True)

with st.container():
	policy_customer_df = client.load_dataset("policy customer dataset")

	##TODO  add date filter
	st.markdown('### Compare the attributes of new and old customers through different dimensions')
	st.markdown('##### Gender distribution of  customers ')
	col1, col2 = st.columns(2)

	filter_by_promotion_code_and_new_df = policy_customer_df[
		(policy_customer_df["promotion code"] == promo_code) & (policy_customer_df["is new customer"] == 1)]

	filter_by_promotion_code_and_old_df = policy_customer_df[
		(policy_customer_df["promotion code"] == promo_code) & (policy_customer_df["is new customer"] == 0)]

	with col1:
		marriage_new_df = filter_by_promotion_code_and_new_df.groupby(['sex']).size().reset_index(name='counts')

		marriage_new_df = marriage_new_df.sort_values(
			by="sex",
			ascending=False)
		labels = list(marriage_new_df["sex"])
		values = list(marriage_new_df["counts"])
		fig = go.Figure(
			data=[go.Pie(labels=labels, values=values, direction='clockwise', sort=False, title="New Customer")])
		st.plotly_chart(fig, use_container_width=True)
	with col2:
		marriage_new_df = filter_by_promotion_code_and_old_df.groupby(['sex']).size().reset_index(name='counts')
		marriage_new_df = marriage_new_df.sort_values(
			by="sex",
			ascending=False)
		labels = list(marriage_new_df["sex"])

		values = list(marriage_new_df["counts"])
		fig = go.Figure(
			data=[go.Pie(labels=labels, values=values, direction='clockwise', sort=False, title="Old Customer")])
		st.plotly_chart(fig, use_container_width=True)

	st.markdown('##### Age distribution of customers ')

	col1, col2 = st.columns(2)

	with col1:
		bins = [0, 5, 14, 24, 34, 44, 54, 120]
		labels = ["0-5", "5-14", "14-24", "24-34", "34-44", "44-54", ">=55"]
		filter_by_promotion_code_and_new_df['binned'] = pandas.cut(filter_by_promotion_code_and_new_df['age'],
		                                                           bins=bins, labels=labels)
		age_new_df = filter_by_promotion_code_and_new_df.groupby(['binned']).size().reset_index(name='counts')
		age_new_df = age_new_df[age_new_df['counts'] != 0]

		age_new_df = age_new_df.sort_values(
			by="binned",
			ascending=False)
		labels = list(age_new_df["binned"])
		values = list(age_new_df["counts"])

		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="New Customer")])
		st.plotly_chart(fig, use_container_width=True)
	with col2:
		bins = [0, 5, 14, 24, 34, 44, 54, 120]
		labels = ["0-5", "5-14", "14-24", "24-34", "34-44", "44-54", ">=55"]
		filter_by_promotion_code_and_old_df['binned'] = pandas.cut(filter_by_promotion_code_and_old_df['age'],
		                                                           bins=bins, labels=labels)
		age_old_df = filter_by_promotion_code_and_old_df.groupby(['binned']).size().reset_index(name='counts')
		age_old_df = age_old_df[age_old_df['counts'] != 0]
		age_old_df = age_old_df.sort_values(
			by="binned",
			ascending=False)
		labels = list(age_old_df["binned"])
		# print(labels)
		values = list(age_old_df["counts"])

		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="Old Customer")])

		st.plotly_chart(fig, use_container_width=True)

	print(age_old_df.compare(age_new_df))

	st.markdown('#### Sale mode distribution of  customers  ')
	col1, col2 = st.columns(2)

	with col1:
		marriage_new_df = filter_by_promotion_code_and_new_df.groupby(['sale mode']).size().reset_index(name='counts')
		labels = list(marriage_new_df["sale mode"])
		values = list(marriage_new_df["counts"])

		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="New Customer")])
		st.plotly_chart(fig, use_container_width=True)
	with col2:
		marriage_new_df = filter_by_promotion_code_and_old_df.groupby(['sale mode']).size().reset_index(name='counts')
		labels = list(marriage_new_df["sale mode"])
		values = list(marriage_new_df["counts"])
		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="Old Customer")])
		st.plotly_chart(fig, use_container_width=True)

	st.markdown('#### Marriage distribution of  customers  ')
	col1, col2 = st.columns(2)

	with col1:
		marriage_new_df = filter_by_promotion_code_and_new_df.groupby(['marriage']).size().reset_index(name='counts')
		labels = list(marriage_new_df["marriage"])
		values = list(marriage_new_df["counts"])
		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="New Customer")])
		st.plotly_chart(fig, use_container_width=True)
	with col2:
		marriage_old_df = filter_by_promotion_code_and_old_df.groupby(['marriage']).size().reset_index(name='counts')
		labels = list(marriage_old_df["marriage"])
		values = list(marriage_old_df["counts"])
		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="Old Customer")])
		st.plotly_chart(fig, use_container_width=True)

	st.markdown('#### Anuual income distribution of  customers  ')
	col1, col2 = st.columns(2)

	with col1:
		bins = [0, 126000, 252000, 378000, 504000, 756000, 1000000000]
		labels = ["0-126000", "126000-252000", "252000-378000", "378000-504000", "504000-756000", ">=756000"]
		filter_by_promotion_code_and_new_df['binned'] = pandas.cut(filter_by_promotion_code_and_new_df['annual income'],
		                                                           bins=bins, labels=labels)
		anul_income_new_df = filter_by_promotion_code_and_new_df.groupby(['binned']).size().reset_index(name='counts')
		anul_income_new_df = anul_income_new_df[anul_income_new_df['counts'] != 0]

		anul_income_new_df = anul_income_new_df.sort_values(
			by="binned",
			ascending=False)
		labels = list(anul_income_new_df["binned"])
		values = list(anul_income_new_df["counts"])

		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="New Customer")])
		st.plotly_chart(fig, use_container_width=True)
	with col2:
		bins = [0, 126000, 252000, 378000, 504000, 756000, 1000000000]
		labels = ["0-126000", "126000-252000", "252000-378000", "378000-504000", "504000-756000", ">=756000"]
		filter_by_promotion_code_and_old_df['binned'] = pandas.cut(filter_by_promotion_code_and_old_df['annual income'],
		                                                           bins=bins, labels=labels)

		anual_income_old_df = filter_by_promotion_code_and_old_df.groupby(['binned']).size().reset_index(name='counts')
		anual_income_old_df = anual_income_old_df[anual_income_old_df['counts'] != 0]
		anual_income_old_df = anual_income_old_df.sort_values(
			by="binned",
			ascending=False)
		labels = list(anual_income_old_df["binned"])
		values = list(anual_income_old_df["counts"])
		fig = go.Figure(data=[go.Pie(labels=labels, values=values, sort=False, title="Old Customer")])
		st.plotly_chart(fig, use_container_width=True)

#
# with st.container:
st.markdown("### User Profile for {}".format(promo_code))

age_binned = age_new_df.append(age_old_df).groupby('binned').sum().sort_values(
	by="counts",
	ascending=False)
sum_counts = age_binned['counts'].sum()


st.markdown("- Most users are in {} age ranges".format(",".join(get_most_covered_index(sum_counts,age_binned,[]))))

anual_income = anul_income_new_df.append(anual_income_old_df)
df2 = anual_income.groupby('binned').sum().sort_values(
	by="counts",
	ascending=False)
sum_counts = df2['counts'].sum()


st.markdown("- The income range of most users is {}".format(",".join(get_most_covered_index(sum_counts,df2,[]))))


annual_income_med = filter_by_promotion_code_and_new_df["annual income"].median()

st.markdown("- The median annual income is {}".format(annual_income_med))

annual_income_avg = 21200*12

st.markdown("- The rate median annual income and HK average annual wages is {:.2f}%".format((annual_income_med/annual_income_avg)*100))

annual_amt_med = filter_by_promotion_code_and_new_df["annual amt"].median()

st.markdown("- The rate median annual income and annual premium  is {:.2f}%".format((annual_amt_med/annual_income_med)*100))
