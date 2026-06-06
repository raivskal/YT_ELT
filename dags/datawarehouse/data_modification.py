import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur, conn, schema, row):

    try:
        if schema == 'staging':
            video_id = 'video_id'
            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);""", row
            )
        else:
            video_id = 'Video_ID'
            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Type", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(Video_ID)s, %(Video_Title)s, %(Upload_Date)s, %(Duration)s, %(Video_Type)s, %(Video_Views)s, %(Likes_Count)s, %(Comments_Count)s);""", row
            )

        conn.commit() # Commit the transaction to save changes to the database
        logger.info(f"Insterted row with Video ID: {row[video_id]}") # Log the successful insertion of the row

    except Exception as e:
        logger.error(f"Error inserting row with Video ID: {row[video_id]}") # Log any errors that occur during the insertion process
        raise e # Re-raise the exception to be handled by the calling code
    
def update_rows(cur, conn, schema, row):

    try:
        #staging
        if schema == 'staging':
            video_id = 'video_id'
            upload_date = 'publishedAt'
            video_title = 'title'
            video_views = 'viewCount'
            likes_count = 'likeCount'
            comments_count = 'commentCount'
        #core
        else:
            video_id = 'Video_ID'
            upload_date = 'Upload_Date'
            video_title = 'Video_Title'
            video_views = 'Video_Views'
            likes_count = 'Likes_Count'
            comments_count = 'Comments_Count'

        cur.execute(
            f"""UPDATE {schema}.{table}
            SET "Video_Title" = %({video_title}s,
                "Video_Views" = %({video_views}s,
                "Likes_Count" = %({likes_count}s,
                "Comments_Count" = %({comments_count}s
            WHERE "Video_ID" = %({video_id}s AND "Upload_Date" = %({upload_date}s;
            """, row
        )

        conn.commit() # Commit the transaction to save changes to the database
        logger.info(f"Updated row with Video ID: {row[video_id]}") # Log the successful update of the row

    except Exception as e:
        logger.error(f"Error updating row with Video ID: {row[video_id]} - {str(e)}") # Log any errors that occur during the update process
        raise e # Re-raise the exception to be handled by the calling code
    
def delete_rows(cur, conn, schema, ids_to_delete):

    try:
        ids_to_delete = f"""({', '.join(f"'{id}'" for id in ids_to_delete)})""" # Format the list of IDs to delete into a string suitable for the SQL IN clause

        cur.execute(
            f"""
            DELETE FROM {schema}.{table}
            WHERE "Video_ID" IN {ids_to_delete};
            """
        )

        conn.commit() # Commit the transaction to save changes to the database
        logger.info(f"Deleted rows with Video ID: {ids_to_delete}") # Log the successful deletion of the rows

    except Exception as e:
        logger.error(f"Error deleting rows with Video ID: {ids_to_delete} - {str(e)}") # Log any errors that occur during the deletion process
        raise e # Re-raise the exception to be handled by the calling code