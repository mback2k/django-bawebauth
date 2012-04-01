from celery.task import task
from bawebauth.models import Device, Usage

@task()
def task_start_worker():
    for device in Device.objects.all():
        task_reduce_device.apply_async(args=[device.id])

@task()
def task_reduce_device(device_id):
    try:
        Device = Device.objects.get(id=device_id)
        
        
        
    except Device.DoesNotExist, e:
        pass
