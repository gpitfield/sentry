"""
sentry.web.urls
~~~~~~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import re

from django.conf.urls.defaults import *

from sentry.web import api
from sentry.web.frontend import accounts, generic, groups, events, \
  projects, admin, docs

__all__ = ('urlpatterns',)


def init_plugins():
    from django.db.models import get_apps, get_models
    for app in get_apps():
        try:
            get_models(app)
        except:
            continue
init_plugins()

urlpatterns = patterns('',
    url(r'^_static/(?P<path>.*)$', generic.static_media, name='sentry-media'),

    # Legacy API
    url(r'^store/$', api.store),

    # Legacy redirects

    url(r'^group/(?P<group_id>.+)$', groups.group),
    url(r'^group/(?P<group_id>.+)/messages$', groups.group_event_list),
    url(r'^group/(?P<group_id>.+)/messages/(?P<event_id>.+)$', groups.group_event_details),
    url(r'^group/(?P<group_id>.+)/actions/(?P<slug>[\w_-]+)$', groups.group_plugin_action),

    # Account

    url(r'^login/$', accounts.login, name='sentry-login'),
    url(r'^logout/$', accounts.logout, name='sentry-logout'),
    url(r'^account/settings/$', accounts.settings, name='sentry-account-settings'),

    # Management

    url(r'^projects/$', projects.project_list, name='sentry-project-list'),
    url(r'^projects/new/$', projects.new_project, name='sentry-new-project'),
    url(r'^projects/(?P<project_id>.+)/edit/$', projects.manage_project,
        name='sentry-manage-project'),
    url(r'^projects/(?P<project_id>.+)/plugins/(?P<slug>[\w_-]+)/$', projects.configure_project_plugin,
        name='sentry-configure-project-plugin'),
    url(r'^projects/(?P<project_id>.+)/remove/$', projects.remove_project,
        name='sentry-remove-project'),
    url(r'^projects/(?P<project_id>.+)/members/new/$', projects.new_project_member,
        name='sentry-new-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/(?P<member_id>.+)/edit/$', projects.edit_project_member,
        name='sentry-edit-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/(?P<member_id>.+)/remove/$', projects.remove_project_member,
        name='sentry-remove-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/(?P<member_id>.+)/suspend/$', projects.suspend_project_member,
        name='sentry-suspend-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/(?P<member_id>.+)/restore/$', projects.restore_project_member,
        name='sentry-restore-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/pending/(?P<member_id>.+)/remove/$', projects.remove_pending_project_member,
        name='sentry-remove-pending-project-member'),
    url(r'^projects/(?P<project_id>.+)/members/pending/(?P<member_id>.+)/reinvite/$', projects.reinvite_pending_project_member,
        name='sentry-reinvite-pending-project-member'),
    url(r'^accept/(?P<member_id>.+)/(?P<token>\w+)/$', projects.accept_invite,
        name='sentry-accept-invite'),

    # Global

    url(r'^$', generic.dashboard, name='sentry'),
    url(r'^manage/status/$', admin.status_env, name='sentry-admin-status'),
    url(r'^manage/status/packages/$', admin.status_packages, name='sentry-admin-packages-status'),
    url(r'^manage/status/queue/$', admin.status_queue, name='sentry-admin-queue-status'),
    url(r'^manage/stats/$', admin.stats, name='sentry-admin-stats'),

    # Admin - Projects
    url(r'^manage/projects/$', admin.manage_projects, name='sentry-admin-projects'),

    # Admin - Users
    url(r'^manage/users/$', admin.manage_users, name='sentry-admin-users'),
    url(r'^manage/users/new/$', admin.create_new_user, name='sentry-admin-new-user'),
    url(r'^manage/users/(?P<user_id>.+)/$', admin.edit_user, name='sentry-admin-edit-user'),
    url(r'^manage/users/(?P<user_id>.+)/remove/$', admin.remove_user, name='sentry-admin-remove-user'),
    url(r'^manage/users/(?P<user_id>.+)/projects/$', admin.list_user_projects, name='sentry-admin-list-user-projects'),

    # Admin - Plugins
    url(r'^manage/plugins/(?P<slug>[\w_-]+)/$', admin.configure_plugin, name='sentry-admin-configure-plugin'),

    # API / JS

    url(r'^api/store/$', api.store, name='sentry-api-store'),
    url(r'^api/notification/$', api.notification, name='sentry-api-notification'),
    url(r'^api/(?P<project_id>.+)/poll/$', api.poll, name='sentry-api-poll'),
    url(r'^api/(?P<project_id>.+)/resolve/$', api.resolve, name='sentry-api-resolve'),
    url(r'^api/(?P<project_id>.+)/bookmark/$', api.bookmark, name='sentry-api-bookmark'),
    url(r'^api/(?P<project_id>.+)/clear/$', api.clear, name='sentry-api-clear'),
    url(r'^api/(?P<project_id>.+)/chart/$', api.chart, name='sentry-api-chart'),

    # Project specific

    # url(r'^(?P<project_id>.+)/docs/$', groups.search, name='sentry-search'),
    url(r'^(?P<project_id>.+)/docs/(?P<platform>%s)/$' % ('|'.join(re.escape(r) for r in docs.PLATFORM_LIST),), docs.client_guide,
        name='sentry-docs-client'),

    url(r'^(?P<project_id>.+)/group/(?P<group_id>.+)/$', groups.group, name='sentry-group'),
    url(r'^(?P<project_id>.+)/group/(?P<group_id>.+)/json/$', groups.group_json, name='sentry-group-json'),
    url(r'^(?P<project_id>.+)/group/(?P<group_id>.+)/events/$', groups.group_event_list, name='sentry-group-events'),
    url(r'^(?P<project_id>.+)/group/(?P<group_id>.+)/events/(?P<event_id>.+)/$', groups.group_event_details, name='sentry-group-event'),
    url(r'^(?P<project_id>.+)/group/(?P<group_id>.+)/actions/(?P<slug>[\w_-]+)/', groups.group_plugin_action, name='sentry-group-plugin-action'),

    url(r'^(?P<project_id>.+)/events/$', events.event_list, name='sentry-events'),
    url(r'^(?P<project_id>.+)/events/(?P<event_id>.+)/replay/$', events.replay_event, name='sentry-replay'),

    url(r'^(?P<project_id>.+)/search/$', groups.search, name='sentry-search'),

    url(r'^(?P<project_id>.+)/view/(?P<view_id>.+)/$', groups.group_list, name='sentry'),
    url(r'^(?P<project_id>.+)/$', groups.group_list, name='sentry'),
)
