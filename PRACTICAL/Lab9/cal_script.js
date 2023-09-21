document.addEventListener("DOMContentLoaded", function() {
    const result = document.getElementById("result");
    let displayString = "";
    const accpeted = ["0","1","2","3","4","5","6","7","8","9",".","+","-","*","/","(",")"]
    document.addEventListener("keypress", function(e) {
        if (e.key == "<"){
            displayString = displayString.slice(0, -1);
        } else if (e.key == "c"){
            displayString = "";
        } else if (e.key == "=" || e.key == "Enter"){
            displayString = eval(displayString);
            displayString = displayString.toString();
        } else if (accpeted.includes(e.key)){
            displayString += e.key;
        } else {
            return;
        }        
        result.innerHTML = displayString;
    });
});