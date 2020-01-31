'use strict';

/*
File: jbr-tags-bulma.js
Override a few JbrTagCloud methods to allow proper Bulma tag styling
*/

JbrTagCloud.prototype.draw = function() {
    var tagArr = this.tagStrArr.map(this.makeTag, this);
    this.elem.innerHTML = '<div class="field is-grouped is-grouped-multiline">' + 
        tagArr.join('') + '</div>';
    if (this.options.showClose)
        this.addCloseListeners('.is-delete');
}

JbrTagCloud.prototype.makeTag = function(tagStr) {
    var text = tagStr.replace(' ', '&nbsp;');
    
    // Generate HTML for "plain" tag or link
    var html = '';
    if (this.options.urlPat == '') {
        html = '<span class="tag is-primary">' + text + '</span>';
    } else {
        var pat = this.options.urlPat;
        var url = pat.replace('{tag}', encodeURIComponent(tagStr.toLowerCase()));
        html = '<a class="tag is-primary" href="' + url + '">' + text + '</a>'; 
    }
    
    // Wrap it in more stuff if there's a close 'x' mark
    if (this.options.showClose) {
        html = '<div class="tags has-addons">' + html +
            '<a class="tag is-delete" data-tag-str="' + tagStr + '" ></a></div>';
    }

    return '<div class="control">' + html + '</div>';
}