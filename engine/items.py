class Item:
    import json

    def __init__(self):
        self.init()

    def init(self):
        self.properties = dict(
            name = None,
            sprite = None,
            price = None,
            equippable = None
        )

    def load(self, itemNum):
        json_data = open("resources/items/" + itemNum, "r")
        item_data = json.loads(json_data.read)

        self.properties = item_data['properties']

        json_data.close()