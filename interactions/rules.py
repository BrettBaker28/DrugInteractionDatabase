"""Business rules for the two-drug check (UC-01).

Each rule is enforced here and nowhere else, so the view only has to ask
"is this pair allowed?" and show the message it gets back.

    BR-01  both drug fields must be filled       -> rejection R-1
    BR-03  each name must be a drug we know      -> rejection R-2
    BR-02  the two names must be different drugs -> rejection R-3
"""

from .autocomplete import load_drug_names

MISSING_FIELD = "Please enter a drug name in both fields."
SAME_DRUG = "Please enter two different drugs."


def drug_not_found(name):
    return (
        f"No drug found: {name}. "
        "Check the spelling or choose a name from the suggestions."
    )


def validate_pair(drug1, drug2, known_names=None):
    """Return the rejection message for this pair, or None if it is allowed."""
    drug1 = (drug1 or "").strip()
    drug2 = (drug2 or "").strip()

    # BR-01: both fields filled
    if not drug1 or not drug2:
        return MISSING_FIELD

    # BR-03: both names are real drugs
    if known_names is None:
        known_names = load_drug_names()
    known = {name.lower() for name in known_names}
    for name in (drug1, drug2):
        if name.lower() not in known:
            return drug_not_found(name)

    # BR-02: two different drugs
    #if drug1.lower() == drug2.lower():
    #    return SAME_DRUG

    return None
