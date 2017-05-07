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
    parseRSS('http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/teams/m/man_utd/rss.xml', function (data) {
        var news_vm = new NewsVM(data);
        var news_block = $('#news-block')[0];
        //ko.cleanNode(news_block);
        ko.applyBindings(news_vm, news_block);
    })
});