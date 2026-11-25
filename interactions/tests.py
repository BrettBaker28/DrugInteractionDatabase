from django.test import SimpleTestCase
from django.urls import reverse

from .autocomplete import load_drug_names, suggest


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
