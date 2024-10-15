"use strict";
(self["webpackChunkmategen"] = self["webpackChunkmategen"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/getUrl.js":
/*!********************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/getUrl.js ***!
  \********************************************************/
/***/ ((module) => {



module.exports = function (url, options) {
  if (!options) {
    options = {};
  }
  if (!url) {
    return url;
  }
  url = String(url.__esModule ? url.default : url);

  // If url is already wrapped in quotes, remove them
  if (/^['"].*['"]$/.test(url)) {
    url = url.slice(1, -1);
  }
  if (options.hash) {
    url += options.hash;
  }

  // Should url be wrapped?
  // See https://drafts.csswg.org/css-values-3/#urls
  if (/["'() \t\n]|(%20)/.test(url) || options.needQuotes) {
    return "\"".concat(url.replace(/"/g, '\\"').replace(/\n/g, "\\n"), "\"");
  }
  return url;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
// Imports



var ___CSS_LOADER_URL_IMPORT_0___ = new URL(/* asset import */ __webpack_require__(/*! image/open-popup.svg */ "./style/image/open-popup.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_1___ = new URL(/* asset import */ __webpack_require__(/*! image/x_circle.svg */ "./style/image/x_circle.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_2___ = new URL(/* asset import */ __webpack_require__(/*! image/icon_edit.svg */ "./style/image/icon_edit.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_3___ = new URL(/* asset import */ __webpack_require__(/*! image/icon_logout.svg */ "./style/image/icon_logout.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_4___ = new URL(/* asset import */ __webpack_require__(/*! image/user_img.svg */ "./style/image/user_img.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_5___ = new URL(/* asset import */ __webpack_require__(/*! image/xiaokeai.png */ "./style/image/xiaokeai.png"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_6___ = new URL(/* asset import */ __webpack_require__(/*! image/send_botton.svg */ "./style/image/send_botton.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_7___ = new URL(/* asset import */ __webpack_require__(/*! image/toggle-sidebar.svg */ "./style/image/toggle-sidebar.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_8___ = new URL(/* asset import */ __webpack_require__(/*! image/new_welcome.svg */ "./style/image/new_welcome.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_9___ = new URL(/* asset import */ __webpack_require__(/*! image/new_chatbot_edit.svg */ "./style/image/new_chatbot_edit.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_10___ = new URL(/* asset import */ __webpack_require__(/*! image/new_chatbot_resp.svg */ "./style/image/new_chatbot_resp.svg"), __webpack_require__.b);
var ___CSS_LOADER_URL_IMPORT_11___ = new URL(/* asset import */ __webpack_require__(/*! image/MateGenAir.svg */ "./style/image/MateGenAir.svg?0302"), __webpack_require__.b);
var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_0___);
var ___CSS_LOADER_URL_REPLACEMENT_1___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_1___);
var ___CSS_LOADER_URL_REPLACEMENT_2___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_2___);
var ___CSS_LOADER_URL_REPLACEMENT_3___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_3___);
var ___CSS_LOADER_URL_REPLACEMENT_4___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_4___);
var ___CSS_LOADER_URL_REPLACEMENT_5___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_5___);
var ___CSS_LOADER_URL_REPLACEMENT_6___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_6___);
var ___CSS_LOADER_URL_REPLACEMENT_7___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_7___);
var ___CSS_LOADER_URL_REPLACEMENT_8___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_8___);
var ___CSS_LOADER_URL_REPLACEMENT_9___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_9___);
var ___CSS_LOADER_URL_REPLACEMENT_10___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_10___);
var ___CSS_LOADER_URL_REPLACEMENT_11___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_11___);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/
/* MateGen相关 */
.header-logo-text-box {
  transition: background-color 0.3s ease, color 0.3s ease; /* 增加平滑过渡效果 */
}
.header-logo-text-box>span{
  border-radius: 4px; /* 添加圆角效果 */
  padding:2px 5px;
  transition: background-color 0.3s ease; /* 增加平滑过渡效果 */
}

/*暂时禁用改功能*/
/* .header-logo-text-box>span:hover {
  background-color: var(--jp-layout-color2); 
  transition: background-color 0.3s ease; 
} */

.header-logo-air {
  color: white; /* 默认白色字体 */
}

.header-logo-pro {
  color: yellow; /* 验证通过后变为黄色 */
}

/* 弹窗居中样式 */
.api-key-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--jp-layout-color1); /* 使用JupyterLab的颜色风格 */
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: none; /* 初始隐藏 */
  flex-direction: column;
  justify-content: space-between;
  width: 300px;
}

/* 弹窗头部样式 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.modal-close {
  cursor: pointer;
  font-size: 25px;
  padding: 0px;
}

.modal-body {
  margin-top: 10px;
}
.modal-body .modal-body-content{
  display: flex;
  align-items: center;
}

.api-key-input {
  flex: 1;
  padding: 0 3px;
  margin-right: 10px;
  height: 22px;
  line-height: 25px;
}

.verify-button {
  background-color: var(--jp-brand-color1);
  color: white;
  border: none;
  padding: 4px 16px;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.reset-button, .cancel-button, .confirm-button {
  padding: 4px 16px;
  border: none;
  cursor: pointer;
}

.reset-button:hover, .cancel-button:hover, .confirm-button:hover, .verify-button:hover {
  background-color: var(--jp-brand-color2); /* Jupyter风格的悬停效果 */
}

.confirm-button:disabled {
  background-color: grey;
  cursor: not-allowed;
}

/* 验证状态提示 */
.api-key-status {
  margin-top: 10px;
  font-size: 12px;
  color: var(--jp-brand-color3);
}

.hidden {
  display: none;
}






.fix-code-button {
  background-color: #D63A36;
  color: white;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  margin-top: 16px;
  font-size: 12px;
}



/*
滚动条样式
*/
/* 自定义整个滚动条 */
.com-scroll ::-webkit-scrollbar {
  width: 8px; /* 设置滚动条的宽度 */
  height: 8px; /* 设置滚动条的高度 */
}
 
/* 自定义滚动条轨道 */
.com-scroll ::-webkit-scrollbar-track {
  background: transparent; /* 设置轨道的背景颜色 */
}
 
/* 自定义滚动条的滑块（thumb） */
.com-scroll ::-webkit-scrollbar-thumb {
  background: var(--jp-ui-font-color3); /* 设置滑块的背景颜色 */
  border-radius: 4px;/* 设置滚动条的圆角 */
}
 
/* 当滑块悬停或活动时，可以添加更多样式 */
.com-scroll ::-webkit-scrollbar-thumb:hover {
  background: var(--jp-layout-color2); /* 设置滑块在悬停状态下的背景颜色 */
}

/*
输入框鼠标光标颜色设置
*/
.chatbot-container .form-control {
  color: var(--jp-ui-font-color1); /* 光标颜色 */
}

.chatbot-container .form-control::-webkit-input-placeholder{
  color: var(--jp-ui-font-color3);
}

/* @supports (caret-color: #F06123) {
  .chatbot-container .form-control {
      color: var(--jp-ui-font-color1); 
      caret-color: #F06123; 
  }
} */

/* 
    登录容器样式 
*/
.smart-programming-button {
  display: inline-block;
  background-color: transparent;  
  color: white;
  margin-left: 2px;  
  margin-bottom: 5px;
  border: none;
  cursor: pointer;
  position: relative;
  top: 0;  
  left: 0;  
  z-index: 1000;
  width: 24px;  /* 缩小按钮宽度 */
  height: 24px; /* 缩小按钮高度 */
  padding: 2px; /* 缩小内边距 */
  font-size: 12px;  
  border-radius: 4px;  
}

/* 设置按钮在hover时显示的样式 */
.smart-programming-button:hover {
  background-color: rgba(255, 255, 255, 0.2);  
}

/* 灯泡图标 */
.smart-programming-button::before {
  content: '💡';  
  font-size: 14px;  /* 缩小图标大小 */
}

/* 在悬停时显示提示框 */
.smart-programming-button::after {
  content: 'AI Programming';  
  display: none;
  position: absolute;
  background-color: black;
  color: white;
  padding: 3px 5px;
  font-size: 12px;
  border-radius: 4px;
  top: 50%;  
  left: -100px;  
  transform: translateY(-50%);  
  white-space: nowrap;  
  z-index: 1001;
}

/* 悬停时显示提示框 */
.smart-programming-button:hover::after {
  display: block;
}

/* 智慧编程下拉按钮组 */
.smart-buttons {
  display: flex;
  justify-content: flex-start; /* 按钮左对齐 */
  margin-top: 5px;
  margin-left: 70px; /* 整体右移 */
}

.smart-buttons button {
  padding: 5px 10px;
  margin: 0 5px;
  cursor: pointer;
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  border: 1px solid var(--jp-border-color2);
  border-radius: 4px;
}

.smart-buttons button:hover {
  background-color: var(--jp-layout-color2);
}

.smart-buttons button:active {
  background-color: var(--jp-brand-color2);
}

.input-popup {
  background-color: transparent;  /* 背景设置为透明，伪装成cell的一部分 */
  border: none;  /* 去掉边框 */
  box-shadow: none;  /* 去掉阴影效果 */
  width: calc(100% - 24px);  /* 占据整个cell的宽度 */
  padding: 0;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  padding-left: 72px;
  padding-top:10px;
}

.input-field {
  width: 100%;  /* 确保输入框宽度填满父容器 */
  padding: 5px;  /* 适当的内边距 */
  border: none;  /* 默认无边框 */
  outline: none;  /* 移除默认的聚焦外边框 */
  background-color: transparent;  /* 透明背景，融入cell */
  color: inherit;  /* 继承父元素的字体颜色 */
  font-size: inherit;  /* 继承父元素的字体大小 */
  box-sizing: border-box;
}


/* 设置占位符颜色为偏白的灰色 */
.input-field::placeholder {
  color: #ccc;  /* 偏白的灰色 */
  opacity: 1;  /* 使占位符颜色不被透明度影响 */
}

/* 输入框聚焦时的边框效果 */
.input-field:focus {
  border: 2px solid #21A2FF;  /* 蓝色边框 */
  border-radius: 0px;  /* 添加边角圆润效果 */
  outline: none;  /* 避免默认的蓝色阴影 */
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.6);  /* 添加蓝色阴影，提升视觉效果 */
}



.user-message-display {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}



/* 主页面样式 */
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background: var(--jp-layout-color1);
    position: relative; /* 确保内部元素相对于容器定位 */
}


/* 欢迎页面 */
/* 内容样式 */
.content {
    position: relative;
    height: 100vh;
    width: 100%vw;
}


.login-container-content{
  height: 100%;
  overflow: hidden;
}

.login-container-box{
  height:100%;
  overflow: hidden;
  overflow-y: auto;
}

.chatbot-container-button{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding:0px 8px;
}

.chatbot-container-button button{
  margin: 0 !important;
}

/* 动态背景样式 */
#demo-canvas {
    position: absolute; /* 绝对定位覆盖整个背景 */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0; /* 背景位于文字的下层 */
    display: block;
}

/* 大标题和按钮容器 */
.large-header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2; /* 确保文字位于动态背景之上 */
    text-align: center;
    transition: transform 0.8s ease, left 0.8s ease; /* 添加过渡效果 */
}

/* 主标题样式 */
.main-title {
    font-weight: bold;
    font-size: 40px;
    color: var(--jp-ui-font-color1);
    margin-bottom: 20px;
    z-index: 2;
}

/* 副标题样式 */
.sub-title {
    font-size: 24px;
    color: var(--jp-ui-font-color1);
    margin-bottom: 0px;
    z-index: 2;
}

/* 说明文字样式 */
.description {
    font-size: 18px;
    color: var(--jp-ui-font-color1);
    margin-bottom: 30px;
    z-index: 2;
}

/* 额外的按钮样式 */
/* 登录按钮样式 */
.action-btn {
    font-size: 18px;
    color: #f9f1e9;
    background-color: #007BFF;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    z-index: 2;
    transition: background-color 0.3s ease, transform 0.1s ease; /* 添加过渡效果 */
}

.action-btn:hover {
    background-color: #0056b3;
}

/* 点击效果 */
.action-btn:active {
    background-color: #003f7f; /* 改变背景颜色 */
    transform: scale(0.95); /* 按下时缩小按钮 */
}

/* 返回按钮样式 */
.back-btn {
    font-size: 18px;
    color: #FFFFFF;
    background-color: #007BFF;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px; /* 与二维码和文字的间距 */
    transition: background-color 0.3s ease, transform 0.1s ease; 
}

.back-btn:hover {
    background-color: #0056b3;
}

/* 点击效果 */
.back-btn:active {
    background-color: #003f7f; /* 改变背景颜色 */
    transform: scale(0.95); /* 按下时缩小按钮 */
}

/* 登录页面的内容 */
.login-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

/* 登录标题 */
.login-title {
    font-size: 24px;
    color: var(--jp-ui-font-color1);
    margin-bottom: 20px;
}

/* 二维码样式 */
.qr-code {
    width: 200px;
    height: 200px;
    margin-bottom: 5px;
}

/* 登录说明文字 */
.login-description {
    font-size: 18px;
    color: var(--jp-ui-font-color1);
}
.qr_space {
	background: linear-gradient(90deg, #F06123 0%, #BEB1FC 100%); /* 渐变效果 */
	-webkit-background-clip: text; /* 用背景填充文字 */
	-webkit-text-fill-color: transparent; /* 将文字颜色设为透明，使渐变效果可见 */
	font-weight: bold; /* 设置加粗 */
  }

/* 登录页面样式 */
/* 进入登录页面时，欢迎页面的滑动效果 */
.large-header.slide-out {
    transform: translate(-100vw, -50%);
}

/* 登录页面从屏幕右侧滑入 */
#login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    position: absolute;
    top: 50%; /* 设置垂直居中 */
    left: 100%; /* 初始位置在屏幕外 */
    transform: translate(-4%, -60%); /* 确保登录页面保持顶部居中 */
    z-index: 2;
    text-align: center;
    transition: left 0.5s ease; /* 设置滑动动画效果 */
}

#login-page.slide-in {
    left: 0;
    transform: translate(-4%, -60%); /* 保持水平居中 */
}

  
  /* 二维码容器样式 */
  #qrcode {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 0;
    width: 200px;
    height: 200px;
    border-radius: 4px;
    background-color: #f0f0f0;
    aspect-ratio: 1 / 1;
    overflow: hidden;
  }
  
  /* 二维码图片样式 */
  #qrcode img,
  #qrcode .qrcode-image {
    width: 100%;
  }
  
  /* 占位符样式 */
  #qrcode .placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  /* 刷新占位符样式 */
  .refresh-placeholder {
    width: 100px;
    height: 100px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .refresh-placeholder svg {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

/* 
主容器样式 
*/
.jp-ChatbotWidget {
  display: flex;
  height: 100%;
  font-family: var(--jp-ui-font-family);
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: 14px;
}

/* 主容器 */
.chatbot-container {
  /* display: flex; */
  position: relative;
  height: 100%; 
  width: 100%; 
  background-color: var(--background-color);
}

.chatbox-container-rel{
  position: relative;
}

.chatbot-container-box{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--chatbot-dailog-bg);
  z-index: 9999;
  display: none;
}

.loading {
  font-size: 14px;
  color: #757575;
  text-align: center;
  margin-top: 20px;
}


.active-session {
  background-color: #e0f7fa;  /* 高亮颜色 */
  border-left: 4px solid #00796b;  /* 当前会话的标记 */
}

/* 当前选中的会话，始终显示三个点按钮 */
.active-session .more-btn {
  display: inline-block;  /* 始终显示三个点按钮 */
}


/* 弹窗容器 */
.popup-container-bg{
  width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);
    position: fixed;
    top: 0;
    left: 0;
}
.popup-container {
  position: fixed;
  top: 50%;
  left: 50%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  z-index: 9999;
  width: 370px;
  height: 225px;
  margin: -114px 0 0 -200px;
  border: 1px solid var(--jp-border-color2);
  padding:24px 16px 10px 16px;
  background-color: var(--jp-layout-color1);
  border-radius:2px;
}

.popup-container.hidden {
  display: none;
}

.popup-content {
  width: 100%;
  position: relative;
}

.popup-header {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding:8px;
}

.popup-header span{
  font-size: 16px;
  color: var(--jp-ui-font-color1);
}

.close-button {
  position: absolute;
  top:-22px;
  right:6px;
  background: none;
  border: none;
  font-size: 30px;
  color: var(--jp-ui-font-color2);
  cursor: pointer;
  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */
}

.close-button:hover{
  transform: scale(1.2);
}

.close-button:active{
  transform: scale(0.95);
}

.com-btn{
  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */
}

.com-btn:hover{
  transform: scale(1.05);
}

.com-btn:active{
  transform: scale(0.95);
}

.popup-body {
  margin-bottom: 20px;
}

.popup-body label {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
}

.popup-body input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  border:1px solid var(--jp-border-color2) !important;
  border-radius: 5px !important;
}

.popup-footer-box{
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
}

.popup-footer {
  display: flex;
  border-top: 1px solid var(--jp-border-color2);
  padding-top: 10px;
}

.popup-footer-desc{
  display: flex;
  align-items: center;
  flex:1;
  color: var(--jp-ui-font-color2);
  font-size: 12px;
}

.popup-footer-btns{
  /* width: 146px; */
}

.popup-button {
  padding: 4px 16px;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  font-size: 14px;
  margin-left: 10px;
  background-color: var(--jp-layout-color3);
  color: var(--jp-ui-font-color1);
  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */
}
.popup-button:hover {
  transform: scale(1.1); 
}
.popup-button:active {
  transform: scale(0.95); 
}

/* 确认按钮样式 */
.popup-button.confirm {
  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%);
  color: var(--jp-ui-font-color1);
  padding: 4px 16px;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  font-size: 14px;
  transition: background-image 0.3s ease; /* 添加渐变的过渡效果 */
}
/* 鼠标悬停效果 */
.popup-button.confirm:hover {
  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%); /* 悬停时渐变效果变化 */
}

/* 鼠标点击效果 */
.popup-button.confirm:active {
  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%); /* 点击时渐变效果变化 */
}

/**/
.popup-head-radio-group{
  display: flex;
  cursor: pointer;
}
.popup-head-radio-item{
  display: flex;
  flex: 1;
  padding: 0;
}
.popup-head-radio-item label{
  flex:1;
  font-size: 14px;
  color: var(--jp-ui-font-color1);
  cursor: pointer;
}
.popup-head-radio-item .popup-head-radio-input{
  width: 15px;
  height: 15px;
  margin: 0 5px 0 0;
  cursor: pointer;
}

.popup-head-select-group{
  display: flex;
  align-items: center;
  padding: 5px 8px;
}

.popup-head-select-group select{
  flex:1;
  width: 100%;
  height: 30px;
  background-color: var(--jp-layout-color0);
  color: var(--jp-layout-font-color0);
  border-radius: 2px;
  border: 1px solid var(--jp-border-color2);
  color: var(--jp-ui-font-color2);
}

.popup-head-select-group select option{
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  padding: 8px 4px;
  cursor: pointer;
}
.popup-head-select-group select option:hover{
  background-color: var(--jp-layout-color0);
}

.popup-head-select-group-reset{
  position: relative;
  font-size: 12px;
  color: var(--jp-ui-font-color1);
  padding: 0 10px;
  cursor: pointer;
  width: 30px;
}

.popup-head-select-group-reset span{
  display: none;;
}

.popup-head-select-group-reset:hover span{
  display: block;
  position: absolute;
  top: -25px;
  right: -15px;
  content: "";
  width: 84px;
  height: 16px;
  text-align: center;
  line-height: 16px;
  color: var(--jp-ui-font-color2);
  background-color: var(--jp-layout-color2);
  font-size: 12px;
  padding: 1px 3px;
}
.popup-head-select-group-reset:hover span::before{
  display: block;
  position: absolute;
  top: 15px;
  right: 35px;
  content: "";
  width: 5px;
  height: 5px;
  background-color: var(--jp-layout-color2);
  border-left: none;
  border-bottom: none;
  transform: rotate(135deg);
  border-radius: 2px;
}
/* 状态信息的样式 */
#knowledge-status {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 12px; /* 更小的字体 */
  color: var(--jp-ui-font-color1);
  margin-top: 10px;
  line-height: 16px;
  padding:0 8px;
}
#knowledge-status a{
  color: #FF8855;
}
#knowledge-status a:hover{
  text-decoration: underline;
}

/* 侧边栏样式 */
.sidebar {
  display: flex;
  width: 200px;
  height: calc(100% - 30px);
  flex-direction: column; /* 垂直排列内容 */
  background-color: var(--jp-layout-color1);
  padding: 8px;
  overflow-y: auto;
  transition: width 0.3s ease;
  border-right: 1px solid var(--jp-border-color2);
}

#session-list {
  flex-grow: 1; /* 让会话列表填充中间剩余空间 */
  overflow-y: auto; /* 使其可以滚动 */
  margin-top: 10px; /* 与"新建会话"按钮保持距离 */
  padding-top: 10px;
}

.sidebar-hidden {
  width: 0;
  padding: 0;
  overflow: hidden;
  border-right: none;
}

.sidebar-button {
  width: 80%; /* 按钮宽度为80% */
  padding: 10px;
  margin: 19px; /* 按钮向下移动，居中对齐 */
  background-color: var(--send-button-color);
  color: rgb(255, 255, 255);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 18px; /* 增大字体大小 */
  background-image: linear-gradient(90deg, #f46325 0%, #5a81ff 100%); /* 渐变效果 */
  transition: background-color 0.5s ease, background-image 0.5s ease; /* 增加过渡时间为0.5s */
  font-weight: bold; /* 加粗文字 */
} 

.sidebar-button:hover {
  background-image: linear-gradient(90deg, #F06123 0%, #B18FFC 100%);
  transition: background-color 0.7s ease, background-image 0.7s ease; /* 鼠标悬停时延长渐变时间 */
}
/* 点击效果 */
.sidebar-button:active {
  transform: scale(0.98); /* 点击时缩小 */
}  

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5px;
  margin-bottom: 5px;
  background-color: var(--jp-layout-color2);
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  position: relative;
  color:var(--jp-ui-font-color1);
  height: 30px;
  line-height: 30px;
}

.session-item:hover {
  background-color:var(--jp-layout-color3)
}

.session-item>span{
  font-size: var(--jp-ui-font-size1);
}
.fade-effect {
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis; 
}

.fade-effect::after {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 30px;  /* 渐变效果的宽度 */
  background: linear-gradient(to right, transparent, transparent);  /* 全透明的渐变 */
}



/* 当处于编辑状态时的输入框样式 */
.rename-input {
  font-size: inherit; /* 确保字体大小一致 */
  border: 1px solid #ccc;
  padding: 5px;
  width: 100%; /* 占据可用空间 */
  box-sizing: border-box; /* 确保内边距不会改变输入框大小 */
  background-color: var(--jp-layout-color2);
  color: var(--jp-ui-font-color1);
}


/* 三个点按钮 */
/* more-options 容器样式 */
.more-options {
  position: relative;
  display: inline-block;
}

.more-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: gray;  /* 默认灰色 */
  display: none;
}

