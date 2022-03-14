!function(){function e(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function t(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}function n(e,n){return function(e){if(Array.isArray(e))return e}(e)||t(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}var o="cookies_policy",i=function(e,t,n){void 0===n&&(n={});var o=e+"="+t+"; path=/";if(n.days){var i=new Date;i.setTime(i.getTime()+864e5*n.days),o=o+"; expires="+i.toGMTString()}"https:"===document.location.protocol&&(o+="; Secure"),document.cookie=o},r=function(){"use strict";function t(e,n,o){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),this.formSelector=e,this.confirmationSelector=n,this.radioButtons=o,this.form=document.querySelector(this.formSelector)}var r,a,s;return r=t,(a=[{key:"boolToValue",value:function(e){return e?"on":"off"}},{key:"valueToBool",value:function(e){return"on"===e}},{key:"getPolicyOrDefault",value:function(){var e=function(e){for(var t=e+"=",n=document.cookie.split(";"),o=0,i=n.length;o<i;o++){for(var r=n[o];" "===r.charAt(0);)r=r.substring(1,r.length);if(0===r.indexOf(t))return decodeURIComponent(r.substring(t.length))}return null}(o),t={essential:!0,settings:!1,usage:!1,campaigns:!1};if(!e)return t;try{var n=JSON.parse(e);t.campaigns=n.campaigns||!1,t.usage=n.usage||!1,t.settings=n.settings||!1}catch(e){return t}return t}},{key:"initFormValues",value:function(){var e=this,t=this.getPolicyOrDefault();Object.entries(this.radioButtons).forEach((function(o){var i=n(o),r=i[0],a=i[1];e.form[a].value=e.boolToValue(t[r])}))}},{key:"setPoliciesCookie",value:function(){var e=this,t={settings:!1,usage:!1,campaigns:!1};Object.entries(this.radioButtons).forEach((function(o){var i=n(o),r=i[0],a=i[1];t[r]=e.valueToBool(e.form[a].value)})),function(e,t,n){var r={essential:!0,settings:!1,usage:!1,campaigns:!1};r.settings=e||!1,r.usage=t||!1,r.campaigns=n||!1;var a=JSON.stringify(r);i(o,a,{days:365})}(t.settings,t.usage,t.campaigns)}},{key:"displayConfirmation",value:function(){document.querySelector(this.confirmationSelector).style.display="block"}},{key:"bindForm",value:function(){var e=this;this.form.addEventListener("submit",(function(t){return t.preventDefault(),e.setPoliciesCookie(),i("cookie_preferences_set","true",{days:365}),e.displayConfirmation(),window.scrollTo(0,0),!1}))}}])&&e(r.prototype,a),s&&e(r,s),t}();(function(e,t,n){var o=new r(e,t,n);o.initFormValues(),o.bindForm()})("#cookie-preferences-form",".cookie-settings__confirmation",{usage:"cookies-usage"})}();
//# sourceMappingURL=cookie-policy-form.js.map
