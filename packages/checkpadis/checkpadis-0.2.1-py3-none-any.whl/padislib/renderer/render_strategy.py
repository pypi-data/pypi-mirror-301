from abc import ABC, abstractmethod


class RenderStrategy(ABC):
    @abstractmethod
    def render(self, data, file_path=None):
        pass
