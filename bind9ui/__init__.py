from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('dns_view', '/')
    config.add_route('dns_addedit', '/{hostname}')
    config.scan()
    return config.make_wsgi_app()
