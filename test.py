import unittest
from unittest.mock import patch, Mock

from main import save_doc, get_content, has_floor_info, _get_html, Card, Cards


class TestScraping(unittest.TestCase):
    def setUp(self):
        self.card = Card('1000', '10', 'Street', '2', '100', '1')
        self.cards = Cards()
        self.cards.add(self.card)

    def test_card_creation(self):
        self.assertEqual(self.card.price, '1000')
        self.assertEqual(self.card.price_per_m2, '10')
        self.assertEqual(self.card.street, 'Street')
        self.assertEqual(self.card.rooms, '2')
        self.assertEqual(self.card.m2, '100')
        self.assertEqual(self.card.floor, '1')

    def test_cards_collection(self):
        self.assertEqual(len(self.cards.get_all()), 1)
        self.assertEqual(self.cards.get_all()[0], self.card)

    def test_card_price_is_digit(self):
        self.assertTrue(self.card.price.isdigit())

    def test_card_price_per_m2_is_digit(self):
        self.assertTrue(self.card.price_per_m2.isdigit())

    def test_card_rooms_is_digit(self):
        self.assertTrue(self.card.rooms.isdigit())

    def test_card_m2_is_digit(self):
        self.assertTrue(self.card.m2.isdigit())

    def test_card_floor_is_digit(self):
        self.assertTrue(self.card.floor.isdigit())

    @patch('requests.get')
    def test_get_html(self, mock_get):
        mock_resp = Mock()
        mock_resp.text = 'html content'
        mock_get.return_value = mock_resp
        result = _get_html('https://www.google.com.ua/')
        self.assertEqual(result, 'html content')

    def test_has_floor_info_true(self):
        item = Mock()
        item.find.return_value.find_all.return_value = ['1', '2', '3']
        self.assertTrue(has_floor_info(item))

    def test_has_floor_info_false(self):
        item = Mock()
        item.find.return_value.find_all.return_value = ['1', '2']
        self.assertFalse(has_floor_info(item))

    @patch('openpyxl.Workbook')
    def test_save_doc(self, mock_workbook):
        mock_workbook.return_value.active.append.side_effect = None
        mock_workbook.return_value.save.side_effect = None
        save_doc([self.card], 'test.xlsx')


if __name__ == '__main__':
    unittest.main()
