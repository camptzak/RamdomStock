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
