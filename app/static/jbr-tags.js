'use strict';

/*
To Do:
- Get Enter to work for creating a new tag

Note: For various reasons this will not work with MSIE 11 or earlier.
*/


// ------------------------------------------------------------------
// Class JbrTagCloud
// ------------------------------------------------------------------


function JbrTagCloud(elem /* , options */) {
    this.elem = elem;
    this.tagStrArr = [];
    
    if (arguments.length > 1)
        this.options = Object.assign({}, this.DEFAULTS, arguments[1]);
    else
        this.options = Object.assign({}, this.DEFAULTS);
    
    if ('cloudUrlPat' in elem.dataset)
        this.options.urlPat = elem.dataset.cloudUrlPat;
    if ('cloudValues' in elem.dataset)
        this.setTags(elem.dataset.cloudValues);
}

JbrTagCloud.prototype.DEFAULTS = {
    urlPat: '',  // a pattern for creating tag links, for example "/foo/bar/{tag}/"
    showClose: false,  // if true, show an 'x' to removeTag()
    changeListener: null  // a DOM element to notify when an 'x' is pressed
}

JbrTagCloud.prototype.getCount = function() {
    return this.tagStrArr.length;
}

JbrTagCloud.prototype.getTags = function() {
    return this.tagStrArr;
}

JbrTagCloud.prototype.pushTag = function(tagStr) {
    tagStr = tagStr.trim();
    if (this.tagStrArr.indexOf(tagStr) == -1) {
        this.tagStrArr.push(tagStr);
        this.draw();
    }
}

JbrTagCloud.prototype.popTag = function() {
    this.tagStrArr.pop();
    this.draw();
}

// 'tagStrAny' can be array or comma-delimited string
JbrTagCloud.prototype.setTags = function(tagStrAny) {
    if (typeof tagStrAny === 'string')
        this.tagStrArr = tagStrAny.split(/\s*,\s*/);
    else
        this.tagStrArr = tagStrAny;
    this.tagStrArr = this.tagStrArr.map(function(tagStr) { 
        return tagStr.trim();
    });
    
    this.tagStrArr = this._getUnique(this.tagStrArr);
    this.draw();
}

JbrTagCloud.prototype.removeTag = function(tagStr) {
    var ix = this.tagStrArr.indexOf(tagStr);
    if (ix != -1) {
        this.tagStrArr.splice(ix, 1);
        this.draw();
    }
}

JbrTagCloud.prototype.addCloseListeners = function(cssSelector) {
    var closeArr = this.elem.querySelectorAll(cssSelector);
    var esto = this;
    closeArr.forEach(function(closeElem) {
        closeElem.addEventListener('click', function(event) {
            if ('tagStr' in event.target.dataset) {
                esto.removeTag(event.target.dataset.tagStr);
                if (esto.options.changeListener) {
                    esto.options.changeListener.dispatchEvent( new Event('change') );
                }
            }

        });
    });
}

JbrTagCloud.prototype._getUnique = function(tagStrArr) {
    var uniqueArr = [];
    tagStrArr.forEach(function(tagStr) {
        if (uniqueArr.indexOf(tagStr) == -1)
            uniqueArr.push(tagStr);
    });
    
    return uniqueArr;
}


// --- overloadable -------------------------------------------------


JbrTagCloud.prototype.draw = function() {
    var tagArr = this.tagStrArr.map(this.makeTag, this);
    this.elem.innerHTML = tagArr.join('');
    if (this.options.showClose)
        this.addCloseListeners('.jbr-tag-close');
}

JbrTagCloud.prototype.makeTag = function(tagStr) {
    var text = tagStr.replace(' ', '&nbsp;');
    if (this.options.showClose) {
        text += '<span class="jbr-tag-close" data-tag-str="' + tagStr + '">x</span>';
    }
    var html = '<span class="jbr-tag">' + text + '</span>';

    if (this.options.urlPat != '') {
        var up = this.options.urlPat;
        var url = up.replace('{tag}', encodeURIComponent(tagStr.toLowerCase()));
        html = '<a href="' + url + '">' + html + '</a>';
    }

    return html;
}


// ------------------------------------------------------------------
// Class JbrTagField
// ------------------------------------------------------------------


function JbrTagField(input) {
    this.oldInput = input;
    this.boxDiv = null;
    this.tagCloud = null;
    this.newInput = null;
    
    this.init();
}

// A not-too-hacky way to keep a class-wide unique ID
JbrTagField.prototype.ClassVars = {
    CloudId: 1
}

JbrTagField.prototype.init = function() {
    // Create a "box" container for cloud & new <input>
    var boxDiv = document.createElement('div');
    boxDiv.classList.add('jbr-tf-box')
    this.boxDiv = boxDiv;
    
    // Add a JbrTagCloud that will grow/shrink to hold tags
    var cloudDiv = document.createElement('div');
    cloudDiv.id = 'jbr-tf-cloud-' + this.ClassVars.CloudId++;
    cloudDiv.classList.add('jbr-tf-cloud');
    boxDiv.appendChild(cloudDiv);
    var opts = {
        showClose: true,
        changeListener: this.boxDiv
    };
    this.tagCloud = new JbrTagCloud(cloudDiv, opts);
    
    // Notify the "box" when a cloud tag's 'x' is clicked on
    var esto = this;
    this.boxDiv.addEventListener('change', function(event) {
        esto._updateOldInput();
    });
    
    // Append a "new" <input> element
    this.newInput = document.createElement('input');
    this.newInput.setAttribute('type', 'text');
    this.newInput.classList.add('jbr-tf-input');
    boxDiv.appendChild(this.newInput);
    
    // Notify the JbrTagField handler when the "new" <input> gets key presses
    this.newInput.addEventListener('keydown', function(event) {
        esto.onNewInputKeydown(event); 
    });
    
    // Insert the "box" in the DOM before the "old" <input>
    this.oldInput.parentNode.insertBefore(this.boxDiv, this.oldInput);
    this.oldInput.style.display = 'none';
    this.tagCloud.setTags( this.oldInput.value );
}

JbrTagField.prototype.getValue = function() {
    return this.oldInput.value;
}

JbrTagField.prototype.pushTag = function(tagStr) {
    this.tagCloud.pushTag(tagStr);
    this._updateOldInput();
}

JbrTagField.prototype.popTag = function() {
    this.tagCloud.popTag();
    this._updateOldInput();
}

JbrTagField.prototype._updateOldInput = function() {
    this.oldInput.value = this.tagCloud.getTags().join();
}

//
// Event handler(s)
//

JbrTagField.prototype.onNewInputKeydown = function(event) {
    switch (event.key) {
            
        //case 'Enter':  // maybe later...
        case ',':
            var newTag = this.newInput.value.replace(',', '');
            this.pushTag(newTag);
            
            // Without a slight delay the ',' will remain in newInput (??)
            var esto = this;
            setTimeout(function() { esto.newInput.value = ''; }, 10);
            
            // (Doesn't work)
            //if (event.key == 'Enter') {
            //    event.stopPropagation();
            //}
            break;
            
        case 'Backspace':
            if (this.newInput.value == '')
                this.popTag();
            break;
    }

}


// ------------------------------------------------------------------
// Bootstrap (*not* the Twitter one)
// ------------------------------------------------------------------


document.addEventListener('DOMContentLoaded', function() {
    var cloudArr = document.querySelectorAll('.jbr-tag-cloud');
    cloudArr.forEach(function(elem) {
        new JbrTagCloud(elem);
    });

    var inputArr = document.querySelectorAll('input.jbr-tag-field');
    inputArr.forEach(function(input) {
        new JbrTagField(input);
    });
});