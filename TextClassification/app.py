from textblob import TextBlob
import pandas as pd
import streamlit as st
import cleantext

st.header(' Sentiment Analysis')
with st.expander('Analyze Text'):
	text=st.text_input('Text Here')
	if text:
		blob=TextBlob(text)
		st.write('Polarity',round(blob.sentiment.polarity,2))
		st.write('Subjectivity',round(blob.sentiment.subjectivity,2))
		pre=st.text_input('Clean Text:')
		if pre:
			st.write(cleantext.clean(pre,clean_all=False,extra_spaces=True,stopwords=True,lowercase=True,numbers=True,punct=True))
with st.expander('Analyze CSV'): 
	file=st.file_uploader('Upload file')
	def score(x):
		a=TextBlob(x)
		return a.sentiment.polarity
	def analyze(x):
		if x>=0.5:
			return "positive"
		elif x<=-0.5:
			return 'Negative'
		else:
			return 'neutral'
	if file:
		df=pd.read_csv(file)
		del df['Unamed: 0']
		df['Score']=df['tweets'].apply(score)
		df['analysis']=df['Score'].apply(analyze)
		st.write(df.head())
		@st.cache
		def convert_df(df):
			return df.to_csv().encode('utf-8')
		csv=convert_df(df)
		st.download_button(
			label='Download data as CSV',
			dat=csv,
			file_name='sentiment.csv',
			mime='text/csv',
			)


