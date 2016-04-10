# encoding=utf-8
import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	FLASKY_MAIL_SUBJECT_PREFIX = ['Flasky']
	FLASKY_MAIL_SENDER = '<li12qiang345@163.com>'
	FLASKY_ADMIN = 'li12qiang345@163.com'
	SSL_DISABLE = True
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_POSTS_PER_PAGE = 5
	FLASKY_FOLLOWERS_PER_PAGE = 50
	FLASKY_COMMENTS_PER_PAGE = 20
	FLASKY_SLOW_DB_QUERY_TIME = 0.5

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
							  'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
							  'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
	SQLALCHEMY_DATABASW_URI = os.environ.get('TEST_DATABASE_URL') or \
							  'sqlite:///' + os.path.join(basedir, 'data.sqlite')

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)


class HerokuConfig(ProductionConfig):
	SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		# handle profxy server handlers
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)

		# 输出到stder
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'heroku': HerokuConfig,
	'default': DevelopmentConfig
}
