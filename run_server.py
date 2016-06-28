try:
    from web_stuff import app
    import classifier_config
except:
    from .web_stuff import app
    from . import classifier_config
    
    
app.run(
    host = classifier_config.app_host,
    port = classifier_config.app_port
)