let displayString = "";
document.addEventListener("DOMContentLoaded", function() {
    const result = document.getElementById("result");

    if (localStorage.getItem("displayString") == null) {
        localStorage.setItem("displayString", "0");
    }
    
    const accpeted = ["0","1","2","3","4","5","6","7","8","9",".","+","-","*","/","(",")"]
    document.querySelectorAll("td").forEach(function(td) {
        td.addEventListener("click", function() {
            if (accpeted.includes(td.id)) {
                displayString += td.innerHTML;
                result.innerHTML = displayString;
            } else if (td.id == "c") {
                displayString = "";
                result.innerHTML = displayString;
            } else if (td.id == "Backspace") {
                displayString = displayString.slice(0, -1);
                result.innerHTML = displayString;
            } else if (td.id == "Enter") {
                calculate();
                result.innerHTML = displayString;
            }
        });
    });

    document.getElementById("sin").addEventListener("click", function() {
        calculate();
        displayString = Math.sin(displayString).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("cos").addEventListener("click", function() {
        calculate();
        displayString = Math.cos(displayString).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("tan").addEventListener("click", function() {
        calculate();
        displayString = Math.tan(displayString).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("pi").addEventListener("click", function() {
        displayString += Math.PI.toString();
        result.innerHTML = displayString;
    });

    document.getElementById("sqrt").addEventListener("click", function() {
        calculate();
        displayString = Math.sqrt(displayString).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("square").addEventListener("click", function() {
        calculate();
        displayString = Math.pow(displayString, 2).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("1/x").addEventListener("click", function() {
        calculate();
        displayString = (1/parseFloat(displayString)).toString();
        result.innerHTML = displayString;
    });

    document.getElementById("factorial").addEventListener("click", function() {
        calculate();
        displayString = factorial(displayString);
        result.innerHTML = displayString;
    });

    document.getElementById("mc").addEventListener("click", function() {
        localStorage.setItem("displayString", "0");
    });

    document.getElementById("m+").addEventListener("click", function() {
        let last = localStorage.getItem("displayString");
        displayString = eval(last + "+" + result.innerHTML).toString();
        result.innerHTML = displayString;
        localStorage.setItem("displayString", displayString);
    });

    document.getElementById("m-").addEventListener("click", function() {
        let last = localStorage.getItem("displayString");
        displayString = eval(result.innerHTML + "-" + last).toString();
        result.innerHTML = displayString;
        localStorage.setItem("displayString", displayString);
    });

    document.getElementById("mr").addEventListener("click", function() {
        displayString = localStorage.getItem("displayString");
        result.innerHTML = displayString;
    });

});

function factorial(n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n-1);
    }
}

function calculate(){
    try {
        displayString = eval(displayString);
        displayString = displayString.toString();
    } catch (e) {
        displayString = "Error";
    }
}