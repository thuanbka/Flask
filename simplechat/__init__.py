from flask import Blueprint

bp_simplechat=Blueprint("simple_chat",__name__, template_folder="templates")

from . import routes, event