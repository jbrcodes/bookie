'use strict';  // (Is this actually *doing* anything?)

/* bookie.js */


//
// Beginnings of my own JS library? ;-)
//


// Alternate between the two (exclusive) classes in 'clsArr'
// Return the new one
function jbrSwitchClass(elem, clsArr) {
    var newCls = '';
    if (elem.classList.contains(clsArr[0])) {
        elem.classList.remove(clsArr[0]);
        elem.classList.add(clsArr[1]);
        newCls = clsArr[1];
    } else {
        elem.classList.remove(clsArr[1]);
        elem.classList.add(clsArr[0]);
        newCls = clsArr[0];
    }
    
    return newCls;
}


//
// Hide/show elems with plus/minus
//


function switchPlusMinus(event) {
    var elem = event.target;
    var clsArr = ['fa-plus-square-o', 'fa-minus-square-o'];
    var newCls = jbrSwitchClass(elem, clsArr);
    var newDisp = (newCls == 'fa-plus-square-o') ? 'none' : 'block';
    var myDiv = document.getElementById(elem.dataset.toggle);
    myDiv.style.display = newDisp;
}

function initPlusMinus() {
    var plusArr = document.querySelectorAll('.plus-minus');
    plusArr.forEach(function(elem) {
        elem.addEventListener('click', switchPlusMinus);
    });
}


//
// Bulma additions
//


function onClickBulmaModal(event) {
    // Add 'is-active' class to modal
    var elem = event.target;  // the link/button
    var id = elem.dataset.jbrTarget;
    var modal = document.getElementById(id);  // the modal
    modal.classList.add('is-active');
    
    // Add handlers to its 'jbr-modal-hide' elem(s) to hide it
    var hideArr = modal.querySelectorAll('.jbr-modal-hide');
    hideArr.forEach(function(elem) {
        elem.addEventListener('click', function(event) {
            modal.classList.remove('is-active');
        });
    });
}

function initBulmaModals() {
    var linkArr = document.querySelectorAll('.jbr-modal');
    linkArr.forEach(function(elem) {
        elem.addEventListener('click', onClickBulmaModal);
    });
}


//
// Load it!
//


document.addEventListener('DOMContentLoaded', function() {
    initPlusMinus();
    initBulmaModals();
});