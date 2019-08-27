import tcod

from components.message import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You can not carry anymore; inventory is full.', tcod.yellow)
            })
        else:

            self.items.append(item)
            results.append({
                'item_added': item,
                'message': Message(f'You pick up the {item.name}.', tcod.blue)
            })

        return results

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owser.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)

        results.append({'item_dropped': item, 'message': Message(
            f'You dropped the {item.name}', tcod.yellow)})

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append(
                    {'message': Message(f'The {item_entity.name} can not be used.', tcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') and kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(
                    self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)
