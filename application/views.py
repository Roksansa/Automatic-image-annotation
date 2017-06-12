from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ContactForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Imaginary function to handle an uploaded file.
from .func import test
def app(request):
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			myfile = request.FILES['image']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			result = test(uploaded_file_url)
			return render(request, 'application.html', {
				'form': form,
				'uploaded_file_url': uploaded_file_url,
				'result':result,
				'image.url':uploaded_file_url,
			})
	else:
		form = ContactForm()
	return render(request, 'application.html', {'form': form})

