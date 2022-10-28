##################################################
## Import libraries
import os
from flask import Flask, make_response, request, send_from_directory, render_template, redirect, url_for, flash
from flask import Flask, make_response, request, send_from_directory, abort, render_template
from rdflib import Graph
from rdflib.query import Result
from etc import FILES, REQUESTS


############################################################
## Dict with file extensions as keys and MIMEtypes as values
MIMES = {
    '.rdf': 'application/rdf+xml',
    '.ttl': 'text/turtle',
    '.nt' : 'text/plain',
    '.jsonld': 'application/ld+json'
}


def create_app() -> Flask:
    app = Flask(__name__)

    # generate secret key:  $ python -c 'import secrets; print(secrets.token_hex())'
    app.secret_key = 'bbe5ab933da0be71ffe196d77527a6a30b7eb73347ca029c6a7447ae3c3ca4e6'

    # create routing rules
    app.add_url_rule('/', view_func=overview)
    app.add_url_rule('/<filename>', view_func=get_file)

    return app



############################################################
## Serve FOAF data in available notations (with redirect and flash)
def get_file(filename:str):
    name, ext = os.path.splitext(filename)
    mime = get_mime(ext)

    if not mime: 
        flash(f'File extension "{ext}" is not supported!')
        return redirect(url_for('overview'), 404)

    resp = make_response(get_notation(name, ext))
    if resp.status_code == 200: resp.mimetype = mime
    return resp


def get_request(name: str) -> str:
    with open(os.path.join(REQUESTS, name), encoding='utf8') as rq:
        return rq.read()

def execute_sparql(g:Graph, rq: str) -> Result:
    return g.query(rq)

def get_table(id: str):
    rq = get_request('placeholder.rq')
    rq = rq.replace('<<Placeholder>>', id)
    g = Graph().parse(os.path.join(FILES, 'data.ttl'))
    try:
        rst = execute_sparql(g, rq)
    except Exception as e:
        rst = [['Invalid Attribute']]
    
    table = []
    for (ts, val, unit) in rst:
        unit = unit.toPython()
        unit = unit[unit.find('#') +1:]
        table.append([ts.toPython(), val.toPython(), unit])

    return render_template('table.html', id=id, table=table)

############################################################
## Show overview of available files and formats (with flash)
def overview():
    root, dirs, files = next(os.walk(FILES))
    names = sorted([os.path.splitext(f)[0] for f in files])
    return render_template('overview_with_flash.html', names=names, exts=sorted(MIMES.keys()))


# ############################################################
## Return Response data''
def get_notation(name, ext: str):
    # get file extension of existing file
    f_ext = get_true_ext(name, ext)

    if not f_ext:
        flash(f'Filename "{name}" does not exist!')
        return redirect(url_for('overview'), 404)
    elif f_ext.startswith('.'):
        f = f'{request.url[:-len(ext)]}{f_ext}'
        return (serialize(parse(f), ext), 200) # request for serialized data
    return send_from_directory(FILES, f_ext) # request for original file


def get_file(filename:str):
    name, ext = os.path.splitext(filename) # [0]: filename [1]: .{file extension}
    mime = get_mime(ext)

    # Return BAD REQUEST (bc file extension is not supported); 404 would be also fine
    if not mime: return (f'File extension "{ext}" is not supported!', 400)

    # Create Response
    resp = make_response(get_notation(name, ext))

    # Assign MIMEtype (default: text/html)
    if resp.status_code == 200: resp.mimetype = mime
    return resp


############################################################
## Return available MIMEtype or ''
def get_mime(ext: str) -> str:
    if ext in MIMES.keys(): return MIMES[ext] 
    return ''


############################################################
## Return Response data''
def get_notation(name: str, ext: str):
    # get file extension of existing file
    f_ext = get_true_ext(name, ext)

    if not f_ext:
        return abort(404) # file does not exist
    elif f_ext.startswith('.'):
        f = f'{request.url[:-len(ext)]}{f_ext}'
        return (serialize(parse(f), ext), 200) # request for serialized data
    return send_from_directory(FILES, f_ext) # request for original file
    
  
############################################################
## Return file extension of existing file in files folder (or '')
def get_true_ext(name: str, ext: str) -> str:
    root, dirs, files = next(os.walk(FILES))
    for file in files:
        if file == f'{name}{ext}':
            return file
        elif os.path.splitext(file)[0] == name: 
            return os.path.splitext(file)[1]
    return ''


############################################################
## load RDF data from file in rdflib.Graph
def parse(file) -> Graph:
    return Graph().parse(file)

############################################################
## Serialize graph triples into requested notation/format
def serialize(g: Graph, ext: str) -> str:
    if ext.startswith('.'): ext = ext[1:]

    # File extension does not match identifier of serializer
    if ext == 'rdf': ext = 'xml' 
    if ext == 'jsonld': ext = 'json-ld'
    return g.serialize(format=ext)