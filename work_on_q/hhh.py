import json

def remove_duplicates(input_path, output_path):
    # Load original data
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # List of duplicate IDs to remove (second in each pair)
    duplicates_to_remove = {
        'genFAQ109', 'genFAQ075', 'genFAQ089', 'genFAQ110',
        'genFAQ116', 'genFAQ200', 'genFAQ127', 'genFAQ126',
        'genFAQ190'
    }

    # Filter entries and preserve order
    filtered_faqs = []
    seen_questions = set()
    
    for faq in data['altq']:
        if faq['id'] not in duplicates_to_remove:
            # Check for question duplicates
            question = faq['altq']['q']
            if question not in seen_questions:
                seen_questions.add(question)
                filtered_faqs.append(faq)

    # Renumber IDs sequentially
    for index, faq in enumerate(filtered_faqs, 1):
        faq['id'] = f"genFAQ{index:03d}"

    # Save cleaned data
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'altq': filtered_faqs}, f, ensure_ascii=False, indent=2)

# Usage
remove_duplicates('alt_q.json', 'alt_q_new.json')