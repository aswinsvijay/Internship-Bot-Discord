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

def sql_set_channel(guild,channel,channel_mention):
    cursor.execute(
        'INSERT INTO guild_channel '
        'values (%s,%s) '
        'ON DUPLICATE KEY UPDATE '
        'ChannelID=%s ',
        (guild, channel_mention, channel_mention)
    )
    botdata.commit()

def sql_get_channel(guild):
    cursor.execute(
        'SELECT ChannelID from guild_channel '
        'WHERE GuildID=%s',
        (guild,)
    )
    return list(cursor)[0][0]
