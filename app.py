import traceback
import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify, url_for, Response
import io
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest
import ocrreadprocess
from spell_checker_script import correction_and_accuracy, highlighting_words
from video_indexer_api import video_indexer_insights
import text_summarization_script
from text_summarization_script import start_summarizing
from phi3_dev import user_chat
import cv2
from datetime import datetime

app = Flask(__name__)

load_dotenv()

@app.route('/')
def index():
	'Show the index page'
	return render_template('index.html')

@app.route('/login')
def login_page():
	'Show the index page'
	return render_template('login.html')

@app.route('/test')
def testpage():
	'Show the test page'
	return render_template('test.html')

@app.route('/index3')
def index3():
	'Show the index3 page'
	return render_template('index3.html')

@app.route('/index4')
def index4():
	'Show the index4 page'
	return render_template('index4.html')

@app.route('/options')
def options():
	'Show the options page'
	return render_template('options.html')

@app.route('/ocr')
def ocr():
	'Show the ocr page'
	return render_template('ocr.html')

# @app.route('/ocr', methods=['POST'])
# def ocr_post():
# 	image = request.form['image']
# 	text_result = analyze_read(image)
# 	return render_template(
#         'results.html',
#         result_paragraph=text_result
#     )

@app.route('/result_ocr_upload', methods=['POST'])
def result_ocr_upload():
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        # Read the image in bytes
        image_bytes = io.BytesIO(file.read()).getvalue()
        text_result, most_lang = ocrreadprocess.analyze_read(image_bytes)
        # Process the image bytes (example: just returning the size)
        # image_bytes.seek(0, io.SEEK_END)
        # size = image_bytes.tell()
        # return f"Image uploaded and processed. Size: {size} bytes"
        # print(text_result)
        
        # return jsonify({"message": "Image uploaded and processed", "test": text_result})
        # return "Success", 200
		
		# backup code
        combined_paragraph = "\n".join(text_result)
        # print(combined_paragraph)
        # return render_template('results.html', result_paragraph = combined_paragraph, most_lang = most_lang)
		
        return render_template('results.html', result_paragraph = text_result, most_lang = most_lang, combined_paragraph = combined_paragraph)
    
    return jsonify({"error": "File upload failed"}), 400

@app.route('/GetTokenAndSubdomain', methods=['GET'])
def getTokenAndSubdomain():
	'Get the access token'
	if request.method == 'GET':
		try:
			headers = { 'content-type': 'application/x-www-form-urlencoded' }
			data = {
				'client_id': str(os.environ.get('CLIENT_ID')),
				'client_secret': str(os.environ.get('CLIENT_SECRET')),
				'resource': 'https://cognitiveservices.azure.com/',
				'grant_type': 'client_credentials'
			}

			resp = requests.post('https://login.windows.net/' + str(os.environ.get('TENANT_ID')) + '/oauth2/token', data=data, headers=headers)
			jsonResp = resp.json()
			
			if ('access_token' not in jsonResp):
				print(jsonResp)
				raise Exception('AAD Authentication error')

			token = jsonResp['access_token']
			subdomain = str(os.environ.get('SUBDOMAIN'))

			return jsonify(token = token, subdomain = subdomain)
		except Exception as e:
			message = 'Unable to acquire Azure AD token. Check the debugger for more information.'
			print(message, e)
			return jsonify(error = message)

@app.route('/checker', methods=['GET'])
def checker_page():
	'Show the test page'
	return render_template('checker.html')

@app.route('/checker', methods=['POST'])
def check():
    input_text = request.form['input_text']
	
    if input_text.isspace():
        return render_template('checker.html', input_text=input_text, highlighted_text='', message='Input cannot contain only spaces.')

    check_accuracy, output_text, splitted_words, list_of_booleans_from_word_checking = correction_and_accuracy(input_text)
    highlighted_text = highlighting_words(splitted_words, list_of_booleans_from_word_checking)
    count_true = sum(1 for boolean_value in list_of_booleans_from_word_checking if boolean_value)
    count_false = sum(1 for boolean_value in list_of_booleans_from_word_checking if not boolean_value)
    count_words = len(list_of_booleans_from_word_checking)
    return render_template('checker.html', original_text=input_text, output_text=output_text, highlighted_text=highlighted_text, check_accuracy=check_accuracy, count_true=count_true, count_false=count_false, count_words=count_words)



@app.route('/checker_from_ocr', methods=['POST'])
def checker_from_ocr():
    list_of_ocred_paragraph = request.form['combined_paragraph']
    print(list_of_ocred_paragraph)
    # combined_paragraph = " \n ".join(list_of_ocred_paragraph)
    # combined_paragraph = "test"
    return render_template('checker.html', resultan_paragraph = list_of_ocred_paragraph)

@app.route('/video_insights')
def video_up_page():
	'Show the test page'
	return render_template('video_page.html')


@app.route('/video_insights', methods=['POST'])
def video_insights():
    video_url = request.form['video_url']
    print(video_url)
    video_insight = video_indexer_insights(video_url)
    # combined_paragraph = " \n ".join(list_of_ocred_paragraph)
    # combined_paragraph = "test"
    return render_template('video_page.html', video_insight = video_insight)


@app.route('/text_summarization')
def text_sum_page():
	'Show the test page'
	return render_template('text_summarization_page.html')

@app.route('/text_summarization', methods=['POST'])
def text_sum_process():
    text = request.form['input_sum_text']
    summarized_text, ori_text_len, summarized_text_len, percentage_of_loss, count_removed_words = start_summarizing(text)
    return render_template('text_summarization_page.html', summarized_text = summarized_text, ori_text_len=ori_text_len, summarized_text_len=summarized_text_len, percentage_of_loss=percentage_of_loss, original_text = text, count_removed_words = count_removed_words)

@app.route('/readme')
def readme_page():
	'Show the test page'
	return render_template('immersive_reader_only.html')

@app.route('/readme', methods=['POST'])
def readme_process():
    text = request.form['input_readme_text']
    return render_template('immersive_reader_only.html', original_text = text)

# videostream

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(-1)  # use 0 for web camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stream_page')
def video_stream_page():
    """Video streaming home page."""
    return render_template('video_stream_page.html')

@app.route('/video_indexer_widget')
def video_indexer_widget():
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('video_indexer_widget.html')


# chat app
chat_history = []

@app.route('/chat_app')
def chat_app():
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('chat_app.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append user message to chat history
    chat_history.append({'sender': 'You', 'message': user_message, 'timestamp': timestamp})
    
    response_message = get_chat_response(user_message)
    chat_history.append({'sender': 'Bot', 'message': response_message, 'timestamp': timestamp})
    
    return jsonify({'response': response_message, 'history': chat_history})

def get_chat_response(message):
    # Replace with your OpenAI call
    response = user_chat(message)
    return response