
function twitter(){
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://twitter.com/share?text=" + "ACT Symbol: " + symbol + "%0a" + "Company: " + company + "%0a" + "&url=" + currentPageUrl + "&hashtags=RandomStock")
};

function facebook() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("https://www.facebook.com/sharer/sharer.php?u=" + currentPageUrl + "&quote= ACT Symbol: " + symbol + "%0a" + "Company: " + company)
}

function instagram() {
  window.open("https://www.instagram.com")
}

function reddit() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://www.reddit.com/submit?url=ACT Symbol: " + symbol + "%0a" + "Company: " + company + "%0a" +"randomstock.net%0a&title=Random%20Stock")
}

function linkedin() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://www.linkedin.com/feed")
}

// coin javascript functions

function twitterCoin(){
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://twitter.com/share?text=" + "Symbol: " + symbol + "%0a" + "Coin: " + company + "%0a" + "&url=" + currentPageUrl + "&hashtags=RandomStock")
};

function facebookCoin() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("https://www.facebook.com/sharer/sharer.php?u=" + currentPageUrl + "&quote=Symbol: " + symbol + "%0a" + "Coin: " + company)
}

function instagramCoin() {
  window.open("https://www.instagram.com")
}

function redditCoin() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://www.reddit.com/submit?url=Symbol: " + symbol + "%0a" + "Coin: " + company + "%0a" +"randomstock.net%0a&title=Random%20Stock")
}

function linkedinCoin() {
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://www.linkedin.com/feed")
}