import os
from django.shortcuts import render
from pytube import YouTube
from pathlib import Path
from django.contrib import messages
import re 
# Create your views here.
def homeview(request) :
	default_filename=''
	new_title=''
	thumbnail=''
	error_msg=''
	if request.method=='POST':
		get_value=request.POST.get('ytlink')
		if get_value !='':
			
			try:
				yt_link=YouTube(get_value)
				
				original_title = yt_link.title
				new_title =''.join(filter(str.isalnum, original_title)) 
				yt_link.title=new_title
				t=yt_link.streams.filter(only_audio=True).all()
				stream= yt_link.streams.get_highest_resolution()
				path_to_download = 'static/media'
				path_to_download_aud='static/media/audio'
				
				t[0].download(path_to_download_aud,filename_prefix=new_title)				
				stream.download(path_to_download,filename_prefix=new_title)
				new_title=new_title+new_title+".mp4"
				
				thumbnail=yt_link.thumbnail_url
				messages.info(request, "signal")
				print(new_title)
				print('finished downloading')
			except Exception as e:
				error_msg=e
			
		else:
			print('null')
	return render(request,'home.html',{"df_name":new_title,"thumb":thumbnail,'err_msg':error_msg})

