from django.db import models
from django.db.models import Avg


# Create your models here.

class SportStructure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0)  # Average rating (updated separately)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='structures')
    address = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', related_name='structures')

    def __str__(self):
        return self.name


class SportStructureImage(models.Model):
    sport_structure = models.ForeignKey(SportStructure, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='construction_images/')
    description = models.TextField(blank=True, null=True)  # Optional image description

    def __str__(self):
        return f"{self.sport_structure.name} - {self.image.name.split('/')[-1]}"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Rating(models.Model):
    sport_structure = models.ForeignKey(SportStructure, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Limit rating to 1-5
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='rating_range')
        ]
        unique_together = ('sport_structure', 'user')  # One rating per user per structure

    def __str__(self):
        return f"{self.rating} by {self.user.username} for {self.sport_structure.name}"


def update_average_rating(sport_structure_id):
    structure = SportStructure.objects.get(id=sport_structure_id)
    avg_rating = structure.ratings.aggregate(Avg('rating'))['rating__avg']
    structure.rating = avg_rating or 0  # Set to 0 if no ratings
    structure.save()


class Comment(models.Model):
    sport_structure = models.ForeignKey(SportStructure, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # For moderation

    def __str__(self):
        return f"Comment by {self.user.username} on {self.sport_structure.name}"
