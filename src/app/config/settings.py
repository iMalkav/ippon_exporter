import confuse

class ExporterConfig():
    SETTINGS_FILE = "conf.yml"

    TEMPLATE = {
            'global':
            {
                'serverurl': str,
                'log_level': str,
                'port': int
            }
        }

    def __init__(self):
        source = confuse.YamlSource(self.SETTINGS_FILE)
        self._settings = confuse.RootView([source])
        self._settings = self._settings.get(self.TEMPLATE)

    @property
    def webport(self):
        return self._settings['global']['port']

    @property
    def logLevel(self):
        return self._settings['global']['log_level']

    @property
    def ipponURL(self):
        return self._settings['global']['serverurl']



_config = ExporterConfig()