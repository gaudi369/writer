import time
import sqlite3
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from PFGeneratorV3_5 import chat_with_retry, parse_with_retry
from memory import conn, save_to_table, write_field_to_file, retrieve_from_database  # Import the database connection

GOOGLE_API_KEY = ''

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp"
THINKING = 'gemini-2.0-flash-thinking-exp'
temperature=0.1
seed=1

# Connect to the database
story_id = 3.41
conn = sqlite3.connect(f"{story_id}_memory.db")
cursor = conn.cursor()
if conn is None:
    raise ValueError("Failed to establish a database connection.")

fact_checking_guidelines = """
    You are an expert editor tasked with ensuring the internal factual consistency of a story as it unfolds chapter by chapter. 
    
    Your goal is to read through the provided chapter and identify important factual errors in the narrative. 

    If no change is required, simply respond 'PASS'. For many chapters, no revisions may be necessary. 
    
    If changes is required identify the factual errors and explain how they should be resolved. Do not write any scenes.

    Unexpected character reactions and motivations being unexplained are NOT factual inconsistencies and should be passed on. 

    Characters may invent new techniques during a fight. New techniques are NOT factual inconsistencies.

    Figurative language is not a factual inconsistency.


    ---
    Example factual inconsistencies:

    If a character loses an important item (e.g., a sword) in one scene but inexplicably has it again later, you should idenitify that error and the relevant scenes.

    If a character was described to have long hair in one scene but short hair in another, you should identify that.

    ---
    Guidelines:
    Read the chapter carefully to identify any inconsistencies.
    Explain which factual inconsistencies and errors you have identified.
    Explain how they should be resolved.
    Include a singular and clear recommendation for each inconsistency.
    You may identify more than one inconsistency per chapter.
    If no change is required, simply respond 'PASS'.

    ---
    Output:
    Either 'PASS' or "There is a factual inconsistency in scenes (sub-sections) regarding... (describe the error). This should be resolved by... (how to resolve it)".

"""

def process_chapters():
    # Retrieves chapters from the database instead of reading from a file.
    input_table = "chapter_drafts"  # Specify the table name
    input_field = "draft_text"        # Specify the field name

    chapters = retrieve_from_database(input_table, input_field, conn)  # Retrieve chapters from the database
    revision_notes = []

    # Initialize the chat object
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=fact_checking_guidelines,
            temperature=temperature,
            seed=seed,
        ),
    )

    for i, chapter in enumerate(chapters):
        chapter = chapter.strip()
        if not chapter:
            continue

        print(f"\nRevising Chapter {i+1}...")
        prompt = f"""{fact_checking_guidelines}
        Here is the original chapter to review:
        {chapter}
        """
        revision_note = chat_with_retry(chat, prompt, True)

        if revision_note and 'PASS' not in revision_note:  # Check if the response text is valid and not 'PASS'
            revision_notes.append(f"\nChapter {i+1} Suggested Revision\n" + revision_note + "\n---\n")
            print(f"Suggested Revision for Chapter {i+1} Added to List")
        elif 'PASS' in revision_note:
            print(f"No revision needed for Chapter {i+1}. PASS!")
        else:
            print(f"Chapter {i+1} revision failed. Skipping.")

    ## Format revision notes and retrieve context
    
    ## Planning step
    #   * should intake all suggested revisions and output a suggested change along with the relevant context (chapter numbers) needed to make the change.

    # Initialize the chat object
    chat2 = client.chats.create(
        model=THINKING,
        config=types.GenerateContentConfig(
            system_instruction="""
            You will be passed all factual inconsistencies found in each chapter of a story. 
            
            Review all suggested revisions, weighing their severity and relationships with other identified errors.
            
            Then, create an alternative plan for fixing the errors in an efficient way.
            
            Your output should cite groups of identified errors and suggest an alternative revision suggestion.

            Example Input:
            Chapter 3: Alan should not have his ring equipped.
            Chapter 4: Alan should not have his ring equipped.
            Chapter 5: Alan should not have his ring equipped.
            Chapter 6: Alan should not have his ring equipped.

            Example Output: 
            Change: Add a scene where Alan finds and equips his ring.
            Chapters: 3
            """,
            temperature=temperature,
            seed=seed,
        ),
    )

    print(f"\nSending revision notes to planner...")
    revision_plan_prompt = f"""
    Here are the revision notes:
    {revision_notes}
    
    ---
    
    Please create a list of changes needed and the chapters where these changes should be implemented. Be concise and actionable.
    """
    revision_plan = chat_with_retry(chat2, revision_plan_prompt, True)
    print(revision_plan)

if __name__ == "__main__":

    process_chapters()
    print("Done")
