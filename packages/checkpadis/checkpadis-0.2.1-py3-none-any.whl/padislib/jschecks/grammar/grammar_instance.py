import tree_sitter_javascript as ts_javascript
from tree_sitter import Language


class JSGrammar:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JSGrammar, cls).__new__(cls)
            cls._instance._initialize_language()
        return cls._instance

    def _initialize_language(self):
        self.language = Language(ts_javascript.language())

    def get_language(self):
        return self.language
