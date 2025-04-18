import json

duplicates_to_remove = {
    'genFAQ109', 'genFAQ075', 'genFAQ089', 'genFAQ110',
    'genFAQ116', 'genFAQ200', 'genFAQ127', 'genFAQ126',
    'genFAQ190'
}

# Read original JSON file
with open('alt_q.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter out entries with duplicate IDs
filtered_altq = [item for item in data['altq'] if item['id'] not in duplicates_to_remove]

# Renumber the IDs sequentially
for index, item in enumerate(filtered_altq, start=1):
    item['id'] = f'genFAQ{index:03d}'  # Format with leading zeros

# Create new JSON structure
new_data = {
    "altq": filtered_altq
}

# Write to new JSON file
with open('alt_new.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4, separators=(',', ': '))

print("alt_new.json created successfully!")