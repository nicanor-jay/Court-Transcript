"""Script to create wordclouds for each judge based on the court cases they have overseen."""

import altair as alt
from pandas import DataFrame
from psycopg2.extensions import connection
from rds_utils import get_db_connection, query_rds

from collections import Counter  # Count the frequency of distinct strings
from wordcloud import WordCloud, ImageColorGenerator  # Generate wordclouds
from PIL import Image  # Load images from files
import numpy as np  # Convert images to numbers

def get_summaries_for_judge(conn: connection, judge_id: int) -> str:
    """Return a list of court transcript summaries which were overseen by a specific judge."""

    all_summary_text = ''
    query = """SELECT hearing_description FROM judge j
            JOIN judge_hearing jh 
	            USING (judge_id)
            JOIN hearing h
	            USING (hearing_id)
            WHERE judge_id = %s;"""
    
    with conn.cursor() as cur:
        cur.execute(query, (judge_id,))
        summaries = cur.fetchall()
    
    for summary in summaries:
        all_summary_text += summary['hearing_description']
    return all_summary_text


def create_word_cloud(text: str):
    """Create a word cloud of the summaries for a judge."""

    fog_machine = WordCloud(background_color='#212838',
                            colormap='Wistia')
    fog_machine.generate(text)
    fog_machine.to_file('test.png')


if __name__ == "__main__":
     
    conn = get_db_connection()

    # print(get_summaries_for_judge(conn, 1))
    summary_text = get_summaries_for_judge(conn, 1)
    create_word_cloud(summary_text)

    conn.close()