from flask import render_template


def root():
    return render_template('200.html'), 200
