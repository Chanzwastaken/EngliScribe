import os 
from spell_checker_script import preprocess_data
# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
# key = os.environ.get('LANGUAGE_KEY')
# endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential

# # Authenticate the client using your key and endpoint 
# def authenticate_client():
#     ta_credential = AzureKeyCredential(key)
#     text_analytics_client = TextAnalyticsClient(
#             endpoint=endpoint, 
#             credential=ta_credential)
#     return text_analytics_client

# client = authenticate_client()

# # Example method for summarizing text
# def sample_extractive_summarization(client, text):
#     from azure.core.credentials import AzureKeyCredential
#     from azure.ai.textanalytics import (
#         TextAnalyticsClient,
#         ExtractiveSummaryAction
#     ) 

#     # paragraphs = text.split('\n')
#     # paragraphs = [p for p in paragraphs if p.strip()]
#     # print(paragraphs)
#     print("text awal:", text)
#     whole_text = []
#     whole_text.append(text)

#     document = [
#         "The extractive summarization feature uses natural language processing techniques to locate key sentences in an unstructured text document. "
#         "These sentences collectively convey the main idea of the document. This feature is provided as an API for developers. " 
#         "They can use it to build intelligent solutions based on the relevant information extracted to support various use cases. "
#         "Extractive summarization supports several languages. It is based on pretrained multilingual transformer models, part of our quest for holistic representations. "
#         "It draws its strength from transfer learning across monolingual and harness the shared nature of languages to produce models of improved quality and efficiency. "
#     ]

#     poller = client.begin_analyze_actions(
#         whole_text,
#         actions=[
#             ExtractiveSummaryAction(max_sentence_count=4)
#         ],
#     )

#     document_results = poller.result()
#     for result in document_results:
#         extract_summary_result = result[0]  # first document, first result
#         print("extract_summary_result:", extract_summary_result)
#         if extract_summary_result.is_error:
#             print("...Is an error with code '{}' and message '{}'".format(
#                 extract_summary_result.code, extract_summary_result.message
#             ))
#         else:
#             # print("Summary extracted: \n{}".format(
#             #     " ".join([sentence.text for sentence in extract_summary_result.sentences]))
#             # )
#             summarized_paragraphs = extract_summary_result.sentences
#             print(summarized_paragraphs)
#             return summarized_paragraphs

# def start_summarizing(text):
#     key = os.environ.get('LANGUAGE_KEY')
#     endpoint = os.environ.get('LANGUAGE_ENDPOINT')
#     client = authenticate_client()
#     summarization_result = sample_extractive_summarization(client, text)
#     return summarization_result


def sample_extractive_summarization(text):
    # [START extract_summary]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    key = os.environ.get('LANGUAGE_KEY')
    endpoint = os.environ.get('LANGUAGE_ENDPOINT')

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    preprocessed_data = preprocess_data(text)
    splitted_ori_text = preprocessed_data.split()
    splitted_ori_text_len = len(splitted_ori_text)

    document = [text]

    poller = text_analytics_client.begin_extract_summary(document)
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.kind == "ExtractiveSummarization":
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in result.sentences]))
            )
            final_summarized_text = " ".join([sentence.text for sentence in result.sentences])
            
            preprocessed_data_summarized_text = preprocess_data(final_summarized_text)
            splitted_summarized_text = preprocessed_data_summarized_text.split()
            splitted_summarized_text_len = len(splitted_summarized_text)

            return final_summarized_text, splitted_ori_text_len, splitted_summarized_text_len
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))
    # [END extract_summary]


def start_summarizing(text):
    key = os.environ.get('LANGUAGE_KEY')
    endpoint = os.environ.get('LANGUAGE_ENDPOINT')
    summarization_result, ori_text_len, summarized_text_len = sample_extractive_summarization(text)
    percentage_of_loss = ((ori_text_len - summarized_text_len)/ori_text_len) * 100
    count_removed_words = ori_text_len - summarized_text_len
    return summarization_result, ori_text_len, summarized_text_len, percentage_of_loss, count_removed_words