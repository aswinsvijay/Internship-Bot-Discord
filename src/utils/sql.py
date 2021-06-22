import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

class Database:
    def __init__(self, db):
        self.db = db

    async def set_internship_channel(self, guild, channel_mention):
        """
        Set channel where Zapier sends internships
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO guild_channel
                VALUES (%s, %s) as val
                ON DUPLICATE KEY UPDATE
                ChannelID=val.ChannelID
                """,
                (guild, channel_mention)
            )
            await self.db.commit()

    async def get_internship_channel(self, guild):
        """
        Get channel where Zapier sends messages in the guild
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT ChannelID from guild_channel
                WHERE GuildID=%s
                """,
                (guild,)
            )
            return (await cursor.fetchall())[0][0]

    async def add_internship(self, message, guild, title, email, date, applyURL, editURL):
        """
        Insert internship information into database
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO internships
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (message, guild, title, email, date, applyURL, editURL)
            )
            await self.db.commit()

    async def set_student_guild(self, student, guild):
        """
        Enrol student to a guild
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO student_guild
                VALUES (%s, %s) as val
                ON DUPLICATE KEY UPDATE
                GuildID=val.GuildID
                """,
                (student, guild)
            )
            await self.db.commit()

    async def get_internships(self, student):
        """
        Get all internships in guild where student is enrolled
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT Title, ApplyURL
                FROM student_guild NATURAL JOIN internships
                WHERE StudentID=%s
                """,
                (student,)
            )
            return cursor

    async def delete_internships(self, date):
        """
        Delete internships after last date to apply
        """
        async with self.db.cursor() as cursor:
            await cursor.execute(
                """
                SELECT ChannelID, MessageID, EditURL
                FROM internships NATURAL JOIN guild_channel
                WHERE LastDate<%s
                """,
                (date,)
            )
            deletable = await cursor.fetchall()
            await cursor.execute(
                """
                DELETE FROM internships
                WHERE LastDate<%s
                """,
                (date,)
            )
            await self.db.commit()
            return deletable


async def database_connect():
    """
    Connect to MySQL database
    """
    # Connect to database
    try:
        botdata = await aiomysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PASSWORD,
            db = MYSQL_DATABASE
        )

    except aiomysql.DatabaseError:          # If database not present
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

    return Database(botdata)
