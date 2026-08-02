class GameObject:
    '''Инициализируем родитлельский край'''

    def __init__(self, color, x, y, width=20, height=20):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        '''передаем пустой метод отрисовки для дочерних классов'''
        pass
