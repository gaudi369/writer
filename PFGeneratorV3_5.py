# Pre Set Up
GOOGLE_API_KEY=''

from google import genai
from google.genai import types
from google.genai.errors import ServerError

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp" 
THINKING = 'gemini-2.0-flash-thinking-exp-01-21'

import time  
import json  # For parsing and handling JSON data
from typing import List  # For type hinting
from pydantic import BaseModel  # For schema validation (using Pydantic)
from pydantic import TypeAdapter
from pydantic import ValidationError

# Set Up
overall_start_time = time.time()  # Start the overall timer
total_story_words = 0
total_story_time_minutes = 0
desired_arcs = 3
story_id = 3.51
seed = 137

from prompts import get_prompts
system_instruction, planner_guidelines, expander_guidelines, writer_guidelines, progression_fantasy_plot_generator, first_arc_prompt, last_arc_prompt, setting_prompt, ef_prompt, parser_instructions, fan_guidelines, synopsis, cover = get_prompts(desired_arcs)

import memory
from memory import TABLE_CONFIG, save_to_table, conn, delete_database, write_field_to_file


# Main functions
delay = 2
max_retries = 6

def chat_with_retry(chat, prompt, verbose=False):
    """Attempts to send a message with retries on server errors."""
    for attempt in range(1, max_retries+1):
        try:
            response = chat.send_message(prompt)
            time.sleep(delay)
            if verbose:
                print(f"{chat} called!")
                try:
                    print(response.text)
                except UnicodeEncodeError:
                    print("[Unicode text cannot be displayed in current console]")
            return response.text  
        except ServerError as e:
            print(f"Server error: {e}. Retrying in {delay * 10 * attempt} seconds...")
            time.sleep(delay * 10 * attempt) 
        except Exception as e:
            if 'RESOURCE_EXHAUSTED' in str(e):
                print(f"Resource exhausted. Retrying in {delay * 10 * attempt} seconds...")
                time.sleep(delay * 10 * attempt)
                continue 
            print(f"Unexpected error: {e}")
            break
    print("Max retries reached. Unable to complete the request.")
    return None
            
def parse_with_retry(
    raw: str,
    table_name: str,
    conn, 
    verbose: bool = False,
    foreign_key: int = None,
    increment_foreign_key: bool = False
):

    table_config = TABLE_CONFIG.get(table_name)
    if not table_config:
        raise ValueError(f"No configuration found for table '{table_name}'.")

    schema = table_config["schema"]
    schema_json = table_config["schema_json"]

    parse_prompt = f"""
    Please analyze the provided response and return a structured output as a JSON array. Each element in the array must adhere to the following schema:
    {schema_json}

    {parser_instructions}

    Here is the original response. Preserve all details. Return a JSON array of objects:
    {raw}
    """
    parser = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=parser_instructions,
            response_mime_type="application/json",
            temperature=0,
            seed=seed,
        )
    )

    for attempt in range(1, max_retries + 1):
        if attempt > 1:
            parse_prompt = f"Your last attempt failed with error: {e}. Please try again and fix what you did wrong last time.\n" + parse_prompt
        response = parser.send_message(parse_prompt)
        if verbose:
            print(parse_prompt)
        time.sleep(delay)
        
        # Clean the response text to remove any Markdown formatting
        cleaned_response_text = response.text.strip()  
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:].strip()  
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3].strip() 

        try:
            data = json.loads(cleaned_response_text)  # Parse the cleaned response text

            result = TypeAdapter(List[schema]).validate_python(data)

            for item in result:
                if foreign_key is not None:
                    item['foreign_key'] = foreign_key
                    if increment_foreign_key:
                        foreign_key += 1
                save_to_table(data=item, table_name=table_name, conn=conn, verbose=verbose)

            print(f"Saved {len(result)} records to '{table_name}'")
            print(f"Last foreign key used: {foreign_key}")
            return result, foreign_key

        except (ValidationError, json.JSONDecodeError) as e:
            print(f"[Retry {attempt}/{max_retries}] Validation failed: {e}")
            if attempt == max_retries:
                print("Max retries reached—returning None.")
                print(f"Here is the response that failed validation {cleaned_response_text}")
                print(f"Here was the retrieved schema: {schema}")
                return None, None

