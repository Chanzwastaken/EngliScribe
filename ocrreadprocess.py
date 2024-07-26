import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import datetime
from PIL import Image
import time
import os
from collections import Counter

def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def analyze_read(image_bytes_data):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # For how to obtain the endpoint and key, please see PREREQUISITES above.
    endpoint = os.environ.get('DOCUMENTINTELLIGENCE_ENDPOINT')
    key = os.environ.get('DOCUMENTINTELLIGENCE_API_KEY')

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(bytes_source=image_bytes_data),
        features=[DocumentAnalysisFeature.LANGUAGES]
    )       
    
    result: AnalyzeResult = poller.result()
    
    # st.write("HASIL OCR")
    # st.write()

    # [START analyze_read]
    # Detect languages.
    
    if result.languages is not None:
        print("----Languages detected in the document----")
        list_of_languages = []
        for language in result.languages:
            print(f"Language code: '{language.locale}' with confidence {language.confidence}")
            list_of_languages.append(language.locale)
        counter = Counter(list_of_languages)
        most_lang = counter.most_common(1)[0][0]
        print("Language: ", most_lang)

    
    # To learn the detailed concept of "bounding polygon" in the following content, visit: https://aka.ms/bounding-region
    # Analyze pages.
    
    for page in result.pages:
        print(f"----Analyzing document from page #{page.page_number}----")
        # print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        # Analyze lines.
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                # print(
                #     f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
                # )

                # Analyze words.
                # for word in words:
                    # print(f"......Word '{word.content}' has a confidence of {word.confidence}")
        
    # Analyze paragraphs.
    if result.paragraphs:
        print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
        list_of_paragraphs = []
        for paragraph in result.paragraphs:
            list_of_paragraphs.append(paragraph.content)
            # print(f"Found paragraph within {paragraph.bounding_regions} bounding region")
            # print(f"...with content: '{paragraph.content}'")
            # print(f"Isi paragraf: '{paragraph.content}'\n")
            # st.write("Isi paragraf: ", paragraph.content)
    return list_of_paragraphs, most_lang