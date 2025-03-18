desired_arcs : int

def get_prompts(desired_arcs):
    progression_fantasy_plot_generator = f"""

            ---

            Progression Fantasy Plot Outline Generator

            You are tasked with generating a new outline for your next arc. Each arc should contribute to the protagonist's growth in skill, power, and narrative depth.
            Your story should have {desired_arcs} arcs in total. Arc {desired_arcs} must conclude the story.
            The number of chapters and the main events in the arc should vary based on narrative needs.
            The structure must follow a clear beginning, middle, and end, ensuring escalation, progression, and resolution.
            Each chapter in the arc must be actively progressing the story. 

            REQUIREMENTS

            * In each arc the main character must grow 1 full rank in cultivation. (half-step and breakthrough).
            * This arc must be between 12, 16, or 20 chapters long, depending on how complex it is. Do not include more than 10 unique characters in the arc.
            * There must be at least 2 chapters tagged Power Up per arc.
            * If the story is finished simply return the word "Finished" and we can revise (must be precisely the word Finished)

            The arc should include:
            Inciting Incident: The event that disrupts the hero's status quo and sets the arc in motion.
            Early Challenges: Introduce minor obstacles that highlight the setting, power system, and potential allies.
            Progression Milestones: Points where the hero trains, discovers, or acquires something that directly contributes to their power or ability to confront the antagonist.
            Major Conflict: Escalating conflicts with antagonists or situations that test the hero's growth.
            Power Progression: Main character grows by a half-step and achieves a breakthrough in every single arc.
            Climactic Confrontation: A high-stakes battle or encounter where the hero uses new powers/skills to overcome the antagonist.
            Quick Resolution: Tying up loose ends, showing the impact of the arc on the world and characters, and transitioning to the next arc.

            Each chapter must include:
            Main Plot Point: The key narrative beats for that chapter including power progression.
            Subplot Focus: Secondary elements that enhance the emotional, thematic, or character-driven aspects of the story.
            Characters: List the characters that appear in each chapter. Ensure each character is unique to maintain a diverse roster. Limit the total number of unique characters across the arc to 10. For groups of side characters (e.g., villagers, bandits), refer to them collectively with a single name (e.g., 'villagers,' 'bandits') without numbering individual members.
            Tags: Categorize the chapter as None or Power Up (most chapters should be None, with Power Up for chapters with significant progression).

            Your response should be a series of Chapter Plot Outlines according to the following structure for each chapter in the arc. Strictly adhere to the outline structure and ensure a complete response.

            ---

            Chapter Plot Outline Structure:
                *   **Chapter number**
                *   **Title**
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
    """
    planner_guidelines = f"""
            ---

            OUTLINE CREATION GUIDELINES:

            Before and throughout the writing process you will be provided with outline and planning instructions.
            Please follow the directions provided. The instructions are intended to create an opportunity for you to plan your story.

    """

    expander_guidelines = f"""
            ---

            OUTLINE EXPANDER GUIDELINES:

            Your task is to expand chapter outlines into detailed plot structures for batches of 4 chapters. 
            Each chapter should support 2500 words when written. 
            Ensure the following for each chapter outline:

            - **Main Plot Point:** Clearly describe the central event or challenge.
            - **Subplot Focus:** Expand secondary storylines, connecting them to the main plot.
            - **5 Scenes:** Provide detailed descriptions of each scene. Each scene should:
                - Support 500 words of narrative content.
                - Be described with 5 sentences / story beats.
                    - Example Scene Description: Scene 1 Morning Chores: The chapter opens with Ren performing his daily chores. He is shown carrying heavy stone blocks up a hill, muscles straining. The villagers, smaller and less physically imposing, are performing simpler tasks like tending to crops. Ren is fast and efficient, but also impatient. He tries to use the *Mountain's Breath* technique to make the work easier, but fails to use the ability. This frustration is made visible in his expression, which is noticed by his grandfather from the porch.
                - Contribute to the development of the plot.
                - Transition smoothly into the next scene to maintain pacing.
            - **Ending:** Ensure a compelling hook or unresolved element propels readers forward.

            Your response should be in the following structure:

            ---

            Expanded Chapter Plot Outline Structure:
                * **Chapter Number**: Number
                * **Main Plot Point:** Expanded Description
                * **Subplot Focus:** Expanded Description
                * **Scene 1:** Expanded Description
                * **Scene 2:** Expanded Description
                * **Scene 3:** Expanded Description
                * **Scene 4: Expanded Description
                * **Scene 5: Expanded Description
                * **Ending:** Expanded Description.

            ---

    """

    writer_guidelines = """
            ---

            CREATIVE WRITING GUIDELINES (Follow these closely when writing each chapter)

            1. Writing Process: 
                * You will be provided with a chapter outline and relevant character descriptions.
                * Expand all 5 scenes thoughtfully to develop the narrative as outlined.
                * Use clear, simple sentences (no higher than high school reading level).
                * Use 3rd person limited viewpoint.
                * Be loose with grammar and usage to maximize readability.
                * Add action and world building scenes when needed to increase word count.

            2. Content:
                * You may bend any rules to create the best story possible.
                * Your target readers are boys age 15-25 interested in the progression fantasy genre.
                * Introduce new terms, concepts, and characters clearly and naturally.
                * Show, don't tell, but avoid melodrama and overly detailed descriptions.
                * Craft dialogue that reflects distinct character personalities, using action beats sparingly to enhance tension or emotion.
                * End chapters with forward momentum. Avoid unnecessary recaps, internal monologues, or clichés (e.g., "falling asleep").
                * Highlight power progression and training explicitly as core elements of the story.
                * Depict a harsh, survival-driven world where the strong dominate, avoiding excessive optimism.
                * Showcase creativity and tactics in fights, emphasizing strategy over brute force.
            ---
            """

    # Initial Planning
    setting_prompt = f'''

            Your task: Use this streamlined formula to design an engaging progression-fantasy setting centered in a cultivation world.

            The world should mix classic cultivation tropes like cultivation ranks and ancient sects with fresh tropes from shounen manga and western fantasy.

            Aim for something unique that celebrates tropes but is still creative.

            For example, introducing shounen adventure quests or power up transformations. Or including western fantasy epic monsters or magical academies.

            This setting should be sized to be exlpored in the length of a novella.

            Craft a setting appealing to young male readers aged 15-25, while focusing on the elements of the formula below.

            FORMULA FOR DESIGNING A CULTIVATION-WORLD SETTING

            Core Concept & Conflict
            Establish the main tension shaping your cultivation world. (e.g., a dark cultivator has fallen and sects are struggling to occupy the power gap, sects competing for dominance over a newly discovered spirit-rich continent, a celestial war is spilling into the mortal plane). Focus on how these conflicts impact individuals and the broader system, creating both personal struggles and world-spanning challenges.

            Geography & Environment
            Design a world that is distinct and memorable (e.g., tiered mountain ranges brimming with rare resources, high seas with powerful wandering spirits, fragmented heavens with divine remnants crashing to earth) the geography should shape the cultivation system and daily life. Dangerous environments might provide breakthroughs in power, while trade, survival, and travel must adapt to unique hazards or opportunities.

            Societal Structures
            Outline how power and authority are organized. Sects, clans, and factions vie for influence, with names and identities that make them stand out (e.g., Scarlet Lotus Sect, Iron Void Hall). Social hierarchies tied to cultivation levels (mortals, initiates, grandmasters) create built-in tension. Explore how these structures generate conflict. Perhaps lower disciples are treated as disposable or failure in a breakthrough leads to public disgrace.

            Magic System (Cultivation)
            Develop a structured cultivation system that blends familiar elements with creative twists. What powers cultivation? (e.g., absorbing celestial essence, forging contracts with martial spirits, intense physical excersize under magical gravity). The system should be internally consistent to its own rules.

            Power Tiers
            Define {desired_arcs} martial ranks (e.g., Qi Foundation, Golden Core Ascendant, Nascent Soul) with a creative theme. Each rank should be earned by achieving a unique internal breakthrough which makes something new possible. Each rank is seperated by a single 'half-step' sub-division before breakthrough. To clarify: half-step rank 1, rank 1 breakthrough, half-step rank 2, rank 2 breakthrough, ... , half-step rank {desired_arcs}, and finally rank {desired_arcs} breakthrough. There are no further ranks.

            Power Progression
            There is always a quantitative measure of breakthrough (e.g., lifting a 500 catty stone, forming a 5-centimeter radius golden internal core, manifesting 1-33 tribulation clouds). It is very important to note what the specific measure (criteria) is for each rank. Be creative.

            Secret (of the World)
            Introduce a hidden truth that could destabilize the world. (e.g., martial scriptures stolen from an ancient deity, there a conspiracy restricting who can truly ascend) Connect this secret to the protagonist's personal journey. (e.g., they discover a forbidden art tied to the secret, they forced to oppose the system and its rulers)

            Story Ending
            Plan a conclusion to the main tension which involves the secret of the world. This should end the story without implying or requiring any further narrative development.

    '''

    ef_prompt = f'''

            Your task: Use this streamlined formula to design an engaging main character and power fantasy arc.

            Your story is driven by our main character transforming from ordinary to the martial peak. He must explore the world and progress through the power system.

            Your readers are incredibly invested in this progression so we must plan it out. Understand that this fantasy will be fully achieved in {desired_arcs} arcs (around {(desired_arcs*20)-10} chapters).

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
            What cultivation method do they use (only 1)? What {desired_arcs} named techniques must they use? What martial skills must they learn? What equipment and weapons must they use?

            Internal Growth. Focus on major milestones but allow for flexibility in the details.
            Plan for the main character's psychological and emotional development. What internal struggles will they face, and how will these shape their journey?

            Arc Outline 
            Plan the milestones over {desired_arcs} arcs. Enumerate the arcs (1 to {desired_arcs}) and list the milestones for each one. Restate the ending clearly.

            Your Mission
            Use this formula to craft a detailed and compelling main character and essential fantasy. Follow the formula directly as written.

    '''

    first_arc_prompt = f'''

            Your task: Outline the plot for the first arc of a long-running series using my Progression Fantasy Plot Outline Generator.

            This arc can stand on its own (with its own villain, setting, and side-cast) yet still build toward a larger overarching narrative.

            You are writing a progression fantasy. It is serial fiction where the hero steadily advances in skill, power, and reputation.

            It borrows from the classic Hero's Journey while incorporating progression fantasy hallmarks: training arcs, stong enemies, magical power systems, and repeated cycles of growth and challenge.

            {progression_fantasy_plot_generator}

            Since this is your first arc I want to offer you some ideas. Keep in mind these are not direct suggestions just inspiration. You should adapt these ideas to suit your purposes:

            Chapter 1: The Hook
            The protagonist's ordinary life is immediately disrupted by a significant threat or call. World-building and character establishment are woven through action. The inciting incident occurs within the first few scenes.
            Variations:
            a. A powerful cultivator's disciple arrives in the village seeking talent, just as bandits attack
            b. Time freezes for everyone except the hero during a festival, forcing them to prevent a catastrophe alone
            c. The hero's shadow gains sentience and warns them of approaching doom, but no one believes them until it's almost too late

            Chapter 2: First Steps
            The hero must immediately deal with the aftermath of Chapter 1's crisis, leading them to leave their home. They demonstrate basic abilities while coping with the situation.
            Variations:
            a. The hero pursues bandits who stole their family's treasured heirloom
            b. A mysterious door appears in their house, leading to a dangerous spirit realm they must traverse
            c. Their hometown is shrinking, literally getting smaller by the day, forcing them to find the cause before everyone is crushed

            Chapter 3: Companions and Complications
            While dealing with the ongoing crisis, the hero meets key allies who have their own stakes in the situation. These meetings occur during tense moments rather than casual encounters.
            Variations:
            a. A wandering swordsman saves the hero from ambush and offers to teach them
            b. A rival cultivator becomes an ally after they both witness a terrifying prophecy in shared dreamspace
            c. The hero meets a talking weapon that can only manifest its power when they argue with each other

            Chapter 4: Power Structures
            The hero and allies discover the true scope of their opposition. Their early actions have attracted attention from major factions. The basic power system is explained through demonstration rather than exposition.
            Variations:
            a. A martial arts tournament reveals the strict hierarchy of the local sects
            b. The hero discovers that powerful cultivators literally rewrite reality around themselves, creating zones of altered physics
            c. Power in the region is determined by who can tame and ride living storms, with the strongest riding hurricanes

            Chapter 5: Building Strength
            The hero and allies attempt their first coordinated action against the opposition. They succeed in a clever way but realize they need much more power.
            Variations:
            a. They infiltrate a bandit camp to rescue hostages using disguises and basic martial arts
            b. They challenge the enemy to a contest where cultivation energy must be used to create living art
            c. They discover they can temporarily borrow power from their future selves, but at a dangerous cost

            Chapter 6: The Game-Changer
            During their operation, they discover something that changes their understanding of their situation and provides a path to power.
            Variations:
            a. An ancient manual revealing the true form of a basic technique everyone uses incorrectly
            b. A living tattoo that teaches martial arts by forcing the body to move in specific patterns
            c. A cultivation method that requires absorbing the memories of falling leaves, each containing fragments of long-dead cultivators' experiences

            Chapter 7: Rising Tension
            The enemy responds to the hero's actions with overwhelming force. The stakes escalate dramatically.
            Variations:
            a. The villain sends their elite disciples to make an example of the hero's supporters
            b. The enemy triggers a phenomenon that begins turning everyone's cultivation energy against them
            c. The villain reveals they've been cultivating by stealing people's shadows, and those without shadows become their puppets

            Chapter 8: First Major Defeat
            The hero's group confronts the main threat and is thoroughly outmatched. The defeat is decisive and changes the story's direction.
            Variations:
            a. The villain easily counters every technique and leaves the hero broken and humiliated
            b. The hero's strongest attack is absorbed and turned into a dark mirror version of themselves
            c. The villain reveals they can trade permanent injuries for temporary power, sacrificing their own body to overwhelm the hero

            Chapter 9: Recovery and Revelation
            While recovering from defeat, the hero learns crucial information about their opponent's powers and their own potential.
            Variations:
            a. A retired grandmaster reveals the villain's technique has a fundamental flaw
            b. The hero discovers they can see cultivation paths as physical roads in the sky while delirious from injuries
            c. Their near-death experience allows them to communicate with their alternate selves from failed timelines

            Chapter 10: The Training Ground
            The hero begins intense training specifically designed to counter the villain's abilities. Training is active and dangerous rather than passive learning.
            Variations:
            a. Training in a valley where gravity fluctuates unpredictably, forcing constant adaptation
            b. Learning to fight inside paintings, where the laws of reality follow artistic principles
            c. Training by reliving their worst moments in a time loop, each iteration making the challenge harder until they perfect their response

            Chapter 11: Mastery and Growth
            The hero's training reaches its peak. They master their new abilities through a supreme test.
            Variations:
            a. Defeating their master in combat by finding a way past their perfect defense
            b. Achieving enlightenment by successfully mediating a war between elemental spirits
            c. Learning to manipulate cause and effect by planting a tree yesterday that they needed today

            Chapter 12: Return to Battle
            The hero brings the fight back to their opponent, now armed with new abilities and understanding.
            Variations:
            a. They challenge the villain's forces during an important ceremony, disrupting their power base
            b. They turn the villain's fortress into a giant cultivation formation that restricts certain types of techniques
            c. They initiate combat by trading their memories of victory for the power to ensure that victory occurs

            Chapter 13: The Confrontation
            The final battle begins. The hero demonstrates their growth but faces unexpected challenges.
            Variations:
            a. A straightforward but intense duel that devastates the surrounding landscape
            b. The battle shifts between physical combat and contests of reality-shaping willpower
            c. Each exchange of blows creates alternate timelines that both fighters must navigate simultaneously

            Chapter 14: Climactic Moment
            The villain reveals their full power while the hero unlocks their true potential. The battle reaches its peak.
            Variations:
            a. The hero overcomes the villain's ultimate technique through determination and perfect execution
            b. Both fighters ascend to a higher plane of existence where thoughts become attacks
            c. The hero wins by purposely losing in all alternate timelines, concentrating all their victory potential into a single decisive moment

            Chapter 15: Resolution
            The villain is defeated, but the victory reveals new challenges ahead. The immediate threat is handled while bigger mysteries unfold.
            Variations:
            a. The villain's defeat creates a power vacuum that multiple factions rush to fill
            b. Their victory breaks a seal holding back ancient beings who view modern cultivation as heresy
            c. Defeating the villain merges all timeline variants of the hero into one being with multiple sets of memories and powers

            Chapter 16: New Horizons
            The hero sets off toward new challenges, changed by their experiences but ready for more.
            Variations:
            a. The hero leaves to challenge stronger opponents in the wider world
            b. They begin a quest to unite the fragmented realms of heaven and earth
            c. The hero must travel back through their own timeline, protecting their younger self while avoiding paradox

            Reminder - your outline should be in the following structure:

            ---

            Chapter Plot Outline Structure:
                *   **Chapter Number** 
                *   **Title**
                *   **Main Plot Point:** Description
                *   **Subplot Focus:** Description
                *   **Characters:** List named characters that appear in the chapter. You must ensure less than 10 characters are tagged in total for your entire plot outline. For groups of side characters (e.g., villagers, bandits), refer to them collectively with a single name (e.g., 'villagers,' 'bandits') without numbering individual members. Names should be listed consistently without adding descriptions or qualifiers for seperate mentions of the same character.
                *   **Tags:** None or Power Up

            ---

    '''

    last_arc_prompt = f"""
            This should be your final arc!
            The protagonist should achive the final breakthrough in cultivation.
            THe story must conclude even if all plot points are not resolved.
            Try to deliver on the most important payoffs to the reader.
            {progression_fantasy_plot_generator}
            """  
    
    parser_instructions = """
        Instructions for Generating Valid JSON with Pydantic:
       
        Adhere to Schema Requirements:
        Include all required fields for every data entry as specified in the schema.
        Follow the expected data types (e.g., strings, arrays of strings) strictly.
        
        Validate Consistency in Required Fields:
        Ensure the data does not include invalid entries.

        Correctly Index your Output
        Do not incorrectly assume missing data for index zero (e.g., chapter 1 should be placed in index zero and so on)

        """
    fan_guidelines = """
        You are a 15 year old boy who loves reading power fantasy and cultivation novels.
        You want to see the main character gradually overcome their limits in a satisfying way. You are not looking for literary fiction, but instead fun genre fiction.
        Please read the following story and write a fan letter to the author.
        Do not critique the writing style but instead focus on what you liked most and what you would like to see next.
        You are excited to see the story progress but are happy to see it conclude too.
        Tell them a little about yourself too (average reader of the genre) including your name.
        Make it realistic not exaggerated. In your response provide only the letter contents. Here is the story so far:

        """
    synopsis = """
        Great job on the story! Please choose a short and unique title. 
        
        Please create a compelling description to hook the reader. Note that the novel shouldn't aim to appeal to everyone. Speak to the interests of our target reader. Do not over explain, your goal is to catch the target reader's interest and set expectations for the story.

        End the description with the following information:

        Aiming for 1-2k words a chapter. New chapters drop every 2-3 days :)

        Select up to four genres from the following list: Action, Adventure, Comedy, Contemporary, Drama, Fantasy, Historical, Horror, Mystery, Psychological, Romance, Satire, Sci-fi, Short Story, Tragedy 

        Select up to ten tags from the following list: Anti-Hero Lead, Artificial Intelligence, Attractive Lead, Cyberpunk, Dungeon, Dystopia, Female Lead, First Contact, GameLit, Gender Bender, Genetically Engineered, Grimdark, Hard Sci-fi, Harem, High Fantasy, LitRPG, Low Fantasy, Magic, Male Lead, Martial Arts, Multiple Lead Characters, Mythos, Non-Human Lead, Portal Fantasy / Isekai, Post Apocalyptic, Progression, Reader Interactive, Reincarnation, Ruling Class, School Life, Secret Identity, Slice of Life, Soft Sci-fi, Space Opera, Sports, Steampunk, Strategy, Strong Lead, Super Heroes, Supernatural, Technologically Engineered, Time Loop, Time Travel, Urban Fantasy, Villainous Lead, Virtual Reality, War and Military, Wuxia.
        """
    
    cover = """
        Write a prompt to be used by an image generation model to create a cover for your story. Be aware that te cover must be readable so do not include text and only 1 or 2 elements max.
        """
    return system_instruction, planner_guidelines, expander_guidelines, writer_guidelines, progression_fantasy_plot_generator, first_arc_prompt, last_arc_prompt, setting_prompt, ef_prompt, parser_instructions, fan_guidelines, synopsis, cover