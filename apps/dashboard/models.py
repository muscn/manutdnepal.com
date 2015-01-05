from auditlog.models import LogEntry


def get_object(self):
    if self.action == 2:
        return self.object_repr
    return self.content_type.model_class().objects.get(pk=self.object_id)


LogEntry.get_object = get_object