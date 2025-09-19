from transformers import pipeline

class TextAnalyzer:
    def __init__(self):
        self.summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

    def extract_key_ideas(self, text, max_length=130, min_length=30):
        """
        Извлекает ключевые идеи из текста с помощью модели суммаризации.
        """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

if __name__ == "__main__":
    sample_text = """
    Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта. К таким задачам относятся распознавание речи, обучение, планирование и решение проблем.
    """
    analyzer = TextAnalyzer()
    print("Ключевые идеи:", analyzer.extract_key_ideas(sample_text))
