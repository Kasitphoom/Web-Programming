let readtable = () => {
    const ths = document.querySelectorAll("th");

    let th_values = [];
    let body = [];
    let footer = [];

    for (let i = 0; i < ths.length; i++) {
        th_values.push(ths[i].innerHTML);
    }

    const trs = document.querySelectorAll("tr");

    for (let i = 1; i < trs.length - 1; i++) {
        let row = {};
        const tds = trs[i].querySelectorAll("td");
        for (let j = 0; j < tds.length; j++) {
            row[`col${j + 1}`] = tds[j].innerHTML;
        }
        body.push(row);
    }

    const footer_td = trs[trs.length - 1].querySelectorAll("td");

    for (let i = 0; i < footer_td.length; i++) {
        let col = {};
        col["value"] = footer_td[i].innerHTML;
        if (footer_td[i].hasAttribute("colspan")) {
            col["span"] = footer_td[i].getAttribute("colspan");
        }
        footer.push(col);
    }

    const data = {
        "Header" : th_values,
        "Body" : body,
        "Footer" : footer
    }

    

    const json = JSON.stringify(data, null, 4);
    document.getElementById("displayTextarea").innerHTML = json;
}

function convert() {
    const json = document.getElementById("displayTextarea").value;
    const data = JSON.parse(json);

    const table = document.getElementById("newTable");

    table.innerHTML = "";

    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const tfoot = document.createElement("tfoot");

    const headtr = document.createElement("tr");
    const foottr = document.createElement("tr");

    for (let i = 0; i < data.Header.length; i++) {
        const th = document.createElement("th");
        th.innerHTML = data.Header[i];
        headtr.appendChild(th);
    }

    for (let i = 0; i < data.Body.length; i++) {
        const tr = document.createElement("tr");
        console.log(data.Body[i]);
        for (const key in data.Body[i]) {
            const td = document.createElement("td");
            td.innerHTML = data.Body[i][key];
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    for (let i = 0; i < data.Footer.length; i++) {
        
        const td = document.createElement("td");
        td.innerHTML = data.Footer[i].value;
        if (data.Footer[i].hasOwnProperty("span")) {
            td.setAttribute("colspan", data.Footer[i].span);
        }
        foottr.appendChild(td);
    }

    thead.appendChild(headtr);
    tfoot.appendChild(foottr);
    
    table.appendChild(thead);
    table.appendChild(tbody);
    table.appendChild(tfoot);
}


document.addEventListener("DOMContentLoaded", readtable);