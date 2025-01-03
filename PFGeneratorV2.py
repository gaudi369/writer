# Pre Set Up
GOOGLE_API_KEY='AIzaSyDQzKErcqZncO59-jAQSeLmyUQl6VNhb1Y'

from google import genai
from google.genai import types
from google.genai.errors import ServerError

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp" # others: "gemini-1.5-flash-8b","gemini-1.5-flash-002","gemini-1.5-pro-002","gemini-2.0-flash-exp"

import time  # For timing
import json  # For parsing and handling JSON data
from typing import List  # For type hinting
from pydantic import BaseModel  # For schema validation (if using Pydantic)
from pydantic import TypeAdapter

# Set Up
total_story_words = 0
total_story_time_minutes = 0
overall_start_time = time.time()  # Start the overall timer

with open('chapter_drafts.txt', 'w', encoding='utf-8') as file:
            file.write(f"\n --- \n")

creative_writing_guidelines = """
        ---

        CREATIVE WRITING GUIDELINES (very important to follow when writing each chapter):

        Style & Audience:
        Write with clear and simple sentences at no higher than a high school reading level.
        Show rather than tell, but avoid melodrama or overly long descriptions.
        Reflect the power fantasy and cultivation genre, highlighting the main character's gradual growth and overcoming limits.
        Focus on pacing, excitement, and satisfaction, especially for a 15â€“25-year-old male audience.
        Avoid repetitive descriptions and keep the tone consistent.
        You may be flexible with language grammar and usage to maintain a suitable style.

        Content & World-Building:
        Introduce new terms and characters clearly.
        Write purposeful dialogue that reflects character personalities.
        Use action beats during dialouge sparingly and only to enhance tension or emotion.
        End the chapter with momentum, avoiding unnecessary recaps, reflection, or clichأ©s (e.g., falling asleep).
        Be specific about training and power progression as it is the core element of world-building.
        Describe a harsh, survival-focused world where the strong rule the weak; avoid an overly positive bias.
        Emphasize cunning or tactical decisions in fights, and bold the name of any action or technique that turns the tide of battle.

        Formatting & Final Output:
        The chapter should be at least 1,250 words long and no longer than 2,000 words long, adjusting as needed for the chapterâ€™s needs.
        When switching speakers or actions, start a new paragraph - even for single sentences.
        Paragraphs must have fewer than 4 sentences AND less than 50 words. Simply split big paragraphs into smaller ones, do not use semi-colons, compound words, or other tricks.
        Your response should include only the chapter text, with no extra commentary.

        ---
        """

progression_fantasy_plot_generator = """

        ---

        Progression Fantasy Plot Outline Generator

        You are tasked with generating a new outline for your next arc. Each arc should contribute to the protagonistâ€™s growth in skill, power, and narrative depth.
        The number of chapters and the main events in the arc should vary based on narrative needs.
        The structure must follow a clear beginning, middle, and end, ensuring escalation, progression, and resolution.
        Each chapter in the arc must be actively progressing the story. 

        REQUIREMENTS

        * In each arc the main character grows 2-4 sub-divisions of a rank in cultivation.
        * This arc must be between 13-27 chapters long, depending on how complex it is. Do not include more than 10 unique characters in the arc.
        * There must be at least 2 chapters tagged Power Up per arc.
        * If the story is finished simply return the word "Finished" and we can revise (must be precisely the word Finished)

        The arc should include:
        Inciting Incident: The event that disrupts the hero's status quo and sets the arc in motion.
        Early Challenges: Introduce minor obstacles that highlight the setting, power system, and potential allies.
        Progression Milestones: Points where the hero trains, discovers, or acquires something that directly contributes to their power or ability to confront the antagonist.
        Major Conflict: Escalating conflicts with antagonists or situations that test the hero's growth.
        Climactic Confrontation: A high-stakes battle or encounter where the hero uses new powers/skills to overcome the antagonist.
        Quick Resolution: Tying up loose ends, showing the impact of the arc on the world and characters, and transitioning to the next arc.

        Each chapter must include:
        Main Plot Point: The key narrative beats for that chapter.
        Subplot Focus: Secondary elements that enhance the emotional, thematic, or character-driven aspects of the story.
        Characters: List the characters that appear in each chapter. Ensure each character is unique to maintain a diverse roster. Limit the total number of unique characters across the arc to 10. For groups of side characters (e.g., villagers, bandits), refer to them collectively with a single name (e.g., 'villagers,' 'bandits') without numbering individual members.
        Tags: Categorize the chapter as None or Power Up (most chapters should be None, with Power Up for chapters with significant progression).

        Your response should be a series of Chapter Plot Outlines according to the following structure for each chapter in the arc. Strictly adhere to the outline structure and ensure a complete response.

        ---

        Chapter Plot Outline Structure:
        Chapter number.  **Title**
            *   **Main Plot Point:** *Description
            *   **Subplot Focus:** Description
            *   **Characters:** List the names of plot relevant characters that appear in the chapter. There should be less than 10 unique characters total across the arc. For groups of side characters (e.g., villagers, bandits), refer to them collectively with a single name (e.g., 'villagers,' 'bandits') without numbering individual members.
            *   **Tags:** None or Power Up

        ---

"""

