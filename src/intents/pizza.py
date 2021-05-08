from transitions import Machine
from src.intents import Intent
import re

# https://stackoverflow.com/questions/60856982/python-transitions-library-how-to-pass-argumnets-to-a-transition

class Pizza(Intent):
    """
    Бот должен обрабатывать следующий диалог

    1. Какую вы хотите пиццу? Большую или маленькую?
    2. Большую
    3. Как вы будете платить?
    4. Наличкой
    5. Вы хотите большую пиццу, оплата - наличкой?
    6. Да
    7. Спасибо за заказ
    """
    states = [
        'start',
        'ask_pizza_size',
        'ask_payment_method',
        'ask_order',
    ]

    transitions = [
        {'trigger': 'next', 'source': '*', 'dest': 'start', 'conditions': ['is_intent_cancel_text'], 'after': ['send_cancel_text']},

        {'trigger': 'next', 'source': 'start', 'dest': 'ask_pizza_size', 'after': ['send_pizza_size_question']},

        {'trigger': 'next', 'source': 'ask_pizza_size', 'dest': 'ask_payment_method', 'conditions': ['is_pizza_size_valid'], 'after': ['save_pizza_size', 'send_payment_question']},
        {'trigger': 'next', 'source': 'ask_pizza_size', 'dest': 'ask_pizza_size', 'unless': ['is_pizza_size_valid'], 'after': ['send_pizza_size_clarification']},

        {'trigger': 'next', 'source': 'ask_payment_method', 'dest': 'ask_order', 'conditions': ['is_payment_method_valid'], 'after': ['save_payment_method', 'send_order_question']},
        {'trigger': 'next', 'source': 'ask_payment_method', 'dest': 'ask_payment_method', 'unless': ['is_payment_method_valid'], 'after': ['send_payment_clarification']},

        {'trigger': 'next', 'source': 'ask_order', 'dest': 'start', 'conditions': ['is_order_confirmed'], 'after': ['send_order_positive_text']},
        {'trigger': 'next', 'source': 'ask_order', 'dest': 'start', 'conditions': ['is_order_not_confirmed'], 'after': ['send_order_negative_text']},
        {'trigger': 'next', 'source': 'ask_order', 'dest': 'ask_order', 'unless': ['is_order_confirmed', 'is_order_not_confirmed'], 'after': ['send_order_clarification']},

    ]

    def __init__(self, api):
        super().__init__()
        self.api = api

        self.machine = Machine(
            model=self,
            states=Pizza.states,
            initial='start',
            transitions=Pizza.transitions,
            before_state_change=lambda event: self.logger.info(f'Change state to: \"{event.state.value}\"'),
            send_event=True
        )

        self.order = {
            'size': 'большую',      # Default
            'payment': 'наличкой',  # Default
        }
        self.pizza_size = {
            'большую': r'больш[уюаяой]{2,}',
            'маленькую': r'маленьк[уюаяой]{2,}'
        }
        self.payment_methods = {
            'наличкой': r'наличк[уаойе]{1,2}',
            'картой': r'карт[ыуаойе]{1,2}'
        }
        self.confirmation_words = {
            'yes': ['Да', 'Подтверждаю', 'Согласен'],
            'no': ['Нет', 'Отказываюсь', 'Не согласен']
        }
        self.cancel_words = [
            'Выход', 'Конец', 'Отстань'
        ]

    def send_pizza_size_question(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text="Какую вы хотите пиццу? Большую или маленькую?")

    def send_pizza_size_clarification(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text=f"""Я не совсем понимаю, для указания размера используйте слова: [{", ".join([f'"{s}"' for s in self.pizza_size])}]""")

    def send_payment_question(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text="Как вы будете платить?")

    def send_payment_clarification(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text=f"""Я не совсем понимаю, для указания способа оплаты используйте слова: [{", ".join([f'"{p}"' for p in self.payment_methods])}]""")

    def send_order_question(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text=f"Вы хотите {self.order['size']} пиццу, оплата - {self.order['payment']}?")

    def send_order_clarification(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text=f"""Я не совсем понимаю, для подтверждения/отмены заказа используйте слова: [{", ".join([f'"{w}"' for words in self.confirmation_words.values() for w in words])}]""")

    def send_order_positive_text(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text="Спасибо за заказ!")

    def send_order_negative_text(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text="Ок, напишите если захотите составить заказ заново или напишите \"Выход\" чтобы закончить диалог!")

    def send_cancel_text(self, event):
        self.api.send_message(chat_id=event.kwargs.get("chat_id"), text="Ок, спасибо за обращение!")

    #####################
    def is_pizza_size_valid(self, event):
        size = str(event.kwargs.get('text')).lower()
        return any(bool(re.search(v, size)) for v in self.pizza_size.values())

    def save_pizza_size(self, event):
        size = str(event.kwargs.get('text')).lower()
        for size_var, size_pat in self.pizza_size.items():
            if re.search(size_pat, size):
                self.order['size'] = size_var
                break

    def is_payment_method_valid(self, event):
        payment = str(event.kwargs.get('text')).lower()
        return any(bool(re.search(v, payment)) for v in self.payment_methods.values())

    def save_payment_method(self, event):
        payment = str(event.kwargs.get('text')).lower()
        for payment_var, payment_pat in self.payment_methods.items():
            if re.search(payment_pat, payment):
                self.order['payment'] = payment_var
                break

    def is_order_confirmed(self, event):
        text = str(event.kwargs.get('text')).lower()
        return any(str(c).lower() in text for c in self.confirmation_words['yes'])

    def is_order_not_confirmed(self, event):
        text = str(event.kwargs.get('text')).lower()
        return any(str(c).lower() in text for c in self.confirmation_words['no'])

    def is_intent_cancel_text(self, event):
        text = str(event.kwargs.get('text')).lower()
        return any(str(cancel_word).lower() == text for cancel_word in self.cancel_words)