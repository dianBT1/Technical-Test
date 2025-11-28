class RagService:
    def __init__(self,document_store):
        self.document_store = document_store
    
    # LangGraph state = plain dict
    def simple_retrieve(self,state):
        query = state["question"]
        results = self.document_store.search_document_store(query)
        state["context"] = results
        return state

    def simple_answer(self,state):
        ctx = state["context"]
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state
