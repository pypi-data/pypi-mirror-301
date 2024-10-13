from datetime import datetime
from pytz import timezone
from flask import Flask, request, Response
from flask import render_template_string, redirect, send_from_directory
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.job import Job
from apscheduler.events import EVENT_ALL, JobExecutionEvent, JobSubmissionEvent, SchedulerEvent
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os


def get_datetime_now() -> datetime:
    if tz := os.environ.get('TZ', None):
        return datetime.now(timezone(tz))
    else:
        return datetime.now()


Base = declarative_base()


class APSEvent(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    job_id = Column(String(255))
    job_name = Column(String(255))
    event_type = Column(String(50))
    info = Column(String(2000))
    timestamp = Column(DateTime, default=get_datetime_now)


class ScheduleManager():
    """
    Class that manages scheduling tasks and provides a web interface
    for interacting with the scheduler.
    """

    def __init__(self, app: Flask, scheduler: BaseScheduler,
                 path: str = '/schedule-manager-ui',
                 require_authentication: bool = True, apikey: str = None):
        """
        Initializes the Manager class.
        Args:
            app (Flask):
                The Flask application instance.
            scheduler (BaseScheduler):
                The scheduler instance.
            path (str, optional):
                The path for the schedule manager UI.
                Defaults to '/schedule-manager-ui'.
            require_authentication (bool, optional):
                Flag to require API key for job updates. Defaults to True.
            apikey (str, optional): The API key for authentication.
                If not provided, it will be fetched from the environment
                variable 'SM_UI_APIKEY'.
        """
        self.app: Flask = app
        self.scheduler: BaseScheduler = scheduler
        self.HOME_PATH: str = path
        self.AUTHENTICATE: bool = require_authentication
        if self.AUTHENTICATE:
            self.API_KEY: str = apikey if apikey else os.environ.get('SM_UI_APIKEY', None)
            if not self.API_KEY:
                raise ValueError('Could not retrieve API key for ScheduleManager!')
        self.last_execution_store: dict[str, datetime] = {}

        self.engine = create_engine('sqlite:///apscheduler_events.db')
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self._init_endpoints()
        self._init_event_listeners()

    def _init_endpoints(self):
        file_path = os.path.abspath(os.path.dirname(__file__))

        def find_in_store(job_id):
            with Session(self.engine) as session:
                if event := (session.query(APSEvent)
                             .filter_by(job_id=job_id, event_type='EVENT_JOB_EXECUTED')
                             .order_by(APSEvent.timestamp.desc())
                             .first()):
                    return event.timestamp
                else:
                    return None

        @self.app.route(self.HOME_PATH + '/files/<path:filename>')
        def schedulemanager_ui_serve_files(filename):
            return send_from_directory(os.path.join(file_path, 'templates'), filename)

        @self.app.route(self.HOME_PATH)
        def schedulemanager_ui_index():
            jobs = self.scheduler.get_jobs()
            jobs.sort(key=lambda x: x.id)
            with open(os.path.join(file_path, 'templates/index.html')) as file:
                scheduler_template = file.read()
            return render_template_string(scheduler_template,
                                          jobs=jobs,
                                          find_in_store=find_in_store,
                                          require_authentication=self.AUTHENTICATE)

        @self.app.route(self.HOME_PATH + '/toggle/<job_id>', methods=['POST'])
        def schedulemanager_ui_toggle_job(job_id):
            if self.AUTHENTICATE:
                api_key = request.headers.get('Authorization')
                if api_key != self.API_KEY:
                    return Response('Invalid API key!', 403)

            job: Job = self.scheduler.get_job(job_id)
            if job.next_run_time is None:
                job.resume()
            else:
                job.pause()
            return redirect(self.HOME_PATH)

        @self.app.route(self.HOME_PATH + '/logs')
        def get_events():
            with Session(self.engine) as session:
                events = session.query(APSEvent).order_by(APSEvent.timestamp.desc()).all()
            with open(os.path.join(file_path, 'templates/logs.html')) as file:
                scheduler_template = file.read()
            return render_template_string(scheduler_template,
                                          events=events,
                                          require_authentication=self.AUTHENTICATE)

    def _init_event_listeners(self):
        def get_job_type(code: int) -> str:
            codes: dict[int, str] = {}
            codes[2 ** 0] = 'EVENT_SCHEDULER_START'
            codes[2 ** 1] = 'EVENT_SCHEDULER_SHUTDOWN'
            codes[2 ** 2] = 'EVENT_SCHEDULER_PAUSED'
            codes[2 ** 3] = 'EVENT_SCHEDULER_RESUMED'
            codes[2 ** 4] = 'EVENT_EXECUTOR_ADDED'
            codes[2 ** 5] = 'EVENT_EXECUTOR_REMOVED'
            codes[2 ** 6] = 'EVENT_JOBSTORE_ADDED'
            codes[2 ** 7] = 'EVENT_JOBSTORE_REMOVED'
            codes[2 ** 8] = 'EVENT_ALL_JOBS_REMOVED'
            codes[2 ** 9] = 'EVENT_JOB_ADDED'
            codes[2 ** 10] = 'EVENT_JOB_REMOVED'
            codes[2 ** 11] = 'EVENT_JOB_MODIFIED'
            codes[2 ** 12] = 'EVENT_JOB_EXECUTED'
            codes[2 ** 13] = 'EVENT_JOB_ERROR'
            codes[2 ** 14] = 'EVENT_JOB_MISSED'
            codes[2 ** 15] = 'EVENT_JOB_SUBMITTED'
            codes[2 ** 16] = 'EVENT_JOB_MAX_INSTANCES'
            return codes[code]

        def job_listener(event: SchedulerEvent):
            args = {}
            args['event_type'] = get_job_type(event.code)
            if isinstance(event, JobSubmissionEvent):
                args['job_id'] = event.job_id
                if job := self.scheduler.get_job(event.job_id):
                    args['job_name'] = job.func.__name__
            if isinstance(event, JobExecutionEvent):
                args['job_id'] = event.job_id
                if job := self.scheduler.get_job(event.job_id):
                    args['job_name'] = job.func.__name__
                if event.retval:
                    args['info'] = str(event.retval)
                if event.exception:
                    args['info'] = f'{event.exception}: {event.traceback}'

            new_event = APSEvent(**args)

            with Session(self.engine) as session:
                session.add(new_event)
                session.commit()

        self.scheduler.add_listener(job_listener, EVENT_ALL)
