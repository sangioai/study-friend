from flask import Flask
import webbrowser
import argparse
import markdown
import urllib
import re
import os

from .utils import (
    add_argument_common,
    add_argument_display,
    print_args,
    extract_url
)

from .constants import (
    DEFAULT_HTML_DIV,
    DEFAULT_HTML_IMAGE,
    DEFAULT_HTML_STYLE
)

contents = {}

def make_routes(app : Flask, html, start_sep=r"<h1>", stop_sep=r"</h1>", verbose=False):
    """
        Describe this function for documentation purposes.
        This function will create routes for each title in the HTML file.
        The routes will be accessible via the route /<title> and will display its speicific content.
        Args:
            app (Flask): The Flask app to add routes to.
            html (str): The HTML content to extract titles from.
            start_sep (str): The start separator for the title.
            stop_sep (str): The stop separator for the title.
        Returns:
            routes (list): A list of routes encoded via urllib.parse.quote_plus
    """
    routes = []
    # let's extraxt both start and finish of titles
    t_starts = list(re.finditer(start_sep, html))
    t_ends = list(re.finditer(stop_sep, html))
    # let's create a route for each of them
    for i in range(len(t_starts)):
        # extract title string
        title = f"{i} - "+html[t_starts[i].end():t_ends[i].start()]
        # encode title in proper URL format
        title = urllib.parse.quote_plus(title)
        # extract content string -  next_i must be consistent
        i_next = t_starts[i+1].start() if (i < len(t_starts)-1) else -1
        # add style to html
        contents[title] = html[t_starts[i].start():i_next] 
        # append to titles
        routes += [title]
    # create route
    @app.route('/<title>') 
    def slide(title):
        if verbose:
            print(title)
        # bug-fix: unquote and requote to have same correct title
        title = urllib.parse.quote_plus(urllib.parse.unquote_plus(title))
        return DEFAULT_HTML_STYLE+contents[title]
    return routes


def display_on_web(html, url, static_directory, verbose):
    """
        This function is used to display HTML content on a web browser via a Flask app.
        Args:
            html (str): HTML content.
            url (str): URL to open in web browser.
            static_directory (str): path to static directory.
            verbose (bool): whether to print verbose output.
        Returns:
            None
    """
    # ensure absolute path
    static_directory = os.path.abspath(static_directory)
    if verbose:
        print(f"static_directory: {static_directory}")
    # init flask webapp at uri
    app = Flask(__name__, static_url_path=static_directory, static_folder=static_directory)
    # get routes
    routes = make_routes(app, html, verbose=verbose)
    if verbose:
        print(f"routes:{routes}")
    # add html in root page
    @app.route("/")
    def index():
        return DEFAULT_HTML_STYLE+"</br>".join(f"""<a href="{url}/{r}">{urllib.parse.unquote_plus(r)}</a>"""for r in routes)
    # open browser at uri
    webbrowser.open(url)
    # serve flask app
    app.run(*extract_url(url))


def markdown_to_html(fileName, verbose):
    """
        This function reads a markdown file and converts it to HTML returning also the images commond directory.
        First, it reads the file line by line. If a line contains a question mark, it replaces it with a proper HTML icon. 
        Then, it searches for images in the line. If it finds any, it replaces them with HTML images. 
        Finally, it appends the line to the HTML content.
        Args:
            fileName (str): path to Markdown file.
            verbose (bool): whether to print verbose output.
        Returns:
            html (str): HTML content.
            common_dir (str): common directory of images.
    """
    html = ""
    images = []
    with open(fileName,"r") as rfile:
        while (line := rfile.readline()) != "" :
            # replace :question: with proper HTML icon 
            line = line.replace(":question:","&#10067;")
            # find all images in row
            files = re.findall(r"Files: \[(.*)\]$", line)
            # replace files with HTML images
            if files != []:
                # extract filenames
                files = files[0].split(",")
                # add html images
                images_html = ""
                for file in files:
                    # ensure absolute path
                    file = os.path.abspath(file.strip())
                    # append image path
                    images += [file]
                    # create HTML image
                    images_html += DEFAULT_HTML_IMAGE.format(file=file)
                # append images to html
                html += DEFAULT_HTML_DIV.format(images=images_html) + "\n"
            # line is ok - write it back
            else:
                html += line + "\n"
    # https://medium.com/@smrati.katiyar/convert-markdown-to-html-with-maths-equation-and-code-snippet-highlighting-1c3144455e4d
    extensions = ['pymdownx.superfences', 'pymdownx.highlight', 'pymdownx.arithmatex', 'pymdownx.inlinehilite']
    extension_configs = {"pymdownx.highlight": {"linenums": True}, 'pymdownx.arithmatex': {'generic': True}}
    html = markdown.markdown(html, extensions=extensions, extension_configs=extension_configs)
    # get common path
    common_dir = os.path.dirname(images[0]) if len(images) == 1 else  os.path.commonpath(images) 
    return html, common_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display a generated Markdown file using a web browser or a Jupyter notebook.")
    add_argument_common(parser)
    add_argument_display(parser)
    args = parser.parse_args()
    if args.verbose:
        print("Options:")
        print_args(args)
    # convert file to html and static_directory
    html, static_dir = markdown_to_html(args.file, args.verbose)
    # check where to display
    if args.here:
        print(html)
    else:
        # display on web
        display_on_web(html, args.url, static_dir, args.verbose)