/*
 The help2.js and tree2.css just apply to the single page layout
*/
checkForNewVersion(location.href);
function checkForNewVersion(href) {     
  if ($("#newver").length == 0 || href.indexOf("file:///") > -1 || href.indexOf("://localhost") > -1) return;
    try {
        var url = href.split('/');
        prod = url[url.length-3]; //get product
        v = prod.charAt(2);     //find version
        
        var vMap = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        var v2 = vMap.charAt(vMap.indexOf(v) + 1);
        var prodChar = prod.split("");
        prodChar[2] = v2;
        prod = prodChar.join("");
        
        url[url.length-3] = prod;
        //url[url.length-1] = "";
        
        href = url.join("/");

        $.ajax({
            url: href, success: function (data) {
                $("#newver").html("<i>A new version of this product is available! </i> [<a href='" + href + "'>learn more</a>]");
            }
        });
    }
    catch(err) { }
}

var treeWidthResizer = {
    isDrag: false,
    x:0,
    init:function(){
        $("#whleftcol").append("<div id='resizerCol'></div>");
        /*
         *The event start have to be the virtual partition line.
         *But the event end just should be that mouse up in the table.
         * Maybe this just is a virtual "drag" event.
         */
        $("#resizerCol").mousedown(function () {
            treeWidthResizer.isDrag = true;
        });
        $("#whlayout").mouseup(function () {
            treeWidthResizer.isDrag = false;
        });

        $("#whcontent").mousemove(function (e) {
            if(treeWidthResizer.isDrag){
                var left = $("#whcontent").position().left;
                var width = Math.ceil(e.pageX - left);
                if (width < 600 && width > 200) {
                    $("#whsizer").css("width", width + "px");
                    $("#whleftcol").css("width", width + "px");
                    $("#whleftcol").css("min-width", width + "px");
                }
                return false; //prevent to select other text content.
            }
        });

    }
}
treeWidthResizer.init();


