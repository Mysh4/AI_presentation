from flask import Flask, render_template_string, request, send_file
from nlp.text_analyzer import TextAnalyzer
from generator.presentation_generator import PresentationGenerator
import os

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<title>AI Presentation Generator</title>
<h2>Create a Presentation</h2>
<form method=post enctype=multipart/form-data>
    <label>Presentation Title:</label><br>
    <input type=text name=title required><br><br>
    <label>Text for Analysis:</label><br>
    <textarea name=text rows=10 cols=50 required></textarea><br><br>
    <label>Number of Main Slides:</label>
    <input type=number name=num_main_slides min=1 max=10 value=3 required><br><br>
    <label>Conclusions:</label><br>
    <input type=text name=conclusions required><br><br>
    <label>Bibliography (comma separated):</label><br>
    <input type=text name=bibliography required><br><br>
    <input type=submit value=Create>
</form>
{% if pptx_ready %}
    <h3>Presentation is ready!</h3>
    <a href="/download">Download presentation</a>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    pptx_ready = False
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        num_main_slides = int(request.form['num_main_slides'])
        conclusions = request.form['conclusions']
        bibliography = [b.strip() for b in request.form['bibliography'].split(',')]

        analyzer = TextAnalyzer()
        key_ideas = analyzer.extract_key_ideas(text)
        # Для примера разбиваем ключевые идеи на секции
        content_sections = [s.strip() for s in key_ideas.split('.') if s.strip()]
        # Гарантируем нужное количество секций
        if len(content_sections) < num_main_slides:
            content_sections += ["Нет данных для этого слайда"] * (num_main_slides - len(content_sections))
        else:
            content_sections = content_sections[:num_main_slides]

        generator = PresentationGenerator(title, content_sections, conclusions, bibliography, num_main_slides)
    generator.generate("presentation.pptx")
        pptx_ready = True
    return render_template_string(HTML_FORM, pptx_ready=pptx_ready)

@app.route('/download')
def download():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presentation.pptx")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Файл не найден", 404

if __name__ == "__main__":
    app.run(debug=True)
