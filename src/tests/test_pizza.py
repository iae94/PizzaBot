import unittest
from unittest.mock import Mock
from src.intents.pizza import Pizza


class TestPizza(unittest.TestCase):
    """
    Simple pizza cases test class
    """
    def setUp(self) -> None:
        api = Mock()
        self.intent = Pizza(api)
        self.intent.order = {
            'size': None,
            'payment': None
        }

    def test_dialog_positive(self):
        """
        Order confirm YES case
        :return:
        """
        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='хочу большую пиццу')
        self.assertEqual(self.intent.order['size'], 'большую')
        self.assertEqual(self.intent.state, 'ask_payment_method')

        self.intent.next(chat_id='', text='оплачивать буду картой')
        self.assertEqual(self.intent.order['payment'], 'картой')
        self.assertEqual(self.intent.state, 'ask_order')

        self.intent.next(chat_id='', text='да подтверждаю')
        self.assertEqual(self.intent.state, 'start')

    def test_dialog_negative(self):
        """
        Order confirm NO case
        :return:
        """
        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='хочу маленькую пиццу')
        self.assertEqual(self.intent.order['size'], 'маленькую')
        self.assertEqual(self.intent.state, 'ask_payment_method')

        self.intent.next(chat_id='', text='оплачивать буду наличкой')
        self.assertEqual(self.intent.order['payment'], 'наличкой')
        self.assertEqual(self.intent.state, 'ask_order')

        self.intent.next(chat_id='', text='нет не согласен')
        self.assertEqual(self.intent.state, 'start')

    def test_dialog_exit(self):
        """
        Intent exit case
        :return:
        """
        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='хочу маленькую пиццу')
        self.assertEqual(self.intent.order['size'], 'маленькую')
        self.assertEqual(self.intent.state, 'ask_payment_method')

        self.intent.next(chat_id='', text='выход')
        self.assertEqual(self.intent.state, 'start')

    def test_sizes(self):
        """
        Different sizes case
        :return:
        """
        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='Большую')
        self.assertEqual(self.intent.order['size'], 'большую')
        self.assertEqual(self.intent.state, 'ask_payment_method')
        self.intent.order['size'] = None

        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='Очень большую')
        self.assertEqual(self.intent.order['size'], 'большую')
        self.assertEqual(self.intent.state, 'ask_payment_method')
        self.intent.order['size'] = None

        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='Маленькую')
        self.assertEqual(self.intent.order['size'], 'маленькую')
        self.assertEqual(self.intent.state, 'ask_payment_method')
        self.intent.order['size'] = None

        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='Очень маленькую')
        self.assertEqual(self.intent.order['size'], 'маленькую')
        self.assertEqual(self.intent.state, 'ask_payment_method')
        self.intent.order['size'] = None

        self.intent.machine.set_state('ask_pizza_size')
        self.intent.next(chat_id='', text='Гигантскую')
        self.assertIsNone(self.intent.order['size'])
        self.assertEqual(self.intent.state, 'ask_pizza_size')
        self.intent.order['size'] = None

    def test_payments(self):
        """
        Different payment methods case
        :return:
        """
        self.intent.machine.set_state('ask_payment_method')
        self.intent.next(chat_id='', text='Картой')
        self.assertEqual(self.intent.order['payment'], 'картой')
        self.assertEqual(self.intent.state, 'ask_order')
        self.intent.order['payment'] = None

        self.intent.machine.set_state('ask_payment_method')
        self.intent.next(chat_id='', text='Наличкой')
        self.assertEqual(self.intent.order['payment'], 'наличкой')
        self.assertEqual(self.intent.state, 'ask_order')
        self.intent.order['payment'] = None

        self.intent.machine.set_state('ask_payment_method')
        self.intent.next(chat_id='', text='Воздухом')
        self.assertIsNone(self.intent.order['payment'])
        self.assertEqual(self.intent.state, 'ask_payment_method')
        self.intent.order['payment'] = None