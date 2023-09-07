var currentmonth = 1;
const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
function createCalendar(){
    document.body.innerHTML = "";
    let August = new Date("2023-"+currentmonth+"-1");

    date_arr = getDateonDayArray(August)

    
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    const trh = document.createElement("tr");
    const th1 = document.createElement("th");
    const th2 = document.createElement("th");
    const th3 = document.createElement("th");

    const dayrow = document.createElement("tr");
    for (let i = 0; i < days.length; i++){
        const th = document.createElement("th");
        th.textContent = days[i];
        dayrow.appendChild(th);
    }

    th2.textContent = "<";
    th3.textContent = ">";

    th2.className = "button";
    th3.className = "button";

    th1.colSpan = 5;
    th1.textContent = August.toLocaleDateString("en-US", {month: "long"}) + " " + August.getFullYear().toString();

    for(let i = 0; i < date_arr.length; i++){
        const tr = document.createElement("tr");
        for(let j = 0; j < date_arr[i].length; j++){
            const td = document.createElement("td");
            td.textContent = date_arr[i][j];
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    trh.appendChild(th2);
    trh.appendChild(th1);
    trh.appendChild(th3);
    thead.appendChild(trh);

    table.appendChild(dayrow);
    table.appendChild(thead);
    table.appendChild(tbody);
    document.body.appendChild(table);

    th2.addEventListener("click", prev);
    th3.addEventListener("click", next);
    
}

function mapday(day){
    return (day + 6) % 7;
}

function next(){
    currentmonth++;
    if (currentmonth > 12){
        return currentmonth = 12;
    }
    console.log(currentmonth);
    createCalendar();
}

function prev(){
    currentmonth--;
    if (currentmonth < 1){
        return currentmonth = 1;
    }
    console.log(currentmonth);
    createCalendar();
}


function getDateonDayArray(date){
    let month_arr = [];
    let week = [];
    let month = date.getMonth();
    date.setMonth(month);
    let year = date.getFullYear();

    let start_day = date.getDay();

    
    for(let i = 0; i < mapday(start_day); i++){
        week.push("");
    }

    let last_date = 1;
    let newMonth = false;

    while(date < new Date(year, month+1, 7)){

        if (date.getDate() < last_date){
            newMonth = true;
        }

        week.push(newMonth ? "" : date.getDate());
        
        if(week.length == 7){
            month_arr.push(week);
            week = [];
        }
        last_date = date.getDate();
        date.setDate(date.getDate() + 1);
        
    }

    date.setMonth(month);
    date.setYear("2023")

    return month_arr;
    
}

document.addEventListener("DOMContentLoaded", createCalendar);