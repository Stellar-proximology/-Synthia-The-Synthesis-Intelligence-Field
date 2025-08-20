
import json

# Core data structures from schema, with expansions
punctuation_resonance = {
    ":": "heaven_to_earth_initiation",     # Genesis 1:3 (cause to manifestation)
    ";": "spirit_breath_pause",            # Ecclesiastes 3:2 (space for Holy Spirit between parallels)
    ".": "archetype_expression_locator"    # Gate.Line model
}

gate_scripture_map = {
    36: ["Proverbs 25:2", "Matthew 5:14-16", "1 Kings 19:12"],
    22: ["2 Corinthians 3:18", "Isaiah 55:8-9", "Philippians 4:8"],
    # Expanded examples
    1: ["Genesis 1:1", "John 1:1"],
    2: ["Genesis 1:2", "Psalm 104:30"],
    64: ["Revelation 22:13", "Ecclesiastes 3:1"]
    # Add more as needed
}

line_genesis_phases = {
    1: "foundation_seed",      # Mirrors Day 1: Light/Creation
    2: "separation_space",     # Day 2: Division of Waters
    3: "tension_struggle",     # Day 3: Emergence/Growth
    4: "structure_ascent",     # Day 4: Structure/Lights
    5: "wisdom_guidance",      # Day 5: Abundance/Life
    6: "completion_judgment"   # Day 6: Completion/Humanity
}

# Expanded: Gate meanings (I Ching base + HD flavor)
gate_meaning_map = {
    22: "Grace / Adorning / Openness and Emotional Surrender",
    36: "Brightness Hiding / Darkening of the Light / Crisis and Emotional Clarity",
    # Added examples for scalability
    1: "The Creative / Heaven / Self-Expression and Pure Potential",
    2: "The Receptive / Earth / Direction and Allowing",
    64: "Before Completion / Transition / Confusion Leading to Renewal"
    # Expand to all 64 here in future
}

# Expanded: Line meanings based on Human Design thematics, with Genesis ties
line_meaning_map = {
    1: "Investigator / Foundation and Research (mirrors Day 1: Building secure knowledge base)",
    2: "Hermit / Natural Genius and Projection (mirrors Day 2: Inner call and separation for depth)",
    3: "Martyr / Experimenter and Adaptation (mirrors Day 3: Trial-error growth through tension)",
    4: "Opportunist / Networker and Influence (mirrors Day 4: External structures and opportunities)",
    5: "Heretic / Universalizer and Projection (mirrors Day 5: Practical solutions and leadership)",
    6: "Role Model / Wise Observer and Integration (mirrors Day 6: Objective completion and example)"
}

# Expanded: Gate field affinity (HD 9-center mapping)
gate_field_affinity_map = {
    22: "Solar Plexus Center (Emotional wave, openness, and mood)",
    36: "Solar Plexus Center (Emotional crisis navigation and clarity)",
    # Added examples
    1: "G Center (Identity and self-expression)",
    2: "G Center (Direction and magnetic monopole)",
    64: "Head Center (Inspiration and mental pressure)"
    # Maps to HD centers: Head, Ajna, Throat, G, Ego/Heart, Solar Plexus, Splenic, Sacral, Root
}

def parse_punctuation(input_str):
    """Decode punctuation in input, with resonance meanings."""
    results = {}
    if ':' in input_str:
        results[':'] = punctuation_resonance[':']
    if ';' in input_str:
        results[';'] = punctuation_resonance[';']
    if '.' in input_str and any(char.isdigit() for char in input_str):
        results['.'] = punctuation_resonance['.']
    return results

def get_gate_line_info(gate, line):
    """Fetch meanings, scriptures, phases for a Gate.Line."""
    info = {
        "gate_meaning": gate_meaning_map.get(gate, "Unknown Gate"),
        "field_affinity": gate_field_affinity_map.get(gate, "Unknown Affinity"),
        "scriptures": gate_scripture_map.get(gate, []),
        "line_genesis_phase": line_genesis_phases.get(line, "Unknown Phase"),
        "line_meaning": line_meaning_map.get(line, "Unknown Meaning")
    }
    return info

def main():
    print("=== Divine Decoder Prototype ===")
    print("Enter a punctuation string, Bible verse snippet, or Gate.Line (e.g., 'Psalm 23:1;', '22.3')")
    user_input = input("Input: ").strip()

    # Decode punctuation
    punct_results = parse_punctuation(user_input)
    if punct_results:
        print("\nPunctuation Decoding:")
        for symbol, meaning in punct_results.items():
            print(f"{symbol} → {meaning}")

    # Handle Gate.Line if present
    if '.' in user_input:
        try:
            parts = user_input.split('.')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                gate = int(parts[0])
                line = int(parts[1])
                if 1 <= gate <= 64 and 1 <= line <= 6:
                    info = get_gate_line_info(gate, line)
                    print("\nGate.Line Info:")
                    print(json.dumps(info, indent=2))
                else:
                    print("Error: Gate must be 1-64, Line 1-6.")
            else:
                print("Invalid Gate.Line format.")
        except ValueError:
            print("Error parsing Gate.Line.")

if __name__ == "__main__":
    main()
