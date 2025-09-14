import streamlit as st
from utils.youtube_api import get_video_details, get_comments
from utils.sentiment_analysis import analyze_comments
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="YouTube Sentiment Analysis", layout="wide")

st.title("📊 YouTube Comments Sentiment Analysis")

video_url = st.text_input("Enter YouTube Video URL:")


def extract_video_id(url):
    parsed_url = urlparse(url)
    if 'youtube' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    else:
        return None


if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL!")
    else:
        with st.spinner("Fetching video details..."):
            details = get_video_details(video_id)
            comments = get_comments(video_id, max_results=100)
        
        if not details:
            st.error("Video not found!")
        else:
            # Display video details
            st.subheader("📹 Video Details")
            st.write(f"**Title:** {details['title']}")
            st.write(f"**Channel:** {details['channel']}")
            st.write(f"**Published At:** {details['published_at']}")
            st.write(f"**Views:** {details['view_count']}")
            st.write(f"**Likes:** {details['like_count']}")
            st.write(f"**Comments:** {details['comment_count']}")
            
            # Analyze comments
            with st.spinner("Analyzing comments..."):
                analysis_results = analyze_comments(comments)
            
            df = pd.DataFrame(analysis_results)
            
            st.subheader("📈 Sentiment Summary")
            sentiment_counts = df['sentiment'].value_counts()
            st.bar_chart(sentiment_counts)

            st.subheader("💬 Sample Comments")
            st.dataframe(df[['comment', 'sentiment']].head(10))

            # Pie chart
            st.subheader("📊 Sentiment Distribution")
            fig, ax = plt.subplots()
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
            st.pyplot(fig)
