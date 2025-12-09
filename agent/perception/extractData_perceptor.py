# perception/extractData_perceptor.py

from bs4 import BeautifulSoup


# ---------------------------------------------------------
# 1. DOM PARSER
# ---------------------------------------------------------
def parse_dom(html: str):
    """Extract clean text elements from DOM."""
    soup = BeautifulSoup(html, "html.parser")
    TARGET_TAGS = ["p", "span", "div", "td", "label"]

    elements = []
    for tag in soup.find_all(TARGET_TAGS):
        text = tag.get_text(strip=True)
        if not text or len(text) <= 1:
            continue

        elements.append({
            "text": text,
            "tag": tag.name,
            "attributes": dict(tag.attrs),
            "raw_tag": tag
        })

    return elements


# ---------------------------------------------------------
# 2. INTENT FILTER
# ---------------------------------------------------------
def filter_by_intent(elements, intent):
    """Return only elements that match intent keywords."""
    keywords = [kw.lower() for kw in intent.get("keywords", [])]
    if not keywords:
        return elements  # If no keywords, return all

    matched = []
    for el in elements:
        text = el["text"].lower()
        if any(kw in text for kw in keywords):
            matched.append(el)

    return matched


# ---------------------------------------------------------
# 3. SELECTOR GENERATOR
# ---------------------------------------------------------
def generate_selector(element):
    """Generate simple CSS/XPath selectors based on attributes."""
    attrs = element["attributes"]

    # prefer id (unique)
    if "id" in attrs:
        return {
            "css": f"#{attrs['id']}",
            "xpath": f"//*[@id='{attrs['id']}']"
        }

    # fall back to first class
    if "class" in attrs and len(attrs["class"]) > 0:
        cls = attrs["class"][0]
        return {
            "css": f".{cls}",
            "xpath": f"//*[@class='{cls}']"
        }

    # fallback: text-based selector
    text = element["text"][:20]
    return {
        "css": None,
        "xpath": f"//*[contains(text(), '{text}')]"
    }


# ---------------------------------------------------------
# 4. LABEL-VALUE PAIRING
# ---------------------------------------------------------
def extract_label_value_pairs(elements):
    """
    Basic label-value logic:
    - Treat labels ending with ':' as keys
    - Next element in DOM order is value
    """
    pairs = []

    for i in range(len(elements) - 1):
        label_text = elements[i]["text"]

        # Detect a label
        if label_text.endswith(":") or "number" in label_text.lower():
            cleaned_label = label_text.replace(":", "").strip()
            value_text = elements[i + 1]["text"]

            pairs.append({
                "label": cleaned_label,
                "value": value_text
            })

    return pairs


# ---------------------------------------------------------
# 5. MAIN PERCEPTION ENTRY POINT
# ---------------------------------------------------------
def extract_perception(observation):
    """
    Main perception orchestrator:
    - Receives raw HTML and intent
    - Performs DOM parsing
    - Filters by intent
    - Extracts label-value pairs
    - Generates selectors
    - Returns structured perception
    """

    html = observation.get("html", "")
    intent = observation.get("intent", {})

    # 1) DOM → element objects
    elements = parse_dom(html)

    # 2) Filter by keywords
    matched = filter_by_intent(elements, intent)

    # 3) Label-value extraction
    label_value_pairs = extract_label_value_pairs(elements)

    # 4) Add selectors to matched elements
    for el in matched:
        el["selectors"] = generate_selector(el)

    # FINAL OUTPUT
    return {
        "status": "processed",
        "goal": intent.get("goal"),
        
        "matched_elements_count": len(matched),
        "matched_elements": matched,

        "label_value_pairs": label_value_pairs,

        "raw_elements_preview": elements[:30]
    }
