'''
 O(1)时间复杂度实现入栈出栈获得栈中最小元素最大元素
'''
class Stack:

    def __init__(self):
        self.data = []
        self.minValue = []
        self.maxValue = []

    def push(self,data):
        self.data.append(data)
        if len(self.minValue) == 0:
            self.minValue.append(data)
        else:
            if data <= self.minValue[-1]:
                self.minValue.append(data)
        if len(self.maxValue) == 0:
            self.maxValue.append(data)
        else:
            if data >= self.maxValue[-1]:
                self.maxValue.append(data)

    def pop(self):
        if len(self.data) == 0:
            return None
        else:
            temp = self.data.pop()
            if temp == self.minValue[-1]:
                self.minValue.pop()
            if temp == self.maxValue[-1]:
                self.maxValue.pop()
            return temp

    def min(self):
        if len(self.minValue) == 0:
            return None
        else:
            return self.minValue[-1]

    def max(self):
        if len(self.maxValue) == 0:
            return None
        else:
            return self.maxValue[-1]

    def show(self):
        print("Stack Data")
        for d in self.data:
            print(d)
        print("min", self.min())
        print("max", self.max())
        print(self.minValue)
        print(self.maxValue)


s = Stack()
s.push(2)
s.push(1)
s.show()
s.push(4)
s.push(3)
s.push(2)
s.show()
s.pop()
s.show()
s.pop()
s.show()

