"""This script generates an HTML email to send to subscribers."""

from rds_utils import get_db_connection, query_rds


def handler(context=None, event=None):
    """Handler function which runs on the lambda."""
    conn = get_db_connection()

    query = """
        SELECT
            *
        FROM
            hearing
        WHERE
            date(hearing_date) = (current_date - interval '1' day);
    """
    hearings = query_rds(conn, query)

    conn.close()


if __name__ == "__main__":
    handler()
