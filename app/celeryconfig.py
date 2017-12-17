broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
database_engine_options = {"pool_recycle": 7200, 'echo': True}
broker_transport_options = {'visibility_timeout': 3600}
