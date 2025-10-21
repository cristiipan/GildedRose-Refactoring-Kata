from gilded_rose import Item, GildedRose

# 测试普通物品
items = [Item("+5 Dexterity Vest", 10, 20)]
gilded_rose = GildedRose(items)

print("Day 0:", items[0])
for day in range(1, 6):
    gilded_rose.update_quality()
    print(f"Day {day}:", items[0])