if __name__ == "__main__":

    delete_database(story_id)
    conn = memory.initialize_database(story_id)

    with open(f'{story_id}_chapter_drafts.txt', 'w') as file:
                file.write(f"\n")

    # Initialize chats/agents
    planner = client.chats.create(
        model=THINKING,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction + planner_guidelines,
            temperature=1,
            seed=seed,
        ),
    )

    expander = client.chats.create(
        model=THINKING,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction + expander_guidelines,
            temperature=1,
            seed=seed,
        ),
    )

    writer = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction + writer_guidelines,
            temperature=1,
            seed=seed,
        ),
    )

    # Generate context
    setting = chat_with_retry(planner, setting_prompt, True)
    essential_fantasy = chat_with_retry(planner, ef_prompt, True)

    # Provide context for expander and writer
    context = f"""Here is the main context for the story. This is not a task, instead it is to prepare you for your next task. Note your thoughts: 

    {setting}

    {essential_fantasy}"""

    expander_setup = chat_with_retry(expander, context)
    writer_setup = chat_with_retry(writer, context)

    # Main Loop
    story_finished = False
    chapter_drafts = []
    all_character_descriptions = []
    character_powers = ""
    arc_stats = []
    total_words = 0
    arc_number = 0
    plot_number = 1
    chunk_number = 1
    chapter_number = 1
    first_iteration = True  # Flag to identify the first iteration

    while not story_finished:
        arc_start_time = time.time()  # Start timer for the arc
        arc_word_count = 0
        arc_number += 1
        chapter_stats = []
        plot_outlines = []

        # Step 1: Generate the next arc
        if arc_number == 1:
            prompt = first_arc_prompt # Special plotting prompt for the first arc
        elif arc_number == (desired_arcs-1): 
            prompt = f"""Remember, this is your second-to-last arc! {progression_fantasy_plot_generator} """
        elif arc_number == desired_arcs:  # Special plotting prompt for the last arc
            prompt = last_arc_prompt
        elif arc_number > desired_arcs:  # Ensure story ends
            print("The story is finished! (Forced because desired arc count reached) Ready for revision.")
            story_finished = True
            break
        else:
            prompt = progression_fantasy_plot_generator # Standard arc prompt for subsequent iterations

        plot = chat_with_retry(planner, prompt, True)

        if plot == "Finished":
            story_finished = True
            print("The story is finished! Ready for revision.")
            break  # Exit the loop

        # Step 2: Generate plot outline and character description objects
        plot_outlines, plot_number = parse_with_retry(plot, "plot_outlines", conn, False, None)

        # Extract unique characters and generate descriptions (unchanged)
        unique_characters = set()
        for outline in plot_outlines:
            unique_characters.update(outline.characters)

        print(f"{len(unique_characters)} unique characters in this arc: {unique_characters}")
        description_prompt = f"""

        Generate specific and concise character descriptions for each element of the following list: {unique_characters}.
        Each character should be unique to create a roster with variety. Groups of side characters (eg., villagers, bandits, etc) should be described together with shared fields.

        Structured Output Format (list these in series for each character, include nothing else)
        ---

        Name: Restate their name exactly as written in the provided list.
        Background: Describe their a distinct background and how it shapes them.
        Goal: State their driving goal or dream.
        Flaws: List their two or three flaws that hamper their progression.
        Appearance: Describe their physical appearance briefly.
        Personality: Describe their personality including any relevant quirks if applicable.

        ---

        Please include only this information in your response. Be specific and concise.

        """
        character_descriptions = chat_with_retry(planner, description_prompt, True)
        character_descriptions_parsed, arc_character_count = parse_with_retry(character_descriptions, "character_descriptions", conn, False, None)

        # Step 2.5: Expand chapter draft chunks in groups of 4
        expanded_chapters = []
        chunk_size = 4
        for draft_number in range(0, len(plot_outlines), chunk_size):
            # Get the current chunk of chapters
            chunk = plot_outlines[draft_number:draft_number + chunk_size]
            
            # Collect all unique characters mentioned in the chunk
            unique_characters = set()
            for chapter in chunk:
                unique_characters.update(chapter.characters)  # Access `characters` attribute directly

            # Retrieve context for all unique characters in the chunk
            context_parts = []
            for name in unique_characters:
                cd = next((cd for cd in character_descriptions_parsed if cd.name == name), None)  # Access `name` attribute directly
                if cd:
                    context_parts.append(
                        f"Name: {cd.name}\n"
                        f"Background: {cd.background}\n"
                        f"Goal: {cd.goal}\n"
                        f"Flaws: {cd.flaws}\n"
                        f"Appearance: {cd.appearance}\n"
                        f"Personality: {cd.personality}\n"
                    )
            context = "\n\n".join(context_parts)

            expansion_prompt = f"""
            Expand the following group of 4 chapter outlines. 

            {json.dumps([chapter.model_dump() for chapter in chunk], indent=2)}

            Here are the character descriptions for this chapter. Please reference them for accurate details and interactions:
            {context}

            Here are your guidelines as a reminder:
            {expander_guidelines}
            """

            # Expansion Section
            expansion_response = chat_with_retry(expander, expansion_prompt)
            parsed_result, foreign_key = parse_with_retry(expansion_response, "expanded_chapters", conn, False, None)
            expanded_chapters.extend(parsed_result)  # Add the parsed result to the list
            chunk_number = foreign_key
            print(f"Expanded chapters generated for arc {arc_number}: {len(expanded_chapters)} chapters expanded.")

        # Step 3: Chapter Writing Section
        for draft_number, chapter_data in enumerate(expanded_chapters):  # Iterate over the parsed chapters
            chapter_start_time = time.time()

            # Prepare character descriptions for the current chapter
            context_parts = []
            for name in plot_outlines[draft_number].characters:  # Access characters from the plot outline
                cd = next((cd for cd in character_descriptions_parsed if cd.name == name), None)  # Match character by name
                if cd:
                    context_parts.append(
                        f"Name: {cd.name}\n"
                        f"Background: {cd.background}\n"
                        f"Goal: {cd.goal}\n"
                        f"Flaws: {cd.flaws}\n"
                        f"Appearance: {cd.appearance}\n"
                        f"Personality: {cd.personality}\n"
                    )
            context = "\n\n".join(context_parts)

            # Create writer prompt using attributes of `chapter_data`
            writer_prompt = f"""
            Write the next chapter of the story according to the following outline:

            Chapter Number: {chapter_data.chapter_number}
            Main Plot Point: {chapter_data.main_plot_point}
            Subplot Focus: {chapter_data.subplot_focus}
            Scene 1: {chapter_data.scene_1}
            Scene 2: {chapter_data.scene_2}
            Scene 3: {chapter_data.scene_3}
            Scene 4: {chapter_data.scene_4}
            Scene 5: {chapter_data.scene_5}
            Ending: {chapter_data.ending}

            Here are the character descriptions for this chapter. Please reference them for accurate details and dialogue:
            {context}

            {writer_guidelines}
            """

            chapter_text = chat_with_retry(writer, writer_prompt, False)
            save_to_table({"draft_text": chapter_text}, "chapter_drafts", conn)

            # Save Progress
            write_field_to_file("chapter_drafts", "draft_text", f'{story_id}_chapter_drafts.txt')
            print(f"Chapter {draft_number+1} of Arc {arc_number} written and added to draft!")

            # Check if Power Up to update character powers
            for tag in plot_outlines[draft_number].tags:
                if tag == "Power Up":
                    power_update_prompt = f"""

                    Great job so far! Here is a reminder of the essential fantasy for your story: {essential_fantasy}

                    I want you to create an updated main character power sheet according to the following outline.

                    You are reminding yourself of the main purpose and essential fantasy of the story as well as tracking your progress towards its realization. 
                    
                    Remember the goal is to progress one full rank in cultivation each arc (achieving both half-step and breakthrough). 
                    
                    This rate of progress is very important to finish the story at an appropriate length ({desired_arcs} arcs total).

                    ---
                    Here are the old main character powers. Please update them in a new sheet:
                    {character_powers}

                    ---

                    Please only include these fields in your responce. Update the sheet according to account for recent power progression. Be specific:

                    (Main Character Name) Power Sheet

                    Cultivation Rank: Rank, Level of Success (initial breakthrough or half-step)

                    Cultivation Method: Description.

                    Combat Talent (relative to rank) which determines how many sub-divisions above their rank they can match: Number.

                    Named Techniques (maximum of {desired_arcs}): Description. 

                    Martial Skills: Description.

                    Weapons and Equipment: Description.

                    Past Power Ups: Description. (Brief but exhaustive list of all fortunate encounters, training boosts, and mid-fight breakthroughs)

                    """
                    character_powers = chat_with_retry(writer, power_update_prompt)
                    save_to_table({"sheet_text": character_powers}, "powersheets", conn)

            # Stats for the chapter
            word_count = len(chapter_text.split())
            arc_word_count += word_count
            total_words += word_count
            chapter_end_time = time.time()
            chapter_time = chapter_end_time - chapter_start_time
            words_per_minute = word_count / (chapter_time / 60) if chapter_time > 0 else 0

            # Store stats for this chapter
            chapter_stats.append({
                'Chapter': draft_number + 1,
                'Words': word_count,
                'Time (seconds)': chapter_time,
                'Words per Minute': words_per_minute,
            })
            print(f"Chapter {draft_number+1} of Arc {arc_number} stats recorded! Wrote {word_count} words. Generated for {chapter_time:.2f} seconds."
                f"This is a rate of {words_per_minute:.2f} words-per-minute.")

        print(f"Post Arc {arc_number} Writing Review.")
        combined_chapters = ""
        with open(f'{story_id}_chapter_drafts.txt', 'r') as file:
            combined_chapters = file.read()

        response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"""
        {fan_guidelines}

        {combined_chapters}
        """
        )
        time.sleep(delay)

        review = f"""
        Please review your creative writing guidelines closely to ensure you stick to them no matter what.
        Score yourself out of 10 on each specific guideline and commit to them going forward.
        Trust these guidelines over conventional writing rules. (VERY IMPORTANT)

        {writer_guidelines}
        """

        fan_letter = f"""
        Here is a letter we got from a reader of yours. Take their words as encouragement but keep in mind that other readers of yours might have different opinions.
        Use your best judgement about their feedback to start thinking about the next arc. Remember that we want only {desired_arcs} arcs in total. Do not outline yet. Note things that are working well and things to try next arc:

        {response.text}
        """
        save_to_table({"letter_text": fan_letter}, "fan_letters", conn)

        review_response = chat_with_retry(writer, review, True)
        save_to_table({"review_text": review_response}, "writer_reviews", conn)
        
        fan_letter_response = chat_with_retry(planner, fan_letter, True)

        # Send new power sheet to planner
        chat_with_retry(planner, f"I wrote the arc. Please review the power progression before you continue {character_powers}", True)

        # Reset the `first_iteration` flag
        first_iteration = False

        # End of arc
        arc_end_time = time.time()
        arc_time_minutes = (arc_end_time - arc_start_time) / 60

        # Add arc stats to `arc_stats`
        arc_stats.append({
            'Arc': len(arc_stats) + 1,
            'Words': arc_word_count,
            'Time (minutes)': arc_time_minutes,
            'Chapters': len(plot_outlines),
            'Chapter Stats': chapter_stats,
        })

        # Save stats
        with open(f'{story_id}_arc_stats.txt', 'a') as arc_file:
            # Write data for each arc
            for arc in arc_stats:
                arc_file.write(f"{arc_stats[-1]['Arc']},{arc_stats[-1]['Words']},{arc_stats[-1]['Time (minutes)']:.2f},{arc_stats[-1]['Chapters']}\n")
                # Write chapter details
                arc_file.write("Chapter,Words,Time (seconds),Words per Minute\n")
                for chapter in arc['Chapter Stats']:
                    arc_file.write(f"{chapter['Chapter']},{chapter['Words']},{chapter['Time (seconds)']:.2f},{chapter['Words per Minute']:.2f}\n")

        print("\nCurrent Arc Stats Report:")
        print("====================")
        print(f"  Arc {len(arc_stats)}:")
        print(f"    Total Words: {arc_word_count}")
        print(f"    Total Time: {arc_time_minutes:.2f} minutes")
        print(f"    Chapters: {len(plot_outlines)}")
        for chapter in chapter_stats:
            print(f"      Chapter {chapter['Chapter']}:")
            print(f"        Words: {chapter['Words']}")
            print(f"        Time: {chapter['Time (seconds)']:.2f} seconds")
            print(f"        Words per Minute: {chapter['Words per Minute']:.2f}")

    # End of story
    overall_end_time = time.time()
    total_story_time_minutes += (overall_end_time - overall_start_time) / 60

    print("\nFinal Story Stats Report:")
    print("====================")
    print(f"Total time spent: {total_story_time_minutes:.2f} minutes")
    print(f"Total words written: {total_story_words}\n")
    print("Arc Stats:")
    for arc in arc_stats:
        print(f"  Arc {arc['Arc']}:")
        print(f"    Words: {arc['Words']}")
        print(f"    Time: {arc['Time (minutes)']:.2f} minutes")
        print(f"    Chapters: {arc['Chapters']}")
        for chapter in arc['Chapter Stats']:
            print(f"      Chapter {chapter['Chapter']}:")
            print(f"        Words: {chapter['Words']}")
            print(f"        Time: {chapter['Time (seconds)']:.2f} seconds")
            print(f"        Words per Minute: {chapter['Words per Minute']:.2f}")

    ## for part 2
    from revisor import process_chapters
    process_chapters(story_id)

    # Synopsis, tags, and cover generation prompt
    synopsis_and_tags = chat_with_retry(planner, synopsis, True)
    cover_prompt = chat_with_retry(planner, cover, True)

    save_to_table({"setting": setting, "essential_fantasy": essential_fantasy, "synopsis": synopsis_and_tags, "cover_prompt": cover_prompt}, "story_memory", conn)

    with open(f'{story_id}_synopsis.txt', 'w') as synopsis_file:
        synopsis_file.write(f"{synopsis_and_tags}\n---\n{cover_prompt}\n---\n{setting}\n---\n{essential_fantasy}")


