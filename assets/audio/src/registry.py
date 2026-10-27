"""
Single source of truth for every asset in the library: id, output path,
category, which function renders it, and the creative-intent metadata that
feeds metadata_gen.py's CSV/JSON catalogs. generate.py, metadata_gen.py and
validate.py all read this module instead of hardcoding asset lists.
"""

from music import science, history, philosophy, mythology, mysteries, knowledge_curiosity as kn_music, \
    religion_cosmology, storytelling
from sfx import science_cosmos, history_archaeology, philosophy as sfx_philosophy, mystery_investigation, \
    mythology_fantasy, knowledge_curiosity as kn_sfx, cinematic_editing


def _slug(title):
    return title.replace(",", "").replace("'", "").replace(" ", "_")


def _mus(id_, title, category, generator, purpose, mood, subject, tonal_center, loop_dur):
    slug = _slug(title)
    return {
        "id": id_, "type": "music", "title": title,
        "filename": f"{id_}_{slug}.wav", "category": category, "rel_dir": f"music/{category}",
        "generator": generator, "purpose": purpose, "mood": mood, "intended_subject": subject,
        "tonal_center": tonal_center, "bpm": "N/A (ambient/textural, non-metric)",
        "loop_compatible": "yes (seamless)" if loop_dur else "no (one-shot)",
        "voiceover_suitability": "backing bed - duck under narration",
        "nominal_duration_sec": loop_dur,
    }


def _sfx(id_, title, category, generator, effect_type, purpose, use, dur):
    slug = _slug(title)
    return {
        "id": id_, "type": "sfx", "title": title,
        "filename": f"{id_}_{slug}.wav", "category": category, "rel_dir": f"sfx/{category}",
        "generator": generator, "effect_type": effect_type, "narrative_purpose": purpose,
        "intended_use": use, "nominal_duration_sec": dur,
    }


