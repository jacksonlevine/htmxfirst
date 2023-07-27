import os
import glob
from flask import Flask, render_template, url_for
app = Flask(__name__)
import markdown

@app.route('/', defaults={'initial_view': 'home'})
@app.route('/<initial_view>')
def index(initial_view):
    return render_template('index.html', initial_view=initial_view)

@app.route('/home')
def homecontent():
    return "Resource content TESTER!!!! Home page"

@app.route('/projects')
def projectspage():
    return "Projects page"

@app.route('/markdowns')
def markdowns():
    directory = './markdowns'

    files = glob.glob(os.path.join(directory, '*.md'))
    files.sort(key=os.path.getctime, reverse=True)
    markdown_content = []

    for file in files:
        with open(file, 'r') as f:
            md = f.read()
            html = markdown.markdown(md)

            header, _, content = html.partition('</h1>')
            header = header.replace('<h1>', '<h2>')
            header += '</h2>'
            markdown_content.append({
                'filename': os.path.basename(file),
                'content': header + content[:100] + '...'
            })
            
    return render_template('markdowns.html', markdown_content=markdown_content)

@app.route('/markdown/<filename>')
def markdown_file(filename):
    directory = './markdowns'
    with open(os.path.join(directory, filename), 'r') as f:
        md = f.read()
        html = markdown.markdown(md)
    return render_template('markdown_file.html', html=html, back_url=url_for('index', initial_view='markdowns'))


if __name__ == '__main__':
    app.run(debug=True)