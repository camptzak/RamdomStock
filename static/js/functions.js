// share button functions
function twitter(){
  let symbol = document.getElementById("symbol").innerHTML;
  let company = document.getElementById("company").innerHTML;
  const currentPageUrl = window.location.href;
  window.open("http://twitter.com/share?text=" + "ACT Symbol: " + symbol + "%0a" + "Company: " + company + "%0a" + "&url=" + currentPageUrl + "&hashtags=RandomStock")
}

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
}

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


// Asynchronous Buttons
function indexButton() {

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

       var response = JSON.parse(xhttp.responseText)
       document.getElementById("symbol").innerHTML = response.symbol;
       document.getElementById("company").innerHTML = response.company;
       document.getElementById("exchange").innerHTML = response.exchange;

       document.getElementById("analysisIndex").href = foo
    }
};

xhttp.open("GET", "/_indexButton", true);
xhttp.send();
}


function pennyButton() {

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

       var response = JSON.parse(xhttp.responseText)
       document.getElementById("symbol").innerHTML = response.symbol;
       document.getElementById("company").innerHTML = response.company;
    }
};
xhttp.open("GET", "/_pennyButton", true);
xhttp.send();
}

function cryptoButton() {

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

       var response = JSON.parse(xhttp.responseText)
       document.getElementById("symbol").innerHTML = response.symbol;
       document.getElementById("company").innerHTML = response.company;
       document.getElementById("lookup").innerHTML = response.lookup;
    }
};
xhttp.open("GET", "/_cryptoButton", true);
xhttp.send();
}

//Checkbox scripts
function indexButtonPost() {
    const AMEX = document.getElementById("AMEX").checked;
    const LSE = document.getElementById("LSE").checked;
    const NASDAQ = document.getElementById("NASDAQ").checked;
    const NYSE = document.getElementById("NYSE").checked;
    const SGX = document.getElementById("SGX").checked;

    var list = [];

    if (AMEX == true){
        list.push("AMEX=true")
    }
    else {
        list.push("AMEX=false")
    }


    if (LSE == true){
        list.push("LSE=true")
    }
    else {
        list.push("LSE=false")
    }


    if (NASDAQ == true){
        list.push("NASDAQ=true")
    }
    else {
        list.push("NASDAQ=false")
    }


    if (NYSE == true){
        list.push("NYSE=true")
    }
    else {
        list.push("NYSE=false")
    }


    if (SGX == true){
        list.push("SGX=true")
    }
    else {
        list.push("SGX=false")
    }

    var result = list.join("&");


    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

           var response = JSON.parse(xhttp.responseText);
           document.getElementById("symbol").innerHTML = response.symbol;
           document.getElementById("company").innerHTML = response.company;
           document.getElementById("exchange").innerHTML = response.exchange;

        }
    };

    xhttp.open("POST", "/_indexButton", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(result);
    }


// Stock Quote script
function stockQuote() {


    var list = [];

    let exchange = document.getElementById("exchange").innerText;
    list.push("exchange=" + exchange);

    let symbol = document.getElementById("symbol").innerText;
    list.push("symbol=" + symbol);
    var result = list.join("&");

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            var my = window.open('/analysis', '_blank');
            var response = JSON.parse(xhttp.responseText);

            my.onload = function () {

                 my.document.getElementById("symbol").innerHTML = response.symbol;
                 my.document.getElementById("exchange").innerHTML = response.exchange;

            };

        }
    };

    xhttp.open("POST", "/_analysis", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(result);
}


// Coinbase Quote
function coinQuote(){

    let lookup = document.getElementById("lookup").innerHTML;
    window.open("https://www.coinbase.com/price/" + lookup)

    }

