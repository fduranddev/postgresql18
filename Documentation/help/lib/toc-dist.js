"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// isInteger polyfill https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isInteger
Number.isInteger = Number.isInteger || function (value) {
  return typeof value === 'number' && isFinite(value) && Math.floor(value) === value;
}; // foreach polyfill https://developer.mozilla.org/en-US/docs/Web/API/NodeList/forEach


if (window.NodeList && !NodeList.prototype.forEach) {
  NodeList.prototype.forEach = function (callback, thisArg) {
    thisArg = thisArg || window;

    for (var i = 0; i < this.length; i++) {
      callback.call(thisArg, this[i], i, this);
    }
  };
}

var TOC =
/*#__PURE__*/
function () {
  function TOC(scrollSelector, level) {
    var _this = this;

    _classCallCheck(this, TOC);

    this.scrollContainer;
    this.tocElement;
    this.level = typeof level === "number" ? level : 0;
    this.tocNodeList = [];
    this.entryNodeList = [];
    this.entryNodeOffsets = [];
    this._firstInit = true;

    if (!!this._firstInit) {
      window.addEventListener("DOMContentLoaded", function (e) {
        _this.onDomLoaded();
      });
      window.addEventListener("load", function (e) {
        _this.init(scrollSelector);
      });
    }
  }

  _createClass(TOC, [{
    key: "onDomLoaded",
    value: function onDomLoaded() {
      this.tocElement = TOC.helper.levelHandler("#table-of-contents", this.level);
      this.tocElement.style.visibility = 'visible';
    }
  }, {
    key: "init",
    value: function init(scrollSelector) {
      var _this2 = this;

      var throttled = TOC.helper.throttled;
      this.scrollContainer = document.querySelector(scrollSelector);
      this.tocElement = document.querySelector("#table-of-contents");
      this.handleData(); // when resizing, reinit

      if (!!this._firstInit) {
        var resizeTimer;
        window.addEventListener('resize', function (e) {
          clearTimeout(resizeTimer);
          resizeTimer = setTimeout(function () {
            _this2.init(scrollSelector);
          }, 250);
        });
        var handleHighlight = throttled(20, function (e) {
          return _this2.highlight();
        });
        this.scrollContainer.addEventListener("scroll", handleHighlight);
      }

      this.highlight(); // first init end

      this._firstInit = false;
    }
  }, {
    key: "handleData",
    value: function handleData() {
      var _this3 = this;

      this.tocNodeList = [];
      this.entryNodeList = [];
      this.entryNodeOffsets = []; // select all entries from toc container

      this.tocNodeList = this.tocElement.querySelectorAll(".toc-entry"); // select all corresponding heading tag nodes from every entry

      this.tocNodeList.forEach(function (i) {
        var href = i.querySelector("a").getAttribute("href").toString();

        _this3.entryNodeList.push(document.querySelector(href));
      }); // calculate offsetTop of each heading tag

      this.entryNodeList.forEach(function (i) {
        _this3.entryNodeOffsets.push(i.offsetTop - 40); // 40 offset

      });
    } // add event listener to highlight current item on scroll

  }, {
    key: "highlight",
    value: function highlight() {
      var findIndex = TOC.helper.findNearestNumIndexInAsendingArray;

      try {
        this.tocElement.querySelector(".active").classList.remove("active");
      } catch (e) {}

      var num = this.scrollContainer.scrollTop;
      if (num < this.entryNodeOffsets[0]) return;
      var index = findIndex(num, this.entryNodeOffsets);

      try {
        this.tocNodeList[index].querySelector("a").classList.add("active");
      } catch (e) {}
    }
  }]);

  return TOC;
}();

TOC.helper = {
  getElementTop: function getElementTop(element) {
    var actualTop = element.offsetTop;
    var current = element.offsetParent;

    while (current !== null) {
      actualTop += current.offsetTop;
      current = current.offsetParent;
    }

    return actualTop;
  },
  findNearestNumIndexInAsendingArray: function findNearestNumIndexInAsendingArray(num, array) {
    if (!Array.isArray(array)) return;
    if (!Number.isInteger(num)) return;
    var largeIndex = array.length - 1;
    var smallIndex = 0;
    var currIndex = Math.floor(largeIndex / 2);

    while (!(currIndex == largeIndex || currIndex == smallIndex)) {
      if (num === array[currIndex]) {
        return currIndex;
      } else if (num > array[currIndex]) {
        smallIndex = currIndex;
        currIndex = Math.floor((currIndex + largeIndex) / 2);
      } else {
        largeIndex = currIndex;
        currIndex = Math.floor((currIndex + smallIndex) / 2);
      }

      if (largeIndex - smallIndex === 1) {
        if (num >= array[largeIndex]) return largeIndex;
      }
    }

    return currIndex;
  },
  throttled: function throttled(delay, fn) {
    var lastCall = 0;
    return function () {
      var now = new Date().getTime();

      if (now - lastCall < delay) {
        return;
      }

      lastCall = now;
      return fn.apply(void 0, arguments);
    };
  },
  levelHandler: function levelHandler(selector, level) {
    var tocElement = document.querySelector(selector); // level handler
    // if level is set, remove all following level nodes

    if (!!level) {
      tocElement.querySelectorAll(".toc-h" + level).forEach(function (i) {
        try {
          i.querySelector("ul").remove();
        } catch (e) {}
      });
      var removeLevels = [];

      for (var index = level + 1; index < 10; index++) {
        removeLevels.push(".toc-h" + index);
      }

      tocElement.querySelectorAll(removeLevels.join(",")).forEach(function (i) {
        try {
          i.remove();
        } catch (e) {}
      });
    }

    return tocElement;
  }
};
//# sourceMappingURL=toc.js.map
