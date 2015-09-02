function NewsVM(data) {
    var self = this;
    self.entries = data.entries;
}

function parseRSS(url, callback) {
    $.ajax({
        url: document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&callback=?&q=' + encodeURIComponent(url),
        dataType: 'json',
        success: function (data) {
            callback(data.responseData.feed);
        }
    });
}

$(function () {
    parseRSS('http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/teams/m/man_utd/rss.xml', function (data) {
        var news_vm = new NewsVM(data);
        var news_block = $('#news-block')[0];
        //ko.cleanNode(news_block);
        ko.applyBindings(news_vm, news_block);
    })
});