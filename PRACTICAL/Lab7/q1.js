var current = new Date(2023, 8, 7, 8, 50, 0);
function AlertTime(time, message){
    this.time = time;
    this.message = message;
}

function displayTable(array){
    const tablectn = document.getElementById("alert-table");
    tablectn.innerHTML = "";
    const table = document.createElement("table");
    const tr = document.createElement("tr");
    const th1 = document.createElement("th");
    const th2 = document.createElement("th");
    th1.innerHTML = "Time";
    th2.innerHTML = "Alert Word";
    tr.appendChild(th1);
    tr.appendChild(th2);
    table.appendChild(tr);

    for (let i = 0; i < array.length; i++) {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        const td2 = document.createElement("td");
        td1.innerHTML = array[i].time.toLocaleTimeString("en-US", {hour: '2-digit', minute:'2-digit', hour12: false});
        td2.innerHTML = array[i].message;
        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);
    }
    tablectn.appendChild(table);
}

function displayForm(array){
    const tablectn = document.getElementById("alert-table");
    tablectn.innerHTML = "";
    const table = document.createElement("table");

    for (let i = 0; i < array.length; i++) {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        const td2 = document.createElement("td");
        const td3 = document.createElement("td");

        const timeinput = document.createElement("input");
        const messageinput = document.createElement("input");
        const removebtn = document.createElement("input");
        

        timeinput.setAttribute("type", "time");
        timeinput.setAttribute("value", array[i].time.toLocaleTimeString("en-US", {hour: '2-digit', minute:'2-digit', hour12: false}));

        messageinput.setAttribute("type", "text");
        messageinput.setAttribute("value", array[i].message);

        removebtn.setAttribute("type", "button");
        removebtn.setAttribute("value", "Remove");


        removebtn.addEventListener("click", function(e){
            array.splice(i, 1);
            displayForm(array);
        });

        td1.appendChild(timeinput);
        td2.appendChild(messageinput);
        td3.appendChild(removebtn);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        table.appendChild(tr);
    }
    const addrowbtn = document.createElement("input");
    addrowbtn.setAttribute("type", "button");
    addrowbtn.setAttribute("value", "Add Row");
    addrowbtn.addEventListener("click", function(){
        save();
        array.push(new AlertTime(new Date(current.getFullYear(), current.getMonth(), current.getDate(), 0, 0, 0), ""));
        displayForm(array);
    });
    tablectn.appendChild(table);
    tablectn.appendChild(addrowbtn);
}

function updateTime(){

    const timectn = document.getElementById("current-time");
    timectn.innerHTML = "Current time: " + current.getHours() + ":" + current.getMinutes();
    current = new Date(current.getTime() + 1000);
}

function save(){
    const table = document.getElementById("alert-table").getElementsByTagName("table")[0];
    const rows = table.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
        const tds = rows[i].getElementsByTagName("td");
        alertTime[i].time = new Date(current.getFullYear(), current.getMonth(), current.getDate(), tds[0].getElementsByTagName("input")[0].value.split(":")[0], tds[0].getElementsByTagName("input")[0].value.split(":")[1], 0);
        alertTime[i].message = tds[1].getElementsByTagName("input")[0].value;
    }

    alertTime.sort(function(a, b){
        return a.time.getTime() - b.time.getTime();
    });
}

function run(){

    updateTime();
    for (let i = 0; i < alertTime.length; i++) {
        if(current.getTime() == alertTime[i].time.getTime()){
            alert(alertTime[i].message);
        }
    }

   
}

var alertTime = [
    new AlertTime(new Date(current.getFullYear(), current.getMonth(), current.getDate(), 9, 0, 0), "Wake up!"),
    new AlertTime(new Date(current.getFullYear(), current.getMonth(), current.getDate(), 12, 0, 0), "Lunch time!"),
    new AlertTime(new Date(current.getFullYear(), current.getMonth(), current.getDate(), 15, 30, 0), "Take a break!"),
]

document.addEventListener("DOMContentLoaded", function(){
    displayTable(alertTime);
    const edit = document.getElementById("edit");
    edit.addEventListener("click", function(e){
        if(e.target.value == "Edit"){
            displayForm(alertTime);
            e.target.value = "Save";
        }else{
            save();
            displayTable(alertTime);
            e.target.value = "Edit";
        }
    });
    setInterval(run, 1);
});