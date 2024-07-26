from dotenv import dotenv_values
from pprint import pprint

from VideoIndexerClient.Consts import Consts
from VideoIndexerClient.VideoIndexerClient import VideoIndexerClient
from dotenv import load_dotenv
import os 

load_dotenv()

def video_indexer_insights(video_url):
    AccountName = os.environ.get('VideoIndexerAccountName')
    ResourceGroup = os.environ.get('ResourceGroup')
    SubscriptionId = os.environ.get('VideoIndexerSubscriptionId')

    ApiVersion = '2024-01-01'
    ApiEndpoint = 'https://api.videoindexer.ai'
    AzureResourceManager = 'https://management.azure.com'

    # create and validate consts
    consts = Consts(ApiVersion, ApiEndpoint, AzureResourceManager, AccountName, ResourceGroup, SubscriptionId)
    # create Video Indexer Client
    client = VideoIndexerClient()

    # Get access tokens (arm and Video Indexer account)
    client.authenticate_async(consts)

    client.get_account_async()

    VideoUrl = video_url
    ExcludedAI = []

    video_id = client.upload_url_async('my-video-name', VideoUrl, ExcludedAI, False)

    client.wait_for_index_async(video_id)

    insights = client.get_video_async(video_id)
    print(insights)
    return insights