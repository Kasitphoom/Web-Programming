document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("fileInput");
    fileInput.addEventListener("change", function(e) {
        const file = e.target.files[0];

        const reader = new FileReader();
        reader.readAsText(file);

        reader.onload = function(e) {
            console.log(e.target)
            const data = JSON.parse(e.target.result);
            LoadInfo(data);
            CreateTranscript(data);
        }
    });
});

function CreateTranscript(data){
    const table = document.getElementById("content_body");

    table.innerHTML = ""

    var gpaPoint = 0;
    var gpaCredit = 0;

    for (var year in data.credit){

        for(var sem in data.credit[year]){

            var gpsPoint = 0;
            var gpsCredit = 0;

            let title = `${sem}, ${year}`;

            let row = document.createElement("tr");
            row.innerHTML = `
                <td style="text-align: center; font-weight: bold; text-decoration: underline;">${title}</td>
                <td></td>
                <td></td>
            `
            table.appendChild(row);

            for(var subjectIndex in data.credit[year][sem]){
                
                let subject = data.credit[year][sem][subjectIndex];

                let row = document.createElement("tr");
                row.innerHTML = `
                    <td style="text-align: left">${subject.subject_id} ${subject.name}</td>
                    <td>${subject.credit}</td>
                    <td>${subject.grade}</td>
                `
                table.appendChild(row);

                gpaPoint += parseFloat(subject.credit) * parseFloat(subject.grade);
                gpaCredit += parseFloat(subject.credit);

                gpsPoint += parseFloat(subject.credit) * parseFloat(subject.grade);
                gpsCredit += parseFloat(subject.credit);

            }

            let gparow = document.createElement("tr");
            gparow.innerHTML = `
                <td style="text-align: center">GPS: ${CalGrade(gpsPoint, gpsCredit)} &emsp; GPA: ${CalGrade(gpaPoint, gpaCredit)}</td>
                <td></td>
                <td></td>
            `
            table.appendChild(gparow);
        }

    }
}

function LoadInfo(data){
    document.getElementById("student_name").value = data.student_name;
    document.getElementById("date_of_birth").value = data.date_of_birth;
    document.getElementById("student_id").value = data.student_id;
    document.getElementById("date_of_admission").value = data.date_of_admission;
    document.getElementById("date_of_graduation").value = data.date_of_graduation;
    document.getElementById("degree").value = data.degree;
    document.getElementById("major").value = data.major;
}

function CalGrade(totalpoint, totalcredit){
    console.log(totalpoint, totalcredit, totalpoint / totalcredit);
    return (totalpoint / totalcredit).toFixed(2);
}