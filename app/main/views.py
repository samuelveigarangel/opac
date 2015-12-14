# coding: utf-8

from collections import OrderedDict

from flask import render_template, abort
from . import main
from app import controllers


@main.route('/')
def index():
    return render_template("collection/index.html")


@main.route('/journals')
def collection_list_alpha():
    journals = controllers.get_journals()
    context = {
        'journals': journals,
    }
    return render_template("collection/list_alpha.html", **context)


@main.route('/journals/theme')
def collection_list_theme():
    objects_by_area = controllers.get_journals_by_study_area()
    objects_by_indexer = controllers.get_journals_by_indexer()

    context = {
        'objects_by_area': objects_by_area,
        'objects_by_indexer': objects_by_indexer
    }

    return render_template("collection/list_theme.html", **context)


@main.route('/journals/institution')
def collection_list_institution():
    context = controllers.get_journals_by_sponsor()

    return render_template("collection/list_institution.html", **context)


@main.route('/journals/<string:journal_id>')
def journal_detail(journal_id):
    journal = controllers.get_journal_by_jid(journal_id)

    if not journal:
        abort(404, 'Journal not found')

    context = {'journal': journal}

    return render_template("journal/detail.html", **context)


@main.route('/journals/<string:journal_id>/issues')
def issue_grid(journal_id):
    journal = controllers.get_journal_by_jid(journal_id)

    if not journal:
        abort(404, 'Journal not found')

    issues = controllers.get_issues_by_jid(journal_id)

    result_dict = OrderedDict()
    for issue in issues:
        key_year = str(issue.year)
        key_volume = str(issue.volume)
        result_dict.setdefault(key_year, OrderedDict())
        result_dict[key_year].setdefault(key_volume, []).append(issue)

    context = {
        'journal': journal,
        'result_dict': result_dict,
    }
    return render_template("issue/grid.html", **context)


@main.route('/issues/<string:issue_id>')
def issue_toc(issue_id):
    issue = controllers.get_issue_by_iid(issue_id)

    if not issue:
        abort(404, 'Issue not found')

    journal = issue.journal
    articles = controllers.get_articles_by_iid(issue.iid)

    context = {'journal': journal,
               'issue': issue,
               'articles': articles}

    return render_template("issue/toc.html", **context)


@main.route('/articles/<string:article_id>')
def article_detail(article_id):
    article = controllers.get_article_by_aid(article_id)

    if not article:
        abort(404, 'Article not found')

    context = {
        'article': article,
        'journal': article.journal,
        'issue': article.issue
    }
    return render_template("article/detail.html", **context)


@main.route('/articles/html/<string:article_id>')
def article_html_by_aid(article_id):
    article = controllers.get_article_by_aid(article_id)

    if not article:
        abort(404, 'Article not found')

    article_html = article.htmls[0].source

    return article_html


@main.route('/abstract/<string:article_id>')
def abstract_detail(article_id):
    article = controllers.get_article_by_aid(article_id)

    if not article:
        abort(404, 'Article not found')

    context = {
        'article': article,
        'journal': article.journal,
        'issue': article.issue
    }
    return render_template("article/abstract.html", **context)