system_instruction=f"""
        You are an experienced online writer with millions of fans.
        You are able to write compelling serialized fiction in the progression fantasy genre.
        You have read cultivation novels, shounen manga, and fantasy novels avidly.
        Your favorite series are Matrial God Asura, Naruto, Hunter x Hunter, Avatar the Last Airbender, and Martial World.
        You write what your readers love.

        ---

        OUTLINE CREATION GUIDELINES:

        Before and throughout the writing process you will be provided with outline and planning instructions.
        Please follow the directions provided. The instructions are intended to create an opportunity for you to plan your story.

        {creative_writing_guidelines}
"""

chat = client.chats.create(
    model=MODEL_ID,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=1.1,
        seed=50,
        #top_p=0.9,
        #top_k=20,
        presence_penalty=1.2,
        #frequency_penalty=0.0,
        #candidate_count=1,
        #max_output_tokens=100,
        #stop_sequences=["STOP!"],
    ),
)

delay = 2

def chat_with_retry(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = chat.send_message(prompt)
            time.sleep(delay)
            return response
        except ServerError as e:
            print(f"Server error: {e}. Retrying in {delay*10} seconds...")
            time.sleep(delay*10)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    print("Max retries reached. Unable to complete the request.")
    return None

# Initial Planning
prompt = '''

        Your task: Use this streamlined formula to design an engaging progression-fantasy setting centered in a cultivation world.

        The world should mix classic cultivation tropes like martial realms and ancient sects with fresh tropes from shounen manga and western fantasy.

        Aim for something that celebrates tropes but is still creative and unique.

        For example, introducing shounen adventure quests or power up transformations. Or including western fantasy epic monsters or magical academies.

        Ensure the setting is distinct and special without going overboard.

        Craft a setting appealing to young male readers aged 15-25, while focusing on the elements of the formula below.

        FORMULA FOR DESIGNING A CULTIVATION-WORLD SETTING

        Core Concept & Conflict
        Establish the main tension shaping your cultivation world. (e.g., a dark cultivator has fallen and sects are struggling to occupy the power gap, sects competing for dominance over a newly discovered spirit-rich continent, a celestial war is spilling into the mortal plane). Focus on how these conflicts impact individuals and the broader system, creating both personal struggles and world-spanning challenges.

        Geography & Environment
        Design a world that is distinct and memorable (e.g., tiered mountain ranges brimming with rare resources, high seas with powerful wandering spirits, fragmented heavens with divine remnants crashing to earth) the geography should shape the cultivation system and daily life. Dangerous environments might provide breakthroughs in power, while trade, survival, and travel must adapt to unique hazards or opportunities.

        Societal Structures
        Outline how power and authority are organized. Sects, clans, and factions vie for influence, with names and identities that make them stand out (e.g., Scarlet Lotus Sect, Iron Void Hall). Social hierarchies tied to cultivation levels (mortals, initiates, grandmasters) create built-in tension. Explore how these structures generate conflictâ€”perhaps lower disciples are treated as disposable, or failure in a breakthrough leads to public disgrace.

        Magic System (Cultivation)
        Develop a structured cultivation system that blends familiar elements with creative twists. What powers cultivation? (e.g., absorbing celestial essence, forging contracts with martial spirits, intense physical excersize under magical gravity). The system should be internally consistent to its own rules.

        Power Tiers
        Define 5 Mortal-realm ranks (e.g., Qi Foundation, Golden Core Ascendant) and 5 Immortal-realm ranks (e.g., Nascent Soul, Grandmaster). Each rank should be earned by achieving a unique internal breakthrough which makes something new possible. Some (not all) ranks have a unique visual or thematic flair, such as glowing runes or environmental phenomena.

        Power Progression
        There is always a quantitative measure of breakthrough (e.g., achiving 100 tons of strength, forming a 5-centimeter radius golden internal core, manifesting 1-33 tribulation clouds). It is very important to note what the specific measure (criteria) is for each rank. Each rank are sub-divided into minor success, major success, and finally peak success (where breakthrough is achieved).

        Secret (of the World)
        Introduce a hidden truth that could destabilize the world. (e.g., martial scriptures stolen from an ancient deity, there a conspiracy restricting who can truly ascend) Connect this secret to the protagonistâ€™s personal journey. (e.g., they discover a forbidden art tied to the secret, they forced to oppose the system and its rulers)


'''

response = chat_with_retry(prompt)

setting = response.text
print(response.text)

prompt = '''

        Your task: Use this streamlined formula to design an engaging main character and power fantasy arc.

        Your story is driven by our main character transforming from ordinary to godlike. He must explore the world and progress through the power system.

        Your readers are incredibly invested in this progression so we must plan it out. Understand that this fantasy will be achieved over hundreds of chapters and is a long term vision.

        Craft an essential fantasy for the story which appeals to young male readers aged 15-25. Use the formula below.

        FORMULA FOR DESIGNING THE ESSENTIAL FANTASY

        Main Character
        Origin & Upbringing
        Give the hero a distinct upbringing or hardship that molds them. (e.g., Raised in a hidden valley by a powerless sect? Descendant of outcast warriors?) Name them. They are a 15 year old boy.

        Motivation & Goals
        State a clear driving goal or desire (e.g., to master an art, avenge a loss, find a missing parent).

        Flaws & Challenges
        Choose two or three flaws that could hamper progression (e.g., impulsiveness, stubborn pride, social awkwardness).

        Mastering the World
        Outline key places to explore, treasures to discover, and history to learn. Focus on major milestones but allow for flexibility in the details.

        Mastering the Power System. List these extensively and in detail based on the setting. They should be relevant to the character.
        What tiers of power must they reach? (all of them) What must they learn to accomplish at each breakthrough?

        Mastering the Power System Part 2. Commit to the style and theme of the main character's powers, but leave room for the details to emerge during the writing process. Prioritze coolness, uniqueness, and synergy.
        What cultivation methods do they use? What techniques and skills must they learn? What equipment and weapons must they use?

        Internal Growth. Focus on major milestones but allow for flexibility in the details.
        Plan for the main characterâ€™s psychological and emotional development. What internal struggles will they face, and how will these shape their journey?

        Your Mission
        Use this formula to craft a detailed and compelling main character and essential fantasy. Follow the formula directly as written.

'''

response = chat_with_retry(prompt)

essential_fantasy = response.text
print(response.text)

first_arc_prompt = f'''

        Your task: Outline the plot for the first arc of a long-running series using my Progression Fantasy Plot Outline Generator.

        This arc can stand on its own (with its own villain, setting, and side-cast) yet still build toward a larger overarching narrative.

        You are writing a progression fantasyâ€”the kind of serial fiction where the hero steadily advances in skill, power, and reputation.

        It borrows from the classic Heroâ€™s Journey while incorporating progression fantasy hallmarks: training arcs, stong enemies, magical power systems, and repeated cycles of growth and challenge.

        {progression_fantasy_plot_generator}

        Since this is your first arc I want to offer you some ideas. Keep in mind these are not direct suggestions just inspiration:

        Chapter 1:
        The protagonist lives in humble and ordinary conditions as a commoner. This chapter focuses on the main character, their life, dream, and relationships. World building is subtley included but not a focus yet. Something or someone spurs them to leave their routine.

        Variations:
        A. Outside Threat: A beast or army arrives at their doorstep, pushing them to act.
        B. Call to the Masses: An important and powerful figure calls for a new era, calling the masses towards some mission or dream.
        C. An Omen or Prophetic Dream: The hero experiences a cryptic vision or a recurring nightmare hinting at their destiny, leaving them no choice but to investigate its meaning.

        Chapter 2:
        The hero takes their first real step on the journey. They leave behind family/friends/shrine to venture to a nearby town or region. Early demonstration of basic skills or magic. Early world-building begins.

        Variations:
        A. Stolen Start: The hero's gear or resources are stolen by a mischievous thief, leading to a chase that inadvertently sets them on the right path.
        B. Rival Encounter: They meet a future rival with a contradictory worldview.
        C. Unexpected Hazard: A sudden natural disaster (flood, earthquake, magical storm) forces the hero to take a dangerous detour, revealing some skills.

        Chapter 3:
        The hero meets key companionsâ€”maybe an older advisor, a peer with knowledge of local threats, or a potential love interest. They form a small traveling group or at least a temporary alliance.

        Variations:
        A. Stranger in Need: The hero saves someone in peril who later reveals hidden talents or crucial knowledge about the journey ahead.
        B. Shady Ally: Someone with questionable motives joinsâ€”will they betray or remain loyal?
        C. Common Purpose: Everyone wants to reach the same city or famed training ground.

        Chapter 4:
        Introduce local/regional power structures: an oppressive faction, a dangerous monster clan, or a martial arts sect that rules the area. The hero learns how strong the opposition truly is. The basic power system is explained in this chapter.

        Variations:
        A. Corrupt Guild: A group extorts villages for resources.
        B. Nobleâ€™s Court: The hero is awed by the grandeur and realizes theyâ€™re an outsider.
        C. Ritual Arena: The hero stumbles upon an ongoing competition or ceremonial duel where the regionâ€™s strongest fighters display their prowess.

        Chapter 5:
        The hero and allies concoct a plan or attempt a smaller-scale mission against the weaker minions of the main threat. Their motives align realistically. They succeed in a comedic or creative way, building confidence.

        Variations:
        A. Disguise or Trickery: They fool minor enemies to steal resources or rescue someone.
        B. Rigged Contest: The team enters a local contest or challenge to gain access or resources. However, the contest is rigged to favor the team's opposition.
        C. Magical Experiment: The hero tries out a new spell/technique with chaotic and comedic side effects.

        Chapter 6:
        While looting or exploring, they discover a special item, hidden technique, or minor power-up assisting future success. (unique weapon, training manual, magic tool, etc).

        Variations:
        A. Hidden Technique: Incomplete instructions once used by a famed cultivator. Boosts the hero's power in an awesome and useful way.
        B. Unique Weapon or Equipment: Found or stolen, adds a new capability to the hero's arsenal.
        C. Cultivation Resource: Valuable resource for the hero's current rank and cultivation method. Boosts the hero's power directly.

        Chapter 7:
        Enemy or rival forces realize someone is interfering. Their leader mobilizes or investigates. Tension escalates: the heroâ€™s small victory attracts big trouble.

        Variations:
        A. Bounty Posted: A reward is offered for capturing the hero.
        B. Rivalâ€™s Notice: A more powerful enemy champion or rival is sent after them.
        C. Direct Threat: The villain threatens and destroys the property of innocents citing the protaganists actions as the cause, sending a clear message.

        Chapter 8:
        The antagonistâ€™s forces confront the hero publicly, demanding surrender or retribution. The hero, determined, refuses. The scale of the villainâ€™s power is made clear.

        Variations:
        A. Duel Challenge: The big bad or second-in-command challenges the hero in front of crowds.
        B. Enemy Show of Force: The villain harms innocents, destroys a landmark, obliterates a small resistance force, or magically alters the environment to make their superiority clear.
        C. Heroâ€™s Hubris: The hero believes new abilities will suffice. The hero confronts the villain directl. They are about to be humbled.

        Chapter 9:
        The hero tries to fight or outsmart the villain (or top lieutenant) but is crushingly beaten. A specific strength of the villain's powers are showcased. They lose a crucial item, or an ally is captured, and the hero barely escapes. True defeat.

        Variations:
        A. Betrayal: A supposed ally sells them out.
        B. Psychological Blow: The villain humiliates them publicly, harming the heroâ€™s resolve.
        C. Unleashed Chaos: The heroâ€™s failure accidentally triggers a larger disaster (releasing a monstrous creature, damaging a sacred site, etc).

        Chapter 10:
        The hero survives but is at a low point. They resolve to gain new power, find a better strategy, and return to defeat their opponent. Specifically, they remember the key strength of the villain which they must learn to counter. This sets the arcâ€™s mid-point turn. The hero must leave to seek new strength.

        Variations:
        A. Information Quest: The hero uncovers rumors about a secluded mentor or hidden training ground that holds the key to countering the villainâ€™s power. They embark on a journey to find it, requiring following clues.
        B. Self-Imposed Trial: Instead of seeking external help, the hero restricts themselves to a harsh training ground (e.g., barren mountains or a treacherous forest) where they impose brutal physical and mental challenges to hone their skills. Perhaps extreme restrictions are self-imposed too.
        C. Dangerous Return: The hero awakens in enemy territory or another perilous land. They fight their way back to familiar ground while learning vital survival skills and gaining insights that spark their determination.

        Chapter 11:
        The hero finds a mentor, a partner, or a unique challenge to train. They practice a specific technique to progress their current cultivation rank success. The training also directly develops the hero's ability to counter the villain. Training techniques should be cool and conceptually satisfying.

        Variations:
        A. Eccentric Mentor: A comedic, mysterious, or otherwise quirky figure who trains the hero intensely.
        B. Training Partner: The hero finds a training parter. They are either collaborative allies or a competitive rivals.
        C. Impossible Feat: The hero must learn to perform a currently impossible feat to unlock a higher tier of power. (cut a waterfall, survive 100 times gravity, etc.)

        Chapter 12:
        The hero endures grueling training pushing their mental and physical limits. Show specific training drills, internal struggles, moments of frustration, and the precise epiphanies that lead to growth. The training directly develops the hero's ability to counter the villain.

        Variations:
        A. Struggle of Character: The hero must struggle with their own weaknesses of character to perservere and grow.
        B. External Struggle: The hero must continue to struggle against their training and environment intensely.
        C. Knowledge Gap: The hero must figure out a essential trick or change in perspective about a skill.

        Chapter 13:
        The mentor deems the hero worthy. They unlock or master a signature technique or achieve a crucial power increase (addressing the villain's key power). The hero is now prepared to face the main threat again.

        Variations:
        A. Timed Rite: The hero finishes right as the villainâ€™s next move begins.
        B. Breakthrough: The hero achieves a breakthrough linked to his powers, adding a new flair to their abilities which is hinted at.
        C. Parting Gift: A new weapon, magical artifact, or blessing is given to the hero.

        Chapter 14:
        The hero goes back to the antagonistâ€™s stronghold or territory. Possibly uses stealth or infiltration to reclaim lost items or allies. A major confrontation is imminent.

        Variations:
        A. Recon First: The hero scouts carefully, showing new caution.
        B. Guns Blazing: The hero breaks and enters into the villain's lair, inviting the villain to a final duel.
        C. Double Agents: Allies pretending to be the villainâ€™s minions assist from within.

        Chapter 15:
        The hero engages the villain or top lieutenants. Although improved, the hero is tested at every step. We see how the hero's preperation interacts with the villain's key powers. The antagonistâ€™s minions or environment pose serious challenges too.

        Variations:
        A. Living Battlefield: The environment actively hinders the hero (shifting terrain, cursed forest, or enchanted structures).
        B. Coordinated Attack: Allies assault from different angles. It is a battle on a few fronts.
        C. Revelation Countdown: The villain reveals hidden powers or an even bigger plan. This puts the hero in a countdown.

        Chapter 16:
        The villain unleashes a trump card or final form (must feel justified). The hero is exhausted, their companions in danger, and the situation appears dire. The villain's motivations are revealed in full.

        Variations:
        A. Emotional Blow: The heroâ€™s mentor or friend is struck down, fueling rage.
        B. Collapsing Arena: The battlefield is literally falling apart (fire, quake, magical overload).
        C. Treachery: One of the heroâ€™s allies panics or betrays them at the worst moment.

        Chapter 17:
        The hero faces a crisis of faith. They recall their training, find new resolve, or unlock the next level of power (power boosts are kept reasonable). The heroâ€™s willpower surges, turning the tide. Intense tension.

        Variations:
        A. Combined Power: Allies channel their energy into the hero or form a synergy attack.
        B. Spiritual Awakening: A cameo or flashback from the heroâ€™s ancestor or deity.
        C. Heightened Emotion: Extreme emotions allow the hero to achieve new levels of strength.

        Chapter 18:
        The hero unleashes a new, heightened form, technique, or synergy (power boosts are kept reasonable). The tide of battle flips decisively. The villainâ€™s shock is palpable.

        Variations:
        A. Berserk Edge: The hero is nearly consumed by the surge and must maintain control.
        B. Unique Element: The hero realized how to apply his powers in a new and surprising way.
        C. Force of Nature: The environment reacts, storms or ground quakes, emphasizing the powerâ€™s scale.

        Chapter 19:
        The villain is defeated or forced to flee. The hero and allies take stock of the damage. The region/town is freed from tyranny. Thereâ€™s a moment to reflect on whatâ€™s been gained and lost.

        Variations:
        A. Heroic Funeral: They honor fallen allies or mentors.
        B. Huge Party: The hero, allies, and innocents party together with food and dance. They celebrate late into the night.
        C. Vanishing Villain: The antagonist escapes with a warning of bigger threats.

        Chapter 20:
        After a brief period of rest (or forced departure), the hero sets off again. They must continue their journey for reasons such as seeking further mastery, discovering bigger mysteries, or stopping larger foes in distant lands.

        Variations:
        A. New Allies: One or two supporting characters join the hero for the next arc.
        B. Parting Gift: The grateful town bestows a unique , gift, or blessing.
        C. Cliffhanger: Another powerful individual or faction learns about the heroâ€™s feats and starts moving against them.

        Reminder - your outline should be in the following structure:

        ---

        Chapter Plot Outline Structure:
        Chapter number.  **Title**
            *   **Main Plot Point:** Description
            *   **Subplot Focus:** Description
            *   **Characters:** List the names of plot relevant characters that appear in the chapter. You must ensure less than 10 characters are tagged in total for your entire plot outline. For groups of side characters (e.g., villagers, bandits), refer to them collectively with a single name (e.g., 'villagers,' 'bandits') without numbering individual members.
            *   **Tags:** None or Power Up

        ---

'''

class Chapter(BaseModel):
    number: int  # Chapter number as an integer
    title: str
    main_plot_point: str
    subplot_focus: str
    characters: list[str]  # List of character names
    tags: list[str]        # List of tags for the chapter

class CharacterDescription(BaseModel):
    name: str
    background: str
    goal: str
    flaws: str
    appearance: str
    personality: str

# Generate schema
chapter_schema = Chapter.model_json_schema()
chapter_schema_json = json.dumps(chapter_schema)

character_descriptions_schema = CharacterDescription.model_json_schema()
character_descriptions_schema_json = json.dumps(character_descriptions_schema)

def ensure_review_tag(chapters: list[Chapter]):
  # Ensure we have enough chapters to apply logic
  if len(chapters) < 2:
      return  # Not enough chapters to apply logic

  # Get the last 5 chapters (or fewer if less than 5 exist)
  last_5_chapters = chapters[-5:]

  # Check if any chapter in the last 5 has the 'Writing Review' tag
  review_tag_present = any('Writing Review' in chapter.tags for chapter in last_5_chapters)

  # If 'Writing Review' is not present, replace the first 'None' tag working backward from second-to-last
  if not review_tag_present:
      for chapter in reversed(chapters[:-1]):  # Iterate backward, excluding the last chapter
          if 'None' in chapter.tags:  # Check for the 'None' tag
              chapter.tags[chapter.tags.index('None')] = 'Writing Review'  # Replace the first occurrence of 'None'
              print(f"'Writing Review' tag replaced 'None' in Chapter {chapter.number}")
              break
      else:
          # If no 'None' tag is found, append 'Writing Review' to the second-to-last chapter
          second_to_last_chapter = chapters[-2]
          second_to_last_chapter.tags.append('Writing Review')
          print(f"'Writing Review' tag added to Chapter {second_to_last_chapter.number}")

# Main Loop
story_finished = False
chapter_drafts = []
character_powers = ""
arc_stats = []
total_words = 0
first_iteration = True  # Flag to identify the first iteration

while not story_finished:
    arc_start_time = time.time()  # Start timer for the arc
    arc_word_count = 0
    chapter_stats = []

    # Step 1: Generate the next arc
    if first_iteration:
        prompt = first_arc_prompt # Special plotting prompt for the first loop
    else:
        prompt = progression_fantasy_plot_generator # Standard arc prompt for subsequent iterations

    response = chat_with_retry(prompt)
    plot = response.text
    print(f"Plot generated: {plot}")

    if plot == "Finished":
        story_finished = True
        print("The story is finished! Ready for revision.")
        break  # Exit the loop

    # Step 2: Generate plot outline and character description objects
    parse_prompt = f"""

    Please analyze the provided plot outline and return a structured output in JSON format that adheres to the following schema:

    {chapter_schema_json}

    Here is the plot outline. Please ensure all details are preserved. Ensure all characters listed are unique:

    """ + plot

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=parse_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0,
        ),
    )
    time.sleep(delay)  # Rate limiting
    response_data = json.loads(response.text)
    chapters = TypeAdapter(list[Chapter]).validate_python(response_data)
    ensure_review_tag(chapters)
    print(f"Chapter outline objects generated: {chapters}")

    # Extract unique characters and generate descriptions (unchanged)
    unique_characters = set()
    for chapter in chapters:
        unique_characters.update(chapter.characters)

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
    response = chat_with_retry(description_prompt)
    character_descriptions = response.text
    print(f"Character descriptions generated: {character_descriptions}")

    parse_prompt_characters = f"""

    Please analyze the provided plot outline and return a structured output in JSON format that adheres to the following schema:

    {character_descriptions_schema_json}

    Here is the plot outline. Please ensure all details are preserved. Ensure all characters listed are unique:

    """ + character_descriptions

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=parse_prompt_characters,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0,
        ),
    )
    time.sleep(delay)  # Rate limiting
    response_data = json.loads(response.text)
    character_descriptions = TypeAdapter(list[CharacterDescription]).validate_python(response_data)
    print(f"Generated character descriptions objects: {character_descriptions}")

    # Step 3: Parse arc and generate chapters
    for draft_number in range(0, len(chapters)):  # This covers chapters 1 to 20

        chapter_start_time = time.time()  # Start timing for this chapter

        context_parts = []
        for name in chapter.characters:
            cd = next((cd for cd in character_descriptions if cd.name == name), None)
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

        prompt = f"""

        Write chapter {chapters[draft_number].number} of the story according to the following outline:

        Title: {chapters[draft_number].title}
        Main Plot Point: {chapters[draft_number].main_plot_point}
        Subplot Focus: {chapters[draft_number].subplot_focus}

        Here are the character descriptions for this chapter. Please reference them for accurate details and dialouge:
        {context}

        {creative_writing_guidelines}

        """
        # For Debugging: print("Here is the writer prompt: \n" + prompt)
        response = chat_with_retry(prompt)
        chapter_text = response.text
        # Save Progress
        with open('chapter_drafts.txt', 'a', encoding='utf-16') as file:
            file.write(f"\n --- \n")
            file.write(response.text)
            file.write("\n\n")
        time.sleep(delay)  # Rate limiting
        print(f"Chapter {chapters[draft_number].number} written and added to draft!")

        # Check if this is a predetermined iteration to update character powers
        for tag in chapters[draft_number].tags:
          if tag == "Power Up":
            power_update_prompt = f"""

            Great job so far! Here is a reminder of the essential fantasy for your story: {essential_fantasy}

            I want you to create an updated main character power sheet according to the following outline.

            Doing so is not meant to rush the story.
            You are reminding yourself of the main purpose and essential fantasy of the story as well as tracking your progress towards its realization.

            ---
            Here are the old main character powers. Please update them in a new sheet:
            {character_powers}

            ---

            Please only include these fields in your responce. Update the sheet according to account for recent power progression. Be specific:

            (Main Character Name) Power Sheet

            Cultivation Rank: Rank, Level of Success (none, minor, major, peak), Realm

            Cultivation Method: Description.

            Combat Talent (relative to rank) which determines how many sub-divisions above their rank they can match: Number.

            Martial Techniques: Description.

            Weapons and Equipment: Description.

            Past Power Ups: Description. (Brief but exhaustive list of all fortunate encounters, training boosts, and mid-fight breakthroughs)

            """
            power_response = chat_with_retry(power_update_prompt)
            character_powers = power_response.text  # Update the character powers description
            print(power_response.text)

          if tag == "Writing Review":
            print(f"Writing Review requested.")
            combined_chapters = ""
            with open('chapter_drafts.txt', 'r', encoding='utf-16') as file:
                combined_chapters = file.read()

            response = client.models.generate_content(
            model=MODEL_ID,
            contents="""

            You are a 15 year old boy who loves reading power fantasy and cultivation novels.
            You want to see the main character gradually overcome their limits in a satisfying way. You are not looking for literary fiction, but instead fun genre fiction.
            Please read the following story and write a fan letter to the author.
            Do not critique the writing style but instead focus on what you liked most and what you would like to see next.
            Tell them a little about yourself too (average reader of the genre) including your name.
            Make it realistic not exaggerated. In your response provide only the letter contents. Here is the story so far:

            """ + combined_chapters,
            )

            # Calculate the average word count for the last 5 chapters
            last_5_chapters = chapter_stats[-5:]  # Get the stats for the last 5 chapters
            average_word_count_last_5 = sum(chapter['Words'] for chapter in last_5_chapters) / len(last_5_chapters)

            review = f"""
            Your average word count in your last 5 chapters is {average_word_count_last_5:.2f}.

            Please review your creative writing guidelines closely to ensure you stick to them no matter what.
            Score yourself out of 10 on each specific guideline and commit to them going forward.
            Trust these guidelines over conventional writing rules. (VERY IMPORTANT)

            {creative_writing_guidelines}

            Here is a letter we got from a reader of yours. Take their words as encouragement but keep in mind that other readers of yours might have different opinions.
            Use your best judgement about their feedback to start thinking about the next arc. Do not outline yet. Note things that are working well and things to try next arc:

            {response.text}
            """
            time.sleep(delay)  # Rate limiting
            print(review)

            review_response = chat_with_retry(review)
            print(review_response.text)

        # Stats for the chapter
        word_count = len(chapter_text.split())
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
        print(f"Chapter {chapters[draft_number].number} stats recorded! Wrote {word_count} words. Generated for {chapter_time:.2f} seconds."
              f"This is a rate of {words_per_minute:.2f} words-per-minute.")

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
        'Chapters': len(chapters),
        'Chapter Stats': chapter_stats,
    })

    # Save stats
    with open('arc_stats.txt', 'a', encoding='utf-16') as arc_file:
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
    print(f"    Chapters: {len(chapters)}")
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
