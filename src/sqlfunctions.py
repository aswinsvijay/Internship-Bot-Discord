import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Connect to database
try:
    botdata = mysql.connector.connect(
        host = MYSQL_HOST,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD,
        database = MYSQL_DATABASE
    )
    cursor = botdata.cursor()
# If database not present
except mysql.connector.errors.DatabaseError:
    botdata = mysql.connector.connect(
        host = MYSQL_HOST,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD
    )
    cursor = botdata.cursor()
    cursor.execute(f'CREATE DATABASE {MYSQL_DATABASE}')
    cursor.execute(f'USE {MYSQL_DATABASE}')

    # Table for channel where Zapier sends internships
    cursor.execute(
        """
        CREATE TABLE guild_channel(
        GuildID BIGINT,
        ChannelID BIGINT NOT NULL,
        PRIMARY KEY (GuildID))
        """
    )

    # Table to store internships
    cursor.execute(
        """
        CREATE TABLE internships(
        MessageID BIGINT PRIMARY KEY,
        GuildID BIGINT,
        Title VARCHAR(255),
        Email VARCHAR(255),
        LastDate DATE,
        ApplyURL VARCHAR(255),
        EditURL VARCHAR(255),
        FOREIGN KEY (GuildID) REFERENCES guild_channel(GuildID))
        """
    )

    # Table for student enrolments
    cursor.execute(
        """
        CREATE TABLE student_guild(
        StudentID BIGINT PRIMARY KEY,
        GuildID BIGINT,
        FOREIGN KEY(GuildID) REFERENCES guild_channel(GuildID))
        """
    )

def set_internship_channel(guild, channel_mention):
    """
    Set channel where Zapier sends internships
    """
    cursor.execute(
        """
        INSERT INTO guild_channel
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        ChannelID=VALUES(ChannelID)
        """,
        (guild, channel_mention)
    )
    botdata.commit()

def get_internship_channel(guild):
    """
    Get channel where Zapier sends messages in the guild
    """
    cursor.execute(
        """
        SELECT ChannelID from guild_channel
        WHERE GuildID=%s
        """,
        (guild,)
    )
    return list(cursor)[0][0]

def add_internship(message, guild, title, email, date, applyURL, editURL):
    """
    Insert internship information into database
    """
    cursor.execute(
        """
        INSERT INTO internships
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (message, guild, title, email, date, applyURL, editURL)
    )
    botdata.commit()

def set_student_guild(student, guild):
    """
    Enrol student to a guild
    """
    cursor.execute(
        """
        INSERT INTO student_guild
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        GuildID=VALUES(GuildID)
        """,
        (student, guild)
    )
    botdata.commit()

def get_internships(student):
    """
    Get all internships in guild where student is enrolled
    """
    cursor.execute(
        """
        SELECT Title, ApplyURL
        FROM student_guild NATURAL JOIN internships
        WHERE StudentID=%s
        """,
        (student,)
    )
    return cursor
