import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

try:
    botdata = mysql.connector.connect(
        host = MYSQL_HOST,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD,
        database = MYSQL_DATABASE
    )
    cursor = botdata.cursor()
except mysql.connector.errors.DatabaseError:
    botdata = mysql.connector.connect(
        host = MYSQL_HOST,
        user = MYSQL_USER,
        password = MYSQL_PASSWORD
    )
    cursor = botdata.cursor()
    cursor.execute(f'CREATE DATABASE {MYSQL_DATABASE}')
    cursor.execute(f'USE {MYSQL_DATABASE}')
    cursor.execute(
        """
        CREATE TABLE guild_channel(
        GuildID BIGINT,
        ChannelID BIGINT NOT NULL,
        PRIMARY KEY (GuildID))
        """
    )
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
    cursor.execute(
        """
        CREATE TABLE student_guild(
        StudentID BIGINT PRIMARY KEY,
        GuildID BIGINT,
        FOREIGN KEY(GuildID) REFERENCES guild_channel(GuildID))
        """
    )

def set_internship_channel(guild,channel,channel_mention):
    cursor.execute(
        """
        INSERT INTO guild_channel
        VALUES (%s,%s)
        ON DUPLICATE KEY UPDATE
        ChannelID=VALUES(ChannelID)
        """,
        (guild, channel_mention)
    )
    botdata.commit()

def get_internship_channel(guild):
    cursor.execute(
        """
        SELECT ChannelID from guild_channel
        WHERE GuildID=%s
        """,
        (guild,)
    )
    return list(cursor)[0][0]

def add_internship(message, guild, title, email, date, applyURL, editURL):
    cursor.execute(
        """
        INSERT INTO internships
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (message, guild, title, email, date, applyURL, editURL)
    )
    botdata.commit()

def set_student_guild(student, guild):
    cursor.execute(
        """
        INSERT INTO student_guild
        VALUES (%s,%s)
        ON DUPLICATE KEY UPDATE
        GuildID=VALUES(GuildID)
        """,
        (student, guild)
    )
    botdata.commit()
