if ($("#whtoc").html() == undefined) {
    var encoding = document.charset || document.characterSet || "utf-8";
    encoding = encoding.toLowerCase();
	
	if (encoding.indexOf("jis") > -1) {
		$.ajax({
			beforeSend: function( xhr ) {
				xhr.overrideMimeType( "text/html; charset=Shift_JIS" );
			},
			url: "_toc.htm", success: function (data) {
				$("#whsizer").html(data);
				loadTree();
			}
		});
	} else {
		$.ajax({
		   url: "_toc.htm", success: function (data) {
				$("#whsizer").html(data);
				loadTree();
			}
		});
	}
} else {
    loadTree();
}
    
checkForNewVersion(location.href);

function loadTree() {
    
    $("#whtoc").addClass("tree").show();
    $('.tree li:has(ul)').addClass('parent_li').prepend("<span class='ygtvtp'></span>").find(' > span').attr('title', 'Expand this branch');
    $('.tree li:not(.parent_li)').prepend("<span class='ygtvln'></span>");

    selectNodeByHref(location.href);

    if (typeof updateHeight == 'function') updateHeight();

    $('.tree li.parent_li > span').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        var isExpanded = false;
        if (children.is(":visible")) {
            children.hide();
            $(this).attr('title', 'Expand this branch').addClass('ygtvtp').removeClass('ygtvlm');
        } else {
            isExpanded = true;
            children.show();
            $(this).attr('title', 'Collapse this branch').addClass('ygtvlm').removeClass('ygtvtp');
        }

        var height = $("#whtoc").height();
        $("#resizerCol").css("height", height+"px"); //make the resizerCol's height auto.

        if (isExpanded) {
            if (typeof onHelpTreeExpanded == 'function') onHelpTreeExpanded($(this));
        } else {
            if (typeof onHelpTreeCollapsed == 'function') onHelpTreeCollapsed($(this));
        }
        e.stopPropagation();
    });
}

//Expand the tree nodes according to current href.
function selectNodeByHref(href) {
    if ("/" == href.slice(href.length - 1)) //if root, then select default.htm 
        href += 'default.htm';

    $("#whtoc li").each(function () {
        var h = "/" + $(this).children("a").attr("href");
        if (href.toLowerCase().indexOf(h.toLowerCase()) > -1) {
            $(this).children("a").addClass("current_bold");
            $(this).parents("ul").each(function () {
                $(this).children('li').show();
                $(this).siblings("span").attr('title', 'Collapse this branch').addClass('ygtvlm').removeClass('ygtvtp');
            });
            $(this).children("ul").children("li").show();
            if ($(this).children("span").hasClass('ygtvtp')) {
                $(this).children("span").attr('title', 'Collapse this branch').addClass('ygtvlm').removeClass('ygtvtp');
            }
            return false;
        }
    });
}

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
        url[url.length-1] = "";
        
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
    $('#whiframe pre').each(function (e) {
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

    if ($("meta[name='author']").length == 0) return;
    var host = $("meta[name='author']").attr('content');
    var formAction = 'https://' + host + '/kb/help/form.rst?force=true';
    var sendto = "support@" + host.replace("www.", "");
    var subject = $("meta[name='generator']").attr('content') || "Help Page:" + document.title;

    //regenerate a bootstrap modals window 
    var modalHtml = "<div class='modal fade' id='questionModal'>" +
      "<div class='modal-dialog' style='width:500px;'>" +
        "<div class='modal-content'>" +
          "<div class='modal-header'>" +
            "<button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button>" +
            "<h4 class='modal-title'>Questions / Feedback?</h4>" +  //modal title
          "</div>" +
          "<div class='modal-body'>" +
            "<form id='modal_feedbackform' action='" + formAction + "' method='post'>" +
            "<div class='form-group'><label>Name</label><input type=text name='name' value='' class='text form-control'/></div>" +
            "<div class='form-group'><label>Email</label><input type=text name='email' value='' class='text form-control'/></div>" +
            "<label>Feedback</label><textarea class='form-control' rows='3' name='message' placeholder='Please enter questions / feedback ...'></textarea>" +
            "<input type=hidden name=sendto value='" + sendto + "' /><input type=hidden name=subject value='" + subject + "' />" +
            "</form>"+
          "</div>" +
          "<div class='modal-footer'>" +
            "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>" +
            "<button type='button' class='btn btn-primary' id='modal-form-submit'>Send Feedback</button>" +
          "</div>" +
        "</div>" +
      "</div>" +
    "</div>";
    $("body").append(modalHtml);

    //show the modal
    $("#whfeedback").bind("click", function () {
        $("#questionModal").modal('show');
    });

    //submit
    $("#modal-form-submit").on("click", function () {
        var message = $("#modal_feedbackform textarea[name='message']").val();
        if (!message) {
            alert("Please enter questions / feedback");
            return false;
        }
        $("#modal_feedbackform").submit();
    });

    var processColumnWrap = function(){
        $("#whcontent>td:last table.table td").each(function(){
            var text = $.trim($(this).text());
            if(text.split(" ").length < 2) {
                $(this).addClass("nowrap");
            }
        });
    }();
});

