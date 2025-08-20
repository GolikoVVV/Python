from address import Address
from mailing import Mailing

fm = Address("183014", "Мурманск", "Ленина", "45", "12")
to = Address("205086", "Тула", "Герцена", "73", "18")

Mail = Mailing(fm,to, "400", "654747747")

print(f"Отправление с трэк-номером:", Mail.track, "из", fm, "в", to, ".", "Стоимость:", Mail.cost, "рублей")