from django.core.management.base import BaseCommand
from quicktechpoints.models import Tag


class Command(BaseCommand):
    help = 'Insert tags'

    def handle(self, *args, **kwargs):
        tagsToAdd = [
            "Electric Cars",
            "Home Appliances",
            "PC",
            "Laptops",
            "Smartphones",
            "Artificial intelligence (AI)",
            "Machine learning (ML)",
            "Robotics",
            "Virtual reality (VR)",
            "Augmented reality (AR)",
            "Internet of Things (IoT)",
            "Blockchain",
            "Cybersecurity",
            "Cloud computing",
            "Data analytics",
            "Mobile development",
            "Web development",
            "Programming languages",
            "Operating systems",
            "Hardware",
            "Software engineering",
            "User experience (UX)",
            "User interface (UI)",
            "E-commerce",
            "Digital marketing",
            "Social media",
            "Gaming",
            "Network infrastructure",
            "Information technology (IT)",
            "Big data",
            "Quantum computing",
            "3D printing",
            "Nanotechnology",
            "Biotechnology",
            "Renewable energy technology",
        ]

        for tag in tagsToAdd:
            try:
                Tag.objects.create(name=tag)
            except:
                continue
        print('Tags were added')