MUSIC = [
    # -- Science (6) --
    _mus("MUS_SC01", "The Discovery", "science", science.make_sc01_the_discovery,
         "Scientific breakthroughs, surprising facts, new discoveries", "curious, bright, forward-moving",
         "science", "D Lydian", 20.0),
    _mus("MUS_SC02", "The Universe Within", "science", science.make_sc02_the_universe_within,
         "Physics, atoms, molecular structures, hidden mechanisms of reality", "precise, synthetic, microscopic",
         "science", "atonal FM/AM textures", 22.0),
    _mus("MUS_SC03", "Cosmic Perspective", "science", science.make_sc03_cosmic_perspective,
         "Astronomy, galaxies, black holes, scale of the universe", "spacious, awe, slow crescendo",
         "science", "A1 drone", 30.0),
    _mus("MUS_SC04", "Evolutionary Time", "science", science.make_sc04_evolutionary_time,
         "Evolution, natural selection, prehistoric life", "organic, slowly evolving",
         "science", "A2 Dorian (drifting)", 26.0),
    _mus("MUS_SC05", "The Human Machine", "science", science.make_sc05_the_human_machine,
         "Neuroscience, biology, cognition, the human body", "rhythmic, mechanical, intelligent",
         "science", "C3 Mixolydian", 20.0),
    _mus("MUS_SC06", "Scientific Paradox", "science", science.make_sc06_scientific_paradox,
         "Counterintuitive discoveries, unresolved scientific questions", "unstable, intellectually intriguing",
         "science", "G3 tritone clash", 24.0),

    # -- History (7) --
    _mus("MUS_HI01", "Echoes of Antiquity", "history", history.make_hi01_echoes_of_antiquity,
         "Ancient history, the passage of civilizations", "solemn, resonant, measured",
         "history", "A2 Aeolian", 28.0),
    _mus("MUS_HI02", "The Lost Civilization", "history", history.make_hi02_the_lost_civilization,
         "Archaeological mysteries, abandoned cities, forgotten societies", "sparse, distant, unresolved",
         "history", "C3 Phrygian", 26.0),
    _mus("MUS_HI03", "Rise and Fall of Empires", "history", history.make_hi03_rise_and_fall_of_empires,
         "Imperial expansion, conquest, political collapse", "building, dramatic momentum",
         "history", "D3 Dorian", 30.0),
    _mus("MUS_HI04", "Ancient Knowledge", "history", history.make_hi04_ancient_knowledge,
         "Ancient manuscripts, mathematics, astronomy, architecture", "reflective, discovery, delicate",
         "history", "A3 Lydian", 22.0),
    _mus("MUS_HI05", "The Historical Revelation", "history", history.make_hi05_the_historical_revelation,
         "Historical facts that challenge familiar narratives", "investigative, tense, resolving",
         "history", "G3 minor-2nd clash", 20.0),
    _mus("MUS_HI06", "Before Recorded Time", "history", history.make_hi06_before_recorded_time,
         "Prehistory, human origins, early migration, the deep past", "primal, earthy, expansive",
         "history", "D2 minor pentatonic", 28.0),
    _mus("MUS_HI07", "The Last Days of an Empire", "history", history.make_hi07_the_last_days_of_an_empire,
         "Civilizational collapse, historical tragedy, the end of an era", "solemn, unlifting",
         "history", "G2 harmonic minor", 30.0),

    # -- Philosophy (6) --
    _mus("MUS_PH01", "The Question of Existence", "philosophy", philosophy.make_ph01_the_question_of_existence,
         "Existence, being, reality, the fundamental nature of life", "minimal, spacious, deliberate pauses",
         "philosophy", "A3 Aeolian", 24.0),
    _mus("MUS_PH02", "The Infinite Regress", "philosophy", philosophy.make_ph02_the_infinite_regress,
         "Infinite questions, paradoxes, causality, limits of explanation", "repeating, transposing, destabilizing",
         "philosophy", "F3 Dorian (shifting)", 24.0),
    _mus("MUS_PH03", "Free Will", "philosophy", philosophy.make_ph03_free_will,
         "Choice, determinism, responsibility, human agency", "structured grid vs. free melodic line",
         "philosophy", "G3 Mixolydian", 22.0),
    _mus("MUS_PH04", "Consciousness", "philosophy", philosophy.make_ph04_consciousness,
         "Subjective experience, awareness, identity, the mystery of the mind", "intimate, slowly evolving",
         "philosophy", "E3", 26.0),
    _mus("MUS_PH05", "The Weight of Time", "philosophy", philosophy.make_ph05_the_weight_of_time,
         "Mortality, impermanence, memory, the passage of time", "reflective, restrained, spacious decay",
         "philosophy", "F3 harmonic minor", 26.0),
    _mus("MUS_PH06", "The Paradox", "philosophy", philosophy.make_ph06_the_paradox,
         "Philosophical thought experiments, contradictions", "minimalist, dissonant, unresolved",
         "philosophy", "Ab3 chromatic fragment", 22.0),

    # -- Mythology (7) --
    _mus("MUS_MY01", "Creation of the Cosmos", "mythology", mythology.make_my01_creation_of_the_cosmos,
         "Creation myths, primordial beginnings, birth of legendary worlds", "emerging from silence, expansive",
         "mythology", "B1", 30.0),
    _mus("MUS_MY02", "The Gods Among Mortals", "mythology", mythology.make_my02_the_gods_among_mortals,
         "Divine figures, supernatural encounters", "grand but restrained, awe",
         "mythology", "C3 Lydian", 26.0),
    _mus("MUS_MY03", "The Underworld", "mythology", mythology.make_my03_the_underworld,
         "Journeys into the realm of the dead, afterlife narratives", "dark, hollow, unsettling depth",
         "mythology", "A1", 24.0),
    _mus("MUS_MY04", "The Hero's Journey", "mythology", mythology.make_my04_the_heros_journey,
         "Legendary heroes, trials, transformation, quests", "developing, determined",
         "mythology", "F3 Mixolydian", 26.0),
    _mus("MUS_MY05", "Primordial Chaos", "mythology", mythology.make_my05_primordial_chaos,
         "Creation from chaos, cosmic conflict, primordial forces", "unstable resolving into order",
         "mythology", "G2 whole-tone", 24.0),
    _mus("MUS_MY06", "Forgotten Pantheons", "mythology", mythology.make_my06_forgotten_pantheons,
         "Lesser-known gods, forgotten traditions, neglected myths", "enigmatic, a little alien",
         "mythology", "D3 Phrygian", 24.0),
    _mus("MUS_MY07", "The Fall of the Gods", "mythology", mythology.make_my07_the_fall_of_the_gods,
         "Divine conflict, collapse of mythological orders", "building to a controlled climax",
         "mythology", "E2 minor-2nd clash", 28.0),

    # -- Mysteries (7) --
    _mus("MUS_MI01", "The Unsolved Mystery", "mysteries", mysteries.make_mi01_the_unsolved_mystery,
         "General mysteries, missing information, unexplained events", "sparse, slowly evolving",
         "mysteries", "F#3 whole-tone", 24.0),
    _mus("MUS_MI02", "The Forbidden Archive", "mysteries", mysteries.make_mi02_the_forbidden_archive,
         "Hidden manuscripts, secret records, forgotten knowledge", "mechanical, dark, investigative",
         "mysteries", "D3", 22.0),
    _mus("MUS_MI03", "The Missing Piece", "mysteries", mysteries.make_mi03_the_missing_piece,
         "Investigations where one crucial fact is still unknown", "fragmented, approaching but not resolving",
         "mysteries", "A3 Dorian", 22.0),
    _mus("MUS_MI04", "The Unexplained Signal", "mysteries", mysteries.make_mi04_the_unexplained_signal,
         "Strange signals, unidentified sounds, unusual observations", "drifting, synthetic, unstable",
         "mysteries", "atonal (signal-based)", 20.0),
    _mus("MUS_MI05", "Shadows of the Past", "mysteries", mysteries.make_mi05_shadows_of_the_past,
         "Historical mysteries, disputed accounts, forgotten events", "restrained, subtly tense",
         "mysteries", "E3 Aeolian", 24.0),
    _mus("MUS_MI06", "The Impossible Question", "mysteries", mysteries.make_mi06_the_impossible_question,
         "Apparent contradictions, strange coincidences, hard-to-explain phenomena", "irregular, ambiguous center",
         "mysteries", "dual center G3/F3", 25.0),
    _mus("MUS_MI07", "The Final Clue", "mysteries", mysteries.make_mi07_the_final_clue,
         "The moment before a mystery becomes understandable", "converging, allowed to resolve",
         "mysteries", "A3 Mixolydian", 20.0),

    # -- Knowledge & Curiosity (6) --
    _mus("MUS_KN01", "The Curiosity Engine", "knowledge_curiosity", kn_music.make_kn01_the_curiosity_engine,
         "Fascinating facts, general knowledge, surprising observations", "bright, sophisticated, exploratory",
         "knowledge/curiosity", "C4 major pentatonic", 20.0),
    _mus("MUS_KN02", "The Hidden Connection", "knowledge_curiosity", kn_music.make_kn02_the_hidden_connection,
         "Videos connecting ideas across science, history, philosophy, or culture", "interlocking patterns",
         "knowledge/curiosity", "A3 major pentatonic (dual root)", 24.0),
    _mus("MUS_KN03", "A Mind Awakens", "knowledge_curiosity", kn_music.make_kn03_a_mind_awakens,
         "Learning, intellectual growth, discovering a new concept", "gradually expanding, optimistic",
         "knowledge/curiosity", "G3 Lydian", 24.0),
    _mus("MUS_KN04", "Beyond Common Knowledge", "knowledge_curiosity", kn_music.make_kn04_beyond_common_knowledge,
         "Rare facts, overlooked details, unexpected explanations", "distinctive motif, restrained reveal",
         "knowledge/curiosity", "B3 major pentatonic", 20.0),
    _mus("MUS_KN05", "The Thought Experiment", "knowledge_curiosity", kn_music.make_kn05_the_thought_experiment,
         "Hypothetical scenarios, logic puzzles, conceptual exploration", "minimalist, electronic",
         "knowledge/curiosity", "A3 (FM-based)", 22.0),
    _mus("MUS_KN06", "The Joy of Understanding", "knowledge_curiosity", kn_music.make_kn06_the_joy_of_understanding,
         "Explainers that turn a confusing subject into an understandable idea", "warm, clear, positive",
         "knowledge/curiosity", "D4 major pentatonic", 20.0),

    # -- Religion & Cosmology (5) --
    _mus("MUS_RC01", "The Sacred Question", "religion_cosmology", religion_cosmology.make_rc01_the_sacred_question,
         "Comparative religion, beliefs about existence and the cosmos", "reflective, unhurried",
         "religion/cosmology", "A2 Dorian", 28.0),
    _mus("MUS_RC02", "The Cosmic Order", "religion_cosmology", religion_cosmology.make_rc02_the_cosmic_order,
         "Creation, destruction, cosmic cycles, universal order", "cyclic, expansive",
         "religion/cosmology", "C3 Mixolydian", 24.0),
    _mus("MUS_RC03", "Visions of the Afterlife", "religion_cosmology",
         religion_cosmology.make_rc03_visions_of_the_afterlife,
         "Comparative beliefs about death, rebirth, judgment", "ethereal, thoughtfully ambiguous",
         "religion/cosmology", "F3 suspended", 28.0),
    _mus("MUS_RC04", "The Origins of Belief", "religion_cosmology", religion_cosmology.make_rc04_the_origins_of_belief,
         "Ancient rituals, religious history, symbolic systems", "ritual, documentary-paced",
         "religion/cosmology", "G2 Aeolian", 26.0),
    _mus("MUS_RC05", "Many Paths, One Question", "religion_cosmology",
         religion_cosmology.make_rc05_many_paths_one_question,
         "Comparing different answers to enduring questions about existence", "coexisting voices, unforced",
         "religion/cosmology", "multi-root (D3/F3/A3)", 26.0),

    # -- General Storytelling (6) --
    _mus("MUS_ST01", "The Unbelievable Fact", "storytelling", storytelling.make_st01_the_unbelievable_fact,
         "A startling fact that demands immediate attention", "punchy hook, compact",
         "general storytelling", "D4 major pentatonic", 16.0),
    _mus("MUS_ST02", "The Deep Dive", "storytelling", storytelling.make_st02_the_deep_dive,
         "A more detailed explanation of a complex topic", "stable, unobtrusive, narration-first",
         "general storytelling", "A3 Dorian", 28.0),
    _mus("MUS_ST03", "The Unexpected Truth", "storytelling", storytelling.make_st03_the_unexpected_truth,
         "Revealing a fact that overturns an assumption", "understated opening, clear turn",
         "general storytelling", "G3 Aeolian->Mixolydian", 22.0),
    _mus("MUS_ST04", "The Dark Side of Knowledge", "storytelling", storytelling.make_st04_the_dark_side_of_knowledge,
         "Dangerous discoveries, ethical dilemmas, unintended consequences", "restrained, dark, controlled",
         "general storytelling", "F2 minor-2nd clash", 24.0),
    _mus("MUS_ST05", "The Great Unknown", "storytelling", storytelling.make_st05_the_great_unknown,
         "Questions science, philosophy, and history haven't fully resolved", "spacious, deliberately open",
         "general storytelling", "D2 suspended", 30.0),
    _mus("MUS_ST06", "The World Reimagined", "storytelling", storytelling.make_st06_the_world_reimagined,
         "A fresh perspective on a familiar subject", "distinctive motif expanding outward",
         "general storytelling", "C4 Lydian", 24.0),
]


