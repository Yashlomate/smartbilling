def generate_item_description(rough_input):
    """
    Smart suggestion engine: expands common billing shorthand into
    professional invoice descriptions using keyword matching.
    Fallback-safe by design — no external API dependency.
    """
    text = rough_input.lower().strip()

    suggestions = {
        'web': 'Website Design and Development Services',
        'design': 'Graphic Design Services',
        'app': 'Mobile Application Development Services',
        'consult': 'Consulting Services',
        'maintenance': 'Website/Software Maintenance Services',
        'hosting': 'Web Hosting Services',
        'logo': 'Logo Design Services',
        'seo': 'Search Engine Optimization Services',
        'content': 'Content Writing Services',
        'support': 'Technical Support Services',
    }

    for keyword, professional_text in suggestions.items():
        if keyword in text:
            return professional_text

    # No match found — return original input, capitalized nicely
    return rough_input.strip().capitalize()


def suggest_tax_percent(description):
    """
    Suggests a likely GST tax percentage based on common Indian
    billing categories — a simple rule-based classifier.
    """
    text = description.lower()
    if any(word in text for word in ['service', 'consult', 'design', 'development', 'support']):
        return 18
    elif any(word in text for word in ['goods', 'product', 'material', 'hardware']):
        return 12
    return 18  # default GST rate for services