$(function() {
// assign polyfill 
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign
if (typeof Object.assign !== 'function') {
    // Must be writable: true, enumerable: false, configurable: true
    Object.defineProperty(Object, "assign", {
      value: function assign(target, varArgs) { // .length of function is 2
        'use strict';
        if (target === null || target === undefined) {
          throw new TypeError('Cannot convert undefined or null to object');
        }
  
        var to = Object(target);
  
        for (var index = 1; index < arguments.length; index++) {
          var nextSource = arguments[index];
  
          if (nextSource !== null && nextSource !== undefined) { 
            for (var nextKey in nextSource) {
              // Avoid bugs when hasOwnProperty is shadowed
              if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
                to[nextKey] = nextSource[nextKey];
              }
            }
          }
        }
        return to;
      },
      writable: true,
      configurable: true
    });
  }

/**
 * Generate a table-of-content html structure based on analyzing <h1>-<h6> tags from provided html string,
 * and return new html string with table-of-content html prepended
 *
 * @param {string} html - html string to be analyzed
 * @param {Object} config - configuration object
 * @return {Object} an object containing attributes "html" for concatenated html string and toc for table-of-content only 
 */
// ! this is converted from \rssbus\v19\cnx\lib\static\mdconverter\libs\tocHTML.js to ES5 using
// https://babeljs.io/repl/
// This section is not intented to be directly modified.
"use strict";

function _instanceof(left, right) { if (right != null && typeof Symbol !== "undefined" && right[Symbol.hasInstance]) { return !!right[Symbol.hasInstance](left); } else { return left instanceof right; } }

/**
 * Generate a table-of-content html structure based on analyzing <h1>-<h6> tags from provided html string,
 * and return new html string with table-of-content html prepended
 *
 * @param {string} html - html string to be analyzed
 * @param {Object} config - configuration object
 * @return {Object} an object containing attributes "html" for concatenated html string and toc for table-of-content only 
 */
function TableOfContents(html, config) {
  var _config = Object.assign({
    StartLevel: 1
  }, config);

  var toc = '';
  var level = Number(_config.StartLevel) - 1;
  var regex = "<h([".concat(_config.StartLevel, "-6])([^>]*)>([^<]+)</h([").concat(_config.StartLevel, "-6])>");
  var modifiedHtml = html;
  modifiedHtml = modifiedHtml.replace(new RegExp(regex, 'gi'), // regex for detecting all <h> tags
  function () {
    var _arguments = Array.prototype.slice.call(arguments),
        str = _arguments[0],
        openLevel = _arguments[1],
        attributeStr = _arguments[2],
        titleText = _arguments[3],
        closeLevel = _arguments[4];

    var anchor;
    var attributes = attributeStr.match(/([\S]+)="([\S]*)"/gi);
    var attributeObj = {};
    if (_instanceof(attributes, Array)) attributes.forEach(function (item, index) {
      var name = item.split("=")[0];
      var value = item.split("=")[1].slice(1, -1);
      attributeObj[name] = value;
    });
    if (openLevel != closeLevel) return str;
    if (openLevel > level) toc += new Array(openLevel - level + 1).join('<ul>');else if (openLevel < level) toc += new Array(level - openLevel + 1).join('</li></ul>');else toc += new Array(level + 1).join('</li>');
    level = parseInt(openLevel); // if heading tag does not have id itself, generate one

    if (attributeObj.id === undefined) {
      anchor = titleText.trim().toLowerCase().replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, "").replace(/ /g, "-");
      // console.warn("Warning:\nheading tag ".concat(str, " are not assigned with id. Generated id \"").concat(anchor, "\" for it. \nIf you have same heading text for different heading tags in one page without your own defined id, it may generate the same id for them which may cause error.\n"));
    } else {
      anchor = attributeObj.id;
    }

    toc += "\n                        <li class=\"toc-entry toc-h".concat(openLevel, "\"><a href=\"#").concat(anchor, "\">").concat(titleText, "</a>\n                        ").trim();
    return "\n                        <h".concat(openLevel, " ").concat(attributeObj["class"] ? "class=\"".concat(attributeObj["class"], "\" ") : '', "id=\"").concat(anchor, "\">").concat(titleText, "</h").concat(openLevel, ">\n                    ").trim();
  });

  if (level) {
    toc += new Array(level + 1).join('</ul>');
  }

  return {
    html: modifiedHtml,
    toc: toc
  };
}

var contents = TableOfContents($('#content').html(), {StartLevel: 2})
$('.right-table-of-contents').append(contents.toc)
// give each heading tag an id 
var $hs = $('#content').find('h1, h2, h3, h4, h5, h6')
if ($hs.length > 5) {
    $('.right-table-of-contents').show()
    $('#content').find('h1, h2, h3, h4, h5, h6').each(function(index, ele){
        if (!$(ele).attr('id'))
            $(ele).attr('id', $(this).text().toLowerCase().trim().replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gi, "").replace(/ /g, "-"))
    })
    // init toc
    new TOC('#whiframe')
}

// hamburger menu handling
$('#hamburger-menu').click(function(e){
  $('#whleftcol').toggle()
})

// make sure active item in left sidebar is always in browser view
var adjustNavHeight = function () {
  // offset should exist first
  if ($("a.current_bold").offset() && $("a.current_bold").offset().top >= $('#whsizer').outerHeight()) {
    $('#whsizer')[0].scrollTop = $("a.current_bold").offset().top - 70
  }
}
adjustNavHeight()

})
