from huggingface_hub import InferenceClient

API_KEY = "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"

class HuggingFaceReader:
    """
    通用 Hugging Face Reader
    """
    def __init__(self, model_name):
        self.client = InferenceClient(api_key=API_KEY)
        self.model_name = model_name

    def generate_answer(self, query, retrieved_docs):
        """
        根据查询和检索到的文档生成答案。
        """
        context = "\n\n".join(
            [
                f"Document {i+1} Title: {doc['title']}\n"
                f"Content: {doc['content'][:1000]}"
                for i, doc in enumerate(retrieved_docs)
            ]
        )

        prompt = (
            f"Answer the following question based on the context provided:\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{query}\n\nAnswer:"
        )

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            answer = completion.choices[0].message["content"].strip()
        except Exception as e:
            answer = f"Error generating answer: {e}"

        return {
            "query": query,
            "answer": answer,
            "documents_used": len(retrieved_docs)
        }