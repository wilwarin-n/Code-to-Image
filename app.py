# app.py
import base64

from flask import (
    Flask, 
    render_template, 
    session,
    redirect,
    request,
    url_for,
)

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer, JavaLexer, CSharpLexer, PhpLexer, JavascriptLexer, get_lexer_by_name
from pygments import lexers




from pygments.styles import get_all_styles

from utils import take_screenshot_from_url

app = Flask(__name__,template_folder="templates",static_folder='static')
app.secret_key = '00bb777569a9cdda23c898611eec43355e319cb9581ebc1e8f0e708e445e034f'

PLACEHOLDER_CODE = "print('Hello World!')"
DEFAULT_STYLE = "monokai"
NO_CODE_FALLBACK = "# No Code Entered"
DEFAULT_LANG = "python"


lang_list = ["Python3Lexer","JavaLexer","CSharpLexer","PhpLexer"]

# main view
@app.route("/", methods=["GET"])
def main():
    if session.get("lang") is None:
        session["lang"] = DEFAULT_LANG
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE

    lines = session["code"].split("\n")

    context = {
        "message": "Select Programming Language 🤍",
        "lang": session["lang"],
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }

    return render_template("code_select.html", **context,lang_list=lang_list)



# save_code view
@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    session["lang"] = request.form.get("lang")
    return redirect(url_for("main"))

# python_input view
@app.route("/get_python", methods=["GET"])
def get_python():
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    context = {
        "message": "Paste Your Python Code 🔥"
    }

    return render_template("python_input.html", **context)

@app.route("/post_python", methods=["POST"])
def post_python():
    session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("get_python"))

@app.route("/get_java", methods=["GET"])
def get_java():
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    context = {
        "message": "Paste Your Java Code 🤍"
    }
    return render_template("java_input.html")

# reset_session view
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("main"))



# style view
@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE

    formatter = HtmlFormatter(style=session["style"])

    
    context = {
        "message": "Select Your Style 🎨",
        "all_styles": list(get_all_styles()),
        
        "style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,

        
        
        "highlighted_code": highlight(
            session["code"], Python3Lexer(), formatter),
        "java_hl_code": highlight(
            session["code"], JavaLexer(), formatter),
        "csharp_hl_code": highlight(
            session["code"], CSharpLexer(), formatter),
        "php_hl_code": highlight(
            session["code"], PhpLexer(), formatter),
        "javasc_hl_code": highlight(
            session["code"], JavascriptLexer(), formatter),
    }
    return render_template("style_selection.html", **context)



# save_style view
@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None: 
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("style"))

# save_lang
@app.route("/save_lang", methods=["POST"])
def save_lang():
    session["lang"] = request.form.get("lang")
    return redirect(url_for("main"))









# image view
@app.route("/image", methods=['GET'])
def image():
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style")
    image_bytes = take_screenshot_from_url(target_url,session_data)
    context = {
        "message": "Done! 🎉",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8")
    }
    return render_template("image.html", **context)


    
# fikirler 1- highlight içini değiştirme, 2-if else kullan 3- en son olarak hiçbiri olmazsa hepsine ayrı buton ekle 4- belki fonksiyonlar