.session-item:hover .more-btn {
  display: inline-block;
}

/* 当鼠标悬停在三个点按钮上时，颜色变为白色 */
.more-btn:hover {
  color: white;  /* 悬停时变为白色 */
}

/* 弹出菜单的样式 */
.dropdown-menu {
  position: absolute;  /* 使用 fixed 以脱离侧边栏的限制 */
  background-color: var(--jp-layout-color1);
  border: 1px solid var(--jp-border-color2);
  border-radius: 5px;
  white-space: nowrap; /* 防止内容换行 */
  z-index: 100000; /* 确保显示在最前 */
  padding: 5px 0;
  width: auto; /* 根据内容自动调整宽度 */
  display: none; /* 默认隐藏 */
  top: 25px;
  right: 15px;

}

/* 确保点击按钮时不会改变布局 */
.dropdown-menu button {
  display: block;
  width: 100%; /* 占满菜单宽度 */
  padding: 10px 20px; /* 设置内边距让按钮看起来整齐 */
  background: none; /* 保持背景透明 */
  color: inherit; /* 继承颜色 */
  border: none; /* 去掉默认边框 */
  text-align: left; /* 左对齐文本 */
  cursor: pointer;
  font-size: 12px;
}

/* 鼠标悬停时的背景颜色 */
.dropdown-menu button:hover {
  background-color: var(--jp-layout-color2); /* 悬停时设置透明背景 */
}

/* 显示下拉菜单 */
.dropdown-menu.show {
  display: block  /* 确保显示 */
}

/* 让下拉菜单按钮保持之前的展示效果，并调整为横向排列 */
.rename-btn, .delete-btn {
  display: block; /* 确保按钮占据独立的行 */
  padding: 10px 20px; /* 设置合适的内边距，保证按钮宽度 */
  background: none; /* 保持背景透明或使用你指定的背景色 */
  border: none; /* 去掉边框 */
  text-align: left; /* 文字左对齐 */
  white-space: nowrap; /* 防止文字换行 */
  cursor: pointer; /* 鼠标悬停时变为指针 */
  font-size: 14px; /* 文字大小合适 */
  color: var(--jp-ui-font-color0); /* 确保文字颜色适配 */
  width: 100%; /* 让按钮宽度占满整个菜单 */
}

/* 鼠标悬停时的效果 */
.rename-btn:hover, .delete-btn:hover {
  background-color: var(--jp-layout-color2); /* 悬停时背景色 */
  color: var(--jp-ui-font-color0); /* 悬停时文字颜色 */
}

/* 聊天区域样式 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--jp-layout-color0);
}

/* 当侧边栏弹出时，压缩聊天区域 */
.chat-area.sidebar-open {
  margin-left: 200px; /* 侧边栏宽度 */
}

/* 顶部栏样式 */
.chat-header {
  display: flex;
  justify-content: space-between; /* 左侧和右侧对齐 */
  align-items: center;
  padding: 10px;
  background-color: var(--jp-layout-color1);
  z-index: 1000;
  height: 10px;
  border-bottom: 1px solid var(--jp-border-color2);
}

.chat-header-btn button{
  margin-right: 10px !important;
}

/* 顶部按钮样式 */
.header-button {
  width: 18px; /* 控制按钮大小 */
  height: 18px;
  border: none;
  cursor: pointer;
  margin-right: 15px;
  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */
}

/* 鼠标悬停效果 */
.header-button:hover {
  color: var(--send-button-hover); /* 鼠标悬停时颜色变化 */
  transform: scale(1.1); /* 放大按钮 */
}

/* 鼠标点击效果 */
.header-button:active {
  transform: scale(0.9); /* 点击时按钮缩小 */
}


/* 导入SVG图标样式 */
.toggle-sidebar {
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_0___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_0___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}

/*侧边导航展开按钮*/
.toggle-sidebar-open {
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_1___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_1___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}

/* API-KEY SVG图标样式 */
.chat-icon-edit {
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_2___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_2___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}

/* 退出登录SVG图标样式 */
.chat-icon-logout {
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_3___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_3___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}

/*用户图像*/
.header-button-user{
  width: 32px;
  height: 32px;
  position: relative;
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_4___});
  background-position: center;
  background-repeat: no-repeat;
  background-size: 16px 16px;
  background-clip: contain;
  background-color: transparent;
  margin: 0 0 0 12px;
}

.header-button-user .header-button-user-block{
  display: none;
}

.header-button-user:hover .header-button-user-block{
  display: block;
  transition: display 0.3s ease-in-out;
}

/*鼠标移入用户图像显示*/
.header-button-user-block{
  position: absolute;
  top: 100%;
  right: 0px;
  width: 171px;
  height: 72px;
  border: 1px solid var(--jp-border-color2);
  border-radius: 2px;
  background-color:var(--jp-layout-color1);;
  padding:14px 5px;
}

.header-button-user-block ul{
  list-style: none;
  padding: 0;
  margin: 0;
}

.header-button-user-block ul li{
  display: flex;
  align-items: center;
  justify-content: left;
  font-size: 12px;
  color: var(--jp-ui-font-color1);
  padding:0 0 0 5px;
  font-weight: normal;
}
.header-button-user-block ul li:hover{
  background-color: var(--jp-layout-color2);
  transition: backgroundColor 0.3s ease-in-out;
}
.header-button-user-block .header-button{
  margin-right: 5px;
}

.chat-bg-show{
  display: block;
}

/* 顶部文字 */
.header-logo-text {
  font-size: 16px; /* "Powered by"的字体大小 */
  color: #ccc; /* "Powered by"的字体颜色 */
  font-weight: normal; /* 设置普通字体 */
  font-weight: bold; /* 设置加粗 */
  display: flex;
  flex:1;
  align-items: center;
}

.header-logo-text .header-logo-title{
  flex: 1;
  text-align: center;
  display: flex;
  justify-content: right;
  align-items: center;
  font-size: 11px;
}

.header-logo-title-span{
  position: relative;
  font-size: 11px;
  border-radius: 1px;
  color: var(--jp-ui-font-color3);
  background: var(--jp-layout-color2);
  padding:2px 18px 2px 6px;
  height: 16px;
  line-height: 16px;
  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */
}

.header-logo-title-span::before{
  width: 6px;
  height: 6px;
  content: "";
  position: absolute;
  top:5px;
  right:6px;
  border:1px solid var(--jp-ui-font-color3);
  border-left: none;
  border-bottom: none;
  transform: rotate(45deg);
}
.header-logo-title-span:hover{
  cursor: pointer;
  background: var(--jp-layout-color3);
  transform: scale(1.05); /* 放大按钮 */
}
.header-logo-title-span:active{
  transform: scale(0.95); /* 按下时缩小按钮 */
}

.header-logo-text .header-logo-text-box{
  flex:1;
  text-align:right;
}

.header-logo {
  font-size: 14px; /* "MateGen"的字体大小 */
  color: #fff; /* "MateGen"的字体颜色 */
  font-weight: bold; /* 设置加粗 */
  background: linear-gradient(90deg, #F06123 0%, #BEB1FC 100%); /* 渐变效果 */
  -webkit-background-clip: text; /* 用背景填充文字 */
  -webkit-text-fill-color: transparent; /* 将文字颜色设为透明，使渐变效果可见 */
}

/* 二维码和提示文本容器 */
.qr-code-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  padding-bottom: 30px; /* 为底部留出一点空间 */
}

/* 侧边底部二维码样式 */
.qr-code-in {
  width: 120px; /* 设置二维码图片宽度 */
  height: 120px; /* 设置二维码图片高度 */
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_5___}); /* 加载二维码图片 */
  background-size: 110px 110px; /* 确保图片不拉伸，按比例显示 */
  background-position: center; /* 图片居中显示 */
  border: 1px solid transparent; /* 为边框留出空间 */
  background-repeat: no-repeat;
  border-image: linear-gradient(180deg, #F06123 0%, #BEB1FC 100%) 1; /* 渐变边框 */
  border-radius: 8px; /* 可选：为边框添加圆角效果 */
  margin: 15px auto; /* 居中对齐 */
  margin-bottom: 10px; /* 二维码与文本之间的间距 */
}

/* 提示文字样式 */
.qr-code-text {
  text-align: center; /* 文本居中 */
  margin: 0;
  padding: 0 10px; /* 给文字留出一点边距 */
}
.qr-code-text p{
  padding: 3px;
  margin: 0;
  font-size: 14px;
  color: var(--jp-ui-font-color1); /* 或者其他你想要的颜色 */
}

/* 聊天记录区域样式 */
#chat-log {
  display: flex;
  flex-direction: column;
  background-color: var(--jp-layout-color0);
  overflow-y: auto;
  padding: 20px;
  height: calc(100% - 40px);
}

/* 消息通用样式 */
.message {
  margin-bottom: 0px;
  max-width: 100%;
  padding: 3px 8px;
  line-height: 1.5;
  border-radius: 5px;
  box-shadow: 0 1px 3px var(--jp-layout-color3);
}

/* 用户消息样式 */
.user-message {
  align-self: flex-end;
  background-color: var(--jp-layout-color2);
  font-size: 14px;
  color: var(--jp-ui-font-color1);
}

/* 机器人消息样式 */
/* 在现有的CSS中添加或更新以下样式 */

.bot-message {
  background-color: var(--jp-layout-color0);
  padding: 10px 5px;
  border-radius: 8px;
  margin-bottom: 15px;
  margin-top: 15px;
  font-size: 14px;
  color: var(--jp-ui-font-color1);
}

.bot-message p {
  margin:0;
}

.bot-message h1, .bot-message h2, .bot-message h3, .bot-message h4, .bot-message h5, .bot-message h6 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #ffffff;
}

.bot-message ul, .bot-message ol {
  margin: 10px 0;
  padding-left: 20px;
}

.bot-message li {
  margin-bottom: 5px;
}

.bot-message code {
  background-color: var(--jp-layout-color2);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

.bot-message pre {
  background-color: #2b2b2b;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
}

.bot-message pre code {
  background-color: transparent;
  padding: 0;
  color: var(--jp-ui-font-color0);
  text-shadow: none;
}

.bot-message blockquote {
  border-left: 4px solid #10a37f;
  padding-left: 10px;
  margin: 10px 0;
  color: #a0a0a0;
}

.bot-message img {
  max-width: 100%;
  height: auto;
}

.bot-message table {
  border-collapse: collapse;
  width: 100%;
  margin: 15px 0;
}

.bot-message th, .bot-message td {
  border: 1px solid #565869;
  padding: 8px;
  text-align: left;
}

.bot-message th {
  background-color: #2b2b2b;
}

.highlighted-code {
  background-color: #2b2b2b;
  display: block;
  padding: 10px;
  border-radius: 5px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

/* 错误消息样式 */
.error-message {
  align-self: center;
  background-color: #ff4d4f;
  color: white;
}

/* 输入区域样式 */
.chat-input {
  display: flex;
  padding: 0;
  background-color: var(--jp-layout-color1); /* 为输入区域添加背景色 */
  align-items: center; /* 垂直方向居中 */
  justify-content: flex-start; /* 水平方向从左到右排列 */
  margin: 0 24px 24px 24px; /* 设置上方外边距为 0px，底部外边距为 15px */
  position: relative; /* 为左侧和右侧按钮提供定位依据 */
}

.chat-input .input-wrapper {
  flex: 1;
  display: flex;
  position: relative; /* 为绝对定位的按钮做准备 */
  align-items: center; /* 垂直居中对齐所有子元素 */
}


.chat-input textarea {
  height: 14px; /* 设置固定的初始高度 */
  min-height: 32px; /* 确保最小高度也是 14px */
  max-height: 150px; /* 保持最大高度限制 */
  padding: 0; /* 调整内边距以适应较小的高度 */
  border: 1px solid var(--jp-border-color2);
  border-radius: 2px;
  font-size: 14px;
  background-color: var(--neutral-fill-input-rest);
  color: var(--jp-ui-font-color0);
  resize: none;
  overflow-y: auto;
  transition: border-color 0.3s, box-shadow 0.3s, height 0.1s;
  box-sizing: border-box; /* 确保padding不会增加总高度 */
  line-height: 18px; 
  padding:5px 45px 5px 5px;
  width: 100%;
}

.chat-input textarea:focus {
  outline: none;
  border-color: var(--jp-brand-color1);
}

.chat-input textarea::placeholder {
  color: var(--jp-ui-font-color3);
}

.chat-input .send-button {
  position: absolute;
  right: 15px;
  bottom: -8px; /* 垂直居中 */
  transform: translateY(-50%); /* 精确垂直居中 */
  color: white;
  border: none;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: transparent;
  transition: background-color 0.3s, transform 0.2s;
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_6___});
  background-size: 25px 15px;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0; /* 初始不显示 */
  transform: translateY(-50%) scale(0.8);
}

.chat-input textarea:not(:placeholder-shown) + button:not(.knowledge-base-button) {
  opacity: 1;
  transform: translateY(-50%) scale(1);
}

/* .chatbot-container-box button:not(.knowledge-base-button):hover {
  background-color: var(--send-button-hover);
  transform: translateY(-50%) scale(1.1);
} */

.chatbot-container-box button::before {
  content: none; /* 使用Unicode箭头作为发送图标 */
  font-size: 16px;
}

/* 输入框左侧的按钮（始终显示） */
.knowledge-base-button {
  width: 18px;
  height: 18px;
  border: none;
  cursor: pointer;
  margin-right: 10px; /* 确保按钮和输入框之间有间距 */
  z-index: 1; /* 确保层级较高，不被覆盖 */
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_7___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_7___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}
/* .chat-input .knowledge-base-button:hover {
  transform: scale(1.1);
}

.chat-input .knowledge-base-button:active {
  transform: scale(0.98);
} */


.new-welcome-base-button {
  width: 14px;
  height: 14px;
  border: none;
  cursor: pointer;
  margin-right: 10px; /* 确保按钮和输入框之间有间距 */
  z-index: 1; /* 确保层级较高，不被覆盖 */
  mask:url(${___CSS_LOADER_URL_REPLACEMENT_8___}) no-repeat 50% 50%;
  -webkit-mask:url(${___CSS_LOADER_URL_REPLACEMENT_8___}) no-repeat 50% 50%;
  mask-size: contain;
  -webkit-mask-size:contain;
  background-color:var(--jp-ui-font-color1);
}

.new-star-left{
  position: absolute;
  background-color: transparent;
  border: none;
  cursor: pointer;
  background-size: cover;
  background-position: center;
  margin-right: 10px; /* 确保按钮和输入框之间有间距 */
  z-index: 1; /* 确保层级较高，不被覆盖 */
}

.new-chatbot-edit{
  top:15px;
  left: 84px;
  width: 23px;
  height: 21px;
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_9___}); /* 替换为你的图标 */
}

.new-chatbot-resp{
  top:10px;
  left: 82px;
  width: 32px;
  height: 32px;
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_10___}); /* 替换为你的图标 */
}

/* 聊天机器人容器样式 */
/* 更新代码框样式 */
.jp-ChatbotWidget .code-wrapper {
  margin: 10px 0;
  border-radius: 6px;
  overflow: hidden;
  background-color: #0D0D0D;  /* 深色背景 */
}

.jp-ChatbotWidget .code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 12px;
  background-color: var(--jp-layout-color2);
  color: var(--jp-ui-font-color1);
}

.jp-ChatbotWidget .code-language {
  font-family: monospace;
  font-size: 1.1em;
}

/* 新增代码换行 */
.jp-ChatbotWidget .code-wrapper pre {
  white-space: pre-wrap;  /* 自动换行 */
  word-wrap: break-word;  /* 处理长单词的换行 */
  overflow-wrap: break-word; /* 处理长单词的换行 */
  max-width: 100%;  /* 限制代码块的最大宽度 */
  box-sizing: border-box;  /* 确保宽度计算包含内边距和边框 */
}

.jp-ChatbotWidget .code-wrapper code {
  white-space: pre-wrap;  /* 自动换行 */
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  font-size: 1.1em;
}

.jp-ChatbotWidget .copy-button {
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
  transition: background-color 0.3s;
}

.jp-ChatbotWidget .copy-button:hover {
  background-color: #5a5a5a;
}

.jp-ChatbotWidget pre {
  margin: 0;
  padding: 12px;
  background-color: var(--jp-layout-color1);  /* 与 code-wrapper 背景色一致 */
  border:1px solid var(--jp-border-color3);
}

.jp-ChatbotWidget code {
  font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
  line-height: 1.5;
  color: var(--jp-ui-font-color1);
}

/* 覆盖 Prism.js 的一些样式 */
.jp-ChatbotWidget .token.comment,
.jp-ChatbotWidget .token.prolog,
.jp-ChatbotWidget .token.doctype,
.jp-ChatbotWidget .token.cdata {
  color: #8292a2;
}

.jp-ChatbotWidget .token.punctuation {
  color: var(--jp-ui-font-color2);
}

.jp-ChatbotWidget .token.namespace {
  opacity: .7;
}

.jp-ChatbotWidget .token.property,
.jp-ChatbotWidget .token.tag,
.jp-ChatbotWidget .token.constant,
.jp-ChatbotWidget .token.symbol,
.jp-ChatbotWidget .token.deleted {
  color: #f92672;
}

.jp-ChatbotWidget .token.boolean,
.jp-ChatbotWidget .token.number {
  color: #ae81ff;
}

.jp-ChatbotWidget .token.selector,
.jp-ChatbotWidget .token.attr-name,
.jp-ChatbotWidget .token.string,
.jp-ChatbotWidget .token.char,
.jp-ChatbotWidget .token.builtin,
.jp-ChatbotWidget .token.inserted {
  color: #a6e22e;
}

.jp-ChatbotWidget .token.operator,
.jp-ChatbotWidget .token.entity,
.jp-ChatbotWidget .token.url,
.jp-ChatbotWidget .language-css .token.string,
.jp-ChatbotWidget .style .token.string,
.jp-ChatbotWidget .token.variable {
  color: #f8f8f2;
}

.jp-ChatbotWidget .token.atrule,
.jp-ChatbotWidget .token.attr-value,
.jp-ChatbotWidget .token.function,
.jp-ChatbotWidget .token.class-name {
  color: #e6db74;
}

.jp-ChatbotWidget .token.keyword {
  color: #66d9ef;
}

.jp-ChatbotWidget .token.regex,
.jp-ChatbotWidget .token.important {
  color: #fd971f;
}

.delete-session {
  background: none;
  border: none;
  color: #ff4d4f;
  cursor: pointer;
  font-size: 16px;
  padding: 5px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.session-item:hover .delete-session {
  opacity: 1;
}

.delete-session:hover {
  color: #ff7875;
}

/* 添加过渡效果 */
.chatbot-container, .login-container {
  transition: opacity 0.3s ease-in-out;
}

/* 默认居中效果 */
.chatbot-body{
  position:absolute;
  top:50%;
  left:50%;
  width:430px;
  height:180px;
  margin:-86px 0 0 -215px;
}
.chatbot-body-header{
  width: 340px;
  height:70px;
  background-color: transparent;
  background-size: 340px 70px; /* 控制图标大小 */
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_11___}); /* 读取图标 */
  background-repeat: no-repeat;
  background-position: center;
  background-origin: border-box;
  background-clip: content-box, border-box;
  margin: -100px auto 50px auto;
}
.chatbot-body-content{
  display:flex;
}
.chatbot-content-item{
  flex:1;
  height:inherit;
  margin: 24px 12px;
  padding:0;
  cursor: pointer;
  border-radius: 8px;
  box-sizing: border-box;
  border: 1px solid transparent;
  background-image: linear-gradient(var(--jp-layout-color1), var(--jp-layout-color1)), linear-gradient(180deg, rgba(240, 97, 35, 0.6) 0%, rgba(190, 177, 252, 0.6) 100%);
  border-radius: 8px;
  background-origin: border-box;
  background-clip: content-box, border-box;
  border-radius: 2px;
  text-align: center;
}

.chatbot-content-item p{
  line-height:26px;
  font-size:12px;
  color: var(--jp-ui-font-color0);
  padding:0 12px 12px 12px;
  margin: 0;
}

.chatbot-content-item-title{
  position: relative;
  font-size:16px;
  font-weight: 600;
  padding: 50px 12px 5px 12px;
  margin: 0;
  color: var(--jp-ui-font-color0);
}

.session-name{
  width: 170px; /* 设置容器宽度 */
  white-space: nowrap; /* 防止文本换行 */
  overflow: hidden; /* 隐藏超出容器的文本 */
  text-overflow: ellipsis; /* 超出部分显示为省略号 */
  word-break: break-all;
  word-wrap: break-word;
}

.chat-hide{
  display: none !important;
}

.chat-show{
  display: block;
}

.chat-show-flex{
  display: flex;
}

/* 重置样式 */
.jp-OutputArea-child .jp-OutputArea-output{
  padding:5px 12px 16px 12px;
}

/*消息提示*/
.chat-message-box{
  position: absolute;
  top:10px;
  left:50%;
  width: 250px;
  margin: 0 0 0 -125px;
  z-index: 9999;
}
.chat-message-box span{
  width: 100%;
  height: 25px;
  background: #e79c38;
  color: #fff;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  font-size: 12px;
}

/*自定义select*/
.popup-select-box{
  position:relative;
  width:100%;
  height:30px;
}
.popup-select-body{
  position:absolute;
  top:34px;
  left:0;
  border-color: transparent;
  width: 100%;
  max-height: 0px;
  overflow-y: auto;
  z-index: 999;
  background-color: var(--jp-layout-color1);
  transition: max-height 0.3s ease, transform 0.1s ease, borderColor 0.1s ease; /* 添加过渡效果 */
  border-radius: 5px;
}
.popup-select-box::before{
  content: "";
  position: absolute;
  right: 6px;
  top: 12px;
  width: 8px;
  height: 8px;
  border: 1px solid var(--jp-border-color2);
  transform: rotate(45deg);
  border-top: none;
  border-right: none;
  transition: transform 0.1s ease, right 0.1s ease;
}
.popup-select-box-show::before{
  transform: rotate(-45deg);
  right: 10px;
  transition: transform 0.1s ease, right 0.1s ease;
}
.popup-select-input{
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  width: calc(100% - 16px) !important;
  cursor: pointer;
}
.popup-select-input:active,.popup-select-input:focus{
  outline: none;
  border-color: var(--jp-brand-color1);
}
.popup-select-body ul{
  list-style: none;
  padding: 0;
  margin: 0;
  border-radius: 5px;
}
.popup-select-body ul li{
  height: 30px;;
  line-height: 30px;
  padding:0 10px;
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  cursor: pointer;
}
.popup-select-body ul li:hover{
  background-color: var(--jp-brand-color1);
  color: var(--jp-ui-font-color0);
}
.popup-select-show{
  max-height: 160px;
  border:1px solid var(--jp-border-color2);
  transition: max-height 0.3s ease, transform 0.1s ease, border-color 0.1s ease; /* 添加过渡效果 */
}

