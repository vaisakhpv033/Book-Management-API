from django.db import models



class Authors(models.Model):
    """
    Model representing an author of a book.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name_plural = "Authors"
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"],
                name="unique_author_full_name"
            )
        ]

class Generes(models.Model):
    """
    Model representing a genre of a book.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Genres"

class Books(models.Model):
    """
    Model representing a book in the library.
    """

    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    book_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(Authors, on_delete=models.PROTECT)
    genre = models.ForeignKey(Generes, on_delete=models.PROTECT)
    language = models.CharField(max_length=50, default="English")
    description = models.TextField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.full_name}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Books"


class ReadingLists(models.Model):
    """
    Model representing a reading list for a user.
    """

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_book"
            )
        ]
        ordering = ["position", "-date_added"]
        verbose_name_plural = "Reading Lists"