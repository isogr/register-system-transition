function s(i) { return (new Date(i * 1000).toISOString()).split(/\.\d*/).join(''); }
var scrapeStart = s(1707185673);
var scrapeEnd = s(1707193601);
var scrapeText = '<span id="scrape-timing">';
scrapeText += '<a href="https://github.com/isogr/register-system-transition/tree/main/isogr-snapshooter" target="_blank">Page scraped</a> from <span title="1707185673">' + scrapeStart + '</span> to <span title="1707193601">' + scrapeEnd + '</span>';
scrapeText += ' by <a href="https://github.com/isogr/register-system-transition/tree/main/isogr-snapshooter" target="_blank">isogr-snapshooter</a>.';
scrapeText += '</span>';
document.querySelector('footer p.text-muted').innerHTML += '<span>(' + scrapeText + ')</span>';
