import os
import glob
from flask import Flask, render_template, url_for
app = Flask(__name__)
import markdown
from datetime import datetime
from markdown.extensions.codehilite import CodeHiliteExtension
from bs4 import BeautifulSoup

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
    markdown_content = []

    for root, dirs, files in os.walk(directory):
        dirs.sort(key=lambda x: datetime.strptime(x, "%m-%d-%Y"), reverse=True)
        for dir in dirs:
            date_object = datetime.strptime(dir, "%m-%d-%Y")
            formatted_date = date_object.strftime("%B %d, %Y")  # Gives 'January 03, 2023'

            # Append the directory name as an h1 element
            markdown_content.append({
                'content': '<h1>{}</h1>'.format(formatted_date),
                'is_dir': True
            })

            # Get path to current directory
            dir_path = os.path.join(root, dir)

            # Get all markdown files in the current directory
            md_files = glob.glob(os.path.join(dir_path, '*.md'))
            
            # Sort markdown files by creation time in descending order
            md_files.sort(key=os.path.getctime, reverse=True)

            for file in md_files:
                with open(file, 'r') as f:
                    md = f.read()
                    html = markdown.markdown(md, extensions=[CodeHiliteExtension(linenums=False)])

                    header, _, content = html.partition('</h1>')
                    header = header.replace('<h1>', '<h2>')
                    header += '</h2>'
                    
                    # Create a soup object from the content
                    soup = BeautifulSoup(content[:100] + '...', 'html.parser')
                    # Use the 'prettify' method to get well-formed HTML
                    content_excerpt = soup.prettify()


                    markdown_content.append({
                        # 'filename' now includes the relative path from the root directory
                        'filename': os.path.relpath(file, start=root),
                        'content': header + content_excerpt + '...',
                        'is_dir': False
                    })

    return render_template('markdowns.html', markdown_content=markdown_content)

@app.route('/markdown/<filename>')
def markdown_file(filename):
    directory = './markdowns'
    with open(os.path.join(directory, filename), 'r') as f:
        md = f.read()
        html = markdown.markdown(md, extensions=[CodeHiliteExtension(linenums=False)])
    return render_template('markdown_file.html', html=html, back_url=url_for('index', initial_view='markdowns'))


if __name__ == '__main__':
    app.run(debug=True)