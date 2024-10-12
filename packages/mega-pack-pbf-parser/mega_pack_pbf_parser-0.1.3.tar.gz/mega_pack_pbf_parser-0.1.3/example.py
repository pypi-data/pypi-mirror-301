"""
pip install -i https://test.pypi.org/simple/ mega-pack-pbf-parser
"""
from typing import List
from mega_pack_pbf_parser import Project_Parser
from mega_pack_pbf_parser import PROJECT_DB_PATH
from mega_pack_pbf_parser import create_db, insert
from mega_pack_pbf_parser import insert_songs_query


def build_db():
    """
    Demonstrates how to build the project database.
    WARNING: the script DROPS all existing tables and builds new versions.
    Be sure to add the full path to the project db to the constants.py file (PROJECT_DB_PATH)
    """
    db_path = PROJECT_DB_PATH
    script_path = r"D:\Python\scripts\rc\mega_pack_pbf_parser\mega_pack_pbf_parser\create_database.sql"
    with open(script_path) as f:
        script = f.read()
    create_db(db_path=db_path, script=script)


def insert_song_data(data: List):
    """
    Inserts song data into the project database. Prints the number of rows inserted.

    Parameters:
    data(List): a list of song info: PBF name, song name, product name, song type
    """
    query = insert_songs_query
    db_path = PROJECT_DB_PATH
    row_count = insert(db_path=db_path, query=query, data=data)
    print(f"Inserted {row_count} rows into the database.")


def main():    
    bb_project_folder = r"C:\Users\RC\Documents\BBWorkspace\GM_Mega_Pack_Project"
    build_db()
    parser = Project_Parser(project_folder=bb_project_folder) 
    song_list = parser.run()
    insert_song_data(song_list)


if __name__ == '__main__':
    main()
