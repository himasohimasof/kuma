import hashlib
import six

from cacheback.base import Job, to_bytestring


class KumaJob(Job):
    """
    A subclass of the cache base job class that implements an optional per job
    version key.
    """
    version = None

    def key(self, *args, **kwargs):
        key = super(KumaJob, self).key(*args, **kwargs)
        if self.version is None:
            return key
        return '%s#%s' % (key, self.version)

    def hash(self, value):
        """
        Generate a hash of the given tuple.

        This is for use in a cache key.

        A fix till https://github.com/codeinthehole/django-cacheback/pull/40
        is merged and released.
        """
        if isinstance(value, tuple):
            value = tuple(to_bytestring(v) for v in value)
        return hashlib.md5(six.b(':').join(value)).hexdigest()


class IPBanJob(KumaJob):
    lifetime = 60 * 60 * 3
    refresh_timeout = 60

    def fetch(self, ip):
        from .models import IPBan
        if IPBan.objects.active(ip=ip).exists():
            return "0/s"
        return "60/m"

    def empty(self):
        return "60/m"
