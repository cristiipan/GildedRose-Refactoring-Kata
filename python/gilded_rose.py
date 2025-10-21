# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """
        更新所有物品的 quality 和 sell_in
        使用策略模式：每种物品类型有自己的更新策略
        """
        for item in self.items:
            # 1. 获取该物品的更新策略
            strategy = StrategyFactory.get_strategy(item.name)
            
            # 2. 使用策略更新物品
            strategy.update(item)
    # def update_quality(self):
    #     for item in self.items:
    #         if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
    #             if item.quality > 0:
    #                 if item.name != "Sulfuras, Hand of Ragnaros":
    #                     item.quality = item.quality - 1
    #         else:
    #             if item.quality < 50:
    #                 item.quality = item.quality + 1
    #                 if item.name == "Backstage passes to a TAFKAL80ETC concert":
    #                     if item.sell_in < 11:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1
    #                     if item.sell_in < 6:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1
    #         if item.name != "Sulfuras, Hand of Ragnaros":
    #             item.sell_in = item.sell_in - 1
    #         if item.sell_in < 0:
    #             if item.name != "Aged Brie":
    #                 if item.name != "Backstage passes to a TAFKAL80ETC concert":
    #                     if item.quality > 0:
    #                         if item.name != "Sulfuras, Hand of Ragnaros":
    #                             item.quality = item.quality - 1
    #                 else:
    #                     item.quality = item.quality - item.quality
    #             else:
    #                 if item.quality < 50:
    #                     item.quality = item.quality + 1

class UpdateStrategy:
    """物品更新策略的基类"""

    def update(self, item):
        raise NotImplementedError("子类必须实现 update 方法")

class SulfurasStrategy(UpdateStrategy):
    """传奇物品 Sulfuras 的更新策略"""
    
    def update(self, item):
        """
        Sulfuras 是传奇物品，永不改变
        - sell_in 不变
        - quality 不变（固定为 80）
        """
        # 什么都不做！Sulfuras 永恒不变
        pass

class NormalItemStrategy(UpdateStrategy):
    """普通物品的更新策略"""
    
    def update(self, item):
        """
        普通物品逻辑：
        1. sell_in 每天减 1
        2. quality 每天减 1
        3. 过期后（sell_in < 0），quality 衰减加倍（每天减 2）
        4. quality 最低为 0
        """
        # 减少 sell_in
        item.sell_in -= 1
        
        # 减少 quality
        if item.sell_in >= 0:
            # 未过期：减 1
            self._decrease_quality(item, 1)
        else:
            # 过期：减 2（衰减加倍）
            self._decrease_quality(item, 2)
    
    def _decrease_quality(self, item, amount):
        """
        减少 quality，确保不小于 0
        
        Args:
            item: 物品对象
            amount: 要减少的数量
        """
        item.quality = max(0, item.quality - amount)
    
class AgedBrieStrategy(UpdateStrategy):
    """Aged Brie（陈年布里奶酪）的更新策略"""
    
    def update(self, item):
        """
        Aged Brie 逻辑：
        1. sell_in 每天减 1
        2. quality 每天增 1（越陈越香）
        3. 过期后，quality 增长加倍（每天增 2）
        4. quality 最高为 50
        """
        # 减少 sell_in
        item.sell_in -= 1
        
        # 增加 quality
        if item.sell_in >= 0:
            # 未过期：增 1
            self._increase_quality(item, 1)
        else:
            # 过期：增 2（增长加倍）
            self._increase_quality(item, 2)
    
    def _increase_quality(self, item, amount):
        """
        增加 quality，确保不超过 50
        
        Args:
            item: 物品对象
            amount: 要增加的数量
        """
        item.quality = min(50, item.quality + amount)

class BackstagePassStrategy(UpdateStrategy):
    """Backstage Pass（后台通行证）的更新策略"""
    
    def update(self, item):
        """
        Backstage Pass 逻辑：
        1. sell_in 每天减 1
        2. 随着演出临近，quality 增长加速：
           - 距离演出 > 10 天：每天 +1
           - 距离演出 6-10 天：每天 +2
           - 距离演出 1-5 天：每天 +3
        3. 演出结束后（sell_in < 0），quality = 0
        4. quality 最高为 50
        """
        # 减少 sell_in
        item.sell_in -= 1
        
        if item.sell_in < 0:
            # 音乐会已经结束，通行证作废
            item.quality = 0
        else:
            # 根据距离演出的天数决定增长速度
            if item.sell_in >= 10:
                # 距离演出超过 10 天
                self._increase_quality(item, 1)
            elif item.sell_in >= 5:
                # 距离演出 5-9 天
                self._increase_quality(item, 2)
            else:
                # 距离演出 0-4 天（最后冲刺）
                self._increase_quality(item, 3)
    
    def _increase_quality(self, item, amount):
        """增加 quality，确保不超过 50"""
        item.quality = min(50, item.quality + amount)

class ConjuredStrategy(UpdateStrategy):
    """Conjured 物品的更新策略"""
    
    def update(self, item):
        """
        Conjured 物品：衰减速度是普通物品的 2 倍
        - 未过期：quality 每天 -2
        - 过期：quality 每天 -4
        - quality 最低为 0
        """
        # 减少 sell_in
        item.sell_in -= 1
        
        # 减少 quality
        if item.sell_in >= 0:
            # 未过期：减 2（普通物品的 2 倍）
            self._decrease_quality(item, 2)
        else:
            # 过期：减 4（普通物品过期的 2 倍）
            self._decrease_quality(item, 4)
    
    def _decrease_quality(self, item, amount):
        """减少 quality，确保不小于 0"""
        item.quality = max(0, item.quality - amount)

class StrategyFactory:
    """策略工厂：根据物品名称创建对应的更新策略"""
    
    # 策略映射表：物品名称 -> 策略类
    STRATEGIES = {
        "Aged Brie": AgedBrieStrategy,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy,
        "Sulfuras, Hand of Ragnaros": SulfurasStrategy,
        "Conjured Mana Cake": ConjuredStrategy,
    }
    
    @staticmethod
    def get_strategy(item_name):
        """
        根据物品名称获取对应的更新策略
        
        Args:
            item_name: 物品名称
            
        Returns:
            UpdateStrategy: 对应的策略对象
        """
        # 从映射表中查找策略类
        strategy_class = StrategyFactory.STRATEGIES.get(item_name)
        
        if strategy_class:
            # 找到了特殊物品的策略，创建并返回
            return strategy_class()
        else:
            # 没找到，说明是普通物品
            return NormalItemStrategy()