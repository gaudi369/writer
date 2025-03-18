import sqlite3

conn = None

def initialize_database(story_id):
    global conn
    """
    Initializes the SQLite database and creates necessary tables.
    :param story_id: Unique identifier for the story.
    """
    # Connect to the database
    conn = sqlite3.connect(f"{story_id}_memory.db")
    cursor = conn.cursor()
    if conn is None:
        raise ValueError("Failed to establish a database connection.")

    # Create tables
    cursor.executescript("""
    -- Story Memory Table
    CREATE TABLE IF NOT EXISTS story_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting TEXT,
        essential_fantasy TEXT,
        synopsis TEXT,
        cover_prompt TEXT
    );

    -- Arcs Table
    CREATE TABLE IF NOT EXISTS arcs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_number INTEGER NOT NULL,
        story_id INTEGER NOT NULL,                              -- Foreign key to story_memory
        FOREIGN KEY (story_id) REFERENCES story_memory (id)
    );

    -- Character Descriptions Table
    CREATE TABLE IF NOT EXISTS character_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        name TEXT NOT NULL,                  -- Character name
        background TEXT,                     -- Character background
        goal TEXT,                           -- Character goal
        flaws TEXT,                          -- JSON string for flaws
        appearance TEXT,                     -- Physical appearance
        personality TEXT,                    -- Personality description
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );

    -- Plot Outlines Table
    CREATE TABLE IF NOT EXISTS plot_outlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        chapter_number INTEGER,              -- Chapter number
        title TEXT,                          -- Chapter title
        main_plot_point TEXT,                -- Main plot point
        subplot_focus TEXT,                  -- Subplot focus
        characters TEXT,                     -- JSON string for characters
        tags TEXT,                           -- JSON string for tags
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );

    -- Expanded Chapters Table
    CREATE TABLE IF NOT EXISTS expanded_chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        chapter_number INTEGER,              -- Chapter number
        title TEXT,                          -- Title of the expanded chapter
        main_plot_point TEXT,                -- Main plot point
        subplot_focus TEXT,                  -- Subplot focus
        scene_1 TEXT,                        -- Scene 1 description
        scene_2 TEXT,                        -- Scene 2 description
        scene_3 TEXT,                        -- Scene 3 description
        scene_4 TEXT,                        -- Scene 4 description
        scene_5 TEXT,                        -- Scene 5 description
        ending TEXT,                         -- Ending description
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );
                         
    -- Chapter Drafts Table
    CREATE TABLE IF NOT EXISTS chapter_drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        draft_text TEXT NOT NULL,            -- Full text of the draft
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );

    -- Powersheets Table
    CREATE TABLE IF NOT EXISTS powersheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_draft_id INTEGER,            -- Foreign key to chapter_drafts
        sheet_text TEXT NOT NULL,            -- Full text of the powersheet
        FOREIGN KEY (chapter_draft_id) REFERENCES chapter_drafts (id)
    );

    -- Fan Letters Table
    CREATE TABLE IF NOT EXISTS fan_letters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        letter_text TEXT NOT NULL,           -- Full text of the fan letter
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );

    -- Writer Reviews Table
    CREATE TABLE IF NOT EXISTS writer_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arc_id INTEGER,                      -- Foreign key to arcs
        review_text TEXT NOT NULL,           -- Full text of the writer review
        FOREIGN KEY (arc_id) REFERENCES arcs (id)
    );
                         
    -- Chapter Revision Table
    CREATE TABLE IF NOT EXISTS chapter_revisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        revision_note TEXT,                   -- Notes for each draft
        revision_plan TEXT                    -- Full plan for revision
    );""")

    print(f"Database {story_id}_memory.db initialized successfully with connection: {conn}")
    return conn


import json
from typing import List
from pydantic import BaseModel

# Define Pydantic models for normalized tables
class PlotOutline(BaseModel):
    chapter_number : int
    title: str
    main_plot_point: str
    subplot_focus: str
    characters: List[str]
    tags: List[str]  # List of tags for the chapter


class CharacterDescription(BaseModel):
    name: str
    background: str
    goal: str
    flaws: str
    appearance: str
    personality: str


class ExpandedChapter(BaseModel):
    chapter_number : int
    main_plot_point: str
    subplot_focus: str
    scene_1: str
    scene_2: str
    scene_3: str
    scene_4: str
    scene_5: str
    ending: str



