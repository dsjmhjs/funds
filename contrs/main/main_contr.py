# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, session
from contrs.main import main
from config import db
from models.users import User
from models.roles import Role
from models.funds import Fund, TrackIndex, ShowIndex
from contrs.main.forms import EditProfileForm, EditProfileAdminForm
from flask_login import login_required, current_user
from models.roles import Perm
from contrs.decorators import permission_required, admin_required
# pyecharts
from pyecharts import Bar
from pyecharts import Overlap


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['order'] = request.values.get('order')
    if 'order' in session:
        # 分位点、起始日、基金数
        if session['order'] == 'fwd':
            query = ShowIndex.query.order_by(ShowIndex.quantile)
        elif session['order'] == '-fwd':
            query = ShowIndex.query.order_by(ShowIndex.quantile.desc())
        elif session['order'] == 'qsr':
            query = ShowIndex.query.order_by(ShowIndex.start_date)
        elif session['order'] == '-qsr':
            query = ShowIndex.query.order_by(ShowIndex.start_date.desc())
        elif session['order'] == 'jjs':
            query = ShowIndex.query.order_by(ShowIndex.count)
        elif session['order'] == '-jjs':
            query = ShowIndex.query.order_by(ShowIndex.count.desc())
        else:
            query = ShowIndex.query.order_by(ShowIndex.start_date)
    else:
        query = ShowIndex.query.order_by(ShowIndex.start_date)
    showindexes = query.all()
    return render_template('index.html', showindexes=showindexes)


@main.route('/passive-index-funds')
def passive_index_funds():
    page = request.args.get('page', 1, type=int)
    funds_filters = {
        Fund.fund_investtype == u'被动指数型基金',
        Fund.fund_trackindexcode != ''
    }
    pagination = Fund.query.filter(*funds_filters).order_by(Fund.fund_fundscale.desc()).paginate(page, 20, False)
    funds = pagination.items
    return render_template('passive_index_funds.html', pagination=pagination, funds=funds)


@main.route('/<fti>/funds')
@login_required
def the_funds(fti):
    funds_filters = {
        Fund.fund_investtype == u'被动指数型基金',
        Fund.fund_trackindexcode == fti
    }
    funds = Fund.query.filter(*funds_filters).order_by(Fund.fund_fundscale.desc()).all()
    return render_template('the_funds.html', fti=fti, funds=funds)


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


@main.route('/<fti>/data')
@login_required
def the_data(fti):
    his_filters = {TrackIndex.fund_trackindexcode == fti}
    histories = TrackIndex.query.filter(*his_filters).order_by(TrackIndex.date).all()
    dates = []
    closes = []
    pe_ttms = []
    for history in histories:
        dates.append(history.date[2:4] + '/' + history.date[5:7] + '/' + history.date[8:10])
        closes.append('%.2f' % history.close)
        pe_ttms.append('%.2f' % history.pe_ttm)
    # 折线图
    bar_close = Bar()
    bar_close.add(
        'POINT',
        dates,
        closes,
        mark_point=[{"coord": [dates[-1], closes[-1]], "name": dates[-1]}],
        mark_point_textcolor='black',
        is_more_utils=True
    )
    bar_pe = Bar()
    bar_pe.add(
        'PE',
        dates,
        pe_ttms,
        mark_point=[{"coord": [dates[-1], pe_ttms[-1]], "name": dates[-1]}],
        mark_point_textcolor='black',
        is_more_utils=True
    )
    overlap = Overlap(width=1150, height=500)
    overlap.add(bar_pe)
    overlap.add(bar_close, yaxis_index=1, is_add_yaxis=True)
    return render_template(
        'the_data.html',
        fti=fti,
        myechart=overlap.render_embed(),
        host=REMOTE_HOST,
        script_list=overlap.get_js_dependencies()
    )


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For administrators!'


@main.route('/moderator')
@login_required
@permission_required(Perm.M)
def for_moderators_only():
    return 'For moderators!'


@main.route('/user-info/<username>')
def user_info(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_info.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user_info', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user_info', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
