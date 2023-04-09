from django.core.management.base import BaseCommand
from quicktechpoints.models import Tag


class Command(BaseCommand):
    help = 'Insert tags'

    def handle(self, *args, **kwargs):
        tagsToAdd = ['Hardware', 'Software', 'Mobile technology', 'Gaming', 'Artificial Intelligence',
                     'Cybersecurity', 'Social media', 'Internet of Things (IoT)', 'Cloud computing',
                     'Virtual reality and augmented reality', 'Blockchain and cryptocurrency',
                     'Emerging technologies', 'E-commerce', 'Startups and entrepreneurship', 'Innovation and research']

        for tag in tagsToAdd:
            try:
                Tag.objects.create(name=tag)
            except:
                continue
        print('Tags were added')