$(document).ready(function () {
    		
    //Syntax Highlighting of Code

    $('.whiframe pre').each(function (e) {
        if (!$(this).hasClass('syntax')) {
            l = $(this).attr('lang');
            if (l == null || l == '') l = 'csharp';

            var found = false;
            if ($(this).find("div.source").get(0)) {
                found = true;
            }

            if (!found) { //Handle Special Help File Case where syntax highlighting was pre configured          
                $(this).replaceWith("<pre class='brush: "+l+"; gutter:false; wrap-lines: true; auto-links: false; class-name:code'>"+$(this).html()+"</pre>");
            } else {
                $(this).replaceWith("<div>" + $(this).html() + "</div>");
            }
        }
    });

    SyntaxHighlighter.defaults['toolbar'] = false;
    SyntaxHighlighter.autoloader(
        'applescript            ../lib/syntaxhighlighter-3.0.83/scripts/shBrushAppleScript.js',
        'actionscript3 as3      ../lib/syntaxhighlighter-3.0.83/scripts/shBrushAS3.js',
        'bash shell             ../lib/syntaxhighlighter-3.0.83/scripts/shBrushBash.js',
        'coldfusion cf          ../lib/syntaxhighlighter-3.0.83/scripts/shBrushColdFusion.js',
        'cpp c                  ../lib/syntaxhighlighter-3.0.83/scripts/shBrushCpp.js',
        'c# c-sharp csharp      ../lib/syntaxhighlighter-3.0.83/scripts/shBrushCSharp.js',
        'css                    ../lib/syntaxhighlighter-3.0.83/scripts/shBrushCss.js',
        'delphi pascal          ../lib/syntaxhighlighter-3.0.83/scripts/shBrushDelphi.js',
        'diff patch pas         ../lib/syntaxhighlighter-3.0.83/scripts/shBrushDiff.js',
        'erl erlang             ../lib/syntaxhighlighter-3.0.83/scripts/shBrushErlang.js',
        'groovy                 ../lib/syntaxhighlighter-3.0.83/scripts/shBrushGroovy.js',
        'java                   ../lib/syntaxhighlighter-3.0.83/scripts/shBrushJava.js',
        'jfx javafx             ../lib/syntaxhighlighter-3.0.83/scripts/shBrushJavaFX.js',
        'js jscript javascript  ../lib/syntaxhighlighter-3.0.83/scripts/shBrushJScript.js',
        'perl pl                ../lib/syntaxhighlighter-3.0.83/scripts/shBrushPerl.js',
        'php                    ../lib/syntaxhighlighter-3.0.83/scripts/shBrushPhp.js',
        'text plain             ../lib/syntaxhighlighter-3.0.83/scripts/shBrushPlain.js',
        'powershell ps          ../lib/syntaxhighlighter-3.0.83/scripts/shBrushPowerShell.js',
        'py python              ../lib/syntaxhighlighter-3.0.83/scripts/shBrushPython.js',
        'ruby rails ror rb      ../lib/syntaxhighlighter-3.0.83/scripts/shBrushRuby.js',
        'sass scss              ../lib/syntaxhighlighter-3.0.83/scripts/shBrushSass.js',
        'scala                  ../lib/syntaxhighlighter-3.0.83/scripts/shBrushScala.js',
        'sql                    ../lib/syntaxhighlighter-3.0.83/scripts/shBrushSql.js',
        'vb vbnet               ../lib/syntaxhighlighter-3.0.83/scripts/shBrushVb.js',
        'xml xhtml xslt html    ../lib/syntaxhighlighter-3.0.83/scripts/shBrushXml.js'
    );

    SyntaxHighlighter.all();

    //scrollto
    function scrollTo(id) {
        var link_id = id || location.hash;
        if (link_id) {
            // $("#whtoc>ul").removeClass("nav");  //remove scrollspy 

            $("#whtoc li.active").removeClass("active");
            $("#whtoc li a[href='" + link_id + "']").parents("li").addClass("active");
            var topGap = 200;  //cdata
            topGap = $(link_id).is("h1,h2") ? 80 : topGap;  //nsoftware
            // $('#whrightcol').animate({ scrollTop: $(link_id).offset().top - topGap }, 500);
        
            //update page's title and desc
            if (link_id!="#default") {
                var chapterTitle = $(link_id).parents(".whiframe").prev("span.whtitle").attr("title");
                var chapterDesc = $(link_id).parents(".whiframe").prev("span.whtitle").attr("desc");
                if (chapterTitle) {
                    document.title = chapterTitle;
                }
                if (chapterDesc) {
                    $("meta[name='description']").attr('content', chapterDesc);
                }
            }

            //add scrollspy 
            // setTimeout(function(){
            //     $("#whtoc>ul").addClass("nav"); setScrollspy();
            // },600);
        
            /*fix the tree's width for IE*/
            var treeWidth = $("#resizerCol").css("margin-left");
            $("#resizerCol").css("margin-left","0px;");
            $("#resizerCol").css("margin-left",treeWidth);
        }
    };
    scrollTo();

    $("#whtoc li a").on("click", function () {
        var id = $(this).attr("href");
        scrollTo(id);
    });
  
    //for embedded links in the helpfile content we should scrollto as well
    $("#whcontent a").on("click", function () {
        var id = $(this).attr("href");
        if (id.indexOf("#") > -1) {//only scrollto if link is local to the page
            scrollTo(id);
        }
    });

    //set the left tree's position is fixed
    function setTreeHeight() {
        var viewHeight = document.body.clientHeight;
        var headerHeight = $("#whheader").height();
        // $("#whsizer").css({ "position": "fixed"});
        // $("#whsizer,#resizerCol").css({ "height": (viewHeight - headerHeight - 5), "min-height": "0" });
    }
    setTreeHeight();

    $(window).resize(function () {
        setTreeHeight();
    });

    function setScrollspy() {
        if($("#whtoc>ul").hasClass("nav")){
            $('#whrightcol').scrollspy({
                offset: 160,
                target: '#whtoc'
            });
        }
    }
    setScrollspy();

    // if we scroll manually, it should open the tree and highlight the correct section 
    var choke = null;
    $('body').on('activate.bs.scrollspy', function (e) {
        //IE issue fixed:if the previous event is the tree expand event, the activate.bs.scrollspy leads to we cannot click the sibling tree node, so skip it
        if (e.isTrigger == 3 && e.namespace == "bs.scrollspy") {
            $("#whtoc li.active").parents(".parent_li").each(function () {
                var children = $(this).find(' > ul > li');
                children.show();
                $(this).find(">span").attr('title', 'Collapse this branch').addClass('ygtvlm').removeClass('ygtvtp');

                //close all siblings nodes
                $(this).siblings().find(">span").attr('title', 'Expand this branch').addClass('ygtvtp').removeClass('ygtvlm');
                $(this).siblings().find(' > ul > li').hide();
            });
            clearTimeout(choke);
            choke = setTimeout(function() {
              setScrollBar();
              treeScrollTop();
            }, 100);
        }
        
    });

    function treeScrollTop() {
        // $("#whsizer").css("overflow-y", "scroll");
        if ($("#whsizer").css("overflow-y").toLowerCase() == "scroll") {
            var nodeCount = $("#whtoc li:visible").length;
            var activeNodeIndex = 0;
            var visibleNode = $("#whtoc li:visible");
            for (var i = 0; i < visibleNode.length; i++) {
                if ($(visibleNode[i]).is(".active")) {
                    activeNodeIndex = i + 1;
                }
            }
            var treeHeight = $("#whtoc>ul").height();
            $("#whsizer").scrollTop(treeHeight * (activeNodeIndex / nodeCount) - 200);
        }
    }

    setScrollBar();

    var processColumnWrap = function(){
        $("#whcontent>td:last table.table td").each(function(){
            var text = $.trim($(this).text());
            if(text.split(" ").length < 2) {
                $(this).addClass("nowrap");
            }
        });
    }();

    // hamburger menu handling
    $('#hamburger-menu').click(function(e){
        $('#whleftcol').toggle()
    })
    // recover ul display
    $('#whtoc > ul > li > ul > li ul').show();
});

