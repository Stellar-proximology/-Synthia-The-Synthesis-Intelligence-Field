
import json

# Core data structures from schema
punctuation_resonance = {
    ":": "heaven_to_earth_initiation",     # Genesis 1:3 (enhanced: cause to manifestation)
    ";": "spirit_breath_pause",            # Ecclesiastes 3:2 (enhanced: space for Holy Spirit between parallels)
    ".": "archetype_expression_locator"    # Gate.Line model
}

gate_scripture_map = {
    36: ["Proverbs 25:2", "Matthew 5:14-16", "1 Kings 19:12"],
    22: ["2 Corinthians 3:18", "Isaiah 55:8-9", "Philippians 4:8"],
    # Expand here as needed, e.g., 1: ["Genesis 1:1"]
}

line_genesis_phases = {
    1: "foundation_seed",
    2: "separation_space", 
    3: "tension_struggle",
    4: "structure_ascent",
    5: "wisdom_guidance",
    6: "completion_judgment"
}

# Expanded maps for depth
gate_meaning_map = {
    22: "Grace / Adorning / Beauty in Surrender",
    36: "Brightness Hiding / Darkening of the Light / Emotional Clarity in Crisis",
    # Add more, e.g., 1: "The Creative / Heaven / Pure Yang Force"
}

line_meaning_map = {
    1: "Investigator / Self-focused foundation (mirrors Day 1: Light creation)",
    2: "Hermit / Natural projection and call (mirrors Day 2: Separation of waters)",
    3: "Martyr / Trial and error adaptation (mirrors Day 3: Land and vegetation emergence)",
    4: "Opportunist / External networking (mirrors Day 4: Lights in the firmament)",
    5: "Heretic / Universalizing solutions (mirrors Day 5: Creatures in sea and air)",
    6: "Role Model / Objective wisdom (mirrors Day 6: Land creatures and humanity)"
}

# Optional: Gate field affinity (for 9-body mapping, stub for now)
gate_field_affinity_map = {
    22: "Heart/Mind Interface (G-Center emotional openness)",
    36: "Solar Plexus / Emotional Wave (crisis navigation)"
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