SFX = [
    # -- Science & Cosmic (8) --
    _sfx("SFX_SC01", "Atomic Pulse", "science_cosmos", science_cosmos.make_sc01_atomic_pulse,
         "electronic pulse", "Suggests a microscopic process", "accent under a close-up science visual", 0.18),
    _sfx("SFX_SC02", "Cosmic Sweep", "science_cosmos", science_cosmos.make_sc02_cosmic_sweep,
         "evolving sweep", "Space imagery or scientific transition", "scene transition", 2.5),
    _sfx("SFX_SC03", "Quantum Glitch", "science_cosmos", science_cosmos.make_sc03_quantum_glitch,
         "granular/digital glitch", "Controlled digital irregularity", "glitch accent on a counterintuitive fact", 0.4),
    _sfx("SFX_SC04", "Scientific Discovery Accent", "science_cosmos", science_cosmos.make_sc04_scientific_discovery_accent,
         "bell-like reveal", "A new fact or breakthrough", "claim/fact reveal", 1.1),
    _sfx("SFX_SC05", "Energy Field", "science_cosmos", science_cosmos.make_sc05_energy_field,
         "evolving synthetic tone", "An invisible field or force", "sustained background accent", 2.2),
    _sfx("SFX_SC06", "Signal Detected", "science_cosmos", science_cosmos.make_sc06_signal_detected,
         "electronic beep sequence", "Discovery of an unusual observation", "signal/detection moment", 0.9),
    _sfx("SFX_SC07", "Deep Space Rumble", "science_cosmos", science_cosmos.make_sc07_deep_space_rumble,
         "low-frequency atmosphere", "Cosmic imagery", "ambient bed under space visuals", 5.0),
    _sfx("SFX_SC08", "Particle Cascade", "science_cosmos", science_cosmos.make_sc08_particle_cascade,
         "rapid transient sequence", "Layered microscopic activity", "fast-cut science montage accent", 1.3),

    # -- History & Archaeology (7) --
    _sfx("SFX_HI01", "Ancient Stone Impact", "history_archaeology", history_archaeology.make_hi01_ancient_stone_impact,
         "heavy impact", "Stone-like impact", "architectural/ruins reveal", 1.0),
    _sfx("SFX_HI02", "Temple Door", "history_archaeology", history_archaeology.make_hi02_temple_door,
         "stylized door movement", "Ancient architectural reveal", "entrance/doorway transition", 1.8),
    _sfx("SFX_HI03", "Artifact Discovery", "history_archaeology", history_archaeology.make_hi03_artifact_discovery,
         "restrained reveal accent", "Uncovering an ancient object", "artifact close-up reveal", 1.0),
    _sfx("SFX_HI04", "Buried Chamber", "history_archaeology", history_archaeology.make_hi04_buried_chamber,
         "low atmospheric transition", "Discovery of a concealed space", "chamber/tomb reveal", 2.0),
    _sfx("SFX_HI05", "Ancient Mechanism", "history_archaeology", history_archaeology.make_hi05_ancient_mechanism,
         "mechanical grind + clicks", "A mechanism or device in motion", "device/trap/mechanism visual", 1.5),
    _sfx("SFX_HI06", "Dust and Debris", "history_archaeology", history_archaeology.make_hi06_dust_and_debris,
         "short textured noise", "An archaeological reveal", "dust/debris visual accent", 0.6),
    _sfx("SFX_HI07", "Historical Transition", "history_archaeology", history_archaeology.make_hi07_historical_transition,
         "cinematic sweep", "Transition between eras or scenes", "era/scene transition", 1.6),

    # -- Philosophy (6) --
    _sfx("SFX_PH01", "The Question", "philosophy", sfx_philosophy.make_ph01_the_question,
         "tonal accent", "Introducing a profound question", "question posed on screen", 1.0),
    _sfx("SFX_PH02", "Thought Shift", "philosophy", sfx_philosophy.make_ph02_thought_shift,
         "pitch-drop transition", "A change in perspective", "perspective shift", 0.7),
    _sfx("SFX_PH03", "Paradox Accent", "philosophy", sfx_philosophy.make_ph03_paradox_accent,
         "unresolved tonal gesture", "A philosophical contradiction", "paradox on screen", 1.1),
    _sfx("SFX_PH04", "Realization", "philosophy", sfx_philosophy.make_ph04_realization,
         "restrained harmonic accent", "A conceptual breakthrough", "SOLID-confidence claim reveal", 1.2),
    _sfx("SFX_PH05", "Existential Void", "philosophy", sfx_philosophy.make_ph05_existential_void,
         "low-intensity atmosphere", "A spacious contemplative moment", "existential pause", 1.8),
    _sfx("SFX_PH06", "Unresolved Thought", "philosophy", sfx_philosophy.make_ph06_unresolved_thought,
         "dissonant tail", "A thought that doesn't fully resolve", "CONTESTED/UNCERTAIN claim reveal", 1.0),

    # -- Mystery & Investigation (8) --
    _sfx("SFX_MI01", "Suspense Tick", "mystery_investigation", mystery_investigation.make_mi01_suspense_tick,
         "precise pulse", "A developing mystery", "rhythmic suspense accent", 0.1),
    _sfx("SFX_MI02", "Hidden Clue", "mystery_investigation", mystery_investigation.make_mi02_hidden_clue,
         "small distinctive accent", "Revealing an overlooked detail", "clue callout", 0.35),
    _sfx("SFX_MI03", "Mystery Stinger", "mystery_investigation", mystery_investigation.make_mi03_mystery_stinger,
         "short dark tonal gesture", "General mystery beat", "mystery stinger", 0.8),
    _sfx("SFX_MI04", "Evidence Reveal", "mystery_investigation", mystery_investigation.make_mi04_evidence_reveal,
         "controlled transition accent", "Introducing an important discovery", "evidence reveal", 1.0),
    _sfx("SFX_MI05", "Ominous Reverse", "mystery_investigation", mystery_investigation.make_mi05_ominous_reverse,
         "reverse swell", "Leading into a scene change", "pre-reveal build", 1.8),
    _sfx("SFX_MI06", "Cryptic Signal", "mystery_investigation", mystery_investigation.make_mi06_cryptic_signal,
         "fragmented tonal pattern", "An unusual, cryptic detail", "cryptic/code moment", 0.7),
    _sfx("SFX_MI07", "Unanswered Question", "mystery_investigation", mystery_investigation.make_mi07_unanswered_question,
         "suspended texture", "A question left deliberately open", "CONTESTED/UNCERTAIN claim reveal (alt.)", 1.1),
    _sfx("SFX_MI08", "Final Revelation", "mystery_investigation", mystery_investigation.make_mi08_final_revelation,
         "memorable controlled accent", "The conclusion of a mystery", "mystery payoff", 1.6),

    # -- Mythology & Fantasy (7) --
    _sfx("SFX_MY01", "Primordial Awakening", "mythology_fantasy", mythology_fantasy.make_my01_primordial_awakening,
         "deep evolving swell", "The beginning of a legendary world", "creation-myth opening", 3.0),
    _sfx("SFX_MY02", "Divine Presence", "mythology_fantasy", mythology_fantasy.make_my02_divine_presence,
         "resonant expansive tone", "An extraordinary presence", "god/deity appearance", 2.2),
    _sfx("SFX_MY03", "Mythic Energy", "mythology_fantasy", mythology_fantasy.make_my03_mythic_energy,
         "layered FM/AM texture", "A supernatural or legendary event", "magic/power moment", 1.4),
    _sfx("SFX_MY04", "Underworld Gate", "mythology_fantasy", mythology_fantasy.make_my04_underworld_gate,
         "heavy dark transition", "Entering an underworld/afterlife realm", "underworld transition", 1.6),
    _sfx("SFX_MY05", "Ancient Power", "mythology_fantasy", mythology_fantasy.make_my05_ancient_power,
         "low evolving texture", "A force growing in intensity", "power building moment", 2.4),
    _sfx("SFX_MY06", "Mythic Transformation", "mythology_fantasy", mythology_fantasy.make_my06_mythic_transformation,
         "rising pitch + timbre shift", "A transformation or metamorphosis", "transformation moment", 1.8),
    _sfx("SFX_MY07", "Legendary Revelation", "mythology_fantasy", mythology_fantasy.make_my07_legendary_revelation,
         "distinctive bell-like accent", "Revealing a mythological figure/location/event", "mythology reveal", 1.5),

    # -- Knowledge & Curiosity (7) --
    _sfx("SFX_KN01", "Curiosity Ping", "knowledge_curiosity", kn_sfx.make_kn01_curiosity_ping,
         "subtle tonal accent", "A small curiosity prompt", "light accent on an interesting detail", 0.4),
    _sfx("SFX_KN02", "Interesting Fact", "knowledge_curiosity", kn_sfx.make_kn02_interesting_fact,
         "memorable bell accent", "A surprising fact", "fact callout", 0.6),
    _sfx("SFX_KN03", "Idea Connection", "knowledge_curiosity", kn_sfx.make_kn03_idea_connection,
         "small layered two-tone", "Two concepts coming together", "concept-connection moment", 0.6),
    _sfx("SFX_KN04", "Discovery Chime", "knowledge_curiosity", kn_sfx.make_kn04_discovery_chime,
         "restrained chime", "A satisfying but restrained reveal", "SOLID-confidence claim reveal (alt.)", 1.0),
    _sfx("SFX_KN05", "Concept Transition", "knowledge_curiosity", kn_sfx.make_kn05_concept_transition,
         "smooth short sweep", "Moving between explanatory sections", "section transition", 0.5),
    _sfx("SFX_KN06", "Unexpected Detail", "knowledge_curiosity", kn_sfx.make_kn06_unexpected_detail,
         "quick FM accent", "An overlooked piece of information", "detail callout", 0.25),
    _sfx("SFX_KN07", "Knowledge Unlocked", "knowledge_curiosity", kn_sfx.make_kn07_knowledge_unlocked,
         "compact arpeggio", "An explanation becoming clear", "understanding-achieved moment", 0.8),

    # -- Universal Cinematic Editing (7) --
    _sfx("SFX_ED01", "Short Whoosh", "cinematic_editing", cinematic_editing.make_ed01_short_whoosh,
         "concise sweep", "A fast cut/transition", "generic cut transition", 0.5),
    _sfx("SFX_ED02", "Deep Cinematic Impact", "cinematic_editing", cinematic_editing.make_ed02_deep_cinematic_impact,
         "powerful impact", "A strong dramatic emphasis", "high-impact hit", 1.2),
    _sfx("SFX_ED03", "Reverse Impact", "cinematic_editing", cinematic_editing.make_ed03_reverse_impact,
         "reverse swell", "Leading into a reveal", "pre-reveal build", 1.4),
    _sfx("SFX_ED04", "Subtle Low Hit", "cinematic_editing", cinematic_editing.make_ed04_subtle_low_hit,
         "restrained low accent", "A quiet emphasis beat", "understated emphasis", 0.5),
    _sfx("SFX_ED05", "Silence Drop", "cinematic_editing", cinematic_editing.make_ed05_silence_drop,
         "transition to near-silence", "A deliberate dynamic drop", "silence-drop transition", 0.6),
    _sfx("SFX_ED06", "Atmospheric Riser", "cinematic_editing", cinematic_editing.make_ed06_atmospheric_riser,
         "gradual build", "A short reveal build-up", "build-up into a reveal", 2.0),
    _sfx("SFX_ED07", "Seamless Ambient Tail", "cinematic_editing", cinematic_editing.make_ed07_seamless_ambient_tail,
         "atmospheric decay", "Blending naturally into an existing soundscape", "outgoing ambience tail", 2.5),
]


ALL_ASSETS = MUSIC + SFX