/*自定义知识库*/
.popup-select-file{
  display: flex;
  padding:10px 0;
}

.popup-select-file-box{
  display: flex;
  color: var(--jp-ui-font-color1);
}
.popup-select-file-label,.popup-select-file-name{
  padding:4px;
}
.popup-select-file-btn{
  width: 72px;
  border: 1px solid var(--jp-border-color2);
  text-align: center;
  padding: 4px 16px;
  border-radius: 3px;
  cursor: pointer;
}
.popup-select-file-btn:hover{
  background-color: var(--jp-layout-color2);
}

@media (max-width: 768px) {
  /* 只保留 message 的 max-width 设置 */
  .message {
    max-width: 100%;
  }
}
  
/* 颜色变量 */
:root {
  --background-color: #00283F;
  --header-color: #00324F;
  --user-message-color: #094060;
  --bot-message-color: #012A43;
  --text-color: #ececf1;
  --border-color: #504E50;
  --input-background: #031926;
  --send-button-color: #083550;
  --send-button-hover: #00283F;
  --scrollbar-thumb:#333333;;
  --scrollbar-thumb-hover:#212121;;
  --chatbot-dailog-bg:rgba(0,0,0,0.25);
  --sidebar-background:rgba(255,255,255,0.05);
  --sidebar-background-hover:rgba(255,255,255,0.1);
  --sidebar-color:#BDBDBD;
}`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n/* MateGen相关 */\n.header-logo-text-box {\n  transition: background-color 0.3s ease, color 0.3s ease; /* 增加平滑过渡效果 */\n}\n.header-logo-text-box>span{\n  border-radius: 4px; /* 添加圆角效果 */\n  padding:2px 5px;\n  transition: background-color 0.3s ease; /* 增加平滑过渡效果 */\n}\n\n/*暂时禁用改功能*/\n/* .header-logo-text-box>span:hover {\n  background-color: var(--jp-layout-color2); \n  transition: background-color 0.3s ease; \n} */\n\n.header-logo-air {\n  color: white; /* 默认白色字体 */\n}\n\n.header-logo-pro {\n  color: yellow; /* 验证通过后变为黄色 */\n}\n\n/* 弹窗居中样式 */\n.api-key-modal {\n  position: fixed;\n  top: 50%;\n  left: 50%;\n  transform: translate(-50%, -50%);\n  background-color: var(--jp-layout-color1); /* 使用JupyterLab的颜色风格 */\n  padding: 15px;\n  border-radius: 8px;\n  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);\n  z-index: 1000;\n  display: none; /* 初始隐藏 */\n  flex-direction: column;\n  justify-content: space-between;\n  width: 300px;\n}\n\n/* 弹窗头部样式 */\n.modal-header {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  font-size: 14px;\n}\n\n.modal-close {\n  cursor: pointer;\n  font-size: 25px;\n  padding: 0px;\n}\n\n.modal-body {\n  margin-top: 10px;\n}\n.modal-body .modal-body-content{\n  display: flex;\n  align-items: center;\n}\n\n.api-key-input {\n  flex: 1;\n  padding: 0 3px;\n  margin-right: 10px;\n  height: 22px;\n  line-height: 25px;\n}\n\n.verify-button {\n  background-color: var(--jp-brand-color1);\n  color: white;\n  border: none;\n  padding: 4px 16px;\n  cursor: pointer;\n}\n\n.modal-footer {\n  display: flex;\n  justify-content: flex-end;\n  gap: 10px;\n  margin-top: 10px;\n}\n\n.reset-button, .cancel-button, .confirm-button {\n  padding: 4px 16px;\n  border: none;\n  cursor: pointer;\n}\n\n.reset-button:hover, .cancel-button:hover, .confirm-button:hover, .verify-button:hover {\n  background-color: var(--jp-brand-color2); /* Jupyter风格的悬停效果 */\n}\n\n.confirm-button:disabled {\n  background-color: grey;\n  cursor: not-allowed;\n}\n\n/* 验证状态提示 */\n.api-key-status {\n  margin-top: 10px;\n  font-size: 12px;\n  color: var(--jp-brand-color3);\n}\n\n.hidden {\n  display: none;\n}\n\n\n\n\n\n\n.fix-code-button {\n  background-color: #D63A36;\n  color: white;\n  padding: 5px 10px;\n  border: none;\n  cursor: pointer;\n  margin-top: 16px;\n  font-size: 12px;\n}\n\n\n\n/*\n滚动条样式\n*/\n/* 自定义整个滚动条 */\n.com-scroll ::-webkit-scrollbar {\n  width: 8px; /* 设置滚动条的宽度 */\n  height: 8px; /* 设置滚动条的高度 */\n}\n \n/* 自定义滚动条轨道 */\n.com-scroll ::-webkit-scrollbar-track {\n  background: transparent; /* 设置轨道的背景颜色 */\n}\n \n/* 自定义滚动条的滑块（thumb） */\n.com-scroll ::-webkit-scrollbar-thumb {\n  background: var(--jp-ui-font-color3); /* 设置滑块的背景颜色 */\n  border-radius: 4px;/* 设置滚动条的圆角 */\n}\n \n/* 当滑块悬停或活动时，可以添加更多样式 */\n.com-scroll ::-webkit-scrollbar-thumb:hover {\n  background: var(--jp-layout-color2); /* 设置滑块在悬停状态下的背景颜色 */\n}\n\n/*\n输入框鼠标光标颜色设置\n*/\n.chatbot-container .form-control {\n  color: var(--jp-ui-font-color1); /* 光标颜色 */\n}\n\n.chatbot-container .form-control::-webkit-input-placeholder{\n  color: var(--jp-ui-font-color3);\n}\n\n/* @supports (caret-color: #F06123) {\n  .chatbot-container .form-control {\n      color: var(--jp-ui-font-color1); \n      caret-color: #F06123; \n  }\n} */\n\n/* \n    登录容器样式 \n*/\n.smart-programming-button {\n  display: inline-block;\n  background-color: transparent;  \n  color: white;\n  margin-left: 2px;  \n  margin-bottom: 5px;\n  border: none;\n  cursor: pointer;\n  position: relative;\n  top: 0;  \n  left: 0;  \n  z-index: 1000;\n  width: 24px;  /* 缩小按钮宽度 */\n  height: 24px; /* 缩小按钮高度 */\n  padding: 2px; /* 缩小内边距 */\n  font-size: 12px;  \n  border-radius: 4px;  \n}\n\n/* 设置按钮在hover时显示的样式 */\n.smart-programming-button:hover {\n  background-color: rgba(255, 255, 255, 0.2);  \n}\n\n/* 灯泡图标 */\n.smart-programming-button::before {\n  content: '💡';  \n  font-size: 14px;  /* 缩小图标大小 */\n}\n\n/* 在悬停时显示提示框 */\n.smart-programming-button::after {\n  content: 'AI Programming';  \n  display: none;\n  position: absolute;\n  background-color: black;\n  color: white;\n  padding: 3px 5px;\n  font-size: 12px;\n  border-radius: 4px;\n  top: 50%;  \n  left: -100px;  \n  transform: translateY(-50%);  \n  white-space: nowrap;  \n  z-index: 1001;\n}\n\n/* 悬停时显示提示框 */\n.smart-programming-button:hover::after {\n  display: block;\n}\n\n/* 智慧编程下拉按钮组 */\n.smart-buttons {\n  display: flex;\n  justify-content: flex-start; /* 按钮左对齐 */\n  margin-top: 5px;\n  margin-left: 70px; /* 整体右移 */\n}\n\n.smart-buttons button {\n  padding: 5px 10px;\n  margin: 0 5px;\n  cursor: pointer;\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 4px;\n}\n\n.smart-buttons button:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.smart-buttons button:active {\n  background-color: var(--jp-brand-color2);\n}\n\n.input-popup {\n  background-color: transparent;  /* 背景设置为透明，伪装成cell的一部分 */\n  border: none;  /* 去掉边框 */\n  box-shadow: none;  /* 去掉阴影效果 */\n  width: calc(100% - 24px);  /* 占据整个cell的宽度 */\n  padding: 0;\n  display: flex;\n  align-items: center;\n  box-sizing: border-box;\n  padding-left: 72px;\n  padding-top:10px;\n}\n\n.input-field {\n  width: 100%;  /* 确保输入框宽度填满父容器 */\n  padding: 5px;  /* 适当的内边距 */\n  border: none;  /* 默认无边框 */\n  outline: none;  /* 移除默认的聚焦外边框 */\n  background-color: transparent;  /* 透明背景，融入cell */\n  color: inherit;  /* 继承父元素的字体颜色 */\n  font-size: inherit;  /* 继承父元素的字体大小 */\n  box-sizing: border-box;\n}\n\n\n/* 设置占位符颜色为偏白的灰色 */\n.input-field::placeholder {\n  color: #ccc;  /* 偏白的灰色 */\n  opacity: 1;  /* 使占位符颜色不被透明度影响 */\n}\n\n/* 输入框聚焦时的边框效果 */\n.input-field:focus {\n  border: 2px solid #21A2FF;  /* 蓝色边框 */\n  border-radius: 0px;  /* 添加边角圆润效果 */\n  outline: none;  /* 避免默认的蓝色阴影 */\n  box-shadow: 0 0 8px rgba(0, 123, 255, 0.6);  /* 添加蓝色阴影，提升视觉效果 */\n}\n\n\n\n.user-message-display {\n  font-size: 14px;\n  color: #555;\n  margin-bottom: 5px;\n}\n\n\n\n/* 主页面样式 */\n.login-container {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    height: 100%;\n    width: 100%;\n    background: var(--jp-layout-color1);\n    position: relative; /* 确保内部元素相对于容器定位 */\n}\n\n\n/* 欢迎页面 */\n/* 内容样式 */\n.content {\n    position: relative;\n    height: 100vh;\n    width: 100%vw;\n}\n\n\n.login-container-content{\n  height: 100%;\n  overflow: hidden;\n}\n\n.login-container-box{\n  height:100%;\n  overflow: hidden;\n  overflow-y: auto;\n}\n\n.chatbot-container-button{\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding:0px 8px;\n}\n\n.chatbot-container-button button{\n  margin: 0 !important;\n}\n\n/* 动态背景样式 */\n#demo-canvas {\n    position: absolute; /* 绝对定位覆盖整个背景 */\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n    z-index: 0; /* 背景位于文字的下层 */\n    display: block;\n}\n\n/* 大标题和按钮容器 */\n.large-header {\n    display: flex;\n    flex-direction: column;\n    justify-content: center;\n    align-items: center;\n    position: absolute;\n    top: 45%;\n    left: 50%;\n    transform: translate(-50%, -50%);\n    z-index: 2; /* 确保文字位于动态背景之上 */\n    text-align: center;\n    transition: transform 0.8s ease, left 0.8s ease; /* 添加过渡效果 */\n}\n\n/* 主标题样式 */\n.main-title {\n    font-weight: bold;\n    font-size: 40px;\n    color: var(--jp-ui-font-color1);\n    margin-bottom: 20px;\n    z-index: 2;\n}\n\n/* 副标题样式 */\n.sub-title {\n    font-size: 24px;\n    color: var(--jp-ui-font-color1);\n    margin-bottom: 0px;\n    z-index: 2;\n}\n\n/* 说明文字样式 */\n.description {\n    font-size: 18px;\n    color: var(--jp-ui-font-color1);\n    margin-bottom: 30px;\n    z-index: 2;\n}\n\n/* 额外的按钮样式 */\n/* 登录按钮样式 */\n.action-btn {\n    font-size: 18px;\n    color: #f9f1e9;\n    background-color: #007BFF;\n    padding: 10px 20px;\n    border: none;\n    border-radius: 5px;\n    cursor: pointer;\n    z-index: 2;\n    transition: background-color 0.3s ease, transform 0.1s ease; /* 添加过渡效果 */\n}\n\n.action-btn:hover {\n    background-color: #0056b3;\n}\n\n/* 点击效果 */\n.action-btn:active {\n    background-color: #003f7f; /* 改变背景颜色 */\n    transform: scale(0.95); /* 按下时缩小按钮 */\n}\n\n/* 返回按钮样式 */\n.back-btn {\n    font-size: 18px;\n    color: #FFFFFF;\n    background-color: #007BFF;\n    padding: 10px 20px;\n    border: none;\n    border-radius: 5px;\n    cursor: pointer;\n    margin-top: 20px; /* 与二维码和文字的间距 */\n    transition: background-color 0.3s ease, transform 0.1s ease; \n}\n\n.back-btn:hover {\n    background-color: #0056b3;\n}\n\n/* 点击效果 */\n.back-btn:active {\n    background-color: #003f7f; /* 改变背景颜色 */\n    transform: scale(0.95); /* 按下时缩小按钮 */\n}\n\n/* 登录页面的内容 */\n.login-content {\n    display: flex;\n    flex-direction: column;\n    justify-content: center;\n    align-items: center;\n}\n\n/* 登录标题 */\n.login-title {\n    font-size: 24px;\n    color: var(--jp-ui-font-color1);\n    margin-bottom: 20px;\n}\n\n/* 二维码样式 */\n.qr-code {\n    width: 200px;\n    height: 200px;\n    margin-bottom: 5px;\n}\n\n/* 登录说明文字 */\n.login-description {\n    font-size: 18px;\n    color: var(--jp-ui-font-color1);\n}\n.qr_space {\n\tbackground: linear-gradient(90deg, #F06123 0%, #BEB1FC 100%); /* 渐变效果 */\n\t-webkit-background-clip: text; /* 用背景填充文字 */\n\t-webkit-text-fill-color: transparent; /* 将文字颜色设为透明，使渐变效果可见 */\n\tfont-weight: bold; /* 设置加粗 */\n  }\n\n/* 登录页面样式 */\n/* 进入登录页面时，欢迎页面的滑动效果 */\n.large-header.slide-out {\n    transform: translate(-100vw, -50%);\n}\n\n/* 登录页面从屏幕右侧滑入 */\n#login-page {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    height: 100%;\n    width: 100%;\n    position: absolute;\n    top: 50%; /* 设置垂直居中 */\n    left: 100%; /* 初始位置在屏幕外 */\n    transform: translate(-4%, -60%); /* 确保登录页面保持顶部居中 */\n    z-index: 2;\n    text-align: center;\n    transition: left 0.5s ease; /* 设置滑动动画效果 */\n}\n\n#login-page.slide-in {\n    left: 0;\n    transform: translate(-4%, -60%); /* 保持水平居中 */\n}\n\n  \n  /* 二维码容器样式 */\n  #qrcode {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    margin-top: 0;\n    width: 200px;\n    height: 200px;\n    border-radius: 4px;\n    background-color: #f0f0f0;\n    aspect-ratio: 1 / 1;\n    overflow: hidden;\n  }\n  \n  /* 二维码图片样式 */\n  #qrcode img,\n  #qrcode .qrcode-image {\n    width: 100%;\n  }\n  \n  /* 占位符样式 */\n  #qrcode .placeholder {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n  }\n  \n  /* 刷新占位符样式 */\n  .refresh-placeholder {\n    width: 100px;\n    height: 100px;\n    cursor: pointer;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n  }\n  \n  .refresh-placeholder svg {\n    width: 100%;\n    height: 100%;\n    object-fit: contain;\n  }\n\n/* \n主容器样式 \n*/\n.jp-ChatbotWidget {\n  display: flex;\n  height: 100%;\n  font-family: var(--jp-ui-font-family);\n  background-color: var(--background-color);\n  color: var(--text-color);\n  font-size: 14px;\n}\n\n/* 主容器 */\n.chatbot-container {\n  /* display: flex; */\n  position: relative;\n  height: 100%; \n  width: 100%; \n  background-color: var(--background-color);\n}\n\n.chatbox-container-rel{\n  position: relative;\n}\n\n.chatbot-container-box{\n  position: absolute;\n  top: 0;\n  left: 0;\n  width: 100%;\n  height: 100%;\n  background: var(--chatbot-dailog-bg);\n  z-index: 9999;\n  display: none;\n}\n\n.loading {\n  font-size: 14px;\n  color: #757575;\n  text-align: center;\n  margin-top: 20px;\n}\n\n\n.active-session {\n  background-color: #e0f7fa;  /* 高亮颜色 */\n  border-left: 4px solid #00796b;  /* 当前会话的标记 */\n}\n\n/* 当前选中的会话，始终显示三个点按钮 */\n.active-session .more-btn {\n  display: inline-block;  /* 始终显示三个点按钮 */\n}\n\n\n/* 弹窗容器 */\n.popup-container-bg{\n  width: 100%;\n    height: 100%;\n    background-color: rgba(0, 0, 0, 0.2);\n    position: fixed;\n    top: 0;\n    left: 0;\n}\n.popup-container {\n  position: fixed;\n  top: 50%;\n  left: 50%;\n  background: rgba(0, 0, 0, 0.5);\n  display: flex;\n  justify-content: center;\n  z-index: 9999;\n  width: 370px;\n  height: 225px;\n  margin: -114px 0 0 -200px;\n  border: 1px solid var(--jp-border-color2);\n  padding:24px 16px 10px 16px;\n  background-color: var(--jp-layout-color1);\n  border-radius:2px;\n}\n\n.popup-container.hidden {\n  display: none;\n}\n\n.popup-content {\n  width: 100%;\n  position: relative;\n}\n\n.popup-header {\n  position: relative;\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: 10px;\n  padding:8px;\n}\n\n.popup-header span{\n  font-size: 16px;\n  color: var(--jp-ui-font-color1);\n}\n\n.close-button {\n  position: absolute;\n  top:-22px;\n  right:6px;\n  background: none;\n  border: none;\n  font-size: 30px;\n  color: var(--jp-ui-font-color2);\n  cursor: pointer;\n  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */\n}\n\n.close-button:hover{\n  transform: scale(1.2);\n}\n\n.close-button:active{\n  transform: scale(0.95);\n}\n\n.com-btn{\n  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */\n}\n\n.com-btn:hover{\n  transform: scale(1.05);\n}\n\n.com-btn:active{\n  transform: scale(0.95);\n}\n\n.popup-body {\n  margin-bottom: 20px;\n}\n\n.popup-body label {\n  display: block;\n  margin-bottom: 10px;\n  font-size: 16px;\n}\n\n.popup-body input {\n  width: 100%;\n  padding: 8px;\n  margin-bottom: 10px;\n  font-size: 14px;\n  border:1px solid var(--jp-border-color2) !important;\n  border-radius: 5px !important;\n}\n\n.popup-footer-box{\n  position: absolute;\n  left: 0;\n  bottom: 0;\n  width: 100%;\n}\n\n.popup-footer {\n  display: flex;\n  border-top: 1px solid var(--jp-border-color2);\n  padding-top: 10px;\n}\n\n.popup-footer-desc{\n  display: flex;\n  align-items: center;\n  flex:1;\n  color: var(--jp-ui-font-color2);\n  font-size: 12px;\n}\n\n.popup-footer-btns{\n  /* width: 146px; */\n}\n\n.popup-button {\n  padding: 4px 16px;\n  border: none;\n  border-radius: 2px;\n  cursor: pointer;\n  font-size: 14px;\n  margin-left: 10px;\n  background-color: var(--jp-layout-color3);\n  color: var(--jp-ui-font-color1);\n  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */\n}\n.popup-button:hover {\n  transform: scale(1.1); \n}\n.popup-button:active {\n  transform: scale(0.95); \n}\n\n/* 确认按钮样式 */\n.popup-button.confirm {\n  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%);\n  color: var(--jp-ui-font-color1);\n  padding: 4px 16px;\n  border: none;\n  border-radius: 2px;\n  cursor: pointer;\n  font-size: 14px;\n  transition: background-image 0.3s ease; /* 添加渐变的过渡效果 */\n}\n/* 鼠标悬停效果 */\n.popup-button.confirm:hover {\n  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%); /* 悬停时渐变效果变化 */\n}\n\n/* 鼠标点击效果 */\n.popup-button.confirm:active {\n  background-image: linear-gradient(180deg, #D75720 0%, #BDB0F2 100%); /* 点击时渐变效果变化 */\n}\n\n/**/\n.popup-head-radio-group{\n  display: flex;\n  cursor: pointer;\n}\n.popup-head-radio-item{\n  display: flex;\n  flex: 1;\n  padding: 0;\n}\n.popup-head-radio-item label{\n  flex:1;\n  font-size: 14px;\n  color: var(--jp-ui-font-color1);\n  cursor: pointer;\n}\n.popup-head-radio-item .popup-head-radio-input{\n  width: 15px;\n  height: 15px;\n  margin: 0 5px 0 0;\n  cursor: pointer;\n}\n\n.popup-head-select-group{\n  display: flex;\n  align-items: center;\n  padding: 5px 8px;\n}\n\n.popup-head-select-group select{\n  flex:1;\n  width: 100%;\n  height: 30px;\n  background-color: var(--jp-layout-color0);\n  color: var(--jp-layout-font-color0);\n  border-radius: 2px;\n  border: 1px solid var(--jp-border-color2);\n  color: var(--jp-ui-font-color2);\n}\n\n.popup-head-select-group select option{\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  padding: 8px 4px;\n  cursor: pointer;\n}\n.popup-head-select-group select option:hover{\n  background-color: var(--jp-layout-color0);\n}\n\n.popup-head-select-group-reset{\n  position: relative;\n  font-size: 12px;\n  color: var(--jp-ui-font-color1);\n  padding: 0 10px;\n  cursor: pointer;\n  width: 30px;\n}\n\n.popup-head-select-group-reset span{\n  display: none;;\n}\n\n.popup-head-select-group-reset:hover span{\n  display: block;\n  position: absolute;\n  top: -25px;\n  right: -15px;\n  content: \"\";\n  width: 84px;\n  height: 16px;\n  text-align: center;\n  line-height: 16px;\n  color: var(--jp-ui-font-color2);\n  background-color: var(--jp-layout-color2);\n  font-size: 12px;\n  padding: 1px 3px;\n}\n.popup-head-select-group-reset:hover span::before{\n  display: block;\n  position: absolute;\n  top: 15px;\n  right: 35px;\n  content: \"\";\n  width: 5px;\n  height: 5px;\n  background-color: var(--jp-layout-color2);\n  border-left: none;\n  border-bottom: none;\n  transform: rotate(135deg);\n  border-radius: 2px;\n}\n/* 状态信息的样式 */\n#knowledge-status {\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n  font-size: 12px; /* 更小的字体 */\n  color: var(--jp-ui-font-color1);\n  margin-top: 10px;\n  line-height: 16px;\n  padding:0 8px;\n}\n#knowledge-status a{\n  color: #FF8855;\n}\n#knowledge-status a:hover{\n  text-decoration: underline;\n}\n\n/* 侧边栏样式 */\n.sidebar {\n  display: flex;\n  width: 200px;\n  height: calc(100% - 30px);\n  flex-direction: column; /* 垂直排列内容 */\n  background-color: var(--jp-layout-color1);\n  padding: 8px;\n  overflow-y: auto;\n  transition: width 0.3s ease;\n  border-right: 1px solid var(--jp-border-color2);\n}\n\n#session-list {\n  flex-grow: 1; /* 让会话列表填充中间剩余空间 */\n  overflow-y: auto; /* 使其可以滚动 */\n  margin-top: 10px; /* 与\"新建会话\"按钮保持距离 */\n  padding-top: 10px;\n}\n\n.sidebar-hidden {\n  width: 0;\n  padding: 0;\n  overflow: hidden;\n  border-right: none;\n}\n\n.sidebar-button {\n  width: 80%; /* 按钮宽度为80% */\n  padding: 10px;\n  margin: 19px; /* 按钮向下移动，居中对齐 */\n  background-color: var(--send-button-color);\n  color: rgb(255, 255, 255);\n  border: none;\n  border-radius: 4px;\n  cursor: pointer;\n  transition: background-color 0.3s ease;\n  font-size: 18px; /* 增大字体大小 */\n  background-image: linear-gradient(90deg, #f46325 0%, #5a81ff 100%); /* 渐变效果 */\n  transition: background-color 0.5s ease, background-image 0.5s ease; /* 增加过渡时间为0.5s */\n  font-weight: bold; /* 加粗文字 */\n} \n\n.sidebar-button:hover {\n  background-image: linear-gradient(90deg, #F06123 0%, #B18FFC 100%);\n  transition: background-color 0.7s ease, background-image 0.7s ease; /* 鼠标悬停时延长渐变时间 */\n}\n/* 点击效果 */\n.sidebar-button:active {\n  transform: scale(0.98); /* 点击时缩小 */\n}  \n\n.session-item {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 0 5px;\n  margin-bottom: 5px;\n  background-color: var(--jp-layout-color2);\n  border-radius: 4px;\n  cursor: pointer;\n  transition: background-color 0.3s ease;\n  position: relative;\n  color:var(--jp-ui-font-color1);\n  height: 30px;\n  line-height: 30px;\n}\n\n.session-item:hover {\n  background-color:var(--jp-layout-color3)\n}\n\n.session-item>span{\n  font-size: var(--jp-ui-font-size1);\n}\n.fade-effect {\n  position: relative;\n  overflow: hidden;\n  white-space: nowrap;\n  text-overflow: ellipsis; \n}\n\n.fade-effect::after {\n  content: '';\n  position: absolute;\n  right: 0;\n  top: 0;\n  height: 100%;\n  width: 30px;  /* 渐变效果的宽度 */\n  background: linear-gradient(to right, transparent, transparent);  /* 全透明的渐变 */\n}\n\n\n\n/* 当处于编辑状态时的输入框样式 */\n.rename-input {\n  font-size: inherit; /* 确保字体大小一致 */\n  border: 1px solid #ccc;\n  padding: 5px;\n  width: 100%; /* 占据可用空间 */\n  box-sizing: border-box; /* 确保内边距不会改变输入框大小 */\n  background-color: var(--jp-layout-color2);\n  color: var(--jp-ui-font-color1);\n}\n\n\n/* 三个点按钮 */\n/* more-options 容器样式 */\n.more-options {\n  position: relative;\n  display: inline-block;\n}\n\n.more-btn {\n  background: none;\n  border: none;\n  font-size: 18px;\n  cursor: pointer;\n  color: gray;  /* 默认灰色 */\n  display: none;\n}\n\n.session-item:hover .more-btn {\n  display: inline-block;\n}\n\n/* 当鼠标悬停在三个点按钮上时，颜色变为白色 */\n.more-btn:hover {\n  color: white;  /* 悬停时变为白色 */\n}\n\n/* 弹出菜单的样式 */\n.dropdown-menu {\n  position: absolute;  /* 使用 fixed 以脱离侧边栏的限制 */\n  background-color: var(--jp-layout-color1);\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 5px;\n  white-space: nowrap; /* 防止内容换行 */\n  z-index: 100000; /* 确保显示在最前 */\n  padding: 5px 0;\n  width: auto; /* 根据内容自动调整宽度 */\n  display: none; /* 默认隐藏 */\n  top: 25px;\n  right: 15px;\n\n}\n\n/* 确保点击按钮时不会改变布局 */\n.dropdown-menu button {\n  display: block;\n  width: 100%; /* 占满菜单宽度 */\n  padding: 10px 20px; /* 设置内边距让按钮看起来整齐 */\n  background: none; /* 保持背景透明 */\n  color: inherit; /* 继承颜色 */\n  border: none; /* 去掉默认边框 */\n  text-align: left; /* 左对齐文本 */\n  cursor: pointer;\n  font-size: 12px;\n}\n\n/* 鼠标悬停时的背景颜色 */\n.dropdown-menu button:hover {\n  background-color: var(--jp-layout-color2); /* 悬停时设置透明背景 */\n}\n\n/* 显示下拉菜单 */\n.dropdown-menu.show {\n  display: block  /* 确保显示 */\n}\n\n/* 让下拉菜单按钮保持之前的展示效果，并调整为横向排列 */\n.rename-btn, .delete-btn {\n  display: block; /* 确保按钮占据独立的行 */\n  padding: 10px 20px; /* 设置合适的内边距，保证按钮宽度 */\n  background: none; /* 保持背景透明或使用你指定的背景色 */\n  border: none; /* 去掉边框 */\n  text-align: left; /* 文字左对齐 */\n  white-space: nowrap; /* 防止文字换行 */\n  cursor: pointer; /* 鼠标悬停时变为指针 */\n  font-size: 14px; /* 文字大小合适 */\n  color: var(--jp-ui-font-color0); /* 确保文字颜色适配 */\n  width: 100%; /* 让按钮宽度占满整个菜单 */\n}\n\n/* 鼠标悬停时的效果 */\n.rename-btn:hover, .delete-btn:hover {\n  background-color: var(--jp-layout-color2); /* 悬停时背景色 */\n  color: var(--jp-ui-font-color0); /* 悬停时文字颜色 */\n}\n\n/* 聊天区域样式 */\n.chat-area {\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n  background-color: var(--jp-layout-color0);\n}\n\n/* 当侧边栏弹出时，压缩聊天区域 */\n.chat-area.sidebar-open {\n  margin-left: 200px; /* 侧边栏宽度 */\n}\n\n/* 顶部栏样式 */\n.chat-header {\n  display: flex;\n  justify-content: space-between; /* 左侧和右侧对齐 */\n  align-items: center;\n  padding: 10px;\n  background-color: var(--jp-layout-color1);\n  z-index: 1000;\n  height: 10px;\n  border-bottom: 1px solid var(--jp-border-color2);\n}\n\n.chat-header-btn button{\n  margin-right: 10px !important;\n}\n\n/* 顶部按钮样式 */\n.header-button {\n  width: 18px; /* 控制按钮大小 */\n  height: 18px;\n  border: none;\n  cursor: pointer;\n  margin-right: 15px;\n  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */\n}\n\n/* 鼠标悬停效果 */\n.header-button:hover {\n  color: var(--send-button-hover); /* 鼠标悬停时颜色变化 */\n  transform: scale(1.1); /* 放大按钮 */\n}\n\n/* 鼠标点击效果 */\n.header-button:active {\n  transform: scale(0.9); /* 点击时按钮缩小 */\n}\n\n\n/* 导入SVG图标样式 */\n.toggle-sidebar {\n  mask:url('image/open-popup.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/open-popup.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n\n/*侧边导航展开按钮*/\n.toggle-sidebar-open {\n  mask:url('image/x_circle.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/x_circle.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n\n/* API-KEY SVG图标样式 */\n.chat-icon-edit {\n  mask:url('image/icon_edit.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/icon_edit.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n\n/* 退出登录SVG图标样式 */\n.chat-icon-logout {\n  mask:url('image/icon_logout.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/icon_logout.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n\n/*用户图像*/\n.header-button-user{\n  width: 32px;\n  height: 32px;\n  position: relative;\n  background-image: url('image/user_img.svg');\n  background-position: center;\n  background-repeat: no-repeat;\n  background-size: 16px 16px;\n  background-clip: contain;\n  background-color: transparent;\n  margin: 0 0 0 12px;\n}\n\n.header-button-user .header-button-user-block{\n  display: none;\n}\n\n.header-button-user:hover .header-button-user-block{\n  display: block;\n  transition: display 0.3s ease-in-out;\n}\n\n/*鼠标移入用户图像显示*/\n.header-button-user-block{\n  position: absolute;\n  top: 100%;\n  right: 0px;\n  width: 171px;\n  height: 72px;\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 2px;\n  background-color:var(--jp-layout-color1);;\n  padding:14px 5px;\n}\n\n.header-button-user-block ul{\n  list-style: none;\n  padding: 0;\n  margin: 0;\n}\n\n.header-button-user-block ul li{\n  display: flex;\n  align-items: center;\n  justify-content: left;\n  font-size: 12px;\n  color: var(--jp-ui-font-color1);\n  padding:0 0 0 5px;\n  font-weight: normal;\n}\n.header-button-user-block ul li:hover{\n  background-color: var(--jp-layout-color2);\n  transition: backgroundColor 0.3s ease-in-out;\n}\n.header-button-user-block .header-button{\n  margin-right: 5px;\n}\n\n.chat-bg-show{\n  display: block;\n}\n\n/* 顶部文字 */\n.header-logo-text {\n  font-size: 16px; /* \"Powered by\"的字体大小 */\n  color: #ccc; /* \"Powered by\"的字体颜色 */\n  font-weight: normal; /* 设置普通字体 */\n  font-weight: bold; /* 设置加粗 */\n  display: flex;\n  flex:1;\n  align-items: center;\n}\n\n.header-logo-text .header-logo-title{\n  flex: 1;\n  text-align: center;\n  display: flex;\n  justify-content: right;\n  align-items: center;\n  font-size: 11px;\n}\n\n.header-logo-title-span{\n  position: relative;\n  font-size: 11px;\n  border-radius: 1px;\n  color: var(--jp-ui-font-color3);\n  background: var(--jp-layout-color2);\n  padding:2px 18px 2px 6px;\n  height: 16px;\n  line-height: 16px;\n  transition: transform 0.2s ease; /* 鼠标点击的缩放效果 */\n}\n\n.header-logo-title-span::before{\n  width: 6px;\n  height: 6px;\n  content: \"\";\n  position: absolute;\n  top:5px;\n  right:6px;\n  border:1px solid var(--jp-ui-font-color3);\n  border-left: none;\n  border-bottom: none;\n  transform: rotate(45deg);\n}\n.header-logo-title-span:hover{\n  cursor: pointer;\n  background: var(--jp-layout-color3);\n  transform: scale(1.05); /* 放大按钮 */\n}\n.header-logo-title-span:active{\n  transform: scale(0.95); /* 按下时缩小按钮 */\n}\n\n.header-logo-text .header-logo-text-box{\n  flex:1;\n  text-align:right;\n}\n\n.header-logo {\n  font-size: 14px; /* \"MateGen\"的字体大小 */\n  color: #fff; /* \"MateGen\"的字体颜色 */\n  font-weight: bold; /* 设置加粗 */\n  background: linear-gradient(90deg, #F06123 0%, #BEB1FC 100%); /* 渐变效果 */\n  -webkit-background-clip: text; /* 用背景填充文字 */\n  -webkit-text-fill-color: transparent; /* 将文字颜色设为透明，使渐变效果可见 */\n}\n\n/* 二维码和提示文本容器 */\n.qr-code-container {\n  display: flex;\n  flex-direction: column;\n  align-items: center; /* 水平居中 */\n  padding-bottom: 30px; /* 为底部留出一点空间 */\n}\n\n/* 侧边底部二维码样式 */\n.qr-code-in {\n  width: 120px; /* 设置二维码图片宽度 */\n  height: 120px; /* 设置二维码图片高度 */\n  background-image: url('image/xiaokeai.png'); /* 加载二维码图片 */\n  background-size: 110px 110px; /* 确保图片不拉伸，按比例显示 */\n  background-position: center; /* 图片居中显示 */\n  border: 1px solid transparent; /* 为边框留出空间 */\n  background-repeat: no-repeat;\n  border-image: linear-gradient(180deg, #F06123 0%, #BEB1FC 100%) 1; /* 渐变边框 */\n  border-radius: 8px; /* 可选：为边框添加圆角效果 */\n  margin: 15px auto; /* 居中对齐 */\n  margin-bottom: 10px; /* 二维码与文本之间的间距 */\n}\n\n/* 提示文字样式 */\n.qr-code-text {\n  text-align: center; /* 文本居中 */\n  margin: 0;\n  padding: 0 10px; /* 给文字留出一点边距 */\n}\n.qr-code-text p{\n  padding: 3px;\n  margin: 0;\n  font-size: 14px;\n  color: var(--jp-ui-font-color1); /* 或者其他你想要的颜色 */\n}\n\n/* 聊天记录区域样式 */\n#chat-log {\n  display: flex;\n  flex-direction: column;\n  background-color: var(--jp-layout-color0);\n  overflow-y: auto;\n  padding: 20px;\n  height: calc(100% - 40px);\n}\n\n/* 消息通用样式 */\n.message {\n  margin-bottom: 0px;\n  max-width: 100%;\n  padding: 3px 8px;\n  line-height: 1.5;\n  border-radius: 5px;\n  box-shadow: 0 1px 3px var(--jp-layout-color3);\n}\n\n/* 用户消息样式 */\n.user-message {\n  align-self: flex-end;\n  background-color: var(--jp-layout-color2);\n  font-size: 14px;\n  color: var(--jp-ui-font-color1);\n}\n\n/* 机器人消息样式 */\n/* 在现有的CSS中添加或更新以下样式 */\n\n.bot-message {\n  background-color: var(--jp-layout-color0);\n  padding: 10px 5px;\n  border-radius: 8px;\n  margin-bottom: 15px;\n  margin-top: 15px;\n  font-size: 14px;\n  color: var(--jp-ui-font-color1);\n}\n\n.bot-message p {\n  margin:0;\n}\n\n.bot-message h1, .bot-message h2, .bot-message h3, .bot-message h4, .bot-message h5, .bot-message h6 {\n  margin-top: 20px;\n  margin-bottom: 10px;\n  color: #ffffff;\n}\n\n.bot-message ul, .bot-message ol {\n  margin: 10px 0;\n  padding-left: 20px;\n}\n\n.bot-message li {\n  margin-bottom: 5px;\n}\n\n.bot-message code {\n  background-color: var(--jp-layout-color2);\n  padding: 2px 4px;\n  border-radius: 3px;\n  font-family: monospace;\n}\n\n.bot-message pre {\n  background-color: #2b2b2b;\n  padding: 15px;\n  border-radius: 5px;\n  overflow-x: auto;\n}\n\n.bot-message pre code {\n  background-color: transparent;\n  padding: 0;\n  color: var(--jp-ui-font-color0);\n  text-shadow: none;\n}\n\n.bot-message blockquote {\n  border-left: 4px solid #10a37f;\n  padding-left: 10px;\n  margin: 10px 0;\n  color: #a0a0a0;\n}\n\n.bot-message img {\n  max-width: 100%;\n  height: auto;\n}\n\n.bot-message table {\n  border-collapse: collapse;\n  width: 100%;\n  margin: 15px 0;\n}\n\n.bot-message th, .bot-message td {\n  border: 1px solid #565869;\n  padding: 8px;\n  text-align: left;\n}\n\n.bot-message th {\n  background-color: #2b2b2b;\n}\n\n.highlighted-code {\n  background-color: #2b2b2b;\n  display: block;\n  padding: 10px;\n  border-radius: 5px;\n  font-family: monospace;\n  white-space: pre-wrap;\n  word-break: break-all;\n}\n\n/* 错误消息样式 */\n.error-message {\n  align-self: center;\n  background-color: #ff4d4f;\n  color: white;\n}\n\n/* 输入区域样式 */\n.chat-input {\n  display: flex;\n  padding: 0;\n  background-color: var(--jp-layout-color1); /* 为输入区域添加背景色 */\n  align-items: center; /* 垂直方向居中 */\n  justify-content: flex-start; /* 水平方向从左到右排列 */\n  margin: 0 24px 24px 24px; /* 设置上方外边距为 0px，底部外边距为 15px */\n  position: relative; /* 为左侧和右侧按钮提供定位依据 */\n}\n\n.chat-input .input-wrapper {\n  flex: 1;\n  display: flex;\n  position: relative; /* 为绝对定位的按钮做准备 */\n  align-items: center; /* 垂直居中对齐所有子元素 */\n}\n\n\n.chat-input textarea {\n  height: 14px; /* 设置固定的初始高度 */\n  min-height: 32px; /* 确保最小高度也是 14px */\n  max-height: 150px; /* 保持最大高度限制 */\n  padding: 0; /* 调整内边距以适应较小的高度 */\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 2px;\n  font-size: 14px;\n  background-color: var(--neutral-fill-input-rest);\n  color: var(--jp-ui-font-color0);\n  resize: none;\n  overflow-y: auto;\n  transition: border-color 0.3s, box-shadow 0.3s, height 0.1s;\n  box-sizing: border-box; /* 确保padding不会增加总高度 */\n  line-height: 18px; \n  padding:5px 45px 5px 5px;\n  width: 100%;\n}\n\n.chat-input textarea:focus {\n  outline: none;\n  border-color: var(--jp-brand-color1);\n}\n\n.chat-input textarea::placeholder {\n  color: var(--jp-ui-font-color3);\n}\n\n.chat-input .send-button {\n  position: absolute;\n  right: 15px;\n  bottom: -8px; /* 垂直居中 */\n  transform: translateY(-50%); /* 精确垂直居中 */\n  color: white;\n  border: none;\n  border-radius: 50%;\n  width: 25px;\n  height: 25px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n  background-color: transparent;\n  transition: background-color 0.3s, transform 0.2s;\n  background-image: url('image/send_botton.svg');\n  background-size: 25px 15px;\n  background-position: center;\n  background-repeat: no-repeat;\n  opacity: 0; /* 初始不显示 */\n  transform: translateY(-50%) scale(0.8);\n}\n\n.chat-input textarea:not(:placeholder-shown) + button:not(.knowledge-base-button) {\n  opacity: 1;\n  transform: translateY(-50%) scale(1);\n}\n\n/* .chatbot-container-box button:not(.knowledge-base-button):hover {\n  background-color: var(--send-button-hover);\n  transform: translateY(-50%) scale(1.1);\n} */\n\n.chatbot-container-box button::before {\n  content: none; /* 使用Unicode箭头作为发送图标 */\n  font-size: 16px;\n}\n\n/* 输入框左侧的按钮（始终显示） */\n.knowledge-base-button {\n  width: 18px;\n  height: 18px;\n  border: none;\n  cursor: pointer;\n  margin-right: 10px; /* 确保按钮和输入框之间有间距 */\n  z-index: 1; /* 确保层级较高，不被覆盖 */\n  mask:url('image/toggle-sidebar.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/toggle-sidebar.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n/* .chat-input .knowledge-base-button:hover {\n  transform: scale(1.1);\n}\n\n.chat-input .knowledge-base-button:active {\n  transform: scale(0.98);\n} */\n\n\n.new-welcome-base-button {\n  width: 14px;\n  height: 14px;\n  border: none;\n  cursor: pointer;\n  margin-right: 10px; /* 确保按钮和输入框之间有间距 */\n  z-index: 1; /* 确保层级较高，不被覆盖 */\n  mask:url('image/new_welcome.svg') no-repeat 50% 50%;\n  -webkit-mask:url('image/new_welcome.svg') no-repeat 50% 50%;\n  mask-size: contain;\n  -webkit-mask-size:contain;\n  background-color:var(--jp-ui-font-color1);\n}\n\n.new-star-left{\n  position: absolute;\n  background-color: transparent;\n  border: none;\n  cursor: pointer;\n  background-size: cover;\n  background-position: center;\n  margin-right: 10px; /* 确保按钮和输入框之间有间距 */\n  z-index: 1; /* 确保层级较高，不被覆盖 */\n}\n\n.new-chatbot-edit{\n  top:15px;\n  left: 84px;\n  width: 23px;\n  height: 21px;\n  background-image: url('image/new_chatbot_edit.svg'); /* 替换为你的图标 */\n}\n\n.new-chatbot-resp{\n  top:10px;\n  left: 82px;\n  width: 32px;\n  height: 32px;\n  background-image: url('image/new_chatbot_resp.svg'); /* 替换为你的图标 */\n}\n\n/* 聊天机器人容器样式 */\n/* 更新代码框样式 */\n.jp-ChatbotWidget .code-wrapper {\n  margin: 10px 0;\n  border-radius: 6px;\n  overflow: hidden;\n  background-color: #0D0D0D;  /* 深色背景 */\n}\n\n.jp-ChatbotWidget .code-header {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 4px 12px;\n  background-color: var(--jp-layout-color2);\n  color: var(--jp-ui-font-color1);\n}\n\n.jp-ChatbotWidget .code-language {\n  font-family: monospace;\n  font-size: 1.1em;\n}\n\n/* 新增代码换行 */\n.jp-ChatbotWidget .code-wrapper pre {\n  white-space: pre-wrap;  /* 自动换行 */\n  word-wrap: break-word;  /* 处理长单词的换行 */\n  overflow-wrap: break-word; /* 处理长单词的换行 */\n  max-width: 100%;  /* 限制代码块的最大宽度 */\n  box-sizing: border-box;  /* 确保宽度计算包含内边距和边框 */\n}\n\n.jp-ChatbotWidget .code-wrapper code {\n  white-space: pre-wrap;  /* 自动换行 */\n  word-wrap: break-word;\n  overflow-wrap: break-word;\n  max-width: 100%;\n  font-size: 1.1em;\n}\n\n.jp-ChatbotWidget .copy-button {\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  border: none;\n  padding: 4px 8px;\n  border-radius: 4px;\n  cursor: pointer;\n  font-size: 0.8em;\n  transition: background-color 0.3s;\n}\n\n.jp-ChatbotWidget .copy-button:hover {\n  background-color: #5a5a5a;\n}\n\n.jp-ChatbotWidget pre {\n  margin: 0;\n  padding: 12px;\n  background-color: var(--jp-layout-color1);  /* 与 code-wrapper 背景色一致 */\n  border:1px solid var(--jp-border-color3);\n}\n\n.jp-ChatbotWidget code {\n  font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;\n  font-size: 0.9em;\n  line-height: 1.5;\n  color: var(--jp-ui-font-color1);\n}\n\n/* 覆盖 Prism.js 的一些样式 */\n.jp-ChatbotWidget .token.comment,\n.jp-ChatbotWidget .token.prolog,\n.jp-ChatbotWidget .token.doctype,\n.jp-ChatbotWidget .token.cdata {\n  color: #8292a2;\n}\n\n.jp-ChatbotWidget .token.punctuation {\n  color: var(--jp-ui-font-color2);\n}\n\n.jp-ChatbotWidget .token.namespace {\n  opacity: .7;\n}\n\n.jp-ChatbotWidget .token.property,\n.jp-ChatbotWidget .token.tag,\n.jp-ChatbotWidget .token.constant,\n.jp-ChatbotWidget .token.symbol,\n.jp-ChatbotWidget .token.deleted {\n  color: #f92672;\n}\n\n.jp-ChatbotWidget .token.boolean,\n.jp-ChatbotWidget .token.number {\n  color: #ae81ff;\n}\n\n.jp-ChatbotWidget .token.selector,\n.jp-ChatbotWidget .token.attr-name,\n.jp-ChatbotWidget .token.string,\n.jp-ChatbotWidget .token.char,\n.jp-ChatbotWidget .token.builtin,\n.jp-ChatbotWidget .token.inserted {\n  color: #a6e22e;\n}\n\n.jp-ChatbotWidget .token.operator,\n.jp-ChatbotWidget .token.entity,\n.jp-ChatbotWidget .token.url,\n.jp-ChatbotWidget .language-css .token.string,\n.jp-ChatbotWidget .style .token.string,\n.jp-ChatbotWidget .token.variable {\n  color: #f8f8f2;\n}\n\n.jp-ChatbotWidget .token.atrule,\n.jp-ChatbotWidget .token.attr-value,\n.jp-ChatbotWidget .token.function,\n.jp-ChatbotWidget .token.class-name {\n  color: #e6db74;\n}\n\n.jp-ChatbotWidget .token.keyword {\n  color: #66d9ef;\n}\n\n.jp-ChatbotWidget .token.regex,\n.jp-ChatbotWidget .token.important {\n  color: #fd971f;\n}\n\n.delete-session {\n  background: none;\n  border: none;\n  color: #ff4d4f;\n  cursor: pointer;\n  font-size: 16px;\n  padding: 5px;\n  opacity: 0;\n  transition: opacity 0.3s ease;\n}\n\n.session-item:hover .delete-session {\n  opacity: 1;\n}\n\n.delete-session:hover {\n  color: #ff7875;\n}\n\n/* 添加过渡效果 */\n.chatbot-container, .login-container {\n  transition: opacity 0.3s ease-in-out;\n}\n\n/* 默认居中效果 */\n.chatbot-body{\n  position:absolute;\n  top:50%;\n  left:50%;\n  width:430px;\n  height:180px;\n  margin:-86px 0 0 -215px;\n}\n.chatbot-body-header{\n  width: 340px;\n  height:70px;\n  background-color: transparent;\n  background-size: 340px 70px; /* 控制图标大小 */\n  background-image: url('image/MateGenAir.svg'); /* 读取图标 */\n  background-repeat: no-repeat;\n  background-position: center;\n  background-origin: border-box;\n  background-clip: content-box, border-box;\n  margin: -100px auto 50px auto;\n}\n.chatbot-body-content{\n  display:flex;\n}\n.chatbot-content-item{\n  flex:1;\n  height:inherit;\n  margin: 24px 12px;\n  padding:0;\n  cursor: pointer;\n  border-radius: 8px;\n  box-sizing: border-box;\n  border: 1px solid transparent;\n  background-image: linear-gradient(var(--jp-layout-color1), var(--jp-layout-color1)), linear-gradient(180deg, rgba(240, 97, 35, 0.6) 0%, rgba(190, 177, 252, 0.6) 100%);\n  border-radius: 8px;\n  background-origin: border-box;\n  background-clip: content-box, border-box;\n  border-radius: 2px;\n  text-align: center;\n}\n\n.chatbot-content-item p{\n  line-height:26px;\n  font-size:12px;\n  color: var(--jp-ui-font-color0);\n  padding:0 12px 12px 12px;\n  margin: 0;\n}\n\n.chatbot-content-item-title{\n  position: relative;\n  font-size:16px;\n  font-weight: 600;\n  padding: 50px 12px 5px 12px;\n  margin: 0;\n  color: var(--jp-ui-font-color0);\n}\n\n.session-name{\n  width: 170px; /* 设置容器宽度 */\n  white-space: nowrap; /* 防止文本换行 */\n  overflow: hidden; /* 隐藏超出容器的文本 */\n  text-overflow: ellipsis; /* 超出部分显示为省略号 */\n  word-break: break-all;\n  word-wrap: break-word;\n}\n\n.chat-hide{\n  display: none !important;\n}\n\n.chat-show{\n  display: block;\n}\n\n.chat-show-flex{\n  display: flex;\n}\n\n/* 重置样式 */\n.jp-OutputArea-child .jp-OutputArea-output{\n  padding:5px 12px 16px 12px;\n}\n\n/*消息提示*/\n.chat-message-box{\n  position: absolute;\n  top:10px;\n  left:50%;\n  width: 250px;\n  margin: 0 0 0 -125px;\n  z-index: 9999;\n}\n.chat-message-box span{\n  width: 100%;\n  height: 25px;\n  background: #e79c38;\n  color: #fff;\n  padding: 0 10px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: 5px;\n  font-size: 12px;\n}\n\n/*自定义select*/\n.popup-select-box{\n  position:relative;\n  width:100%;\n  height:30px;\n}\n.popup-select-body{\n  position:absolute;\n  top:34px;\n  left:0;\n  border-color: transparent;\n  width: 100%;\n  max-height: 0px;\n  overflow-y: auto;\n  z-index: 999;\n  background-color: var(--jp-layout-color1);\n  transition: max-height 0.3s ease, transform 0.1s ease, borderColor 0.1s ease; /* 添加过渡效果 */\n  border-radius: 5px;\n}\n.popup-select-box::before{\n  content: \"\";\n  position: absolute;\n  right: 6px;\n  top: 12px;\n  width: 8px;\n  height: 8px;\n  border: 1px solid var(--jp-border-color2);\n  transform: rotate(45deg);\n  border-top: none;\n  border-right: none;\n  transition: transform 0.1s ease, right 0.1s ease;\n}\n.popup-select-box-show::before{\n  transform: rotate(-45deg);\n  right: 10px;\n  transition: transform 0.1s ease, right 0.1s ease;\n}\n.popup-select-input{\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  width: calc(100% - 16px) !important;\n  cursor: pointer;\n}\n.popup-select-input:active,.popup-select-input:focus{\n  outline: none;\n  border-color: var(--jp-brand-color1);\n}\n.popup-select-body ul{\n  list-style: none;\n  padding: 0;\n  margin: 0;\n  border-radius: 5px;\n}\n.popup-select-body ul li{\n  height: 30px;;\n  line-height: 30px;\n  padding:0 10px;\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  cursor: pointer;\n}\n.popup-select-body ul li:hover{\n  background-color: var(--jp-brand-color1);\n  color: var(--jp-ui-font-color0);\n}\n.popup-select-show{\n  max-height: 160px;\n  border:1px solid var(--jp-border-color2);\n  transition: max-height 0.3s ease, transform 0.1s ease, border-color 0.1s ease; /* 添加过渡效果 */\n}\n\n/*自定义知识库*/\n.popup-select-file{\n  display: flex;\n  padding:10px 0;\n}\n\n.popup-select-file-box{\n  display: flex;\n  color: var(--jp-ui-font-color1);\n}\n.popup-select-file-label,.popup-select-file-name{\n  padding:4px;\n}\n.popup-select-file-btn{\n  width: 72px;\n  border: 1px solid var(--jp-border-color2);\n  text-align: center;\n  padding: 4px 16px;\n  border-radius: 3px;\n  cursor: pointer;\n}\n.popup-select-file-btn:hover{\n  background-color: var(--jp-layout-color2);\n}\n\n@media (max-width: 768px) {\n  /* 只保留 message 的 max-width 设置 */\n  .message {\n    max-width: 100%;\n  }\n}\n  \n/* 颜色变量 */\n:root {\n  --background-color: #00283F;\n  --header-color: #00324F;\n  --user-message-color: #094060;\n  --bot-message-color: #012A43;\n  --text-color: #ececf1;\n  --border-color: #504E50;\n  --input-background: #031926;\n  --send-button-color: #083550;\n  --send-button-hover: #00283F;\n  --scrollbar-thumb:#333333;;\n  --scrollbar-thumb-hover:#212121;;\n  --chatbot-dailog-bg:rgba(0,0,0,0.25);\n  --sidebar-background:rgba(255,255,255,0.05);\n  --sidebar-background-hover:rgba(255,255,255,0.1);\n  --sidebar-color:#BDBDBD;\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/image/xiaokeai.png":
/*!**********************************!*\
  !*** ./style/image/xiaokeai.png ***!
  \**********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "461345dc5a8be18c202d.png";

/***/ }),

/***/ "./style/image/MateGenAir.svg?0302":
/*!************************************!*\
  !*** ./style/image/MateGenAir.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='253' height='51' viewBox='0 0 253 51'%3e%3cdefs%3e%3cfilter id='master_svg0_211_19161' filterUnits='objectBoundingBox' color-interpolation-filters='sRGB' x='0' y='0' width='253' height='51'%3e%3cfeFlood flood-opacity='0' result='BackgroundImageFix'/%3e%3cfeColorMatrix in='SourceAlpha' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0'/%3e%3cfeOffset dy='3' dx='0'/%3e%3cfeGaussianBlur stdDeviation='0'/%3e%3cfeColorMatrix type='matrix' values='0 0 0 0 0.065476194024086 0 0 0 0 0.008691529743373394 0 0 0 0 0.008691529743373394 0 0 0 0.7400000095367432 0'/%3e%3cfeBlend mode='normal' in2='BackgroundImageFix' result='effect1_dropShadow'/%3e%3cfeBlend mode='normal' in='SourceGraphic' in2='effect1_dropShadow' result='shape'/%3e%3c/filter%3e%3clinearGradient x1='-15.048326030373573' y1='20.999998569488525' x2='284.97769045829773' y2='59.333330154418945' gradientUnits='userSpaceOnUse' id='master_svg1_75_3289'%3e%3cstop offset='3.57142873108387%25' stop-color='%23F06123' stop-opacity='1'/%3e%3cstop offset='46.50000035762787%25' stop-color='%23BEB1FC' stop-opacity='1'/%3e%3cstop offset='100%25' stop-color='%23F06123' stop-opacity='1'/%3e%3c/linearGradient%3e%3c/defs%3e%3cg filter='url(%23master_svg0_211_19161)'%3e%3cpath d='M10.6%2c39.84Q10.6%2c27.68%2c10.48%2c24.52Q10.92%2c25.96%2c14.52%2c35L20.64%2c35Q22.2%2c30.76%2c23.04%2c28.56Q24.48%2c24.6%2c24.52%2c24.48Q24.36%2c29.92%2c24.36%2c39.84L33.28%2c39.84L33.28%2c16.2L20.52%2c16.2Q18.68%2c21.8%2c17.6%2c27Q17.36%2c25.88%2c16.54%2c22.9Q15.72%2c19.92%2c14.48%2c16.2L1.64%2c16.2L1.64%2c39.84L10.6%2c39.84ZM54.16%2c40.16Q56.92%2c40.16%2c58.48%2c39.52L58.48%2c34.32Q58.08%2c34.56%2c57.32%2c34.56Q56.56%2c34.56%2c56.28%2c33.96Q56.04%2c33.52%2c56.04%2c32.2L56.08%2c30.96L56.08%2c29.44Q56.08%2c27.68%2c55.6%2c26.68Q55.04%2c25.64%2c54.08%2c24.96Q51.72%2c23.44%2c46.88%2c23.44Q44.48%2c23.44%2c42.16%2c23.88Q39.44%2c24.52%2c38.12%2c25.24L38.12%2c30.6L38.24%2c30.6Q41.2%2c28.84%2c45.08%2c28.84Q46.76%2c28.84%2c47.4%2c29.36Q47.88%2c29.64%2c47.88%2c30.44L47.88%2c30.72Q46.28%2c30.44%2c45.56%2c30.44Q42.64%2c30.44%2c40.6%2c30.92Q38.64%2c31.44%2c37.56%2c32.4Q36.28%2c33.44%2c36.28%2c35.28Q36.28%2c37.8%2c38.2%2c39Q40.08%2c40.2%2c43.36%2c40.2Q45.04%2c40.2%2c46.36%2c39.76Q48.08%2c39.16%2c48.8%2c38.36Q49.12%2c38.76%2c49.62%2c39.06Q50.12%2c39.36%2c51%2c39.68Q52.32%2c40.16%2c54.16%2c40.16ZM47.88%2c33.96Q47.88%2c34.56%2c47.92%2c34.94Q47.96%2c35.32%2c47.96%2c35.52Q47.32%2c36.24%2c45.96%2c36.24Q44.12%2c36.24%2c44.12%2c35.08Q44.12%2c34.28%2c45.2%2c34Q46.2%2c33.8%2c46.76%2c33.8Q47.72%2c33.8%2c47.88%2c33.96ZM69.6%2c40.08Q72.68%2c40.08%2c74.16%2c39.2L74.16%2c33.84L73.96%2c33.84Q73.4%2c34.2%2c72.2%2c34.2Q71.32%2c34.2%2c70.8%2c33.68Q70.48%2c33.2%2c70.48%2c32L70.48%2c27.64L73.56%2c27.64L73.56%2c22.88L70.48%2c22.88L70.48%2c18L63.64%2c18Q63.64%2c19.84%2c63.56%2c21.26Q63.48%2c22.68%2c63.48%2c22.88L61.28%2c22.88L61.28%2c27.64L63.36%2c27.64L63.36%2c33.88Q63.36%2c35.44%2c63.68%2c36.52Q64%2c37.6%2c64.72%2c38.36Q66.2%2c40.08%2c69.6%2c40.08ZM88.56%2c40.96Q93.96%2c40.96%2c97.24%2c39.2L97.24%2c33.6L97.08%2c33.6Q94.16%2c35.12%2c90.12%2c35.12Q87.84%2c35.12%2c86.88%2c34.68Q85.68%2c34.32%2c85.28%2c33.04L98.16%2c33.04Q98.32%2c32.08%2c98.32%2c30.84Q98.24%2c26.64%2c95.56%2c24.56Q92.96%2c22.52%2c88.24%2c22.52Q83.04%2c22.52%2c80.08%2c24.96Q76.96%2c27.24%2c76.96%2c31.8Q76.96%2c36.32%2c79.96%2c38.6Q82.88%2c40.96%2c88.56%2c40.96ZM90.96%2c29.68L85.28%2c29.68Q85.92%2c27.56%2c88.36%2c27.56Q89.56%2c27.56%2c90.2%2c28.08Q90.96%2c28.64%2c90.96%2c29.48L90.96%2c29.68ZM124.44%2c40.12Q127.84%2c39.36%2c129.44%2c38.4L129.44%2c25.96L116.6%2c25.96L116.6%2c32L120.48%2c32L120.48%2c33.24Q120.04%2c33.56%2c118.56%2c33.56Q115.36%2c33.56%2c113.36%2c32.28Q111.24%2c30.92%2c111.24%2c28.08Q111.24%2c25.44%2c113.14%2c24.1Q115.04%2c22.76%2c118.72%2c22.76Q121.32%2c22.76%2c123.8%2c23.44Q126.68%2c24.2%2c127.92%2c25.2L128.08%2c25.2L128.08%2c17.4Q126.44%2c16.32%2c123.92%2c15.8Q121.08%2c15.16%2c117.4%2c15.16Q113.12%2c15.16%2c109.4%2c16.64Q105.96%2c17.88%2c103.52%2c20.92Q101.32%2c23.96%2c101.32%2c27.96Q101.32%2c34.04%2c105.8%2c37.48Q110.16%2c40.88%2c117.16%2c40.88Q121.12%2c40.88%2c124.44%2c40.12ZM144.04%2c40.96Q149.44%2c40.96%2c152.72%2c39.2L152.72%2c33.6L152.56%2c33.6Q149.64%2c35.12%2c145.6%2c35.12Q143.32%2c35.12%2c142.36%2c34.68Q141.16%2c34.32%2c140.76%2c33.04L153.64%2c33.04Q153.8%2c32.08%2c153.8%2c30.84Q153.72%2c26.64%2c151.04%2c24.56Q148.44%2c22.52%2c143.72%2c22.52Q138.52%2c22.52%2c135.56%2c24.96Q132.44%2c27.24%2c132.44%2c31.8Q132.44%2c36.32%2c135.44%2c38.6Q138.36%2c40.96%2c144.04%2c40.96ZM146.44%2c29.68L140.76%2c29.68Q141.4%2c27.56%2c143.84%2c27.56Q145.04%2c27.56%2c145.68%2c28.08Q146.44%2c28.64%2c146.44%2c29.48L146.44%2c29.68ZM164.92%2c40L164.92%2c29.96Q165.68%2c28.6%2c167.48%2c28.6Q168.68%2c28.6%2c169.28%2c29.44Q169.48%2c29.64%2c169.48%2c31.08L169.48%2c40L177.88%2c40L177.88%2c29.32Q177.88%2c27.2%2c177.44%2c26.16Q176.28%2c23.04%2c170.96%2c23.04Q169%2c23.04%2c167.28%2c23.72Q165.56%2c24.48%2c164.68%2c25.84L164.68%2c23.36L156.6%2c23.36L156.6%2c40L164.92%2c40ZM203.16%2c39.84L205.28%2c35.36L213.16%2c35.36L215.32%2c39.84L225.76%2c39.84L214.12%2c16.2L204.48%2c16.2L192.88%2c39.84L203.16%2c39.84ZM207.52%2c28.76Q208%2c27.56%2c208.12%2c27.2Q209%2c25.16%2c209.04%2c24.88Q209.36%2c25.8%2c210.76%2c28.76L207.52%2c28.76ZM234.88%2c21.64Q235.84%2c20.72%2c235.84%2c19.4Q235.84%2c17.88%2c234.76%2c17.24Q233.76%2c16.44%2c232.32%2c16.44Q231%2c16.44%2c229.88%2c17.24Q228.8%2c17.92%2c228.8%2c19.4Q228.8%2c20.76%2c229.8%2c21.64Q230.8%2c22.4%2c232.32%2c22.4Q233.96%2c22.4%2c234.88%2c21.64ZM235.88%2c40L235.88%2c23.44L228.76%2c23.44L228.76%2c40L235.88%2c40ZM245.68%2c40.08L245.68%2c31.12Q245.84%2c30.04%2c246.66%2c29.48Q247.48%2c28.92%2c248.92%2c28.92Q250.44%2c28.92%2c251.44%2c29.48L251.56%2c29.48L251.56%2c23.48Q251%2c23.08%2c249.52%2c23.08Q247.88%2c23.08%2c246.84%2c24Q245.84%2c24.92%2c245.44%2c26.12L245.44%2c23.44L238.68%2c23.44L238.68%2c40.08L245.68%2c40.08Z' fill='url(%23master_svg1_75_3289)' fill-opacity='1'/%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/icon_edit.svg":
/*!***********************************!*\
  !*** ./style/image/icon_edit.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='16' height='16' viewBox='0 0 16 16'%3e%3cdefs%3e%3cclipPath id='master_svg0_211_3776'%3e%3crect x='0' y='0' width='16' height='16' rx='0'/%3e%3c/clipPath%3e%3c/defs%3e%3cg clip-path='url(%23master_svg0_211_3776)'%3e%3cg%3e%3cpath d='M5.66650390625%2c4.06650390625L9.66650390625%2c4.06650390625Q9.725593906250001%2c4.06650390625%2c9.783553906249999%2c4.07803290625Q9.84151390625%2c4.08956190625%2c9.896113906250001%2c4.11217590625Q9.95071390625%2c4.13479090625%2c9.99984390625%2c4.16762190625Q10.048983906250001%2c4.20045390625%2c10.09076390625%2c4.24223990625Q10.13255390625%2c4.28402590625%2c10.16538390625%2c4.33316190625Q10.19821390625%2c4.38229690625%2c10.22083390625%2c4.43689390625Q10.24344390625%2c4.49148990625%2c10.254973906250001%2c4.54944990625Q10.26650390625%2c4.6074091062499996%2c10.26650390625%2c4.66650390625Q10.26650390625%2c4.7255987062500004%2c10.254973906250001%2c4.78355790625Q10.24344390625%2c4.84151790625%2c10.22083390625%2c4.89611390625Q10.19821390625%2c4.95071090625%2c10.16538390625%2c4.99984590625Q10.13255390625%2c5.04898190625%2c10.09076390625%2c5.09076790625Q10.048983906250001%2c5.13255390625%2c9.99984390625%2c5.16538590625Q9.95071390625%2c5.19821690625%2c9.896113906250001%2c5.22083190625Q9.84151390625%2c5.24344590625%2c9.783553906249999%2c5.25497490625Q9.725593906250001%2c5.26650390625%2c9.66650390625%2c5.26650390625L5.66650390625%2c5.26650390625Q5.6074091062499996%2c5.26650390625%2c5.54944990625%2c5.25497490625Q5.49148990625%2c5.24344590625%2c5.43689390625%2c5.22083190625Q5.38229690625%2c5.19821690625%2c5.33316190625%2c5.16538590625Q5.28402590625%2c5.13255390625%2c5.24223990625%2c5.09076790625Q5.20045390625%2c5.04898190625%2c5.16762190625%2c4.99984590625Q5.13479090625%2c4.95071090625%2c5.11217590625%2c4.89611390625Q5.08956190625%2c4.84151790625%2c5.07803290625%2c4.78355790625Q5.06650390625%2c4.7255987062500004%2c5.06650390625%2c4.66650390625Q5.06650390625%2c4.6074091062499996%2c5.07803290625%2c4.54944990625Q5.08956190625%2c4.49148990625%2c5.11217590625%2c4.43689390625Q5.13479090625%2c4.38229690625%2c5.16762190625%2c4.33316190625Q5.20045390625%2c4.28402590625%2c5.24223990625%2c4.24223990625Q5.28402590625%2c4.20045390625%2c5.33316190625%2c4.16762190625Q5.38229690625%2c4.13479090625%2c5.43689390625%2c4.11217590625Q5.49148990625%2c4.08956190625%2c5.54944990625%2c4.07803290625Q5.6074091062499996%2c4.06650390625%2c5.66650390625%2c4.06650390625Z' fill-rule='evenodd' fill='%23BDBDBD' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M7.06650390625%2c5Q7.06650390625%2c4.9409051999999996%2c7.07803290625%2c4.882946Q7.08956190625%2c4.824986%2c7.11217590625%2c4.77039Q7.13479090625%2c4.715793%2c7.16762190625%2c4.666658Q7.20045390625%2c4.617522%2c7.24223990625%2c4.575736Q7.28402590625%2c4.53395%2c7.33316190625%2c4.501118Q7.38229690625%2c4.468287%2c7.43689390625%2c4.445672Q7.49148990625%2c4.423058%2c7.54944990625%2c4.411529Q7.6074091062499996%2c4.4%2c7.66650390625%2c4.4Q7.7255987062500004%2c4.4%2c7.78355790625%2c4.411529Q7.84151790625%2c4.423058%2c7.89611390625%2c4.445672Q7.95071090625%2c4.468287%2c7.99984590625%2c4.501118Q8.04898190625%2c4.53395%2c8.09076790625%2c4.575736Q8.13255390625%2c4.617522%2c8.16538590625%2c4.666658Q8.19821690625%2c4.715793%2c8.22083190625%2c4.77039Q8.24344590625%2c4.824986%2c8.25497490625%2c4.882946Q8.26650390625%2c4.9409051999999996%2c8.26650390625%2c5L8.26650390625%2c9.3Q8.26650390625%2c9.35909%2c8.25497490625%2c9.41705Q8.24344590625%2c9.475010000000001%2c8.22083190625%2c9.52961Q8.19821690625%2c9.584209999999999%2c8.16538590625%2c9.63334Q8.13255390625%2c9.68248%2c8.09076790625%2c9.724260000000001Q8.04898190625%2c9.76605%2c7.99984590625%2c9.79888Q7.95071090625%2c9.831710000000001%2c7.89611390625%2c9.854330000000001Q7.84151790625%2c9.876940000000001%2c7.78355790625%2c9.88847Q7.7255987062500004%2c9.9%2c7.66650390625%2c9.9Q7.6074091062499996%2c9.9%2c7.54944990625%2c9.88847Q7.49148990625%2c9.876940000000001%2c7.43689390625%2c9.854330000000001Q7.38229690625%2c9.831710000000001%2c7.33316190625%2c9.79888Q7.28402590625%2c9.76605%2c7.24223990625%2c9.724260000000001Q7.20045390625%2c9.68248%2c7.16762190625%2c9.63334Q7.13479090625%2c9.584209999999999%2c7.11217590625%2c9.52961Q7.08956190625%2c9.475010000000001%2c7.07803290625%2c9.41705Q7.06650390625%2c9.35909%2c7.06650390625%2c9.3L7.06650390625%2c5Z' fill-rule='evenodd' fill='%23BDBDBD' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M13.4%2c2.31515290625L13.4%2c5.46651390625Q13.4%2c5.525613906249999%2c13.4115%2c5.58356390625Q13.4231%2c5.641523906250001%2c13.4457%2c5.69612390625Q13.4683%2c5.75072390625%2c13.5011%2c5.79985390625Q13.5339%2c5.84899390625%2c13.5757%2c5.89077390625Q13.6175%2c5.93256390625%2c13.6667%2c5.96539390625Q13.7158%2c5.99822390625%2c13.7704%2c6.02084390625Q13.825%2c6.04345390625%2c13.8829%2c6.05498390625Q13.9409%2c6.06651390625%2c14%2c6.06651390625Q14.0591%2c6.06651390625%2c14.1171%2c6.05498390625Q14.175%2c6.04345390625%2c14.2296%2c6.02084390625Q14.2842%2c5.99822390625%2c14.3333%2c5.96539390625Q14.3825%2c5.93256390625%2c14.4243%2c5.89077390625Q14.466%2c5.84899390625%2c14.4989%2c5.79985390625Q14.5317%2c5.75072390625%2c14.5543%2c5.69612390625Q14.5769%2c5.641523906250001%2c14.5885%2c5.58356390625Q14.6%2c5.525613906249999%2c14.6%2c5.46651390625L14.6%2c5.46544390625L14.6%2c2.31515290625Q14.6%2c1.79311590625%2c14.2232%2c1.42645590625Q13.8532%2c1.06650390625%2c13.3333%2c1.06650390625L2.666667%2c1.06650390625Q2.146797%2c1.06650390625%2c1.776849%2c1.42645290625Q1.4%2c1.79311690625%2c1.4%2c2.31515290625L1.4%2c13.01790390625Q1.4%2c13.53990390625%2c1.776851%2c13.90660390625Q2.146796%2c14.26650390625%2c2.666667%2c14.26650390625L6.7143%2c14.26650390625Q6.7734%2c14.26650390625%2c6.83135%2c14.25500390625Q6.88931%2c14.24340390625%2c6.94391%2c14.22080390625Q6.99851%2c14.19820390625%2c7.04764%2c14.16540390625Q7.09678%2c14.13250390625%2c7.13856%2c14.09080390625Q7.18035%2c14.04900390625%2c7.21318%2c13.99980390625Q7.24601%2c13.95070390625%2c7.26863%2c13.89610390625Q7.29124%2c13.84150390625%2c7.30277%2c13.78360390625Q7.3143%2c13.72560390625%2c7.3143%2c13.66650390625Q7.3143%2c13.60740390625%2c7.30277%2c13.54940390625Q7.29124%2c13.49150390625%2c7.26863%2c13.43690390625Q7.24601%2c13.38230390625%2c7.21318%2c13.33320390625Q7.18035%2c13.28400390625%2c7.13856%2c13.24220390625Q7.09678%2c13.20040390625%2c7.04764%2c13.16760390625Q6.99851%2c13.13480390625%2c6.94391%2c13.11220390625Q6.88931%2c13.08960390625%2c6.83135%2c13.07800390625Q6.7734%2c13.06650390625%2c6.7143%2c13.06650390625L2.666667%2c13.06650390625Q2.6%2c13.06650390625%2c2.6%2c13.01790390625L2.6%2c2.31515290625Q2.6%2c2.26650390625%2c2.666667%2c2.26650390625L13.3333%2c2.26650390625Q13.3658%2c2.26650390625%2c13.3863%2c2.28652190625Q13.4%2c2.29982490625%2c13.4%2c2.31515290625Z' fill-rule='evenodd' fill='%23BDBDBD' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M9.4%2c12.83333L9.4%2c14.16667Q9.4%2c14.225760000000001%2c9.411529%2c14.283719999999999Q9.423058%2c14.34168%2c9.445672%2c14.39628Q9.468287%2c14.45087%2c9.501118%2c14.50001Q9.53395%2c14.549140000000001%2c9.575736%2c14.59093Q9.617522%2c14.632719999999999%2c9.666658%2c14.66555Q9.715793%2c14.69838%2c9.77039%2c14.72099Q9.824985999999999%2c14.74361%2c9.882946%2c14.75514Q9.9409052%2c14.766670000000001%2c10%2c14.766670000000001L11.33333%2c14.766670000000001Q11.40401%2c14.766670000000001%2c11.47275%2c14.75024Q11.5415%2c14.73382%2c11.60454%2c14.70187Q11.66759%2c14.66993%2c11.72148%2c14.6242Q11.77538%2c14.578479999999999%2c11.81718%2c14.52149L15.48384%2c9.52148Q15.51816%2c9.47469%2c15.54287%2c9.4222Q15.56758%2c9.3697%2c15.581769999999999%2c9.31344Q15.595970000000001%2c9.25718%2c15.59912%2c9.19924Q15.60227%2c9.1413%2c15.594249999999999%2c9.08383Q15.58624%2c9.02636%2c15.56737%2c8.971495Q15.5485%2c8.916627%2c15.519459999999999%2c8.866392Q15.49042%2c8.816157%2c15.45229%2c8.772418Q15.41417%2c8.728679%2c15.36836%2c8.693055L13.86836%2c7.526389Q13.860240000000001%2c7.520071%2c13.85191%2c7.514035Q13.75524%2c7.444036%2c13.63915%2c7.416358Q13.52305%2c7.38868%2c13.40521%2c7.407536Q13.28736%2c7.426391%2c13.185690000000001%2c7.48891Q13.08403%2c7.55143%2c13.01403%2c7.648094L9.514035%2c12.48143Q9.4%2c12.6389%2c9.4%2c12.83333ZM10.6%2c13.56667L11.02929%2c13.56667L14.171240000000001%2c9.28219L13.621780000000001%2c8.854833L10.6%2c13.02776L10.6%2c13.56667Z' fill-rule='evenodd' fill='%23BDBDBD' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/icon_logout.svg":
/*!*************************************!*\
  !*** ./style/image/icon_logout.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='16' height='16' viewBox='0 0 16 16'%3e%3cdefs%3e%3cclipPath id='master_svg0_211_3770'%3e%3crect x='0' y='0' width='16' height='16' rx='0'/%3e%3c/clipPath%3e%3c/defs%3e%3cg clip-path='url(%23master_svg0_211_3770)'%3e%3cg%3e%3cpath d='M10.9%2c3L10.9%2c4.5Q10.9%2c4.559089999999999%2c10.91153%2c4.61705Q10.92306%2c4.67501%2c10.94567%2c4.72961Q10.96828%2c4.78421%2c11.00112%2c4.83334Q11.03395%2c4.88248%2c11.07574%2c4.92426Q11.11752%2c4.96605%2c11.16666%2c4.99888Q11.21579%2c5.03171%2c11.27039%2c5.05433Q11.32499%2c5.0769400000000005%2c11.38295%2c5.08847Q11.44091%2c5.1%2c11.5%2c5.1Q11.5591%2c5.1%2c11.6171%2c5.08847Q11.675%2c5.0769400000000005%2c11.7296%2c5.05433Q11.7842%2c5.03171%2c11.8333%2c4.99888Q11.8825%2c4.96605%2c11.9243%2c4.92426Q11.9661%2c4.88248%2c11.9989%2c4.83334Q12.0317%2c4.78421%2c12.0543%2c4.72961Q12.0769%2c4.67501%2c12.0885%2c4.61705Q12.1%2c4.559089999999999%2c12.1%2c4.5L12.1%2c4.49893L12.1%2c3Q12.1%2c2.337258%2c11.6314%2c1.86863Q11.16274%2c1.4%2c10.5%2c1.4L2.5%2c1.4Q1.837258%2c1.4%2c1.368629%2c1.868629Q0.9%2c2.337258%2c0.9%2c3L0.9%2c13Q0.9%2c13.6627%2c1.368629%2c14.1314Q1.837258%2c14.6%2c2.5%2c14.6L10.5%2c14.6Q11.16274%2c14.6%2c11.6314%2c14.1314Q12.1%2c13.6627%2c12.1%2c13L12.1%2c12Q12.1%2c11.94091%2c12.0885%2c11.88295Q12.0769%2c11.82499%2c12.0543%2c11.77039Q12.0317%2c11.71579%2c11.9989%2c11.66666Q11.9661%2c11.61752%2c11.9243%2c11.57573Q11.8825%2c11.53395%2c11.8333%2c11.50112Q11.7842%2c11.46828%2c11.7296%2c11.44567Q11.675%2c11.42306%2c11.6171%2c11.41153Q11.5591%2c11.4%2c11.5%2c11.4Q11.44091%2c11.4%2c11.38295%2c11.41153Q11.32499%2c11.42306%2c11.27039%2c11.44567Q11.21579%2c11.46829%2c11.16666%2c11.50112Q11.11752%2c11.53395%2c11.07573%2c11.57574Q11.03395%2c11.61752%2c11.00112%2c11.66666Q10.96828%2c11.71579%2c10.94567%2c11.77039Q10.92306%2c11.82499%2c10.91153%2c11.88295Q10.9%2c11.94091%2c10.9%2c12L10.9%2c13Q10.9%2c13.4%2c10.5%2c13.4L2.5%2c13.4Q2.1%2c13.4%2c2.1%2c13L2.1%2c3Q2.1%2c2.834315%2c2.2171570000000003%2c2.7171570000000003Q2.334315%2c2.6%2c2.5%2c2.6L10.5%2c2.6Q10.66569%2c2.6%2c10.78284%2c2.7171570000000003Q10.9%2c2.834314%2c10.9%2c3Z' fill-rule='evenodd' fill='%23EEEEEE' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M9%2c7.4L14%2c7.4Q14.059090000000001%2c7.4%2c14.117049999999999%2c7.411529Q14.17501%2c7.423058%2c14.229610000000001%2c7.445672Q14.28421%2c7.468287%2c14.33334%2c7.501118Q14.382480000000001%2c7.53395%2c14.42426%2c7.575736Q14.46605%2c7.617522%2c14.49888%2c7.666658Q14.53171%2c7.715793%2c14.55433%2c7.77039Q14.57694%2c7.824986%2c14.588470000000001%2c7.882946Q14.6%2c7.9409051999999996%2c14.6%2c8Q14.6%2c8.0590948%2c14.588470000000001%2c8.117054Q14.57694%2c8.175014000000001%2c14.55433%2c8.22961Q14.53171%2c8.284207%2c14.49888%2c8.333342Q14.46605%2c8.382478%2c14.42426%2c8.424264Q14.382480000000001%2c8.46605%2c14.33334%2c8.498882Q14.28421%2c8.531713%2c14.229610000000001%2c8.554328Q14.17501%2c8.576942%2c14.117049999999999%2c8.588471Q14.059090000000001%2c8.6%2c14%2c8.6L9%2c8.6Q8.9409052%2c8.6%2c8.882946%2c8.588471Q8.824985999999999%2c8.576942%2c8.77039%2c8.554328Q8.715793%2c8.531713%2c8.666658%2c8.498882Q8.617522%2c8.46605%2c8.575736%2c8.424264Q8.53395%2c8.382478%2c8.501118%2c8.333342Q8.468287%2c8.284207%2c8.445672%2c8.22961Q8.423058%2c8.175014000000001%2c8.411529%2c8.117054Q8.4%2c8.0590948%2c8.4%2c8Q8.4%2c7.9409051999999996%2c8.411529%2c7.882946Q8.423058%2c7.824986%2c8.445672%2c7.77039Q8.468287%2c7.715793%2c8.501118%2c7.666658Q8.53395%2c7.617522%2c8.575736%2c7.575736Q8.617522%2c7.53395%2c8.666658%2c7.501118Q8.715793%2c7.468287%2c8.77039%2c7.445672Q8.824985999999999%2c7.423058%2c8.882946%2c7.411529Q8.9409052%2c7.4%2c9%2c7.4Z' fill-rule='evenodd' fill='%23EEEEEE' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M13.05962290625%2c5.729651024261474L15.01752390625%2c7.687630024261475Q15.05931390625%2c7.729420024261475%2c15.09214390625%2c7.778550024261475Q15.12497390625%2c7.827690024261475%2c15.14758390625%2c7.882280024261474Q15.17019390625%2c7.936880024261475%2c15.18172390625%2c7.9948400242614746Q15.19325390625%2c8.052790024261474%2c15.19325390625%2c8.111890024261475Q15.19325390625%2c8.170980024261475%2c15.18172390625%2c8.228940024261474Q15.17019390625%2c8.286900024261474%2c15.14758390625%2c8.341490024261475Q15.12497390625%2c8.396090024261476%2c15.09214390625%2c8.445220024261474Q15.05931390625%2c8.494360024261475%2c15.01753390625%2c8.536140024261474L13.05972090625%2c10.494060024261476L13.05952990625%2c10.494250024261476Q12.97513790625%2c10.578650024261474%2c12.86487190625%2c10.624320024261475Q12.75460590625%2c10.670000024261475%2c12.63525390625%2c10.670000024261475Q12.57615910625%2c10.670000024261475%2c12.51819990625%2c10.658470024261476Q12.460239906249999%2c10.646940024261475%2c12.40564390625%2c10.624330024261475Q12.35104690625%2c10.601710024261475%2c12.30191190625%2c10.568880024261475Q12.25277590625%2c10.536050024261474%2c12.21098990625%2c10.494260024261475Q12.16920390625%2c10.452480024261476%2c12.13637190625%2c10.403340024261475Q12.10354090625%2c10.354210024261475%2c12.08092590625%2c10.299610024261476Q12.05831190625%2c10.245010024261475%2c12.04678290625%2c10.187050024261474Q12.03525390625%2c10.129090024261474%2c12.03525390625%2c10.070000024261475Q12.03525390625%2c9.950660024261474%2c12.08092290625%2c9.840400024261474Q12.12659190625%2c9.730140024261475%2c12.21097790625%2c9.645750024261474L12.21116890625%2c9.645560024261474L13.744743906250001%2c8.111890024261475L12.21107690625%2c6.578161024261474L12.21098090625%2c6.578065024261474Q12.12659390625%2c6.493675024261474%2c12.08092390625%2c6.383414024261475Q12.03525390625%2c6.2731540242614745%2c12.03525390625%2c6.153810024261475Q12.03525390625%2c6.094715224261474%2c12.04678290625%2c6.036756024261474Q12.05831190625%2c5.978796024261475%2c12.08092590625%2c5.9242000242614745Q12.10354090625%2c5.869603024261474%2c12.13637190625%2c5.820468024261475Q12.16920390625%2c5.771332024261475%2c12.21098990625%2c5.729546024261475Q12.25277590625%2c5.6877600242614745%2c12.30191190625%2c5.654928024261475Q12.35104690625%2c5.622097024261475%2c12.40564390625%2c5.599482024261475Q12.460239906249999%2c5.576868024261475%2c12.51819990625%2c5.565339024261474Q12.57615910625%2c5.553810024261475%2c12.63525390625%2c5.553810024261475Q12.75460490625%2c5.553810024261475%2c12.86486990625%2c5.599485024261474Q12.97513490625%2c5.645159024261474%2c13.05952690625%2c5.729555024261475L13.05962290625%2c5.729651024261474Z' fill-rule='evenodd' fill='%23EEEEEE' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/new_chatbot_edit.svg":
/*!******************************************!*\
  !*** ./style/image/new_chatbot_edit.svg ***!
  \******************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='25' height='23' viewBox='0 0 25 23'%3e%3cdefs%3e%3clinearGradient x1='-0.12584161758422852' y1='0.5' x2='1.1620374917984009' y2='0.5' id='master_svg0_195_02528'%3e%3cstop offset='2.142857201397419%25' stop-color='%23E47557' stop-opacity='1'/%3e%3cstop offset='100%25' stop-color='%23C4A9E5' stop-opacity='1'/%3e%3c/linearGradient%3e%3clinearGradient x1='-0.12584161758422852' y1='0.5' x2='1.1620374917984009' y2='0.5' id='master_svg1_195_02528'%3e%3cstop offset='2.142857201397419%25' stop-color='%23E47557' stop-opacity='1'/%3e%3cstop offset='100%25' stop-color='%23C4A9E5' stop-opacity='1'/%3e%3c/linearGradient%3e%3c/defs%3e%3cg%3e%3cg%3e%3crect x='1' y='1' width='23' height='21' rx='4' fill-opacity='0' stroke-opacity='1' stroke='%23E27963' fill='none' stroke-width='2'/%3e%3c/g%3e%3cg transform='matrix(-0.258819043636322%2c0.9659258127212524%2c-0.9659258127212524%2c-0.258819043636322%2c25.109630121471127%2c-6.373253771555028)'%3e%3cpath d='M15.155941%2c5.459255484375L26.096600000000002%2c7.1864894843750005Q26.1842%2c7.200308484375%2c26.267899999999997%2c7.229306484375Q26.351599999999998%2c7.2583044843749995%2c26.429000000000002%2c7.3015764843749995Q26.5063%2c7.344849484375%2c26.5748%2c7.401047484375Q26.6433%2c7.457241484375%2c26.7009%2c7.524621484375Q26.758499999999998%2c7.591991484375%2c26.8033%2c7.668441484375Q26.848100000000002%2c7.744881484375%2c26.8788%2c7.828021484375Q26.9095%2c7.911161484375%2c26.9251%2c7.998401484375Q26.9407%2c8.085631484375%2c26.9407%2c8.174251484375Q26.9407%2c8.272751484375%2c26.9215%2c8.369341484375Q26.9022%2c8.465941484375%2c26.8646%2c8.556941484374999Q26.826900000000002%2c8.647931484375%2c26.772100000000002%2c8.729821484375Q26.717399999999998%2c8.811721484375%2c26.6478%2c8.881361484375Q26.5781%2c8.951001484375%2c26.4962%2c9.005721484375Q26.4143%2c9.060441484375%2c26.3234%2c9.098131484375Q26.2324%2c9.135821484375%2c26.1358%2c9.155041484375Q26.0392%2c9.174251484375%2c25.9407%2c9.174251484375Q25.8622%2c9.174251484375%2c25.7847%2c9.162021484375L25.7843%2c9.161951484374999L14.844059%2c7.434787484375Q14.756523%2c7.420968484375%2c14.672783%2c7.391970484375Q14.589042%2c7.362972484375%2c14.511705%2c7.319700484375Q14.434369%2c7.276427484375%2c14.365848%2c7.220229484375Q14.297327%2c7.164031484375%2c14.239756%2c7.096659484375Q14.182186%2c7.029286484375%2c14.13736%2c6.952840484375Q14.092535%2c6.876393484375%2c14.061852%2c6.793255484375Q14.031169%2c6.710117484375%2c14.015584%2c6.622879484375Q14%2c6.535640884375%2c14%2c6.447021484375Q14%2c6.348530084375%2c14.019214999999999%2c6.251931484375Q14.03843%2c6.155332484375%2c14.076121%2c6.064338484375Q14.113812%2c5.973343484375%2c14.16853%2c5.891451484375Q14.223249%2c5.809558484375%2c14.292893%2c5.739914484375Q14.362537%2c5.670270484375%2c14.44443%2c5.615551484375Q14.526322%2c5.560833484375%2c14.617317%2c5.523142484375Q14.708311%2c5.485451484375%2c14.80491%2c5.466236484375Q14.9015086%2c5.447021484375%2c15%2c5.447021484375Q15.0784505%2c5.447021484375%2c15.155941%2c5.459255484375Z' fill-rule='evenodd' fill='%23BFB1FA' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M8.70711%2c9.707107Q8.847760000000001%2c9.566454%2c8.92388%2c9.382683Q9%2c9.198912%2c9%2c9Q9%2c8.9015086%2c8.98078%2c8.80491Q8.96157%2c8.708311%2c8.92388%2c8.617317Q8.88619%2c8.526322%2c8.83147%2c8.44443Q8.77675%2c8.362537%2c8.70711%2c8.292893Q8.63746%2c8.223249%2c8.55557%2c8.16853Q8.47368%2c8.113812%2c8.38268%2c8.076121Q8.29169%2c8.03843%2c8.19509%2c8.019214999999999Q8.09849%2c8%2c8%2c8Q7.80109%2c8%2c7.617319999999999%2c8.07612Q7.43355%2c8.152241%2c7.29289%2c8.292893L4.292893%2c11.29289Q4.223249%2c11.36254%2c4.16853%2c11.44443Q4.113812%2c11.52632%2c4.076121%2c11.61732Q4.03843%2c11.70831%2c4.019215%2c11.80491Q4%2c11.90151%2c4%2c12Q4%2c12.09849%2c4.019215%2c12.19509Q4.03843%2c12.29169%2c4.076121%2c12.38268Q4.113812%2c12.47368%2c4.16853%2c12.55557Q4.223249%2c12.63746%2c4.292893%2c12.70711L7.29258%2c15.70679L7.29289%2c15.70711Q7.43355%2c15.847760000000001%2c7.617319999999999%2c15.92388Q7.80109%2c16%2c8%2c16Q8.09849%2c16%2c8.19509%2c15.98078Q8.29169%2c15.96157%2c8.38268%2c15.92388Q8.47368%2c15.88619%2c8.55557%2c15.83147Q8.63746%2c15.77675%2c8.70711%2c15.70711Q8.77675%2c15.63746%2c8.83147%2c15.55557Q8.88619%2c15.47368%2c8.92388%2c15.38268Q8.96157%2c15.29169%2c8.98078%2c15.19509Q9%2c15.09849%2c9%2c15Q9%2c14.80109%2c8.92388%2c14.61732Q8.847760000000001%2c14.43355%2c8.70711%2c14.29289L8.70679%2c14.292580000000001L6.41421%2c12L8.70711%2c9.707107Z' fill-rule='evenodd' fill='url(%23master_svg0_195_02528)' fill-opacity='1'/%3e%3c/g%3e%3cg transform='matrix(-1%2c0%2c0%2c1%2c40%2c0)'%3e%3cpath d='M23.70711%2c9.707107Q23.84776%2c9.566454%2c23.92388%2c9.382683Q24%2c9.198912%2c24%2c9Q24%2c8.9015086%2c23.98078%2c8.80491Q23.961570000000002%2c8.708311%2c23.92388%2c8.617317Q23.88619%2c8.526322%2c23.83147%2c8.44443Q23.77675%2c8.362537%2c23.70711%2c8.292893Q23.63746%2c8.223249%2c23.55557%2c8.16853Q23.47368%2c8.113812%2c23.38268%2c8.076121Q23.29169%2c8.03843%2c23.19509%2c8.019214999999999Q23.098489999999998%2c8%2c23%2c8Q22.80109%2c8%2c22.61732%2c8.07612Q22.43355%2c8.152241%2c22.29289%2c8.292893L19.292893%2c11.29289Q19.223249%2c11.36254%2c19.16853%2c11.44443Q19.113812%2c11.52632%2c19.076121%2c11.61732Q19.038429999999998%2c11.70831%2c19.019215%2c11.80491Q19%2c11.90151%2c19%2c12Q19%2c12.09849%2c19.019215%2c12.19509Q19.038429999999998%2c12.29169%2c19.076121%2c12.38268Q19.113812%2c12.47368%2c19.16853%2c12.55557Q19.223249%2c12.63746%2c19.292893%2c12.70711L22.29258%2c15.70679L22.29289%2c15.70711Q22.43355%2c15.847760000000001%2c22.61732%2c15.92388Q22.80109%2c16%2c23%2c16Q23.098489999999998%2c16%2c23.19509%2c15.98078Q23.29169%2c15.96157%2c23.38268%2c15.92388Q23.47368%2c15.88619%2c23.55557%2c15.83147Q23.63746%2c15.77675%2c23.70711%2c15.70711Q23.77675%2c15.63746%2c23.83147%2c15.55557Q23.88619%2c15.47368%2c23.92388%2c15.38268Q23.961570000000002%2c15.29169%2c23.98078%2c15.19509Q24%2c15.09849%2c24%2c15Q24%2c14.80109%2c23.92388%2c14.61732Q23.84776%2c14.43355%2c23.70711%2c14.29289L23.706789999999998%2c14.292580000000001L21.41421%2c12L23.70711%2c9.707107Z' fill-rule='evenodd' fill='url(%23master_svg1_195_02528)' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/new_chatbot_resp.svg":
/*!******************************************!*\
  !*** ./style/image/new_chatbot_resp.svg ***!
  \******************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='32' height='32' viewBox='0 0 32 32'%3e%3cdefs%3e%3clinearGradient x1='-0.12584161758422852' y1='0.5' x2='1.1620374917984009' y2='0.5' id='master_svg0_195_02528'%3e%3cstop offset='2.142857201397419%25' stop-color='%23E47557' stop-opacity='1'/%3e%3cstop offset='100%25' stop-color='%23C4A9E5' stop-opacity='1'/%3e%3c/linearGradient%3e%3c/defs%3e%3cg%3e%3cg%3e%3c/g%3e%3cg%3e%3cpath d='M5.62521%2c26.737Q5.75065%2c28%2c6.8%2c28Q7.6315100000000005%2c28%2c12.15456%2c25.173Q14.43415%2c25.6842%2c16%2c25.6842Q21.133%2c25.6842%2c24.7819%2c22.5613Q28.5%2c19.3792%2c28.5%2c14.8421Q28.5%2c10.30498%2c24.7819%2c7.12294Q21.1329%2c4%2c16%2c4Q10.867049999999999%2c4%2c7.21805%2c7.12294Q3.5%2c10.30498%2c3.5%2c14.8421Q3.5%2c17.7626%2c6.30622%2c21.4629Q5.79819%2c24.074%2c5.66115%2c25.4538Q5.57945%2c26.2763%2c5.62521%2c26.737ZM7.65932%2c25.5734Q8.80485%2c24.9187%2c11.44239%2c23.2589L11.79769%2c23.0353L12.20612%2c23.1323Q14.5293%2c23.6842%2c16%2c23.6842Q20.394%2c23.6842%2c23.4815%2c21.0418Q26.5%2c18.458399999999997%2c26.5%2c14.8421Q26.5%2c11.225760000000001%2c23.4815%2c8.642430000000001Q20.394%2c5.999999%2c16%2c5.999999Q11.60604%2c6%2c8.51849%2c8.642430000000001Q5.5%2c11.225760000000001%2c5.5%2c14.8421Q5.5%2c17.2134%2c8.16062%2c20.5918L8.44557%2c20.9536L8.35584%2c21.4054Q7.8058499999999995%2c24.1742%2c7.65932%2c25.5734Z' fill-rule='evenodd' fill='%23E27963' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M13%2c12L20%2c12Q20.098489999999998%2c12%2c20.19509%2c12.019214999999999Q20.29169%2c12.03843%2c20.38268%2c12.076121Q20.47368%2c12.113812%2c20.55557%2c12.16853Q20.63746%2c12.223249%2c20.70711%2c12.292893Q20.77675%2c12.362537%2c20.83147%2c12.44443Q20.88619%2c12.526322%2c20.92388%2c12.617317Q20.961570000000002%2c12.708311%2c20.98078%2c12.80491Q21%2c12.9015086%2c21%2c13Q21%2c13.0984914%2c20.98078%2c13.19509Q20.961570000000002%2c13.291689%2c20.92388%2c13.382683Q20.88619%2c13.473678%2c20.83147%2c13.55557Q20.77675%2c13.637463%2c20.70711%2c13.707107Q20.63746%2c13.776751%2c20.55557%2c13.83147Q20.47368%2c13.886188%2c20.38268%2c13.923879Q20.29169%2c13.96157%2c20.19509%2c13.980785000000001Q20.098489999999998%2c14%2c20%2c14L13%2c14Q12.9015086%2c14%2c12.80491%2c13.980785000000001Q12.708311%2c13.96157%2c12.617317%2c13.923879Q12.526322%2c13.886188%2c12.44443%2c13.83147Q12.362537%2c13.776751%2c12.292893%2c13.707107Q12.223249%2c13.637463%2c12.16853%2c13.55557Q12.113812%2c13.473678%2c12.076121%2c13.382683Q12.03843%2c13.291689%2c12.019214999999999%2c13.19509Q12%2c13.0984914%2c12%2c13Q12%2c12.9015086%2c12.019214999999999%2c12.80491Q12.03843%2c12.708311%2c12.076121%2c12.617317Q12.113812%2c12.526322%2c12.16853%2c12.44443Q12.223249%2c12.362537%2c12.292893%2c12.292893Q12.362537%2c12.223249%2c12.44443%2c12.16853Q12.526322%2c12.113812%2c12.617317%2c12.076121Q12.708311%2c12.03843%2c12.80491%2c12.019214999999999Q12.9015086%2c12%2c13%2c12Z' fill-rule='evenodd' fill='%23BFB1FA' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M14%2c17L19%2c17Q19.098489999999998%2c17%2c19.19509%2c17.019215Q19.29169%2c17.038429999999998%2c19.38268%2c17.076121Q19.47368%2c17.113812%2c19.55557%2c17.16853Q19.63746%2c17.223249%2c19.70711%2c17.292893Q19.77675%2c17.362537%2c19.83147%2c17.44443Q19.88619%2c17.526322%2c19.92388%2c17.617317Q19.961570000000002%2c17.708311%2c19.98078%2c17.80491Q20%2c17.9015086%2c20%2c18Q20%2c18.0984914%2c19.98078%2c18.19509Q19.961570000000002%2c18.291689%2c19.92388%2c18.382683Q19.88619%2c18.473678%2c19.83147%2c18.55557Q19.77675%2c18.637463%2c19.70711%2c18.707107Q19.63746%2c18.776751%2c19.55557%2c18.83147Q19.47368%2c18.886188%2c19.38268%2c18.923879Q19.29169%2c18.961570000000002%2c19.19509%2c18.980785Q19.098489999999998%2c19%2c19%2c19L14%2c19Q13.9015086%2c19%2c13.80491%2c18.980785Q13.708311%2c18.961570000000002%2c13.617317%2c18.923879Q13.526322%2c18.886188%2c13.44443%2c18.83147Q13.362537%2c18.776751%2c13.292893%2c18.707107Q13.223249%2c18.637463%2c13.16853%2c18.55557Q13.113812%2c18.473678%2c13.076121%2c18.382683Q13.03843%2c18.291689%2c13.019214999999999%2c18.19509Q13%2c18.0984914%2c13%2c18Q13%2c17.9015086%2c13.019214999999999%2c17.80491Q13.03843%2c17.708311%2c13.076121%2c17.617317Q13.113812%2c17.526322%2c13.16853%2c17.44443Q13.223249%2c17.362537%2c13.292893%2c17.292893Q13.362537%2c17.223249%2c13.44443%2c17.16853Q13.526322%2c17.113812%2c13.617317%2c17.076121Q13.708311%2c17.038429999999998%2c13.80491%2c17.019215Q13.9015086%2c17%2c14%2c17Z' fill-rule='evenodd' fill='url(%23master_svg0_195_02528)' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/new_welcome.svg":
/*!*************************************!*\
  !*** ./style/image/new_welcome.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='25' height='25' viewBox='0 0 25 25'%3e%3cg%3e%3cg%3e%3cpath d='M24.7464%2c10.98351L24.7461%2c10.9819Q24.7289%2c10.89787%2c24.6976%2c10.818Q24.6664%2c10.73813%2c24.622%2c10.66474Q24.5776%2c10.59136%2c24.5213%2c10.52661Q24.4651%2c10.46185%2c24.3986%2c10.40762Q24.3322%2c10.35339%2c24.2575%2c10.31127Q24.1827%2c10.26915%2c24.102%2c10.24037Q24.0212%2c10.21158%2c23.9366%2c10.19698Q23.8521%2c10.18237%2c23.7664%2c10.18237Q23.6679%2c10.18237%2c23.5713%2c10.20159Q23.4747%2c10.2208%2c23.3837%2c10.25849Q23.2927%2c10.29618%2c23.2108%2c10.3509Q23.1289%2c10.40562%2c23.0592%2c10.47527Q22.9896%2c10.54491%2c22.9349%2c10.6268Q22.8802%2c10.70869%2c22.8425%2c10.79969Q22.8048%2c10.89068%2c22.7856%2c10.98728Q22.7664%2c11.08388%2c22.7664%2c11.18237Q22.7664%2c11.28364%2c22.7867%2c11.38285Q23%2c12.4254%2c23%2c13.5Q23%2c17.716%2c19.9712%2c20.381Q16.9945%2c23%2c12.5%2c23L2.40069%2c23Q3.3792%2c21.7066%2c3.7597%2c20.8142Q4.11822%2c19.9733%2c3.65989%2c19.1302Q2%2c16.076999999999998%2c2%2c13.5Q2%2c9.15076%2c5.07538%2c6.07538Q8.15076%2c3%2c12.5%2c3Q12.5985%2c3%2c12.6951%2c2.980785Q12.7917%2c2.96157%2c12.8827%2c2.923879Q12.9737%2c2.8861879999999998%2c13.0556%2c2.83147Q13.1375%2c2.776751%2c13.2071%2c2.707107Q13.2767%2c2.637463%2c13.3315%2c2.55557Q13.3862%2c2.473678%2c13.4239%2c2.382683Q13.4616%2c2.291689%2c13.4808%2c2.19509Q13.5%2c2.0984914%2c13.5%2c2Q13.5%2c1.9015086%2c13.4808%2c1.80491Q13.4616%2c1.7083110000000001%2c13.4239%2c1.617317Q13.3862%2c1.526322%2c13.3315%2c1.44443Q13.2767%2c1.362537%2c13.2071%2c1.2928929999999998Q13.1375%2c1.223249%2c13.0556%2c1.16853Q12.9737%2c1.113812%2c12.8827%2c1.076121Q12.7917%2c1.03843%2c12.6951%2c1.019215Q12.5985%2c1%2c12.5%2c1Q7.32233%2c1%2c3.66117%2c4.66117Q0%2c8.322330000000001%2c0%2c13.5Q0%2c16.5823%2c1.89882%2c20.0782Q1.58318%2c20.787%2c0.6839919999999999%2c21.9526Q0.638479%2c22.0116%2c0.61634%2c22.0404Q-0.11301499999999998%2c22.987%2c0.4216376%2c24.0095Q0.9395370000000001%2c25%2c2.10492%2c25L12.5%2c25Q17.7492%2c25%2c21.2923%2c21.8825Q25%2c18.6202%2c25%2c13.5Q25%2c12.2237%2c24.7464%2c10.98351Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M8%2c15L16.5%2c15Q16.598489999999998%2c15%2c16.69509%2c15.019214999999999Q16.79169%2c15.03843%2c16.88268%2c15.076121Q16.97368%2c15.113812%2c17.05557%2c15.16853Q17.13746%2c15.223249%2c17.20711%2c15.292893Q17.27675%2c15.362537%2c17.33147%2c15.44443Q17.38619%2c15.526322%2c17.42388%2c15.617317Q17.461570000000002%2c15.708311%2c17.48078%2c15.80491Q17.5%2c15.9015086%2c17.5%2c16Q17.5%2c16.0984914%2c17.48078%2c16.19509Q17.461570000000002%2c16.291689%2c17.42388%2c16.382683Q17.38619%2c16.473678%2c17.33147%2c16.55557Q17.27675%2c16.637463%2c17.20711%2c16.707107Q17.13746%2c16.776751%2c17.05557%2c16.83147Q16.97368%2c16.886188%2c16.88268%2c16.923879Q16.79169%2c16.961570000000002%2c16.69509%2c16.980785Q16.598489999999998%2c17%2c16.5%2c17L8%2c17Q7.9015086%2c17%2c7.80491%2c16.980785Q7.708311%2c16.961570000000002%2c7.617317%2c16.923879Q7.526322%2c16.886188%2c7.44443%2c16.83147Q7.362537%2c16.776751%2c7.292893%2c16.707107Q7.223249%2c16.637463%2c7.16853%2c16.55557Q7.113812%2c16.473678%2c7.076121%2c16.382683Q7.03843%2c16.291689%2c7.019215%2c16.19509Q7%2c16.0984914%2c7%2c16Q7%2c15.9015086%2c7.019215%2c15.80491Q7.03843%2c15.708311%2c7.076121%2c15.617317Q7.113812%2c15.526322%2c7.16853%2c15.44443Q7.223249%2c15.362537%2c7.292893%2c15.292893Q7.362537%2c15.223249%2c7.44443%2c15.16853Q7.526322%2c15.113812%2c7.617317%2c15.076121Q7.708311%2c15.03843%2c7.80491%2c15.019214999999999Q7.9015086%2c15%2c8%2c15Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M16%2c4L24%2c4Q24.098489999999998%2c4%2c24.19509%2c4.019215Q24.29169%2c4.03843%2c24.38268%2c4.076121Q24.47368%2c4.113812%2c24.55557%2c4.16853Q24.63746%2c4.223249%2c24.70711%2c4.292893Q24.77675%2c4.362537%2c24.83147%2c4.44443Q24.88619%2c4.526322%2c24.92388%2c4.617317Q24.961570000000002%2c4.708311%2c24.98078%2c4.80491Q25%2c4.9015086%2c25%2c5Q25%2c5.0984914%2c24.98078%2c5.19509Q24.961570000000002%2c5.291689%2c24.92388%2c5.382683Q24.88619%2c5.473678%2c24.83147%2c5.55557Q24.77675%2c5.637463%2c24.70711%2c5.707107Q24.63746%2c5.776751%2c24.55557%2c5.83147Q24.47368%2c5.886188%2c24.38268%2c5.923879Q24.29169%2c5.96157%2c24.19509%2c5.980785Q24.098489999999998%2c6%2c24%2c6L16%2c6Q15.9015086%2c6%2c15.80491%2c5.980785Q15.708311%2c5.96157%2c15.617317%2c5.923879Q15.526322%2c5.886188%2c15.44443%2c5.83147Q15.362537%2c5.776751%2c15.292893%2c5.707107Q15.223249%2c5.637463%2c15.16853%2c5.55557Q15.113812%2c5.473678%2c15.076121%2c5.382683Q15.03843%2c5.291689%2c15.019214999999999%2c5.19509Q15%2c5.0984914%2c15%2c5Q15%2c4.9015086%2c15.019214999999999%2c4.80491Q15.03843%2c4.708311%2c15.076121%2c4.617317Q15.113812%2c4.526322%2c15.16853%2c4.44443Q15.223249%2c4.362537%2c15.292893%2c4.292893Q15.362537%2c4.223249%2c15.44443%2c4.16853Q15.526322%2c4.113812%2c15.617317%2c4.076121Q15.708311%2c4.03843%2c15.80491%2c4.019215Q15.9015086%2c4%2c16%2c4Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg transform='matrix(0%2c-1%2c1%2c0%2c11%2c29)'%3e%3cpath d='M20%2c8L28%2c8Q28.098489999999998%2c8%2c28.19509%2c8.019214999999999Q28.29169%2c8.03843%2c28.38268%2c8.076121Q28.47368%2c8.113812%2c28.55557%2c8.16853Q28.63746%2c8.223249%2c28.70711%2c8.292893Q28.77675%2c8.362537%2c28.83147%2c8.44443Q28.88619%2c8.526322%2c28.92388%2c8.617317Q28.961570000000002%2c8.708311%2c28.98078%2c8.80491Q29%2c8.9015086%2c29%2c9Q29%2c9.0984914%2c28.98078%2c9.19509Q28.961570000000002%2c9.291689%2c28.92388%2c9.382683Q28.88619%2c9.473678%2c28.83147%2c9.55557Q28.77675%2c9.637463%2c28.70711%2c9.707107Q28.63746%2c9.776751%2c28.55557%2c9.83147Q28.47368%2c9.886188%2c28.38268%2c9.923879Q28.29169%2c9.96157%2c28.19509%2c9.980785000000001Q28.098489999999998%2c10%2c28%2c10L20%2c10Q19.9015086%2c10%2c19.80491%2c9.980785000000001Q19.708311%2c9.96157%2c19.617317%2c9.923879Q19.526322%2c9.886188%2c19.44443%2c9.83147Q19.362537%2c9.776751%2c19.292893%2c9.707107Q19.223249%2c9.637463%2c19.16853%2c9.55557Q19.113812%2c9.473678%2c19.076121%2c9.382683Q19.038429999999998%2c9.291689%2c19.019215%2c9.19509Q19%2c9.0984914%2c19%2c9Q19%2c8.9015086%2c19.019215%2c8.80491Q19.038429999999998%2c8.708311%2c19.076121%2c8.617317Q19.113812%2c8.526322%2c19.16853%2c8.44443Q19.223249%2c8.362537%2c19.292893%2c8.292893Q19.362537%2c8.223249%2c19.44443%2c8.16853Q19.526322%2c8.113812%2c19.617317%2c8.076121Q19.708311%2c8.03843%2c19.80491%2c8.019214999999999Q19.9015086%2c8%2c20%2c8Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M8%2c10L12.5%2c10Q12.59849%2c10%2c12.69509%2c10.019214999999999Q12.79169%2c10.03843%2c12.88268%2c10.076121Q12.97368%2c10.113812%2c13.05557%2c10.16853Q13.13746%2c10.223249%2c13.20711%2c10.292893Q13.27675%2c10.362537%2c13.33147%2c10.44443Q13.38619%2c10.526322%2c13.42388%2c10.617317Q13.46157%2c10.708311%2c13.48078%2c10.80491Q13.5%2c10.9015086%2c13.5%2c11Q13.5%2c11.0984914%2c13.48078%2c11.19509Q13.46157%2c11.291689%2c13.42388%2c11.382683Q13.38619%2c11.473678%2c13.33147%2c11.55557Q13.27675%2c11.637463%2c13.20711%2c11.707107Q13.13746%2c11.776751%2c13.05557%2c11.83147Q12.97368%2c11.886188%2c12.88268%2c11.923879Q12.79169%2c11.96157%2c12.69509%2c11.980785000000001Q12.59849%2c12%2c12.5%2c12L8%2c12Q7.9015086%2c12%2c7.80491%2c11.980785000000001Q7.708311%2c11.96157%2c7.617317%2c11.923879Q7.526322%2c11.886188%2c7.44443%2c11.83147Q7.362537%2c11.776751%2c7.292893%2c11.707107Q7.223249%2c11.637463%2c7.16853%2c11.55557Q7.113812%2c11.473678%2c7.076121%2c11.382683Q7.03843%2c11.291689%2c7.019215%2c11.19509Q7%2c11.0984914%2c7%2c11Q7%2c10.9015086%2c7.019215%2c10.80491Q7.03843%2c10.708311%2c7.076121%2c10.617317Q7.113812%2c10.526322%2c7.16853%2c10.44443Q7.223249%2c10.362537%2c7.292893%2c10.292893Q7.362537%2c10.223249%2c7.44443%2c10.16853Q7.526322%2c10.113812%2c7.617317%2c10.076121Q7.708311%2c10.03843%2c7.80491%2c10.019214999999999Q7.9015086%2c10%2c8%2c10Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/open-popup.svg":
/*!************************************!*\
  !*** ./style/image/open-popup.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='32' height='32' viewBox='0 0 32 32'%3e%3cdefs%3e%3cclipPath id='master_svg0_75_5466'%3e%3crect x='0' y='0' width='32' height='32' rx='0'/%3e%3c/clipPath%3e%3c/defs%3e%3cg clip-path='url(%23master_svg0_75_5466)'%3e%3cg%3e%3cg%3e%3cpath d='M4%2c24L4%2c8Q4%2c7.80349%2c4.0192611%2c7.60793Q4.0385222%2c7.41237%2c4.0768589%2c7.21964Q4.115196%2c7.02691%2c4.172239%2c6.83886Q4.229282%2c6.6508199999999995%2c4.304482%2c6.46927Q4.379682%2c6.28772%2c4.472315%2c6.1144099999999995Q4.564948%2c5.94111%2c4.6741209999999995%2c5.77772Q4.783295%2c5.61433%2c4.907958%2c5.4624299999999995Q5.03262%2c5.31052%2c5.17157%2c5.17157Q5.31052%2c5.03262%2c5.4624299999999995%2c4.907958Q5.61433%2c4.783295%2c5.77772%2c4.6741209999999995Q5.94111%2c4.564948%2c6.1144099999999995%2c4.472315Q6.28772%2c4.379682%2c6.46927%2c4.304482Q6.6508199999999995%2c4.229282%2c6.83886%2c4.172239Q7.02691%2c4.115196%2c7.21964%2c4.0768589Q7.41237%2c4.0385222%2c7.60793%2c4.0192611Q7.80349%2c4%2c8%2c4L22%2c4Q22.1965%2c4%2c22.3921%2c4.0192611Q22.5876%2c4.0385222%2c22.7804%2c4.0768589Q22.9731%2c4.115196%2c23.1611%2c4.172239Q23.3492%2c4.229282%2c23.5307%2c4.304482Q23.7123%2c4.379682%2c23.8856%2c4.472315Q24.0589%2c4.564948%2c24.2223%2c4.6741209999999995Q24.3857%2c4.783295%2c24.5376%2c4.907958Q24.6895%2c5.03262%2c24.8284%2c5.17157Q24.9674%2c5.31052%2c25.092%2c5.4624299999999995Q25.2167%2c5.61433%2c25.3259%2c5.77772Q25.4351%2c5.94111%2c25.5277%2c6.1144099999999995Q25.6203%2c6.28772%2c25.6955%2c6.46927Q25.7707%2c6.6508199999999995%2c25.8278%2c6.83886Q25.8848%2c7.02691%2c25.9231%2c7.21964Q25.9615%2c7.41237%2c25.9807%2c7.60793Q26%2c7.80349%2c26%2c8L26%2c16.6754Q25.0455%2c16.2227%2c24%2c16.0718L24%2c8Q24%2c6%2c22%2c6L8%2c6Q6%2c6%2c6%2c8L6%2c24Q6%2c26%2c8%2c26L16.6754%2c26Q17.21%2c27.127%2c18.101%2c28L8%2c28Q7.80349%2c28%2c7.60793%2c27.9807Q7.41237%2c27.9615%2c7.21964%2c27.9231Q7.02691%2c27.8848%2c6.83886%2c27.8278Q6.6508199999999995%2c27.7707%2c6.46927%2c27.6955Q6.28772%2c27.6203%2c6.1144099999999995%2c27.5277Q5.94111%2c27.435%2c5.77772%2c27.3259Q5.61433%2c27.2167%2c5.4624299999999995%2c27.092Q5.31052%2c26.9674%2c5.17157%2c26.8284Q5.03262%2c26.6895%2c4.907958%2c26.5376Q4.783295%2c26.3857%2c4.6741209999999995%2c26.2223Q4.564948%2c26.0589%2c4.472315%2c25.8856Q4.379682%2c25.7123%2c4.304482%2c25.5307Q4.229282%2c25.3492%2c4.172239%2c25.1611Q4.115196%2c24.9731%2c4.0768589%2c24.7804Q4.0385222%2c24.5876%2c4.0192611%2c24.3921Q4%2c24.1965%2c4%2c24Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cellipse cx='23' cy='23' rx='6' ry='6' fill-opacity='0' stroke-opacity='1' stroke='%23E8EDF7' fill='none' stroke-width='2'/%3e%3c/g%3e%3cg%3e%3cpath d='M8.5%2c11L17%2c11Q17.098489999999998%2c11%2c17.19509%2c11.019214999999999Q17.29169%2c11.03843%2c17.38268%2c11.076121Q17.47368%2c11.113812%2c17.55557%2c11.16853Q17.63746%2c11.223249%2c17.70711%2c11.292893Q17.77675%2c11.362537%2c17.83147%2c11.44443Q17.88619%2c11.526322%2c17.92388%2c11.617317Q17.961570000000002%2c11.708311%2c17.98078%2c11.80491Q18%2c11.9015086%2c18%2c12Q18%2c12.0984914%2c17.98078%2c12.19509Q17.961570000000002%2c12.291689%2c17.92388%2c12.382683Q17.88619%2c12.473678%2c17.83147%2c12.55557Q17.77675%2c12.637463%2c17.70711%2c12.707107Q17.63746%2c12.776751%2c17.55557%2c12.83147Q17.47368%2c12.886188%2c17.38268%2c12.923879Q17.29169%2c12.96157%2c17.19509%2c12.980785000000001Q17.098489999999998%2c13%2c17%2c13L8.5%2c13Q8.4015086%2c13%2c8.30491%2c12.980785000000001Q8.208311%2c12.96157%2c8.117317%2c12.923879Q8.026322%2c12.886188%2c7.94443%2c12.83147Q7.862537%2c12.776751%2c7.792893%2c12.707107Q7.723249%2c12.637463%2c7.66853%2c12.55557Q7.613812%2c12.473678%2c7.576121%2c12.382683Q7.53843%2c12.291689%2c7.519215%2c12.19509Q7.5%2c12.0984914%2c7.5%2c12Q7.5%2c11.9015086%2c7.519215%2c11.80491Q7.53843%2c11.708311%2c7.576121%2c11.617317Q7.613812%2c11.526322%2c7.66853%2c11.44443Q7.723249%2c11.362537%2c7.792893%2c11.292893Q7.862537%2c11.223249%2c7.94443%2c11.16853Q8.026322%2c11.113812%2c8.117317%2c11.076121Q8.208311%2c11.03843%2c8.30491%2c11.019214999999999Q8.4015086%2c11%2c8.5%2c11Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M8.5%2c16L15%2c16Q15.09849%2c16%2c15.19509%2c16.019215Q15.29169%2c16.038429999999998%2c15.38268%2c16.076121Q15.47368%2c16.113812%2c15.55557%2c16.16853Q15.63746%2c16.223249%2c15.70711%2c16.292893Q15.77675%2c16.362537%2c15.83147%2c16.44443Q15.88619%2c16.526322%2c15.92388%2c16.617317Q15.96157%2c16.708311%2c15.98078%2c16.80491Q16%2c16.9015086%2c16%2c17Q16%2c17.0984914%2c15.98078%2c17.19509Q15.96157%2c17.291689%2c15.92388%2c17.382683Q15.88619%2c17.473678%2c15.83147%2c17.55557Q15.77675%2c17.637463%2c15.70711%2c17.707107Q15.63746%2c17.776751%2c15.55557%2c17.83147Q15.47368%2c17.886188%2c15.38268%2c17.923879Q15.29169%2c17.961570000000002%2c15.19509%2c17.980785Q15.09849%2c18%2c15%2c18L8.5%2c18Q8.4015086%2c18%2c8.30491%2c17.980785Q8.208311%2c17.961570000000002%2c8.117317%2c17.923879Q8.026322%2c17.886188%2c7.94443%2c17.83147Q7.862537%2c17.776751%2c7.792893%2c17.707107Q7.723249%2c17.637463%2c7.66853%2c17.55557Q7.613812%2c17.473678%2c7.576121%2c17.382683Q7.53843%2c17.291689%2c7.519215%2c17.19509Q7.5%2c17.0984914%2c7.5%2c17Q7.5%2c16.9015086%2c7.519215%2c16.80491Q7.53843%2c16.708311%2c7.576121%2c16.617317Q7.613812%2c16.526322%2c7.66853%2c16.44443Q7.723249%2c16.362537%2c7.792893%2c16.292893Q7.862537%2c16.223249%2c7.94443%2c16.16853Q8.026322%2c16.113812%2c8.117317%2c16.076121Q8.208311%2c16.038429999999998%2c8.30491%2c16.019215Q8.4015086%2c16%2c8.5%2c16Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3cg%3e%3cpath d='M22%2c20Q22%2c19.9015086%2c22.019215%2c19.80491Q22.038429999999998%2c19.708311%2c22.076121%2c19.617317Q22.113812%2c19.526322%2c22.16853%2c19.44443Q22.223249%2c19.362537%2c22.292893%2c19.292893Q22.362537%2c19.223249%2c22.44443%2c19.16853Q22.526322%2c19.113812%2c22.617317%2c19.076121Q22.708311%2c19.038429999999998%2c22.80491%2c19.019215Q22.9015086%2c19%2c23%2c19Q23.0984914%2c19%2c23.19509%2c19.019215Q23.291689%2c19.038429999999998%2c23.382683%2c19.076121Q23.473678%2c19.113812%2c23.55557%2c19.16853Q23.637463%2c19.223249%2c23.707107%2c19.292893Q23.776751%2c19.362537%2c23.83147%2c19.44443Q23.886188%2c19.526322%2c23.923879%2c19.617317Q23.961570000000002%2c19.708311%2c23.980785%2c19.80491Q24%2c19.9015086%2c24%2c20L24%2c22L26%2c22Q26.098489999999998%2c22%2c26.19509%2c22.01921Q26.29169%2c22.038429999999998%2c26.38268%2c22.07612Q26.47368%2c22.11381%2c26.55557%2c22.16853Q26.63746%2c22.22325%2c26.70711%2c22.29289Q26.77675%2c22.36254%2c26.83147%2c22.44443Q26.88619%2c22.52632%2c26.92388%2c22.61732Q26.961570000000002%2c22.70831%2c26.98078%2c22.80491Q27%2c22.901510000000002%2c27%2c23Q27%2c23.098489999999998%2c26.98078%2c23.19509Q26.961570000000002%2c23.29169%2c26.92388%2c23.38268Q26.88619%2c23.47368%2c26.83147%2c23.55557Q26.77675%2c23.63746%2c26.70711%2c23.70711Q26.63746%2c23.77675%2c26.55557%2c23.83147Q26.47368%2c23.88619%2c26.38268%2c23.92388Q26.29169%2c23.961570000000002%2c26.19509%2c23.98078Q26.098489999999998%2c24%2c26%2c24L23%2c24Q22.9015086%2c24%2c22.80491%2c23.98078Q22.708311%2c23.961570000000002%2c22.617317%2c23.92388Q22.526322%2c23.88619%2c22.44443%2c23.83147Q22.362537%2c23.77675%2c22.292893%2c23.70711Q22.223249%2c23.63746%2c22.16853%2c23.55557Q22.113812%2c23.47368%2c22.076121%2c23.38268Q22.038429999999998%2c23.29169%2c22.019215%2c23.19509Q22%2c23.098489999999998%2c22%2c23L22%2c20Z' fill-rule='evenodd' fill='%23E8EDF7' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/send_botton.svg":
/*!*************************************!*\
  !*** ./style/image/send_botton.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='20.982023239135742' height='17.485055923461914' viewBox='0 0 20.982023239135742 17.485055923461914'%3e%3cdefs%3e%3clinearGradient x1='0.5' y1='0' x2='0.5' y2='1' id='master_svg0_75_3222'%3e%3cstop offset='0%25' stop-color='%23D75720' stop-opacity='1'/%3e%3cstop offset='100%25' stop-color='%23BDB0F2' stop-opacity='1'/%3e%3c/linearGradient%3e%3c/defs%3e%3cg%3e%3cpath d='M19.9484%2c0.0898518C19.9484%2c0.0898518%2c0.79289%2c7.48156%2c0.79289%2c7.48156C-0.286607%2c7.89812%2c-0.259564%2c8.50348%2c0.847932%2c8.83211C0.847932%2c8.83211%2c0.848395%2c8.83225%2c0.849312%2c8.83252C3.75086%2c9.69345%2c6.05651%2c11.9318%2c7.02068%2c14.8007C7.22097%2c15.3967%2c7.35816%2c15.8049%2c7.35816%2c15.8049C7.60453%2c16.538%2c8.24815%2c16.6925%2c8.79868%2c16.1472C8.79868%2c16.1472%2c8.79893%2c16.147%2c8.79941%2c16.1465C10.1978%2c14.7612%2c12.3931%2c14.5971%2c13.9808%2c15.7607C15.0483%2c16.543%2c16.0188%2c17.2541%2c16.0188%2c17.2541C16.6415%2c17.7104%2c17.2816%2c17.4703%2c17.4496%2c16.7129C17.4496%2c16.7129%2c20.9468%2c0.954833%2c20.9468%2c0.954833C21.1144%2c0.199672%2c20.668%2c-0.187825%2c19.9484%2c0.0898518ZM17.0333%2c3.6527C17.0333%2c3.6527%2c8.86261%2c10.9327%2c8.86261%2c10.9327C8.71569%2c11.0636%2c8.58274%2c11.323%2c8.56233%2c11.515C8.56233%2c11.515%2c8.20161%2c14.9063%2c8.20161%2c14.9063C8.1611%2c15.2871%2c8.0298%2c15.3028%2c7.9087%2c14.9378C7.9087%2c14.9378%2c6.32767%2c10.1721%2c6.32767%2c10.1721C6.26582%2c9.98566%2c6.35054%2c9.75714%2c6.5157%2c9.65809C6.5157%2c9.65809%2c16.8778%2c3.44291%2c16.8778%2c3.44291C17.5381%2c3.04685%2c17.6084%2c3.14039%2c17.0333%2c3.6527Z' fill='url(%23master_svg0_75_3222)' fill-opacity='1'/%3e%3c/g%3e%3c/svg%3e";

/***/ }),

/***/ "./style/image/toggle-sidebar.svg":
/*!****************************************!*\
  !*** ./style/image/toggle-sidebar.svg ***!
  \****************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "9591665ae5747407f855.svg";

/***/ }),

/***/ "./style/image/user_img.svg":
/*!**********************************!*\
  !*** ./style/image/user_img.svg ***!
  \**********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "934aca7d3f24ac6b8dbd.svg";

/***/ }),

/***/ "./style/image/x_circle.svg":
/*!**********************************!*\
  !*** ./style/image/x_circle.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' fill='none' version='1.1' width='18' height='18' viewBox='0 0 18 18'%3e%3cdefs%3e%3cclipPath id='master_svg0_211_19413'%3e%3crect x='0' y='0' width='18' height='18' rx='0'/%3e%3c/clipPath%3e%3c/defs%3e%3cg clip-path='url(%23master_svg0_211_19413)'%3e%3cg transform='matrix(0.7071067690849304%2c-0.7071067690849304%2c0.7071067690849304%2c0.7071067690849304%2c-7.970252357801655%2c7.242483239067951)'%3e%3cpath d='M4.75732421875%2c12.7421875L16.75732421875%2c12.7421875Q16.80652421875%2c12.7421875%2c16.85482421875%2c12.7517945Q16.90312421875%2c12.761402499999999%2c16.94862421875%2c12.7802475Q16.994124218750002%2c12.7990935%2c17.03512421875%2c12.8264525Q17.07602421875%2c12.8538125%2c17.11092421875%2c12.8886345Q17.14572421875%2c12.9234565%2c17.17302421875%2c12.9644025Q17.20042421875%2c13.0053485%2c17.21922421875%2c13.0508455Q17.238124218750002%2c13.0963425%2c17.24772421875%2c13.1446424Q17.25732421875%2c13.1929418%2c17.25732421875%2c13.2421875Q17.25732421875%2c13.2914332%2c17.24772421875%2c13.3397326Q17.238124218750002%2c13.3880325%2c17.21922421875%2c13.4335295Q17.20042421875%2c13.4790265%2c17.17302421875%2c13.5199725Q17.14572421875%2c13.5609185%2c17.11092421875%2c13.5957405Q17.07602421875%2c13.6305625%2c17.03512421875%2c13.6579225Q16.994124218750002%2c13.6852815%2c16.94862421875%2c13.7041275Q16.90312421875%2c13.722972500000001%2c16.85482421875%2c13.7325805Q16.80652421875%2c13.7421875%2c16.75732421875%2c13.7421875L4.75732421875%2c13.7421875Q4.70807851875%2c13.7421875%2c4.65977911875%2c13.7325805Q4.61147921875%2c13.722972500000001%2c4.56598221875%2c13.7041275Q4.52048521875%2c13.6852815%2c4.47953921875%2c13.6579225Q4.43859321875%2c13.6305625%2c4.40377121875%2c13.5957405Q4.36894921875%2c13.5609185%2c4.34158921875%2c13.5199725Q4.31423021875%2c13.4790265%2c4.29538421875%2c13.4335295Q4.27653921875%2c13.3880325%2c4.26693121875%2c13.3397326Q4.25732421875%2c13.2914332%2c4.25732421875%2c13.2421875Q4.25732421875%2c13.1929418%2c4.26693121875%2c13.1446424Q4.27653921875%2c13.0963425%2c4.29538421875%2c13.0508455Q4.31423021875%2c13.0053485%2c4.34158921875%2c12.9644025Q4.36894921875%2c12.9234565%2c4.40377121875%2c12.8886345Q4.43859321875%2c12.8538125%2c4.47953921875%2c12.8264525Q4.52048521875%2c12.7990935%2c4.56598221875%2c12.7802475Q4.61147921875%2c12.761402499999999%2c4.65977911875%2c12.7517945Q4.70807851875%2c12.7421875%2c4.75732421875%2c12.7421875Z' fill-rule='evenodd' fill='%23EEEEEE' fill-opacity='1'/%3e%3c/g%3e%3cg transform='matrix(0.7071067690849304%2c0.7071067690849304%2c0.7071067690849304%2c-0.7071067690849304%2c-1.9705480968696065%2c4.75732421875)'%3e%3cpath d='M4.75732421875%2c4.25732421875L16.75732421875%2c4.25732421875Q16.80652421875%2c4.25732421875%2c16.85482421875%2c4.26693121875Q16.90312421875%2c4.27653921875%2c16.94862421875%2c4.29538421875Q16.994124218750002%2c4.31423021875%2c17.03512421875%2c4.34158921875Q17.07602421875%2c4.36894921875%2c17.11092421875%2c4.40377121875Q17.14572421875%2c4.43859321875%2c17.17302421875%2c4.47953921875Q17.20042421875%2c4.52048521875%2c17.21922421875%2c4.56598221875Q17.238124218750002%2c4.61147921875%2c17.24772421875%2c4.65977911875Q17.25732421875%2c4.70807851875%2c17.25732421875%2c4.75732421875Q17.25732421875%2c4.80656991875%2c17.24772421875%2c4.85486931875Q17.238124218750002%2c4.90316921875%2c17.21922421875%2c4.94866621875Q17.20042421875%2c4.99416321875%2c17.17302421875%2c5.03510921875Q17.14572421875%2c5.07605521875%2c17.11092421875%2c5.11087721875Q17.07602421875%2c5.14569921875%2c17.03512421875%2c5.17305921875Q16.994124218750002%2c5.20041821875%2c16.94862421875%2c5.21926421875Q16.90312421875%2c5.23810921875%2c16.85482421875%2c5.24771721875Q16.80652421875%2c5.25732421875%2c16.75732421875%2c5.25732421875L4.75732421875%2c5.25732421875Q4.70807851875%2c5.25732421875%2c4.65977911875%2c5.24771721875Q4.61147921875%2c5.23810921875%2c4.56598221875%2c5.21926421875Q4.52048521875%2c5.20041821875%2c4.47953921875%2c5.17305921875Q4.43859321875%2c5.14569921875%2c4.40377121875%2c5.11087721875Q4.36894921875%2c5.07605521875%2c4.34158921875%2c5.03510921875Q4.31423021875%2c4.99416321875%2c4.29538421875%2c4.94866621875Q4.27653921875%2c4.90316921875%2c4.26693121875%2c4.85486931875Q4.25732421875%2c4.80656991875%2c4.25732421875%2c4.75732421875Q4.25732421875%2c4.70807851875%2c4.26693121875%2c4.65977911875Q4.27653921875%2c4.61147921875%2c4.29538421875%2c4.56598221875Q4.31423021875%2c4.52048521875%2c4.34158921875%2c4.47953921875Q4.36894921875%2c4.43859321875%2c4.40377121875%2c4.40377121875Q4.43859321875%2c4.36894921875%2c4.47953921875%2c4.34158921875Q4.52048521875%2c4.31423021875%2c4.56598221875%2c4.29538421875Q4.61147921875%2c4.27653921875%2c4.65977911875%2c4.26693121875Q4.70807851875%2c4.25732421875%2c4.75732421875%2c4.25732421875Z' fill-rule='evenodd' fill='%23EEEEEE' fill-opacity='1'/%3e%3c/g%3e%3c/g%3e%3c/svg%3e";

/***/ })

}]);
//# sourceMappingURL=style_index_js.29dffbb8de26f47d18f6.js.map