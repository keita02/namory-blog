from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Category, Author, PostView
from marketing.models import SignUp
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import CommentForm, PostForm, ContactForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView 
from django.http import Http404

# RECUPERER UN AUTEUR
def get_author(user):
	queryset = Author.objects.filter(user=user)

	if queryset.exists():
		return queryset[0]
	return None



#----------------------------------------------------------------------------------------------#
# FONCTION DE RECHERCHE
def search(request):
	queryset = Post.objects.all()
	query = request.GET.get('q')
	category_count = get_category_count()

	# post_list = Post.objects.all()
	# most_recent = Post.objects.order_by('-timestamp')[:4]
	# paginator = Paginator(queryset, 4)
	# page_request_var = 'page'
	# page = request.GET.get(page_request_var)

	# try:
	# 	paginated_queryset = paginator.page(page)
	# except PageNotAnInteger:
	# 	paginated_queryset = paginator.page(1)
	# except EmptyPage:
	# 	paginated_queryset = paginator.page(paginator.num_pages)


	if query:

		queryset = queryset.filter(

				Q(title__icontains=query) |
				Q(overview__icontains=query) | Q(content__icontains=query)
		).distinct()


	# paginator = Paginator(queryset, 4)
	# page_request_var = 'page'
	# page = request.GET.get(page_request_var)

	# try:
	# 	paginated_queryset = paginator.page(page)
	# except PageNotAnInteger:
	# 	paginated_queryset = paginator.page(1)
	# except EmptyPage:
	# 	paginated_queryset = paginator.page(paginator.num_pages)

	context = {

		'queryset'         : queryset,
		# 'page_request_var' : page_request_var,
		# 'most_recent'      : most_recent, 
		# 'category_count'   : category_count
	}

	return render(request, 'search_results.html', context)



#----------------------------------------------------------------------------------------------#
# RECUPERER LE NOMBRE D'ARTICLE ASSOCIE A UNE CATEGORIE
def get_category_count():
	queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
	return queryset



#----------------------------------------------------------------------------------------------#
# PAGE D'ACCUEIL

def index(request):
	queryset = Post.objects.filter(featured = True)
	latest = Post.objects.order_by('-timestamp')[0:3]

	if request.method == "POST":
		email = request.POST['email']
		new_signup = SignUp()
		new_signup.email = email
		new_signup.save()

	context = {

	   'queryset' : queryset,
	   'latested'   : latest
	}
	return render(request, 'index.html', context)



#----------------------------------------------------------------------------------------------#
# PAGE DU BLOG

def blog(request):

	category_count = get_category_count()

	post_list = Post.objects.all()
	most_recent = Post.objects.order_by('-timestamp')[:4]
	paginator = Paginator(post_list, 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	context = {
		'queryset'         : paginated_queryset,
		'page_request_var' : page_request_var,
		'most_recent'      : most_recent, 
		'category_count'   : category_count
	}
	return render(request, 'blog.html', context)



#----------------------------------------------------------------------------------------------#
# LISTE DE TOUS LES ARTICLES
def post(request, id):

	post = get_object_or_404(Post, id=id)
	most_recent = Post.objects.order_by('-timestamp')[:4]
	category_count = get_category_count()

	if request.user.is_authenticated:
		PostView.objects.get_or_create(user=request.user, post=post)

	form = CommentForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			form.instance.user = request.user
			form.instance.post = post
			form.save()
			return redirect(reverse('post', kwargs={'id':post.id}))

	context = {
		'form': form,
		'post': post,
		# 'page_request_var' : page_request_var,
		'most_recent'      : most_recent, 
		'category_count'   : category_count
	}

	return render(request, 'post.html', context)


#----------------------------------------------------------------------------------------------#
# CREATION D'UN ARTICLE
@login_required
def post_create(request):
    titre = 'Créer'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog", kwargs={
                'id': form.instance.id
            }))
    context = {
        'titre': titre,
        'form': form
    }
    return render(request, "post_create.html", context)

#----------------------------------------------------------------------------------------------#
# MODIFICATION D'UN ARTICLE
@login_required
def post_update(request, id):
    titre = 'Modifier'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)

    if request.method == "POST":
    	if form.is_valid():
    		form.instance.author = author
    		form.save()
    		return redirect(reverse("post", kwargs={
			'id': form.instance.id
			}))


    context = {
        'titre': titre,
        'form': form
    }
    return render(request, "post_create.html", context)



#----------------------------------------------------------------------------------------------#
# SUPPRESSION D'UN ARTICLE
@login_required
def post_delete(request, id):
	post = get_object_or_404(Post, id=id)
	author = get_author(request.user)

	if post.author == request.user:
		post.delete()
		return redirect(reverse("blog"))
	else :
		raise Http404
	# post = get_object_or_404(Post, pk=id)
	# post.delete()
	# return redirect(reverse('blog')



def contact(request):
	form = ContactForm()

	context = {
	  'form' : form
	}
	
	return render(request, 'contact.html', context)