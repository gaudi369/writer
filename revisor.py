import re
import time
from google import genai
from google.genai import types

GOOGLE_API_KEY=''

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp"

delay = 6

story_id = 3.5

revision_guidelines= f"""
        ---

        1. Formatting:
            * Begin a new paragraph for each speaker or action, even for single sentences.
            * Keep paragraphs under 4 sentences (3 or fewer) by splitting longer ones appropriately.
            * Respond with only the chapter text in the final output without commentary or sub-headings.
        
        2. Clarity:
            * Clear up any severe clarity issues if the fix is obvious. Otherwise make none or minimal changes.

        ---
"""

def revise_chapter(chapter_text, instruction):
    """Revises a chapter using the Gemini API."""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=f"{instruction}\n\n{chapter_text}",
            config=types.GenerateContentConfig(
            temperature=0,
            seed = 137,
            )
        )
        print(f"\nGemini Revisor Call!")
        time.sleep(delay)
        return response.text
    except Exception as e:
        print(f"Error revising chapter: {e}")
        return None

def process_chapters(story_id):
    # Parses chapters, revises them, and saves the results.
    input_file = f"{story_id}_chapter_drafts.txt"
    output_file = f"{story_id}_chapter_formatted.txt"

    instruction= f"""
    You are an expert editor. Revise according to the guidelines. 
    {revision_guidelines}
    Do not change any details from the original text. If you are unsure about a change, simply do not change the original text. Output only the revised chapter.
    
    Here is the original chapter to revise:

    """

    try:
        with open(input_file, "r") as infile:
            text = infile.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    chapters = re.split(r"---", text)
    revised_chapters = []

    for i, chapter in enumerate(chapters):
        chapter = chapter.strip()
        if not chapter:
            continue

        print(f"\nRevising Chapter {i+1}...")
        revised_chapter = revise_chapter(chapter, instruction)

        if revised_chapter:
            revised_chapters.append(revised_chapter + "\n---\n")
            print(f"\nRevised Chapter {i+1} Added to List")
        else:
            print(f"Chapter {i+1} revision failed. Skipping.")
            revised_chapters.append(chapter + "\n---\n")
        try:
            with open(output_file, "w") as outfile:
                outfile.writelines(revised_chapters)
            print(f"\nRevised chapters saved to '{output_file}'.")
        except Exception as e:
            print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    input_filename = f"{story_id}_chapter_drafts.txt"
    output_filename = f"{story_id}_chapter_formatted.txt"

    process_chapters(story_id)
    print("Done")

    # result
