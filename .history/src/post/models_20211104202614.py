from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# from tinymce.models import HTMLField
from tinymce import models as tinymce_models
from ckeditor.fields import RichTextField

# Create your models here.

User = get_user_model()

#----------------------------------------------------------------------------------------------#
# MODELE ASSOCIE A UN AUTEUR D'ARTICLE
class Author(models.Model):
	user        = models.OneToOneField(User, on_delete=models.CASCADE ,verbose_name='Auteur', related_name='author')
	profile_pic = models.ImageField(verbose_name='Photo de profil')

	class Meta:
		verbose_name = 'Utilisateur'
		verbose_name_plural = 'Utilisateurs'

	def __str__(self):
		return self.user.username


#----------------------------------------------------------------------------------------------#
# MODELE ASSOCIE A UNE CATEGORIE
class Category(models.Model):
	title = models.CharField(max_length=80, verbose_name='Titre de la categorie')

	class Meta:
		verbose_name = 'Categorie'
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.title 


#----------------------------------------------------------------------------------------------#
# MODELE DU NOMBRE DE VU SUR UN ARTICLE
class PostView(models.Model):
	post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Article vu')
	user = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='Nom du visiteur')

	class Meta:
		verbose_name = 'Vue article'
		verbose_name_plural = 'Vues article'

	def __str__(self):
		return self.user.username



#----------------------------------------------------------------------------------------------#
# MODELE ASSOCIE A UN COMMENTAIRE
class Comment(models.Model):
	user        = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='Nom du visiteur')
	timestamp   = models.DateTimeField(auto_now_add=True, verbose_name='Commentaire publié')
	commentaire = models.TextField(blank=True, verbose_name='Commentaire') 
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Article commenté')


	class Meta:
		verbose_name = 'Commentaire'
		verbose_name_plural = 'Commentaires'

	def __str__(self):
		return self.user.username



#----------------------------------------------------------------------------------------------#
# MODELE ASSOCIE A UN ARTICLE
class Post(models.Model):
	title         = models.CharField(max_length=200, verbose_name='Titre')
	overview      = tinymce_models.HTMLField(blank=True, null=True ,verbose_name='Aperçu')
	content       = tinymce_models.HTMLField(blank=True, null=True, verbose_name='Contenu')
	timestamp     = models.DateTimeField(auto_now_add=True, verbose_name='Date de publication')
	author        = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Editeur')
	post_image    = models.ImageField()
	categories    = models.ManyToManyField(Category, verbose_name='Categorie')
	featured      = models.BooleanField(default=False, verbose_name='Fonctionnalité')
	previous_post = models.ForeignKey('self', related_name='precedent', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Article precedent')
	next_post     = models.ForeignKey('self', related_name='suivant', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Article suivant')


	class Meta:
		verbose_name = 'Article'
		verbose_name_plural = 'Articles'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post', kwargs={'id':self.id})

	def get_update_url(self):
		return reverse('post-update', kwargs={'id':self.id})

	def get_delete_url(self):
		return reverse('post-delete', kwargs={'id':self.id})

	@property
	def get_comments(self):
		return self.comments.all().order_by('-timestamp')


	@property
	def view_count(self):
		return PostView.objects.filter(post=self).count()


	@property
	def comment_count(self):
		return Comment.objects.filter(post=self).count()


#----------------------------------------------------------------------------------------------#

 
class Contact(models.Model):
	nom     = models.CharField(max_length=200, verbose_name='Nom')
	email   = models.EmailField(verbose_name='Email')
	message = models.TextField()

	def __str__(self):
		return f" {self.nom} " + " - " + {self.email}