from smartphone import Smartphone
catalog = [
        Smartphone(brand="RealMe", model="10", number="+79943543636"),
        Smartphone(brand="Xiaomi", model="13", number="+79309741212"),
        Smartphone(brand="OPPO", model="A5x", number="+79328643737"),
        Smartphone(brand="POCO", model="F2F", number="+79203845757"),
        Smartphone(brand="Tecno", model="SPARK", number="+79234859595")
        ]
for Smartphone in catalog:
    print(f"{Smartphone.brand} - {Smartphone.model}. {Smartphone.number}")