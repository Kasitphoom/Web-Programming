function createCalendar(){
    let August = new Date(2023, 8);

    date_arr = getDateonDayArray(August)
    
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    const trh = document.createElement("tr");
    const th = document.createElement("th");
    th.colSpan = 7;
    August.setMonth(August.getMonth() - 1);
    th.textContent = August.toLocaleDateString("en-US", {month: "long"}) + " " + August.getFullYear().toString();

    for(let i = 0; i < date_arr.length; i++){
        const tr = document.createElement("tr");
        for(let j = 0; j < date_arr[i].length; j++){
            const td = document.createElement("td");
            td.textContent = date_arr[i][j];
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    trh.appendChild(th);
    thead.appendChild(trh);

    table.appendChild(thead);
    table.appendChild(tbody);
    document.body.appendChild(table);
}

function mapday(day){
    return day - 1 % 7;
}


function getDateonDayArray(date){
    let month_arr = [];
    let week = [];
    let month = date.getMonth();
    date.setMonth(month - 1);
    let year = date.getFullYear();

    let start_day = date.getDay();
    
    for(let i = 0; i < mapday(start_day); i++){
        week.push("");
    }

    let last_date = 1;
    let newMonth = false;

    while(date < new Date(year, month, 7)){

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

    return month_arr;
    
}

document.addEventListener("DOMContentLoaded", createCalendar);