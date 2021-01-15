from app.latex import bp
from app import db
from config import basedir
from flask import send_from_directory, redirect, url_for
from app.models import Carnet, Answer



@bp.route('/latex/<id_carnet>', methods=['GET', 'POST'])
def latex(id_carnet):
	print("latex page")
	directory, filename = generate_latex(id_carnet)

	return send_from_directory(directory=directory, filename=filename, as_attachment=True)



LATEX_HEAD = """
\\documentclass{article}
\\usepackage{blindtext}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[french]{babel}
\\usepackage{amsfonts}

\\setlength\\parindent{0pt}

\\begin{document}
"""


def tex_section(str):
	return  "\\section{" + str + "}\n"
def tex_subsection(str):
	return "\\subsection{" + str + "}\n"

def answers_to_tex(answers):
	return "\\\\\n".join(list(map(lambda a: a.text_content, answers))) + "\n"

def subcarnet_to_tex(carnet):
	str = tex_subsection(carnet.name)
	str += answers_to_tex(carnet.answers)
	str += "\n"

	for c in carnet.children_carnets:
		str += subcarnet_to_tex(c)

	return str

def generate_latex(id_carnet):
	directory = basedir + "/tmp/"
	filename = f"testfile{id_carnet}.tex"
	path = directory + filename
	f = open(path, "w+")

	carnet = Carnet.query.get(int(id_carnet))

	str_to_write = LATEX_HEAD
	str_to_write += tex_section(carnet.name)
	
	# Answers in main carnet
	str_to_write += answers_to_tex(carnet.answers) + "\n"

	# Sub carnet
	for c in carnet.children_carnets:
		str_to_write += subcarnet_to_tex(c)

	f.write(str_to_write)

	f.write("\\end{document}")
	f.close()

	return directory, filename