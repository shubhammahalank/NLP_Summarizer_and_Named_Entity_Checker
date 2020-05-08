import streamlit as st

# NLP
import spacy
nlp = spacy.load('en')
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

# Summary Packages
from gensim.summarization import summarize

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

# @st.cache(allow_output_mutation=True)
def analyze_text(text):
	return nlp(text)

# Web scrapping Packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

def main():


	st.title("Summary and Entity Checker")

	activities = ["Summarize", "NER Checker", "NER for URL"]
	choice = st.sidebar.selectbox("Select Activity",activities)

	if choice == "Summarize":
		st.subheader("Summary with NLP")
		raw_text = st.text_area("Enter Text Here","Type Here")
		summary_coice = st.selectbox("Summary Choice",("Genism","Sumy Lex Rank"))
		if st.button("Summarize"):
			if summary_coice == "Genism":
				summary_result = summarize(raw_text)
			elif summary_coice == "Sumy Lex Rank":
				summary_result = sumy_summarizer(raw_text)


			st.write(summary_result)


	if choice == "NER Checker":
		st.subheader("Entity Recognition with SpaCy")
		raw_text = st.text_area("Enter Text Here","Type Here")
		if st.button("Analyze"):
			docx = analyze_text(raw_text)
			html = displacy.render(docx,style='ent')
			html = html.replace("\n\n","\n")
			# st.write(html,unsafe_allow_html=True)
			st.markdown(html,unsafe_allow_html=True)

	if choice =="NER for URL":
		st.subheader("Analyze text from URL")
		raw_url = st.text_input("Enter URL","Type Here")
		text_length = st.slider("Length to preview:",50,100)
		if st.button("Extract"):
			if raw_url != "Type Here":
				result = get_text(raw_url)
				len_of_full_text = len(result)
				len_of_short_text = round(len(result)/text_length)
				st.info("Length::Full Text::{}".format(len_of_full_text))
				st.info("Length::Short Text::{}".format(len_of_short_text))
				st.write(result[:len_of_short_text])

				summary_docx = sumy_summarizer(result)
				docx = analyze_text(summary_docx)
				html = displacy.render(docx,style='ent')
				html = html.replace("\n\n","\n")
				# st.write(html,unsafe_allow_html=True)
				st.markdown(html,unsafe_allow_html=True)







if __name__ == '__main__':
	main()
