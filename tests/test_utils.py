from django.test import TestCase

from template_forms import utils


class BS3ColsTests(TestCase):
    def test_simple(self):
        result = utils.bs3_cols({'xs': '8'})
        self.assertEqual(result, 'col-xs-8')

    def test_multiple(self):
        result = utils.bs3_cols({'md': '6', 'xs': '8'})
        self.assertEqual(result, 'col-md-6 col-xs-8')

    def test_number_coercion(self):
        result = utils.bs3_cols({'md': 6, 'xs': 8})
        self.assertEqual(result, 'col-md-6 col-xs-8')

    def test_list_of_tuples(self):
        result = utils.bs3_cols([('md', '6'), ('xs', '8')])
        self.assertEqual(result, 'col-md-6 col-xs-8')


class BS3InverseColsTests(TestCase):
    def test_simple(self):
        result = utils.bs3_inverse_cols({'xs': '8'})
        self.assertEqual(result, 'col-xs-4')

    def test_multiple(self):
        result = utils.bs3_inverse_cols({'md': '6', 'xs': '8'})
        self.assertEqual(result, 'col-md-6 col-xs-4')

    def test_offset(self):
        result = utils.bs3_inverse_cols({'md': '6', 'xs': '8'}, offset=True)
        self.assertEqual(result, 'col-md-offset-6 col-xs-offset-4')

    def test_number_coercion(self):
        result = utils.bs3_inverse_cols({'md': 6, 'xs': 8})
        self.assertEqual(result, 'col-md-6 col-xs-4')

    def test_list_of_tuples(self):
        result = utils.bs3_inverse_cols([('md', '6'), ('xs', '8')])
        self.assertEqual(result, 'col-md-6 col-xs-4')
