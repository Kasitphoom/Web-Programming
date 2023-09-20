document.addEventListener("DOMContentLoaded", function() {
    const data = [
        {
            name: "John",
            age: 30
        },
        {
            name: "Jane",
            age: 25
        }
    ]
    const btn = document.getElementById("btn");
    btn.addEventListener("click", async function(e) {
        e.preventDefault();
        const newHandle = await window.showSaveFilePicker();
        const writable = await newHandle.createWritable();
        console.log(JSON.stringify(data));
        await writable.write(JSON.stringify(data, null, 2));
        alert("File saved!");
        await writable.close();
    });
});