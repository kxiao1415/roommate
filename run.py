from pyws import create_app
import logging


if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')

    handler = logging.FileHandler(app.config['LOGGING']['log_file_path'])
    handler.setLevel(app.config['LOGGING']['level'])
    formatter = logging.Formatter(app.config['LOGGING']['format'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.run(debug=True)
