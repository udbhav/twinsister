from backends.s3boto import S3BotoStorage


class SongStorage(S3BotoStorage):
    def __init__(self, **kwargs):
        S3BotoStorage.__init__(self, **kwargs)

        self.querystring_auth = True
        self.querystring_expire = 3600
        self.acl = 'private'

    def url(self, name):
        name = self._clean_name(name)
        if self.bucket.get_key(name) is None:
            return ''
        return self.bucket.get_key(name).generate_url(self.querystring_expire, method='GET', query_auth=self.querystring_auth)
        
