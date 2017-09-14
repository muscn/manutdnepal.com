$(function () {
  var config = {
    'domain': 'reddevils',
    'show_sticky': false,
    'num_threads': 6,
    'allow_internal': false,
    'upvoted_only': true
  };
  var reddit_vm = new RedditVM(config);
  ko.applyBindings(reddit_vm, $('#reddit-block')[0]);
});

function ThreadVM(data) {
  var self = this;
  if (data.thumbnail != 'self' && data.thumbnail != 'default') {
    self.thumbnail = data.thumbnail;
    self.internal = false;
  }
  else {
    self.internal = true;
  }

  var prefix_url = 'https://reddit.com/'
  self.url = data.url;
  self.sticky = data.stickied;
  self.title = $('<textarea />').html(data.title).text(); //decodes HTML entities
  self.date = new Date(data.created_utc * 1000);
  self.date_str = self.date.toString().slice(0, -15);
  self.author = data.author;
  self.author_url = prefix_url + 'u/' + self.author;
  self.permalink = prefix_url + data.permalink;
  self.score = data.score;
  self.over_18 = data.over_18;
  self.num_comments = data.num_comments;
  self.domain = data.domain;
  self.selftext = data.selftext;

  if (self.selftext) {
    self.text = self.selftext;
  } else {
    self.text = self.title;
  }
}

function RedditVM(config) {
  var config_defaults = {
    'show_sticky': true,
    'num_threads': 10,
    'allow_internal': true,
    'allowed_domains': [], //empty means allow all domains
    'blocked_domains': [], //empty means block no domains
    'upvoted_only': false,
  };

  var self = this;

  self.config = $.extend(config_defaults, config);

  if (config.allow_internal && config.allowed_domains) {
    self.config.allowed_domains.push('self.' + config.domain);
  }

  self.threads = ko.observableArray();


  $.getJSON(
    "https://www.reddit.com/r/" + config.domain + ".json?jsonp=?",
    function foo(data) {
      var max = self.config.num_threads;
      var cnt = 0;
      var threads = [];
      $.each(
        data.data.children,
        function (i, thread) {
          var to_add = true;
          if (!self.config.allow_internal && thread.data.domain.toLowerCase() == 'self.' + config.domain.toLowerCase()) {
            return true;
          }
          if (!self.config.show_sticky && thread.data.stickied) {
            return true;
          }
          if (self.config.allowed_domains.length && self.config.allowed_domains.indexOf(thread.data.domain) == -1) {
            return true;
          }
          if (self.config.blocked_domains.length && self.config.blocked_domains.indexOf(thread.data.domain) != -1) {
            return true;
          }

          if (self.config.upvoted_only && thread.data.domain < 1) {
            return true;
          }
          if (to_add) {
            threads.push(new ThreadVM(thread.data));
            cnt++;
            if (cnt >= max)
              return false;
          }
        }
      );
      ko.utils.arrayPushAll(self.threads, threads);
    }
  )
}

function NewsVM(data) {
  var self = this;
  self.entries = data;
}

function parseRSS(url, callback) {
  $.ajax({
    url: 'https://api.rss2json.com/v1/api.json?rss_url=' + encodeURIComponent(url),
    dataType: 'json',
    success: function (data) {
      callback(data.items);
    }
  });
}

$(function () {
  parseRSS('http://talksport.com/rss/football/manchester-united/feed', function (data) {
    var news_vm = new NewsVM(data);
    var news_block = $('#news-block')[0];
    //ko.cleanNode(news_block);
    ko.applyBindings(news_vm, news_block);
  })
});

(function (d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s);
  js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.4&appId=745752022186281";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));