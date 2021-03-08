// showing stocks info on homepage
$("#reload").click(function () {
    $.ajax({
        url: "",
        type: "POST",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            'amex': $('#amex').is(":checked"),
            'nasdaq': $('#nasdaq').is(":checked"),
            'lse': $('#lse').is(":checked"),
            'nyse': $('#nyse').is(":checked"),
            'sgx': $('#sgx').is(":checked")
        },
        success: function (result) {
            console.log(result);
            document.getElementById("symbol").innerHTML = result.symbol;
            document.getElementById("name").innerHTML = result.company_name;
            document.getElementById("listed_on").innerHTML = result.listed_on
        },
        error: function (result) {
            console.log(result);
        }
    });
});

function getURL() {
    var url = window.location.href;
    var arr = url.split("/");
    return (arr[0] + "//" + arr[2]);
}

function slideToElementById(elementId) {
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#" + elementId).offset().top
    }, 500);
}

function showToaster(msg, time, alertClass) {
    const toasterID = "my-toaster";
    $("#" + toasterID).addClass(alertClass);
    $("#" + toasterID).html(msg);
    $("#" + toasterID).slideDown();
    setTimeout(function () {
        $("#" + toasterID).slideUp();
    }, time);
}

// this function takes toaster id to toggle any other toaster (if required)
function showToaster2(msg, time, alertClass, id) {
    const toasterID = id;
    $("#" + toasterID).removeClass("alert-danger");
    $("#" + toasterID).removeClass("alert-success");
    $("#" + toasterID).addClass(alertClass);
    $("#" + toasterID).html(msg);
    $("#" + toasterID).slideDown();
    setTimeout(function () {
        $("#" + toasterID).slideUp();
    }, time);
}

// loader for ajax requests and responses
function loader(flag) {
    if (flag) {
        // alert(flag);
        $(".my-loader-section").removeClass("hide");
        $(".main-section").addClass("make-main-section-unclickable");
    } else {
        // alert(flag);
        $(".my-loader-section").addClass("hide");
        $(".main-section").removeClass("make-main-section-unclickable");
    }
}

// [START] BUTTONS CODE

// share button functions
function twitter() {
    if (getURLLastSegment() == "crypto") {
        twitterCoin();
    } else {
        let symbol = document.getElementById("symbol").innerHTML;
        let company = document.getElementById("name").innerHTML;
        const currentPageUrl = window.location.href;
        window.open("http://twitter.com/share?text=" + "ACT Symbol: " + symbol + "%0a" + "Company: " + company + "%0a" + "&url=" + currentPageUrl + "&hashtags=RandomStock")
    }
}

function facebook() {
    if (getURLLastSegment() == "crypto") {
        facebookCoin();
    } else {
        let symbol = document.getElementById("symbol").innerHTML;
        let company = document.getElementById("name").innerHTML;
        const currentPageUrl = window.location.href;
        window.open("https://www.facebook.com/sharer/sharer.php?u=" + currentPageUrl + "&quote= ACT Symbol: " + symbol + "%0a" + "Company: " + company)
    }
}

function instagram() {
    if (getURLLastSegment() == "crypto") {
        instagramCoin();
    } else {
        window.open("https://www.instagram.com")
    }
}

function reddit() {
    if (getURLLastSegment() == "crypto") {
        redditCoin();
    } else {
        let symbol = document.getElementById("symbol").innerHTML;
        let company = document.getElementById("name").innerHTML;
        const currentPageUrl = window.location.href;
        window.open("http://www.reddit.com/submit?url=ACT Symbol: " + symbol + "%0a" + "Company: " + company + "%0a" + "randomstock.net%0a&title=Random%20Stock")
    }
}

function linkedin() {
    if (getURLLastSegment() == "crypto") {
        linkedinCoin()
    } else {
        let symbol = document.getElementById("symbol").innerHTML;
        let company = document.getElementById("name").innerHTML;
        const currentPageUrl = window.location.href;
        window.open("http://www.linkedin.com/feed")
    }
}

function getURLLastSegment() {
    const url = window.location.href;
    let arr = url.split("/");
    if (arr[3] != null || arr[3] != undefined || arr[3] != "") {
        return arr[3];
    } else {
        return false;
    }

}

// coin javascript functions
function twitterCoin() {
    let symbol = document.getElementById("symbol").innerHTML;
    let company = document.getElementById("name").innerHTML;
    const currentPageUrl = window.location.href;
    window.open("http://twitter.com/share?text=" + "Symbol: " + symbol + "%0a" + "Coin: " + company + "%0a" + "&url=" + currentPageUrl + "&hashtags=RandomStock")
}

function facebookCoin() {
    let symbol = document.getElementById("symbol").innerHTML;
    let company = document.getElementById("name").innerHTML;
    const currentPageUrl = window.location.href;
    window.open("https://www.facebook.com/sharer/sharer.php?u=" + currentPageUrl + "&quote=Symbol: " + symbol + "%0a" + "Coin: " + company)
}

function instagramCoin() {
    window.open("https://www.instagram.com")
}

function redditCoin() {
    let symbol = document.getElementById("symbol").innerHTML;
    let company = document.getElementById("name").innerHTML;
    const currentPageUrl = window.location.href;
    window.open("http://www.reddit.com/submit?url=Symbol: " + symbol + "%0a" + "Coin: " + company + "%0a" + "randomstock.net%0a&title=Random%20Stock")
}

function linkedinCoin() {
    let symbol = document.getElementById("symbol").innerHTML;
    let company = document.getElementById("name").innerHTML;
    const currentPageUrl = window.location.href;
    window.open("http://www.linkedin.com/feed")
}


// Stock Quote script
function stockQuote() {

    let exchange = document.getElementById("listed_on").innerText;
    let symbol = document.getElementById("symbol").innerText;

    if (exchange === 'SGX') {
        window.open("https://www.tradingview.com/symbols/SGX-:" + symbol)
    } else if (exchange === 'LSE') {
        window.open("https://www.tradingview.com/symbols/LSE-" + symbol)
    } else {
        // symbol value has already been set inside form, input field is hidden
        $("#hiddenFormForAnalysis").submit();
    }
}


// Coinbase Quote
function coinQuote() {
    let lookup = document.getElementById("lookup").innerHTML;
    window.open("https://www.coinbase.com/price/" + lookup)
}

// [END] BUTTONS CODE




