#pylint:disable=import-error
"""
Streamlit dashboard layout for court hearings data.
"""
import re
import streamlit as st
from dotenv import load_dotenv
from psycopg2.extensions import connection
from rds_utils import get_db_connection


# CSS Injection
GOLD_COLOR = "#b29758"
SECONDARY_GOLD_COLOUR = "#a38c64"

st.markdown(
    f"""
    <style>
    /* Force Markdown headers (H1) to the GOLD color */
    h1, h2{{
        color: {GOLD_COLOR} !important;
    }}
    h3{{
        color: {SECONDARY_GOLD_COLOUR} !important;
    }}

    /* FIX: Target the sidebar container and set the text color */
    [data-testid="stSidebar"] {{
        /* This applies to the elements inside the sidebar */
        color: {GOLD_COLOR} !important;
    }}

    /* Optional: Ensure all text elements (labels, markdown) within the sidebar use the color */
    [data-testid="stSidebar"] * {{
        color: {GOLD_COLOR} !important;
    }}

    /* NEW: Hide the judge_details.py link from the sidebar navigation */
    /* Streamlit converts pages/judge_details.py to the URL path /judge_details */
    [data-testid="stSidebarNavLink"][href$="/judge_details"] {{
        display: none;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


MAIN_LOGO = "images/BarristerBrief.png"
SIDEBAR_LOGO = "images/courtlogo.png"

st.logo(SIDEBAR_LOGO, size='large')
st.sidebar.image(MAIN_LOGO)

def insert_subscriber(con: connection, first_name:str, last_name: str, email: str):
    """Function to insert subscribers into the RDS. """
    query="""
        INSERT INTO
            subscriber (first_name, last_name, email)
        VALUES (%s, %s, %s)
    """
    with con.cursor() as cur:
        cur.execute(query, (first_name, last_name, email,))
        con.commit()

def validate_name(name, field_name="Name"):
    """Validates user input against name regex"""
    if not name:
        return False, f"{field_name} is required"
    if not re.match(r'^[A-Za-z\\\\s-]+$', name):
        return False, f"{field_name} should only contain letters, spaces, and hyphens"
    if len(name) < 2:
        return False, f"{field_name} should be at least 2 characters long"
    return True, ""


def validate_email(email):
    """Validates user email against email regex. """
    if not email:
        return False, "Email is required."
    if not re.match(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$", email):
        return False, "Invalid email format."
    return True, ""

def main():
    """Main function to load and create dashboard. """
    load_dotenv()
    st.set_page_config(page_title="News Letter Sign-Up", layout="wide")

    # Connect to database
    conn = get_db_connection()

    # Layout
    st.title("Sign Up For Barrister's Brief")
    st.markdown("Enter your detail's below to receive daily court summaries!")
    st.divider()

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email",)

    if st.button("Enter"):
        valid_first, msg_first = validate_name(first_name, "First Name")
        valid_last, msg_last = validate_name(last_name, "Last Name")
        valid_email, msg_email = validate_email(email)

        if all([valid_first, valid_last, valid_email]):
            st.success(f"Thank You {first_name}! \
                       You have successfully signed up for Barrister's Brief")
            insert_subscriber(conn, first_name, last_name, email)
        else:
            if not valid_first:
                st.error(msg_first)
            if not valid_last:
                st.error(msg_last)
            if not valid_email:
                st.error(msg_email)

if __name__ == "__main__":
    main()
