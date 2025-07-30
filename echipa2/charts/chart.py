import abc

class chart(abc.ABC):

    @abc.abstractmethod
    def layout(self):
        pass

    @abc.abstractmethod
    def draw_chart(self, x,y, title):
        pass

    @abc.abstractmethod
    def register_callback(self,id):
        pass

    # @abc.abstractmethod
    # def