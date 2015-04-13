var KokuaObject = (function () {
    var Kokua = function () {

        var xhr = new XMLHttpRequest();

        this.init = function(siteId) {
            if (!getCookie('first_visit')) {
                setCookie('js_id', randomId());
                var params = {
                    resolution: {width: screen.width, height: screen.height},
                    lang: (navigator.language || navigator.browserLanguage || '').substr(0, 2),
                    protocol: location.protocol.substr(0, location.protocol.length - 1),
                    port: location.port,
                    domain: location.hostname,
                    href: encodeURIComponent(location.pathname + location.search),
                    param: location.search,
                    referer: encodeURIComponent(location.origin)
                };
                sendParams(params);
            }
            setCookie('first_visit', false, 60 * 15);

            this.startTracker();

            this.siteId = siteId;
            this.jsId = getCookie('js_id');
        };

        this.startTracker = function () {
            var that = this;
            document.onmousemove = debounce(function (event) {
                var params = {
                    type: 'mouse_move',
                    position: {
                        x: event.clientX,
                        y: event.clientY
                    }
                };
                sendParams.call(that, params);
            }, 100);

            document.onclick = function (event) {
                var params = {
                    type: event.type,
                    target: event.target.localName,
                    position: {
                        x: event.clientX,
                        y: event.clientY
                    }
                };
                sendParams.call(that, params);
            }
        };

        function sendParams(params) {
            xhr.open('POST', '/sauron');
            xhr.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
            params.site_id = this.siteId;
            params.js_id = this.jsId;
            xhr.send(JSON.stringify(params));
        }

        function getCookie(name) {
            var ca = document.cookie.split(';');
            for (var i = 0, l = ca.length; i < l; i++) {
                if (ca[i].match(new RegExp("\\b" + name + "="))) return decodeURIComponent(ca[i].split(name + '=')[1]);
            }
            return '';
        }

        function setCookie(name, value, expires) {
            var ex = new Date;
            ex.setTime(ex.getTime() + (expires || 20 * 365 * 86400) * 1000);
            document.cookie = name + "=" + value + ";expires=" + ex.toGMTString() + ";path=/;";
        }

        function randomId() {
            var i = 0;
            do {
                var r = Math.round(Math.random() * 4294967295);
            } while (r == 1421816160 && i++ < 100);
            return r;
        }

        function debounce(fn, delay) {
            var timer = null;

            return function () {
                var context = this;
                var args = arguments;

                clearTimeout(timer);
                timer = setTimeout(function () {
                   fn.apply(context, args);
                }, delay);
            };
        }
    };

    var instance = null;
    return new function () {
        this.getInstance = function () {
            if (instance == null) {
                instance = new Kokua();
                instance.constructeur = null;
            }

            return instance;
        }
    }
})();

var kokua = KokuaObject.getInstance();
kokua.init('1ed98kloix');
