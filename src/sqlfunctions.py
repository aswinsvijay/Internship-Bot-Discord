import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

async def database_connect():
    """
    Connect to MySQL database
    """
    global botdata
    # Connect to database
    try:
        botdata = await aiomysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PASSWORD,
            db = MYSQL_DATABASE
        )
        cursor = await botdata.cursor()
    # If database not present
    except aiomysql.DatabaseError:
        botdata = await aiomysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PASSWORD
        )
        cursor = await botdata.cursor()
        await cursor.execute(f'CREATE DATABASE {MYSQL_DATABASE}')
        await cursor.execute(f'USE {MYSQL_DATABASE}')

        # Table for channel where Zapier sends internships
        await cursor.execute(
            """
            CREATE TABLE guild_channel(
            GuildID BIGINT,
            ChannelID BIGINT NOT NULL,
            PRIMARY KEY (GuildID))
            """
        )

        # Table to store internships
        await cursor.execute(
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
        await cursor.execute(
            """
            CREATE TABLE student_guild(
            StudentID BIGINT PRIMARY KEY,
            GuildID BIGINT,
            FOREIGN KEY(GuildID) REFERENCES guild_channel(GuildID))
            """
        )

async def set_internship_channel(guild, channel_mention):
    """
    Set channel where Zapier sends internships
    """
    async with botdata.cursor() as cursor:
        await cursor.execute(
            """
            INSERT INTO guild_channel
            VALUES (%s, %s) as val
            ON DUPLICATE KEY UPDATE
            ChannelID=val.ChannelID
            """,
            (guild, channel_mention)
        )
        await botdata.commit()

async def get_internship_channel(guild):
    """
    Get channel where Zapier sends messages in the guild
    """
    async with botdata.cursor() as cursor:
        await cursor.execute(
            """
            SELECT ChannelID from guild_channel
            WHERE GuildID=%s
            """,
            (guild,)
        )
        return (await cursor.fetchall())[0][0]

async def add_internship(message, guild, title, email, date, applyURL, editURL):
    """
    Insert internship information into database
    """
    async with botdata.cursor() as cursor:
        await cursor.execute(
            """
            INSERT INTO internships
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (message, guild, title, email, date, applyURL, editURL)
        )
        await botdata.commit()

async def set_student_guild(student, guild):
    """
    Enrol student to a guild
    """
    async with botdata.cursor() as cursor:
        await cursor.execute(
            """
            INSERT INTO student_guild
            VALUES (%s, %s) as val
            ON DUPLICATE KEY UPDATE
            GuildID=val.GuildID
            """,
            (student, guild)
        )
        await botdata.commit()

async def get_internships(student):
    """
    Get all internships in guild where student is enrolled
    """
    async with botdata.cursor() as cursor:
        await cursor.execute(
            """
            SELECT Title, ApplyURL
            FROM student_guild NATURAL JOIN internships
            WHERE StudentID=%s
            """,
            (student,)
        )
        return cursor
