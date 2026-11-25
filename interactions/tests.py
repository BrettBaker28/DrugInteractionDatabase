from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from . import rules
from .autocomplete import load_drug_names, suggest
from .models import DrugInteraction


class AutocompleteAcceptanceTests(SimpleTestCase):
    """Acceptance tests (Given/When/Then) run against the real drug list."""

    def get_suggestions(self, text):
        response = self.client.get(reverse('autocomplete'), {'q': text})
        self.assertEqual(response.status_code, 200)
        return response.json()['suggestions']

    def test_partial_name_suggests_matching_drug(self):
        # Given the drug list contains Warfarin
        # When the user types the start of its name
        suggestions = self.get_suggestions('warf')
        # Then Warfarin is offered as a completion
        self.assertIn('Warfarin', suggestions)

    def test_unknown_text_is_rejected_with_no_suggestions(self):
        # Given no drug name contains "zzzqqq"
        # When the user types it
        suggestions = self.get_suggestions('zzzqqq')
        # Then no completions are offered
        self.assertEqual(suggestions, [])

    def test_empty_input_is_rejected_with_no_suggestions(self):
        # Given the user has typed nothing but spaces
        # When the autocomplete is asked for completions
        suggestions = self.get_suggestions('   ')
        # Then no completions are offered (not the whole drug list)
        self.assertEqual(suggestions, [])


class SuggestUnitTests(SimpleTestCase):
    NAMES = ['Warfarin', 'Aspirin', 'Aspartame', 'Bivalirudin', 'Ibuprofen']

    def test_matching_ignores_case_and_spaces(self):
        self.assertEqual(suggest('  ASPI ', self.NAMES), ['Aspirin'])

    def test_names_starting_with_query_come_before_names_containing_it(self):
        self.assertEqual(suggest('i', self.NAMES)[0], 'Ibuprofen')
        self.assertIn('Aspirin', suggest('i', self.NAMES))

    def test_results_are_alphabetical_within_a_group(self):
        self.assertEqual(suggest('asp', self.NAMES), ['Aspartame', 'Aspirin'])

    def test_limit_caps_the_number_of_suggestions(self):
        self.assertEqual(len(suggest('a', self.NAMES, limit=2)), 2)
        self.assertEqual(suggest('a', self.NAMES, limit=0), [])

    def test_non_string_input_returns_nothing(self):
        self.assertEqual(suggest(None, self.NAMES), [])

    def test_drug_list_spreadsheet_loads(self):
        names = load_drug_names()
        self.assertGreater(len(names), 1000)
        self.assertIn('Warfarin', names)


class PageTests(SimpleTestCase):
    def test_pages_load(self):
        for name in ('home', 'search_drug', 'check_interactions'):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)


class CheckInteractionAcceptanceTests(TestCase):
    """UC-01 Check Two-Drug Interaction: Phase 2 acceptance tests, automated."""

    @classmethod
    def setUpTestData(cls):
        DrugInteraction.objects.create(
            ddinter_id_a='DDInter1951', drug_a='Warfarin',
            ddinter_id_b='DDInter20', drug_b='Acetylsalicylic acid',
            level='Major',
        )

    def check(self, drug1, drug2):
        return self.client.post(
            reverse('check_interactions'), {'drug1': drug1, 'drug2': drug2}
        )

    def test_AT01_known_pair_shows_its_severity_level(self):
        # Given Warfarin and Acetylsalicylic acid have a Major interaction on record
        # When the user enters both names and presses Find Interactions
        response = self.check('Warfarin', 'Acetylsalicylic acid')
        # Then the result shows both drugs and the DDInter level
        self.assertContains(response, 'Interaction Found')
        self.assertContains(response, 'Interaction Level: Major')

    def test_AT01_pair_is_found_in_either_order_and_any_case(self):
        # Given the record is stored as Warfarin + Acetylsalicylic acid
        # When the user enters them the other way round, in lower case
        response = self.check('acetylsalicylic acid', 'warfarin')
        # Then the same interaction is found
        self.assertContains(response, 'Interaction Level: Major')

    def test_AT01_7a_pair_with_no_record_shows_no_known_interaction(self):
        # Given both drugs exist but no interaction is on record for the pair
        # When the user checks them
        response = self.check('Warfarin', 'Abacavir')
        # Then the valid "no known interaction" result is shown, not an error
        self.assertContains(response, 'No known interaction found in our data')
        self.assertNotContains(response, 'Check Your Entry')

    def test_AT01_R1_missing_field_is_rejected(self):
        # Given the user fills only the first field
        # When they press Find Interactions
        response = self.check('Warfarin', '   ')
        # Then they are asked for both names and no result is shown (BR-01)
        self.assertContains(response, rules.MISSING_FIELD)
        self.assertNotContains(response, 'Interaction Found')

    def test_AT01_R2_unknown_drug_is_rejected(self):
        # Given "Notadrug" is not in the drug list
        # When the user checks it against Warfarin
        response = self.check('Warfarin', 'Notadrug')
        # Then the unknown name is reported back to them (BR-03)
        self.assertContains(response, 'No drug found: Notadrug')
        self.assertNotContains(response, 'No known interaction')

    def test_AT01_R3_same_drug_twice_is_rejected(self):
        # Given the user enters the same drug in both fields
        # When they press Find Interactions
        response = self.check('Warfarin', 'warfarin')
        # Then they are asked for two different drugs (BR-02)
        self.assertContains(response, rules.SAME_DRUG)

    def test_rejected_entry_is_kept_in_the_form(self):
        response = self.check('Warfarin', 'Notadrug')
        self.assertContains(response, 'value="Notadrug"')


class RulesUnitTests(SimpleTestCase):
    """Each business rule tested in isolation, without the web page."""

    NAMES = ('Warfarin', 'Aspirin')

    def test_BR01_both_fields_required(self):
        self.assertEqual(rules.validate_pair('', 'Aspirin', self.NAMES), rules.MISSING_FIELD)
        self.assertEqual(rules.validate_pair('Warfarin', None, self.NAMES), rules.MISSING_FIELD)

    def test_BR03_names_must_be_known_drugs(self):
        self.assertEqual(
            rules.validate_pair('Warfarin', 'Xyz', self.NAMES), rules.drug_not_found('Xyz')
        )

    def test_BR02_drugs_must_differ(self):
        self.assertEqual(rules.validate_pair('Aspirin', 'ASPIRIN ', self.NAMES), rules.SAME_DRUG)

    def test_valid_pair_is_allowed(self):
        self.assertIsNone(rules.validate_pair('warfarin', 'Aspirin', self.NAMES))


class ModelTests(SimpleTestCase):
    def test_interaction_is_described_by_its_two_drugs(self):
        interaction = DrugInteraction(drug_a='Warfarin', drug_b='Aspirin')
        self.assertEqual(str(interaction), 'Warfarin + Aspirin')
