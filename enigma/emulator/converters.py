class ConfigConverter:
    regex = r'([^;]+\s)*[^;]+;[^;]+;([^;][^;]\s)*[^;][^;];(\d+\s)*\d+;[^;]+'

    def to_python(self, value):
        return ''

    def to_url(self, value):
        return ''