# Generate table configuration
TABLE_CONFIG = {

    "story_memory": {
        "schema": None,  # No Pydantic schema needed for simple text fields
        "fields_map": {
            "setting": "setting",
            "essential_fantasy": "essential_fantasy",
            "synopsis": "synopsis",
            "cover_prompt": "cover_prompt"
        },
        "schema_json": None 
    },

    "character_descriptions": {
        "schema": CharacterDescription,
        "fields_map": {
            "name": "name",
            "background": "background",
            "goal": "goal",
            "flaws": "flaws",
            "appearance": "appearance",
            "personality": "personality"
        },
        "schema_json": json.dumps(CharacterDescription.model_json_schema())
    },
    "plot_outlines": {
        "schema": PlotOutline,
        "fields_map": {
            "chapter_number" : "chapter_number",
            "title" : "title",
            "main_plot_point": "main_plot_point",
            "subplot_focus": "subplot_focus",
            "characters" : "characters",
            "tags": "tags"
        },
        "schema_json": json.dumps(PlotOutline.model_json_schema())
    },
    "expanded_chapters": {
        "schema": ExpandedChapter,
        "fields_map": {
            "chapter_number" : "chapter_number",
            "main_plot_point": "main_plot_point",
            "subplot_focus": "subplot_focus",
            "scene_1": "scene_1",
            "scene_2": "scene_2",
            "scene_3": "scene_3",
            "scene_4": "scene_4",
            "scene_5": "scene_5",
            "ending": "ending"
        },
        "schema_json": json.dumps(ExpandedChapter.model_json_schema())
    },
    "chapter_drafts": {
        "schema": None,
        "fields_map": {
            "arc_id": "arc_id",
            "draft_text": "draft_text"
        },
        "schema_json": None
    },
    "powersheets": {
        "schema": None,
        "fields_map": {
            "chapter_draft_id": "chapter_draft_id",
            "sheet_text": "sheet_text"
        },
        "schema_json": None
    },
    "fan_letters": {
        "schema": None,
        "fields_map": {
            "arc_id": "arc_id",
            "letter_text": "letter_text"
        },
        "schema_json": None
    },
    "writer_reviews": {
        "schema": None,
        "fields_map": {
            "arc_id": "arc_id",
            "review_text": "review_text"
        },
        "schema_json": None
    }
}

def save_to_table(data, table_name, conn=conn, verbose=False):
    def clean_data(raw_data, fields):
        # Ensure raw_data is a dictionary
        if hasattr(raw_data, "dict"):
            raw_data = raw_data.dict()
        return {field: raw_data.get(field) for field in fields if raw_data.get(field) is not None}

    table_config = TABLE_CONFIG.get(table_name)
    if not table_config:
        raise ValueError(f"No configuration found for table '{table_name}'.")

    fields_map = table_config["fields_map"]
    columns, values = [], []

    # Clean the data
    data = clean_data(data, fields_map.keys())
    if verbose:
        print(f"Cleaned data for table '{table_name}': {data}")

    for model_field, column_name in fields_map.items():
        if model_field in data:
            value = data[model_field]
            value = json.dumps(value) if isinstance(value, (list, dict)) else value
            columns.append(column_name)
            values.append(value)

    placeholders = ",".join(["?"] * len(columns))
    query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting into {table_name}: {e}")
        return None

    row_id = cursor.lastrowid
    print(f"Inserted data into '{table_name}' with ID: {row_id}")
    return row_id

def retrieve_from_database(table_name, field_name, conn=conn):

    cursor = conn.cursor()
    query = f"SELECT {field_name} FROM {table_name}"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return [row[0] for row in rows]  # Return a list of values
    except sqlite3.Error as e:
        print(f"Error reading from {table_name}: {e}")
        return []
    finally:
        cursor.close()

def write_field_to_file(table_name, field_name, output_file):
    """
    Writes all values of a specified field from a given table to a text file.
    :param table_name: Name of the table to read from.
    :param field_name: Name of the field to write to the file.
    :param output_file: Name of the output text file.
    """
    cursor = conn.cursor()
    query = f"SELECT {field_name} FROM {table_name}"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        with open(output_file, 'w') as f:
            for row in rows:
                f.write(f"{row[0]}---")  # Write each field value followed by the delimiter
            print(f"Data written to {output_file} successfully.")
    except sqlite3.Error as e:
        print(f"Error reading from {table_name}: {e}")
    finally:
        cursor.close()

def close():
    global conn
    if conn:
        conn.close()
        print("Database connection closed.")
    else:
        print("No database connection to close.")

import os

def delete_database(story_id):
    db_name = f"{story_id}_memory.db"  # Construct the database file name
    try:
        # Check if the file exists
        if os.path.exists(db_name):
            # Delete the database file
            os.remove(db_name)
            print(f"Database '{db_name}' has been deleted successfully.")
        else:
            print(f"Database '{db_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the database: {e}")
