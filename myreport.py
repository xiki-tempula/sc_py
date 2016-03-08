import os, sys
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from matplotlib.figure import Figure
from webbrowser import open_new
import urllib.parse, urllib.request, urllib.parse, urllib.error
import cgi
import base64

class html_report:

    def __init__(self,filename,mode="w"):
        #mode is w for overwrite existing report file
        #        a to append to existing report file
        self.filename=filename
        self.mode=mode
        self.saved=False
        self.html_items=[]
        self.written=False

    text_template="<{tag} {attr}'>{content}</{tag}>\n"
    code_template="<div class='code'><caption>{caption}</caption><pre class='brush:python'>{content}</pre></div><br/>\n"
    fig_template="<figure><figcaption>{caption}</figcaption><img <img src='data:image/png;base64,{imgdata}'/></figure><br/>\n"
    marker="<div id='insert_html'/>"
    animation_js="""
    $( document ).ready(function() {
    $('div.animation').each(function(){
       	var rate=1;
        var $anim=$(this);
        var test=(function($anim){
        	var myInterval;
        	var ms;
        	var myfunc=function(){
        	//alert($anim.attr('id'));
            window.clearInterval(myInterval);
            var n=$anim.data('frame');
            var images=$anim.data('images');
            var n_img=images.length;
            ms=2000/n_img;
            var increment=$anim.data('rate');
            increment=increment%n_img
            n=(n+increment+n_img)%n_img;
            $anim.data('frame',n);
            var image_src=images[n];
            $anim.find('#frame').attr('src', image_src);
            if (increment==0) return;
            myInterval = setInterval(myfunc,ms);
            }
            return myfunc
        });
        var animate=test($anim)
        var go=function(rate){ $anim.data('rate',rate); animate();  };
        var timeout=function(){setTimeout(function(){play(0); },20000)};
        var play=function(rate){go(rate); timeout()};
        $anim.find('#rew').on('click',function(){play(-1);play(0)});
        $anim.find('#fastFwd').on('click',function(){play(1);play(0)});
        $anim.find('#play').on('click',function(){play(1);});
       	$anim.find('#pause').on('click',function(){play(0);});
        $anim.find('#restart').on('click',function(){play();$anim.attr('data-frame',0);});
        play(1);
    });
    });
    """
    html_template="""<html><!doctype html>
    <head>
    <style> body {{padding: 2em 2em 2em 2em; font-size: 16px;font-family: 'Georgia', 'serif';}}
            div.code {{ padding-left: 2em; }}
            </style>
    <link href='https://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/styles/shCore.css' rel='stylesheet' type='text/css'>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/styles/shThemeDefault.css" rel="stylesheet" type="text/css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/scripts/shCore.js" type="text/javascript"> </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/scripts/shAutoloader.js" type="text/javascript"> </script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/SyntaxHighlighter/3.0.83/scripts/shBrushPython.js' type='text/javascript'> </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>

    </head>
    <body>\n{marker}\n</body>
    <script type="text/javascript">
    SyntaxHighlighter.all()
    {js}
    </script>
    </html>""".format(marker=marker,js=animation_js)

    def add_text(self,text,tag='div',tag_class=None,verbose=True):
        if tag_class is not None:
            tag_class="class='{}'".format(tag_class)
        else: tag_class=""
        self.html_items.append(self.text_template.format(content=text,tag=tag,attr=tag_class))
        if not verbose:
            return
        print("ADDING TEXT TO REPORT:")
        print(text)

    def add_heading(self,text,tag='h2',tag_class=None,verbose=True):
        self.add_text(text,tag,tag_class,verbose)

    def add_subheading(self,text,tag='h3',tag_class=None,verbose=True):
        self.add_text(text,tag,tag_class,verbose)

    def add_code(self,text,tag='pre',tag_class=None,verbose=True):
        self.add_text(text,tag,tag_class,verbose)


    def add_figure(self,fig,caption="",verbose=True):
        canvas=FigureCanvas(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output, format = 'png')
        png_output.seek(0)
        png_output = base64.b64encode(png_output.getvalue())
        self.html_items.append(html_report.fig_template.format(imgdata=png_output.decode("utf-8") ,caption=caption))
        if not verbose:
            return
        print("ADDING FIGURE TO REPORT:")
        print("Caption:",caption)

    def init_figure(self,*args, **kwargs):
        return plt.Figure(*args, **kwargs)

    def view(self):
        if not self.written:
            self.write()
        path = os.path.abspath(self.filename)
        url=urllib.parse.urljoin('file:', urllib.request.pathname2url(path))
        open_new(url)

    def init_animation(self):
        my_animation=html_animation()
        return my_animation

    def add_animation(self,my_animation,caption='',verbose=True):
        html_animation=my_animation.generate(caption)
        self.html_items.append(html_animation)
        if not verbose:
            return
        print("ADDING ANIMATION TO REPORT:")
        print("Caption:",caption)

    def add_source(self,code_filename=None,caption='',verbose=True):
        if code_filename is None:
            code_filename=os.path.realpath(__file__)
        if not os.path.isfile(code_filename):
            print("Unable to find source code")
            return False
        with open(code_filename,'r') as infile:
            code=infile.read()
            code=cgi.escape(code).encode('ascii', 'xmlcharrefreplace')
            code = code.decode("utf-8")
        self.html_items.append(self.code_template.format(content=code,caption=caption))
        if not verbose:
            return
        print("ADDING CODE TO REPORT:")
        print(code)


    def write(self):
        html_page=self.html_template
        if self.mode == "a":
            with open(self.filename,'r') as infile:
                html_page=infile.read()
        content=""
        for line in self.html_items:
            content+=line
        if html_page.find(self.marker)==-1:
            print("Unable to find insert marker in file")
            return False
        html_page=html_page.replace(self.marker,content+self.marker)
        with open(self.filename,'w') as outfile:
                outfile.write(html_page)
                self.written=True
                self.mode="a"
                self.html_items=[]
        return True

class html_animation(object):

    def __init__(self):
        self.frames=[]

    def init_figure(self,*args, **kwargs):
        return plt.Figure(*args, **kwargs)

    def add_frame(self,fig):
        canvas=FigureCanvas(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output, format = 'png')
        png_output.seek(0)
        png_output = base64.b64encode(png_output.getvalue())
        png_output = png_output.decode("utf-8")
        self.frames.append(png_output)

    def generate(self,caption=''):
        image_list=self.frames
        html_template="""
                <div class='animation' data-rate='1'  data-frame='1' data-images='[ {img_list} ]'>
                <figure><figcaption>{caption}</figcaption><img id='frame'/>
                    <div id="buttonbar">
                    <button id="restart" >&#10226;</button>
                    <button id="rew" >&#9669;&#9669;</button>
                    <button id="pause" >&#10073;&#10073;</button>
                    <button id="play" > &#9658;</button>
                    <button id="fastFwd">&#9659;&#9659;</button>
                    </div></figure><br/>
                </div>
                """
        tag='"data:image/png;base64,{img_data}"\n'
        js_image_list=""
        sep=''
        for img in image_list:
            js_image_list+=sep+tag.format(img_data=img)
            sep=','
        html=html_template.format(img_list=js_image_list,caption=caption)
        return html



#test=html_report("test.html")
#test.add_text("here")
#test.write()
#test.view()
#fig=test.init_figure()
#ax=fig.add_subplot(1,1,1)
#ax.plot([1,2,3],[1,2,3],'o')
#test.add_figure(fig,"cattttt")
#test.write()
#test.view()
#print(os.path.realpath(__file__))
