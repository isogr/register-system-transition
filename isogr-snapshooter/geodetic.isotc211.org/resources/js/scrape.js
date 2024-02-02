function s(i) { return (new Date(i * 1000).toISOString()).split(/\.\d*/).join(''); }
var scrapeStart = s(1706840039);
var scrapeEnd = s(1706848714);
var scrapeText = '<span id="scrape-timing">';
scrapeText += '<a href="" target="_blank">Page scraped</a> from <span title="1706840039">' + scrapeStart + '</span> to <span title="1706848714">' + scrapeEnd + '</span>';
scrapeText += ' by <a href="" target="_blank">isogr-snapshooter</a>.';
scrapeText += '</span>';
document.querySelector('footer p.text-muted').innerHTML += '<span>(' + scrapeText + ')</span>';
