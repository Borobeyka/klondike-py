import pygame

from objects.glob import *
from objects.actions import *
from objects.heap import *

class Stack(Actions):

    def __init__(self, surface, x, y):
        super().__init__(surface, x, y)
        self.cards = []

    def count(self):
        return len(self.cards)

    def is_empty(self):
        return False if self.count() > 0 else True

    def show(self):
        if self.is_empty():
            surface = pygame.Surface((config["card"]["width"], config["card"]["height"]), pygame.SRCALPHA)
            
            pygame.draw.rect(surface, config["color"]["darkgreen"],
                (0, 0, config["card"]["width"], config["card"]["height"]),
                border_radius=config["card"]["radius"])
            pygame.draw.rect(surface, config["color"]["lightgreen"],
                (0, 0, config["card"]["width"], config["card"]["height"]),
                2, config["card"]["radius"])
            self.surface.blit(surface, (self.x, self.y))

        else:
            for card in self.cards:
                card.show()
    
    def is_in_area(self, x, y):
        if (x > self.x and x < self.x + config["card"]["width"] and
            y > self.y and y < self.y + config["card"]["height"] +
            (self.count() == 1 or 0 if self.count() == 0 else (self.count() - 1) * config["stack"]["offset"])):
            return True
        return False
    
    def is_can_stack(self, heap):
        if self.is_empty() and heap.cards[0].nominal != 12:
            return False
        if self.count() > 0 and (self.get_last_card().icon_color == heap.cards[0].icon_color or
            self.get_last_card().nominal - heap.cards[0].nominal != 1) and self.get_last_card().is_visible:
            return False
        return True
    
    def get_last_card(self):
        return self.cards[-1]

    def get_heap_on_focus(self, x, y):
        for card in self.cards[::-1]:
            if card.is_in_area(x, y) and card.is_visible:
                heap = Heap(window, card.x, card.y)
                heap.mouse_offset_x = abs(x - card.x)
                heap.mouse_offset_y = abs(y - card.y)
                index = self.cards.index(card)

                for idx, card in enumerate(self.cards):
                    if idx >= index:
                        heap.add_card(card)
                del self.cards[index:]
                return heap
        
    def push_heap(self, heap):
        for card in heap.cards:
            card.x = self.x
            card.y = self.y + self.count() * config["stack"]["offset"]
            self.cards.append(card)

    def push_card(self, card):
        cards.remove(card)
        card.x = self.x;
        card.y = self.y + self.count() * config["stack"]["offset"];
        self.cards.append(card)

    def add_card(self, card):
        if self.is_empty() and card.nominal != 12:
            return
        if self.count() >= 1 and (self.get_last_card().icon_color == card.icon_color or
            self.get_last_card().nominal - card.nominal != 1):
            return
        card.x = self.x
        card.y = self.y + self.count() * config["stack"]["offset"]
        self.cards.append(card)