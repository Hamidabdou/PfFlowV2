

from background_task import background



@background(queue='q1')
def notify_user():
    # lookup user by id and send them a message
    # user = User.objects.all()
    # print('testtesttest')
    while True:
        print('.......')
    return None


@background(queue='q2')
def notify():
    # lookup user by id and send them a message
    # user = User.objects.all()
    # print('testtesttest')
    while True:
        print('blabla')
    return None


