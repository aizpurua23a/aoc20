from copy import deepcopy

class FoodSafety:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

        self.menu = []
        for row in data:
            ingredients = set(row.split('(')[0][:-1].split(' '))
            allergens = set(row.split('contains ')[1][:-1].split(', '))

            self.menu.append((ingredients, allergens))

        self.allergens = []

    def _remove_ingredient_and_allergen_from_menu(self, menu, ingredient, allergen):
        for i in range(len(menu)):
            menu[i][0].discard(ingredient)
            menu[i][1].discard(allergen)

        return menu

    def assign_allergens_to_ingredients_alternative_way(self):
        menu = deepcopy(self.menu)

        found_correlations = {}

        finished = False
        while not finished:
            allergens = set()
            ingredients = set()
            [allergens.update(row[1]) for row in menu]
            [ingredients.update(row[0]) for row in menu]

            if len(allergens) == 0:
                break

            for allergen in allergens:
                ingredients = set()
                [ingredients.update(row[0]) for row in menu]
                for new_ingredients, new_allergens in menu:
                    if allergen in new_allergens:
                        ingredients.intersection_update(new_ingredients)

                if len(ingredients) == 1:
                    (ingredient,) = ingredients
                    found_correlations[allergen] = ingredient
                    menu = self._remove_ingredient_and_allergen_from_menu(menu, ingredient, allergen)
                    break

        safe_ingredients = set()
        for ingredients, _ in menu:
            safe_ingredients.update(ingredients)

        self.allergens = list(found_correlations.items())
        self.allergens.sort(key=lambda x: x[0])

        return self.allergens, safe_ingredients

    def count_appearances_of_ingredients(self, ingredient_set):
        sum = 0
        for ingredient in ingredient_set:
            for ingredient_list, _ in self.menu:
                if ingredient in ingredient_list:
                    sum += 1
        return sum


if __name__ == '__main__':
    fs = FoodSafety('input.txt')
    allergens_list, safe_ingredients = fs.assign_allergens_to_ingredients_alternative_way()
    print(fs.count_appearances_of_ingredients(safe_ingredients))
    print(','.join(ingredient for _, ingredient in allergens_list))
