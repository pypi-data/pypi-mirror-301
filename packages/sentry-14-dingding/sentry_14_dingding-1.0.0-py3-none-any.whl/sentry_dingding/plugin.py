# coding: utf-8

import json
import logging

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"

logging.basicConfig(
    filename='sentry_dingding.log',  # 指定日志文件名
    filemode='a',  # 追加模式
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 设置日志记录器
logger = logging.getLogger('sentry.plugins.dingding')

class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'season'
    author_url = 'https://github.com/cench/sentry-10-dingding'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'https://github.com/cench/sentry-10-dingding'),
        ('Bug Tracker', 'https://github.com/cench/sentry-10-dingding/issues'),
        ('README', 'https://github.com/cench/sentry-10-dingding/blob/master/README.md'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        is_configured = bool(self.get_option('access_token', project))
        logger.debug(f"DingDing plugin configuration status for project {project.slug}: {is_configured}")
        return is_configured

    def notify_users(self, group, event, *args, **kwargs):
        logger.info(f"Notifying users for event {event.event_id} in group {group.id}")
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            logger.warning(f"DingDing plugin not configured for project {group.project.slug}")
            return

        if group.is_ignored():
            logger.info(f"Ignoring notification for ignored group {group.id}")
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = u'【%s】的项目异常' % event.project.slug

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n\n > {message} \n\n [详细信息]({url})".format(
                    title=title,
                    message=event.title or event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }

        logger.info(f"Sending DingDing notification for event {event.event_id}")
        try:
            response = requests.post(
                url=send_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data).encode("utf-8")
            )
            response.raise_for_status()
            logger.info(f"Successfully sent DingDing notification for event {event.event_id}")
        except requests.RequestException as e:
            logger.error(f"Failed to send DingDing notification for event {event.event_id}: {str(e)}")